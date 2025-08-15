---
title: "ASP.NET Core で Microsoft Entra ID 認証を設定する方法"
emoji: "🪪"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "aspnetcore", "azure",  "entraid"]
published: true
published_at: 2025-08-18 21:05
publication_name: zead
---

## はじめに 

Microsoft Entra ID（旧称 Azure Active Directory）を使って、ASP.NET Core アプリケーションにシングルサインオン（SSO）認証を導入する方法を、Azure ポータル側の設定からアプリ側のコードまで、エラー対応も含めて解説します。


---

## 1. Entra ID 側の準備

### 1-1. Azure ポータルにログイン

* URL: [https://portal.azure.com](https://portal.azure.com)
* Microsoft アカウントまたは組織アカウントでログイン

### 1-2. Microsoft Entra ID → アプリの登録

1. 左メニューで「Microsoft Entra ID」→「アプリの登録」
2. 「+ 新規登録」をクリック
3. 以下の内容でアプリ登録：

   * **名前**: 任意（例：MyAspNetCoreApp）
   * **アカウントの種類**: 「この組織のディレクトリ内のアカウントのみ」
   * **リダイレクト URI**（重要）:

     ```
     https://localhost:5001/signin-oidc
     ```

    ポート番号は環境により異なります。これは開発用 URL なので、本番環境では必ず変更してください。

     ![](https://storage.googleapis.com/zenn-user-upload/789549d234dd-20250805.png)


---

### 1-3. 認証設定（Authentication）

1. 上記アプリの登録が完了するとアプリの詳細が見られるページに遷移。

2. このページで左メニューの「Authentication（Preview）」を選び、「設定」タブを開く

3. WebとSPAの設定で、「ID トークン」にチェック。

    ![](https://storage.googleapis.com/zenn-user-upload/cdb42008651e-20250805.png)

    これを有効化しないと、次のエラーが発生します。

    ```
    unsupported_response_type: AADSTS700054: response_type 'id_token' is not enabled for the application
    ```

4. 「保存」をクリック

:::message
再びこのアプリ登録の詳細ページを開くには、以下の手順に従ってください。
1. 「Microsoft Entra ID」を選択
2. 左メニューから「アプリの登録」を選択
3. 「ディレクトリ内のすべてのアプリケーションを表示」ボタンをクリック
4. 一覧から該当アプリを選択
:::

### 1-4 設定値をメモ

1. 概要ページで `TenantId`、`ClientId` をメモ

    ![](https://storage.googleapis.com/zenn-user-upload/3b7fc495abca-20250805.png)

    赤で囲んだ上が、ClientID,下がTenantIdです。

2. Domainを調べる

    Azure ポータル → Microsoft Entra ID → **カスタムドメイン名** に表示される
    例：`contoso.onmicrosoft.com`




---

## 2. ASP.NET Core アプリの設定

### 2-1. appsettings.json の構成

appsettings.jsonに”AzureAD”セクションを追加します。`Domain`, `TenantId`, `ClientId` の値は、Azure Portalでメモしていた値を使います。


```json:appsettings.json
"AzureAd": {
  "Instance": "https://login.microsoftonline.com/",
  "Domain": "yourtenant.onmicrosoft.com",
  "TenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "ClientId": "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy",
  "CallbackPath": "/signin-oidc"
}
```

- CallbackPath の既定値 /signin-oidc は OpenIdConnect の標準

- 実運用では、これらの値はappsettings.jsonではなく環境変数や Azure Key Vault に置き換えましょう


---

### 2-2. Program.cs 設定

Entra ID認証を使用するよう、Program.csを変更します。


```csharp:Program.cs
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.Identity.Web;

var builder = WebApplication.CreateBuilder(args);

// 認証サービスの登録
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"));

// 認可とUIの構成
builder.Services.AddAuthorization();
builder.Services.AddRazorPages(); // MVCの場合は AddControllersWithViews()

var app = builder.Build();

app.UseAuthentication();　 // 必ず Authorization の前に
app.UseAuthorization();

app.MapRazorPages(); // MVCの場合は app.MapControllers()

app.Run();
```

### 2-3 Authorize属性の付加

認証が必要なページやコントローラーに [Authorize] 属性を付けます。

```csharp
[Authorize]
public class MyPageModel : PageModel
{
    public void OnGet() { }
}
```


---

## まとめ

Microsoft Entra ID を ASP.NET Core に統合する手順は以下の3ステップです。

1. Azure ポータルでアプリを登録し、リダイレクトURIとトークン設定を行う

2. appsettings.json に認証情報を追加

3. Program.cs で認証と認可を有効化

これで安全なシングルサインオン（SSO）が実現できます。
Role ベースのアクセス制御も可能ですが、本記事では割愛しました。

