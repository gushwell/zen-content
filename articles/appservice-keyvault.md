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

Azure Key Vault は、クラウド環境でシークレットや証明書、暗号鍵を安全に管理できるサービスです。
App Service で動くアプリがデータベース接続文字列や API キーなどの機密情報を扱う場合、コードや環境変数に直接書き込むのではなく、Key Vault に格納して必要な時に取得するのが推奨されます。


### 認証するためにマネージドIDを使う

App Service から Key Vault に安全にアクセスするには、Microsoft Entra ID（旧 Azure AD）の**マネージド ID（Managed Identity）**を利用します。
マネージド ID は Azure リソースに自動で割り当てられる ID で、パスワード不要の認証が可能です。

※マネージド ID には「システム割り当て」と「ユーザー割り当て」の2種類がありますが、本記事では「システム割り当てマネージド ID」を使用します。


---

## 2. 手順

### Step 0: 前提条件

- App Service と Key Vault が同一の Azure テナント内に存在していること

- App Service の実行環境が Azure（ローカル開発では動作方法が異なる）であること



### Step 1: App Service のマネージドIDを有効化

1. Azure Portal で対象の App Service を開く

2. 左のメニュ－から「設定」-「ID」を選択

3. 「システム割り当てマネージドID」を「オン」にして保存

    ![](https://storage.googleapis.com/zenn-user-upload/94f2c631eb78-20250808.png)

4. 保存後、自動的に Entra ID 上にサービス プリンシパルが作成される

    ![](https://storage.googleapis.com/zenn-user-upload/4450405eed2b-20250808.png)

---

### Step 2: Key Vault にマネージドIDのアクセス権を付与

Key Vault ではアクセス権の付与方法が2種類あります。

- Azure ロールベースのアクセス制御 (RBAC) … 「アクセス制御 (IAM)」で設定

- Key Vault アクセス ポリシー(レガシー) … Key Vault 独自のアクセス設定

この記事では Azure RBAC を使用します。


1. Azure Portal で Key Vault を開く

1. 「アクセス制御 (IAM)」に移動

1. ページ上部の「＋追加」ー「ロールの割り当ての追加」をクリック

    ![](https://storage.googleapis.com/zenn-user-upload/84627dd68a9f-20250808.png)

1. 「ロールの割り当て」から「キー コンテナー シークレット責任者」等の適切なロールを選択

    ![](https://storage.googleapis.com/zenn-user-upload/acfd83d0d4c4-20250808.png)

    - 読み取り専用なら「キー コンテナー シークレット ユーザー」
    - 読み書き両方なら「キー コンテナー シークレット責任者」

1. 「次へ」ボタンをクリック

1. 「マネージドID」ラジオボタンをチェック
    ![](https://storage.googleapis.com/zenn-user-upload/b45cdadf6ec2-20250808.png)

1. 「メンバーを選択する」をクリック

1. マネージドIDで、「すべてのシステム割り当てマネージドID」を選択

   ![](https://storage.googleapis.com/zenn-user-upload/3079d93b2bcb-20250812.png)


1. 検索された一覧から、該当するApp Serviceを選択し、「選択」ボタンをクリック

    ![](https://storage.googleapis.com/zenn-user-upload/add05873ed1b-20250812.png)

1. 「次へ」→「レビューと割り当て」をクリック


以上で、Key Vault にマネージドIDのアクセス権を付与できました。

---

### Step 3: アプリケーションコードの変更

1. 必要な NuGet パッケージを追加します

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

**ポイント：**

- DefaultAzureCredential はローカル開発時は開発者アカウントを使用し、Azure 上ではマネージド ID を自動で使用します。

- 実運用では SetSecretAsync は管理用のスクリプトで実行し、アプリ側は GetSecretAsync のみにすることが多いです。


:::message
.NETのアプリケーション構成として利用することが可能ですが、この記事では扱っていません。
アプリで直接読み書きするコード示しています。
:::


---

### Step 4: 動作確認

これで同一テナント内の App Service から安全に Key Vault のシークレットにアクセスできます。  

アプリケーションをデプロイし、Key Vault からシークレットを書き込み、読み込みができるかテストしてください。

**よくあるエラー:**
- 403 Forbidden → Key Vault のアクセス許可を再確認

- KeyVaultReferenceException → URL や権限設定の誤りを確認

なお、Azure Portalで、KeyVaultのシークレットの値を確認してプログラムで値を設定できたかも確認してみてください。


![](https://storage.googleapis.com/zenn-user-upload/3d244810bbd0-20250808.png)


![](https://storage.googleapis.com/zenn-user-upload/5da6b3c4f19b-20250812.png)


## まとめ

- Key Vault を使うと、App Service から機密情報を安全に扱える

- マネージド ID を利用すると、パスワードレスで認証可能

- Azure RBAC を使えば権限管理が一元化できる

これで、同一テナント内の App Service から安全に Key Vault のシークレットを取得できるようになります
