---
title: "爆速検索エンジン Meilisearch で Wiki 活用を加速させる！"
emoji: "🔍"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["meilisearch", "docker", "gitlab", "javascript"]
published: true
published_at: 2025-11-04 21:05
publication_name: zead
---


## はじめに

「あの情報、Wikiのどこかにあったはずなのに…」「誰か、あの資料のリンク知らない？」
チームで使っているWiki、情報が増えるほど、必要なものを見つけ出すのが難しくなっていませんか？

そんな悩みを解決してくれるのが、Meilisearch です。これは、誰でも簡単に構築できる高速な全文検索エンジン。今回は、GitLab Wikiを例に、Meilisearchを使ってWikiの情報をインデックス化し、欲しい情報に一瞬でたどり着く方法をご紹介します。


## Meilisearchとは？

[Meilisearch](https://www.meilisearch.com/) は、軽量かつ高速なオープンソース全文検索エンジンです。
Elasticsearch などと比べてシンプルで導入が容易であり、開発者がアプリケーションに手軽に検索機能を組み込めることを目的としています。

以下のような特徴があります。

* **高速**: ミリ秒単位で検索結果を返す
* **シンプルなAPI**: REST API / SDK を使って簡単に利用可能
* **自然な検索体験**: タイポ補正や関連度の高い検索が標準で使える
* **軽量**: Dockerを使ってすぐに立ち上げられる

---

## 準備

以下を用意しておきます。

* Node.js が動作する環境（バージョン18以上）
* Docker / docker-compose が使える環境

---

## 導入の手順

### GitLab Wiki を clone

ローカルに GitLab Wiki を clone します。

```bash
git clone https://gitlab.example.com/mygroup.wiki.git wiki
cd wiki
```

Cloneすると、wikiフォルダが作成され `.md` ファイルが取得できます。


#### クローン用URLの確認方法

1. WikiページのプロジェクトのGitLabページにアクセス。
2. 左側メニューの[Wiki]を選択。
3. 画面右上付近の縦3点リーダー「⋮」をクリックし、「リポジトリーをクローン」をクリック。
4. ダイアログが表示されるので、クローン用URLを確認。


###  `.env` ファイルを作成

まず、環境変数をまとめて管理するために `.env` ファイルを作ります。

```env
# Meilisearch設定
MEILI_HOST=http://localhost:7700
MEILI_MASTER_KEY=masterKey
MEILI_PORT=7700

# GitLab Wiki の clone URL
GITLAB_WIKI_URL=https://gitlab.example.com/mygroup.wiki.git
```

**セキュリティ注意（重要）**
- `MEILI_MASTER_KEY`（管理用キー）は絶対にフロントエンドや公開リポジトリに含めないでください。管理操作（インデックス作成・更新・削除など）はサーバー側でのみ実行し、キーは安全に保管してください。
- フロントエンドから検索を行う場合は、読み取り専用の Search API Key（Meilisearch の検索専用キー）を作成して使用してください。Search API Key は検索のみを許可し、書き込みや管理操作は行えません。
- デプロイ時や Docker 設定では、環境変数を平文で埋め込まず、環境変数ファイル（env_file）やシークレット管理機能を活用してください。
- もし Master Key が漏洩した場合は直ちにローテーション（新しいキーの発行）を行い、既存のキーを無効化してください。

MEILI_MASTER_KEYは任意の文字列を与えてください。


### `docker-compose.yml` を作成

Meilisearch を Docker 上で起動し、データを永続化するために `docker-compose.yml` を用意します。

```yaml
services:
  meilisearch:
    image: getmeili/meilisearch:v1.11
    container_name: meilisearch
    ports:
      - "${MEILI_PORT}:7700"
    volumes:
      - ./meili_data:/meili_data
    environment:
      - MEILI_MASTER_KEY=${MEILI_MASTER_KEY}
    restart: unless-stopped
```

これで `docker-compose up -d` を実行すれば、Meilisearch が起動します。
データは `./meili_data` に保存されるため、コンテナを再起動してもインデックスは保持されます。


### Wiki をインデックス化するスクリプト

次に、Wiki の内容を Meilisearch に登録するスクリプトを用意します。
ここでは Node.js を例にします。

```bash
npm init -y
npm install meilisearch gray-matter dotenv
```

作成されたpackage.jso"type"の行を以下のように書き換えます。

```
  "type": "module",
```

`scripts/index.js` を作成します。

```js
// index.js
// このスクリプトは wiki ディレクトリ内の Markdown ファイルを読み込み、
// MeiliSearch の "wiki" インデックスにドキュメントとして登録します。
// 環境変数:
//   - MEILI_HOST: MeiliSearch サーバーの URL（未指定時は http://localhost:7700）
//   - MEILI_MASTER_KEY: 管理用 API キー（未指定でも動作しますが、タスク確認時に必要になることがあります）

// 環境変数の読み込み（.env を自動で読みます）とモジュールのインポート
import 'dotenv/config';
import fs from "fs";
import path from "path";
import matter from "gray-matter"; // Markdown のフロントマターをパースする
import { MeiliSearch } from "meilisearch"; // MeiliSearch クライアント
import crypto from "crypto";

// 実行開始ログ（MEILI_MASTER_KEY が設定されているかの確認）
console.log("START: index.js - process.env MEILI_MASTER_KEY present:", !!process.env.MEILI_MASTER_KEY);

// MeiliSearch クライアントを初期化
// host と apiKey は環境変数から取得します（なければデフォルト host を使用）
const client = new MeiliSearch({
  host: process.env.MEILI_HOST || "http://localhost:7700",
  apiKey: process.env.MEILI_MASTER_KEY,
});

// クライアント初期化結果のデバッグ出力（実際のキーは表示しない）
console.log("MEILI_CLIENT:", { host: client.config?.host ?? process.env.MEILI_HOST, apiKeyPresent: !!process.env.MEILI_MASTER_KEY });

// 使用するインデックス名を指定（ここでは "wiki"）
const index = client.index("wiki");

// wiki ディレクトリの絶対パスを取得
const wikiDir = path.resolve("./wiki");
let files = [];
try {
  // ディレクトリ内のファイル名を取得し、.md 拡張子のみを対象にする
  files = fs.readdirSync(wikiDir).filter(f => f.endsWith(".md"));
} catch (err) {
  // 失敗したらエラーログを出してプロセス終了（ディレクトリが存在しない等）
  console.error("ERROR: failed to read wiki directory:", wikiDir, err && err.stack ? err.stack : err);
  process.exit(1);
}

// 見つかったファイル数とパスを出力
console.log("FILES_FOUND:", files.length, "path=", wikiDir, "files=", files);

// ファイルごとにドキュメントオブジェクトを作成
// 各ドキュメントは { id, title, content } の形式にする
const documents = files.map(file => {
  const filePath = path.join(wikiDir, file);
  // Markdown ファイルを UTF-8 で読み込む
  const raw = fs.readFileSync(filePath, "utf-8");
  // front-matter をパースして本文を取得（必要なら title 等も取得できる）
  const { content } = matter(raw);

  // ファイル名から拡張子を取り除いたものを rawId とする（タイトル兼元の識別子）
  const rawId = file.replace(/\.md$/, "");
  // スラッグ化（英数字、アンダースコア、ハイフン以外を _ に置換）
  const slug = rawId.replace(/[^a-zA-Z0-9_-]/g, "_");
  // 元の rawId に基づく短いハッシュを付与して一意性を確保（日本語ファイル名でも衝突を避ける）
  const hash = crypto.createHash("sha1").update(rawId, "utf8").digest("hex").slice(0, 8);
  const id = `${slug}-${hash}`;

  return {
    id,         // 一意の識別子（インデックス内でのユニークキー）
    title: rawId, // 表示用タイトル（ここではファイル名を使用）
    content,    // 実際の本文（検索対象）
  };
});

// 準備したドキュメントの数とサンプルをログに出力
console.log("DOCUMENTS_PREPARED:", documents.length, "sample:", documents[0] ?? null);

// ドキュメントを MeiliSearch に登録し、タスク完了まで待機する処理
try {
  // addDocuments は非同期でタスクを返す（taskUid / updateId 等）
  const response = await index.addDocuments(documents);
  console.log("MEILI RESPONSE:", response);

  // Meili のレスポンスからタスク ID を取り出す（バージョン差異を吸収）
  const taskUid = response.taskUid ?? response.updateId ?? response.taskUid;
  if (taskUid == null) {
    // タスク ID が取れない場合は待機できない旨を警告
    console.warn("WARN: addDocuments did not return taskUid - cannot wait for completion");
  } else {
    const host = process.env.MEILI_HOST || "http://localhost:7700";
    const apiKey = process.env.MEILI_MASTER_KEY;

    // 簡易ポーリングでタスク状態を確認（最大 30 回、500ms 間隔）
    let taskStatus = null;
    for (let i = 0; i < 30; i++) {
      try {
        // 直接 /tasks/{id} エンドポイントを叩いて状態を確認
        const res = await fetch(`${host}/tasks/${taskUid}`, {
          headers: apiKey ? { "Authorization": `Bearer ${apiKey}` } : {},
        });
        const json = await res.json();
        // API のバージョン差で status の位置が変わるため両方を参照
        taskStatus = json.status || json.task?.status;
        console.log("MEILI TASK:", { attempt: i + 1, status: taskStatus, raw: json });
        // 成功または処理済みでループを抜ける
        if (taskStatus === "succeeded" || taskStatus === "processed") {
          break;
        }
        // 失敗ならエラーログを出してループを抜ける
        if (taskStatus === "failed") {
          console.error("MEILI TASK FAILED:", json);
          break;
        }
      } catch (err) {
        // ネットワークエラーや JSON 解析エラーのハンドリング
        console.error("ERROR fetching task status:", err && err.stack ? err.stack : err);
      }
      // 次の試行まで 500ms 待つ
      await new Promise(r => setTimeout(r, 500));
    }
  }
} catch (err) {
  // addDocuments 自体が失敗した場合の処理（致命的とみなして終了）
  console.error("MEILI ERROR: addDocuments failed:", err && err.stack ? err.stack : err);
  process.exit(1);
}

// 登録後にインデックス統計を取得して実際の件数等を確認（任意のチェック）
try {
  const stats = await index.getStats();
  console.log("INDEX_STATS:", stats);
} catch (err) {
  // 統計取得が失敗しても終了はしない（情報取得の失敗）
  console.error("ERROR fetching index stats:", err && err.stack ? err.stack : err);
}

// 登録完了のユーザー向けメッセージ
console.log("✅ Wiki を Meilisearch に登録しました！");

```


実行（インデックスの登録）は以下のように行います。(すでに docker compose up -dは実行済とします。)


```
node scripts/index.js
```

:::message
ここで示したindex.jsはWikiドキュメントの更新や削除に対応していません。本格的な運用には、ドキュメントの更新・削除に対応する必要があります。
:::
---

## 動作確認

ブラウザで `http://localhost:7700` にアクセスすると、Meilisearch の管理コンソールが表示されます。

![](https://storage.googleapis.com/zenn-user-upload/a90408c4466e-20250908.png)

<br />

検索 API を叩く例も以下に示します。(PowerShell 7 で実行)

```bash
curl -X POST `
    -H "Authorization: Bearer masterKey" `
    -H "Content-Type: application/json" `
    "http://localhost:7700/indexes/wiki/search" `
    --data '{"q":"デプロイ"}'
```

Wiki 内から「デプロイ」に関連するページが検索結果として返ってきます。

---

## まとめ

* Meilisearch を **docker-compose** で簡単に立ち上げ
* GitLab Wiki を **clone してインデックス化**
* `.env` にキーやURLをまとめて管理

これで GitLab Wiki の検索体験を大幅に改善できます！
あとはフロントエンドをつければ、チーム内で便利な検索ポータルが完成します。
少人数ならば、Meilisearch の管理コンソールをそのまま使っても良いかもしれません。

