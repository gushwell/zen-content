---
title: "Azure App Service で SQLite を使う方法（ASP.NET Core 編）"
emoji: "🤸"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["sqlite", "aspnetcore", "csharp", "azure"]
published: true
published_at: 2025-09-01 21:00
publication_name: zead
---

## はじめに

ASP.NET Core で作成したアプリケーションを Azure App Service にデプロイしつつ、**SQLite** を使いたいというニーズは意外と多くあります。

「軽量でファイルベース」「手軽に始められる」という魅力のある SQLite ですが、通常の使い方とは少し異なる工夫が必要です。

この記事では、**Azure App Service 上で SQLite を安全に使う方法**について解説します。

:::message
Microsoftでは、App ServiceでのSQLiteの利用は推奨していないようですので、利用する場合は自己責任でお願いします。
:::

---

## 1. SQLite は App Service で使えるのか？

### 結論：

**技術的には可能**ですが、本番利用には注意が必要です。

App Service には「永続的ストレージを利用しない」が基本原則であるため、アプリが保存したファイルは **再起動・スケールアウト・再デプロイで消える可能性があります**。

そのため、SQLite の `.db` ファイルをそのまま `wwwroot` などに置いてしまうと、データが消えてしまうリスクがあります。

---

## 2. 一時的に使う方法（非永続）

### /home フォルダを使う

App Service の `/home`ディレクトリ（Windowsでは、`D:\home`）配下は **一時的な書き込み領域**として使用可能です。

例えば以下のように SQLite のファイルパスを指定すれば、一応動作します。

```csharp
var dbPath = Path.Combine(Environment.GetEnvironmentVariable("HOME"), "myapp.sqlite");
options.UseSqlite($"Data Source={dbPath}");
```

SQLiteをキャッシュ的な用途で利用するならばこれでOKですが、このファイルは **App Service の再起動などで消える可能性がある**ため、通常のデータベースと同じような使い方はできません。

---

## 3. 永続化するには？（Azure File Storage を活用）

本番利用を想定して SQLite を使いたい場合は、**Azure File Storage（Azure Files）を App Service にマウントして使う構成**が有効です。

:::message
`/home`を永続化するオプションもありますが、本記事では扱いません。
:::


以下にその手順の概要を示します。

### 手順概要

#### ① Azure Files を作成

まず、ストレージアカウントを作成します。既に作成済みの場合はスキップしてください。

1. Azure ポータルで「ストレージアカウント」を検索し、「+ 作成」

2. サブスクリプション・リソースグループ・アカウント名などを入力

    - プライマリーサービス：Azure Files
    - パフォーマンス：Standard
    - 冗長性：LRS（ローカル冗長）推奨

    ![](https://storage.googleapis.com/zenn-user-upload/ac5bcb27e48c-20250807.png)

3. 「レビューと作成」ボタンをクリック

4. 内容を確認し「作成」ボタンをクリック

5. デプロイが完了したら、「リソースに移動」ボタンをクリック

6. 左のメニューから「ファイル共有」を選択

    ![](https://storage.googleapis.com/zenn-user-upload/108cc2841b11-20250807.png)

7. ページ上部の 「+ ファイル共有」をクリック

8. 名前を入力し、ファイル共有を作成
    名前：例 sqlitefileshare

    ![](https://storage.googleapis.com/zenn-user-upload/cc1a7a52a030-20250807.png)



#### ② App Service にマウント

App Serviceはすでに作成済みとします。

1. Azure Portalで 該当のApp Service を開く

2. 左メニューの「設定」-「構成」で 「パスのマッピング」タブを開く

    ![](https://storage.googleapis.com/zenn-user-upload/2f8cd1c4d642-20250807.png)

3. 「＋新しい Azure Storageマウント」をクリック

    以下のスクリーンショットのように共有を `/mount/sqlitedb` などにマウント

    ![](https://storage.googleapis.com/zenn-user-upload/01622b884fcd-20250807.png)


#### ③ SQLite の接続文字列を設定

```csharp
builder.Services.AddDbContext<MyBoxContext>(options =>
    options.UseSqlite("Data Source=/mount/sqlitedb/myapp.db");
);

```

> Windows プランでは `D:\home\mounts\sqlitedb\myapp.db` のようなパスになります。

---

### Azure File Storage を利用するメリット

* **永続化**：再起動・再デプロイでもデータが保持される
* **簡単にマウント**できる（App Service の設定画面だけで完結）

SQLiteは以下のようなデメリットがあるため、大規模かつ高負荷な用途には適していませんが、少人数で利用する小規模なWebアプリケーションや、テスト・開発用途であれば、十分に実用に耐えうる性能を備えています。

#### デメリット

- 同時接続が多いとパフォーマンスが劣化（ファイルベースでロックがかかる）
- スケーラビリティが低い（クライアント／サーバー型ではない）
- ユーザー管理や細かな権限管理ができない
- 常時書き込みが発生するシステムでは不利


---

## 4. 補足：ASP.NET Core で必要な NuGet パッケージ

SQLite を ASP.NET Core アプリで使うには、以下の NuGet パッケージを導入します。

| パッケージ名                                 | 用途                                   |
| -------------------------------------- | ------------------------------------ |
| `Microsoft.EntityFrameworkCore.Sqlite` | SQLite を使うためのメインパッケージ                |
| `Microsoft.EntityFrameworkCore.Tools`  | マイグレーションなど開発ツール                      |

### インストール例（.NET CLI）

```bash
dotnet add package Microsoft.EntityFrameworkCore.Sqlite
dotnet add package Microsoft.EntityFrameworkCore.Tools
```

### DbContext の設定例

```csharp
services.AddDbContext<MyDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("MyDbConnection"));
```

### appsettings.jsonの記述例

```json
  "ConnectionStrings": {
    "MyDbConnection": "Data Source=/mount/sqlitedb/myapp.db",
  }
```

---

## まとめ

Azure App Service で SQLite を使うには、「ファイルの置き場所」と「運用の前提」をしっかり理解することが重要です。

SQLite にこだわりがない場合は、**Azure SQL Database** や **Azure Database for PostgreSQL/MySQL** といったマネージドDBサービスへの移行も検討しましょう。

