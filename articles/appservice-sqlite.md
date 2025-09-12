---
title: "Azure App Service で SQLite を使う方法（ASP.NET Core 編）"
emoji: "🤸"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["sqlite", "aspnetcore", "csharp", "azure"]
published: true
published_at: 2025-09-16 12:20
publication_name: zead
---

## はじめに

ASP.NET Core で作成したアプリケーションを Azure App Service にデプロイしつつ、SQLite を使いたいというニーズは意外と多くあります。

SQLite は「軽量でファイルベース」「手軽に始められる」「なんといっても低コスト」という魅力がありますが、クラウド環境、特に Azure App Service 上では通常のローカル環境とは異なる制約があります。

この記事では、Azure App Service 上で SQLite を利用する際の注意点と構成方法について解説します。

Microsoft では App Service での SQLite 利用を公式には推奨していません。理由は、永続性の保証やスケーラビリティの問題、複数インスタンス間でのファイル共有不可などです。利用する場合は自己責任で検証・運用してください。


---

## 1. SQLite は App Service で使えるのか？

### 結論：

技術的には利用可能ですが、本番利用には制約があります。

App Service は基本的に アプリケーションファイルとデータをインスタンスごとに分離しており、スケールアウト（複数インスタンス化）やインスタンス再作成時にファイルが失われたり共有できなかったりします。

特に、.db ファイルを wwwroot 直下に置くと再デプロイで消えるため危険です。


---

## 2. 一時的に使う方法（非永続）

### /home フォルダの利用

App Service の `/home`（Windowsでは、`D:\home`）は 単一インスタンス内では永続的ですが、複数インスタンス間では共有されません。スケールアウトやインスタンス再作成時にデータが失われる可能性があるため、本番用途には不向きです。

とはいえ、スケールアウトするような環境で、App Service + SQLiteという構成にしたいという方はいないと思いますが...

キャッシュやセッションデータなど、消えても問題ない用途なら以下のように設定可能です。


```csharp
var dbPath = Path.Combine(Environment.GetEnvironmentVariable("HOME"), "myapp.sqlite");
options.UseSqlite($"Data Source={dbPath}");
```

---

## 3. 永続化するには？（Azure File Storage を活用）

本番利用を想定して SQLite を使う場合は、**Azure File Storage（Azure Files）を App Service にマウントする方法**があります。

:::message
`/home`を永続化する構成（App Service Storage 永続化設定）もありますが、本記事では Azure Files マウントを解説します。
:::


以下にその手順の概要を示します。

### 手順概要

#### ① Azure Files を作成

まず、ストレージアカウントを作成します。既に作成済みの場合はスキップしてください。

1. Azure ポータルで「ストレージアカウント」を検索し、「+ 作成」

2. サブスクリプション・リソースグループ・アカウント名などを入力

    - プライマリーサービス：Azure Files
    - パフォーマンス：Standard
    - 冗長性：LRS（ローカル冗長）ストレージ

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

App Service(Linuxプランの場合)

```csharp
builder.Services.AddDbContext<MyBoxContext>(options =>
    options.UseSqlite("Data Source=/mount/sqlitedb/myapp.db");
);
```

> Windows プランでは `D:\home\mounts\sqlitedb\myapp.db` のようなパスになります。



---

### Azure File Storage を利用するメリット

**永続化:**
App Service の再起動・再デプロイ・スケールインでもデータが保持される

**インスタンス間共有:**
スケールアウト構成でも全インスタンスから同じ DB ファイルにアクセス可能

**管理の容易さ:**
Azure Portal から容量やスナップショットの管理ができる

**設定の簡便さ:**
App Service の設定画面で数クリックでマウント可能、コード変更は最小限

**バックアップ・復元が容易:**
Azure Files のスナップショット機能で DB ファイルを簡単にバックアップ可能

:::message alert
注意点：Azure Files はネットワーク経由のため、ローカルディスクよりも遅延があります。書き込み頻度が高い場合は性能に注意してください。
:::


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

:::message alert
実運用では、ソースコードやappsettings.jsonに接続文字列を記述するのではなく環境変数やKey Vaultなどから取得するようにしてください。
:::


---

## まとめ

- App Service でも SQLite は利用可能ですが、永続性・スケーラビリティの制限を理解する必要があります。

- 本番利用では Azure Files をマウントする方法が有効です。

- 高頻度書き込みや大規模アクセスには不向きです。

SQLite にこだわらない場合は、Azure SQL Database や Azure Database for PostgreSQL/MySQL の利用を検討するのが望ましいです。

