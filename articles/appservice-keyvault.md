---
title: "Azure App Service から Azure Key Vault を安全に利用する（ASP.NET Core編）"
emoji: "🔏"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "aspnetcore", "azure",  "keyvault"]
published: true
published_at: 2025-09-16 21:05
publication_name: zead
---

## 1. 概要

この記事では、Azure 上でアプリケーションを動かしている方に向けて、Azure App Service から Azure Key Vault のシークレットを安全に取得・利用する手順をわかりやすく解説します。

### なぜ Azure Key Vault を使うのか？

Azure Key Vault はクラウド環境でシークレットや証明書、鍵を安全に管理できるサービスです。
App Service で動くアプリがデータベース接続文字列やAPIキーなどの機密情報を扱う場合、直接コードや環境変数に書くのではなく、Key Vault に格納し必要な時に取得するのが推奨されます。


### 認証するためにマネージドIDを使う

App Service から Key Vault に安全にアクセスするには、Entra ID の「マネージドID（Managed Identity）」を利用します。
マネージドIDは、Azure リソースに自動で割り当てられるIDで、これを使うとパスワード不要の認証が可能です。


---

## 2. 手順

### Step 0: 前提条件

同一の Azure テナント内のサブスクリプションで App Service と Key Vault が存在することが前提です。


### Step 1: App Service のマネージドIDを有効化

1. Azure Portal で対象 App Service を開く

2. 左のメニュ－から「設定」-「ID」を選択

3. 「システム割り当てマネージドID」を「オン」にして保存

    ![](https://storage.googleapis.com/zenn-user-upload/94f2c631eb78-20250808.png)

4. これにより App Service の Azure AD 上にサービスプリンシパルが自動作成される

    ![](https://storage.googleapis.com/zenn-user-upload/4450405eed2b-20250808.png)

---

### Step 2: Key Vault にマネージドIDのアクセス権を付与

1. Azure Portal で Key Vault を開く

1. 「アクセス制御 (IAM)」に移動

1. ページ上部の「＋追加」ー「ロールの割り当ての追加」をクリック

    ![](https://storage.googleapis.com/zenn-user-upload/84627dd68a9f-20250808.png)

1. 「ロールの割り当て」から「キー コンテナー シークレット責任者」等の適切なロールを選択

    ![](https://storage.googleapis.com/zenn-user-upload/acfd83d0d4c4-20250808.png)

1. 「次へ」ボタンをクリック

1. 「マネージドID」ラジオボタンをチェック
    ![](https://storage.googleapis.com/zenn-user-upload/b45cdadf6ec2-20250808.png)

1. 「メンバーを選択する」をクリック

1. マネージドIDで、「すべてのシステム割り当てマネージドID」を選択

    ![](https://storage.googleapis.com/zenn-user-upload/7ab4ee4e1aa7-20250808.png)


1. 検索された一覧から、該当するApp Serviceを選択し、「選択」ボタンをクリック
    ![](https://storage.googleapis.com/zenn-user-upload/19c870c053b4-20250808.png)

1. 「次へ」をクリック

1. 「レビューと割り当て」ボタンをクリック
  

以上で、Key Vault にマネージドIDのアクセス権を付与できました。

---

### Step 3: アプリケーションコードの変更

1. パッケージをインストール

```xml
    <PackageReference Include="Azure.Identity" Version="1.14.2" />
    <PackageReference Include="Azure.Security.KeyVault.Secrets" Version="4.8.0" />
```

2. SecretClientクラスを使い、Key Vaultのシークレットにアクセス。

```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

var keyVaultUrl = "https://{your-keyvault-name}.vault.azure.net/";
var credential = new DefaultAzureCredential();
var client = new SecretClient(new Uri(keyVaultUrl), credential);

// シークレット設定例
await client.SetSecretAsync("MySecret","これは秘密の値です");


// シークレット取得例
KeyVaultSecret secret = await client.GetSecretAsync("MySecret");
string secretValue = secret.Value;
```

- `DefaultAzureCredential` は App Service のマネージドIDを自動的に検出して使用

:::message
.NETのアプリケーション構成として利用することが可能ですが、この記事では扱っていません。
アプリで直接読み書きするコード示しています。
:::


---

### Step 4: 動作確認

これで同一テナント内の App Service から安全に Key Vault のシークレットにアクセスできます。  

アプリケーションをデプロイし、Key Vault からシークレットを書き込み、読み込みができるかテストしてください。

もし、403 Forbidden エラーが出る場合は、マネージドIDのロール割り当てを再確認してください。

なお、Azure Portalで、KeyVaultのシークレットの値を確認してプログラムで値を設定できたかも確認してみてください。


![](https://storage.googleapis.com/zenn-user-upload/3d244810bbd0-20250808.png)


![](https://storage.googleapis.com/zenn-user-upload/8eae1a887de5-20250808.png)
