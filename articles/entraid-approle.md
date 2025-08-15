---
title: "Microsoft Entra ID のアプリロール方式で ASP.NET Core のページアクセスを簡単制御"
emoji: "🪪"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "aspnetcore", "azure",  "entraid"]
published: true
published_at: 2025-09-29 21:05
publication_name: zead
---

## はじめに 

Microsoft Entra ID（旧 Azure Active Directory）の**アプリロール**機能を使うと、ユーザーの権限管理を Azure 側で一元化し、ASP.NET Core アプリケーション内では `[Authorize(Roles = "...")]` 属性だけで簡単にアクセス制御を実装できます。

この記事では、グループ方式ではなく**アプリロール方式**焦点を当て、Azure ポータルの設定から ASP.NET Core のコード実装まで、最短の手順を解説します。

**対象読者**は、Microsoft Entra ID を使った認証・認可を初めて設定する開発者や、グループ方式からアプリロール方式への移行を検討している方です。

Entra IDによる認証が初めての方は、最初に以下の記事を読んでいただけると良いかと思います。
https://zenn.dev/zead/articles/aspnetcode-entraid

---

## アプリロール方式とは？

通常、Entra ID で「誰がどのページにアクセスできるか」を分ける場合、主に以下の2つのパターンがあります。

- **グループ方式**: 既存の組織グループを利用し、コード側で `groups` クレームを判定してロールを割り当てる。たとえば、グループIDをコード内でチェックするロジックが必要になる場合があります。

- **アプリロール方式**: アプリ固有のロールを Azure 側で定義し、トークンの `roles` クレームに直接含める。アプリ側では `[Authorize(Roles="...")]` で簡単に制御可能。

### アプリロール方式のメリット
- **コードがシンプル**: ロール判定のロジックをアプリ側に書く必要がない。
- **運用が容易**: Azure ポータルでロールを追加・変更すれば、即時反映（※トークンの有効期限に依存する場合あり）。
- **柔軟性**: アプリ専用のロールを自由に定義でき、組織のグループ構造に依存しない。

---

## 手順

### 1. Azure 側の設定


#### ① アプリロールの作成

1. Azure ポータルにログインし、**Microsoft Entra ID** → **アプリの登録** → 対象のアプリケーションを選択。
   - **補足**: 「アプリの登録」は、アプリケーションの認証設定を管理する場所です。後述の「エンタープライズアプリケーション」とは同じアプリを異なる視点で管理する画面です。
2. 左メニューから **「管理」→「アプリロール」** を選択。
3. **「アプリロールの作成」** をクリックし、以下を入力

例：Admin ロール

* **表示名**: `Admin`
* **値**: `Admin`（`[Authorize(Roles="Admin")]` と一致させる）
* **説明**: 管理者が利用できる機能
* **メンバーの種類**: ユーザー/グループ（例: 部署ごとのグループに割り当てる場合に便利）
* **有効化**: チェックON

例：User ロール

* **表示名**: `User`
* **値**: `User`
* **説明**: 一般ユーザーが利用できる機能
* **メンバーの種類**: ユーザー/グループ
* **有効化**: チェックON

- 保存すると、内部的にアプリのマニフェストが自動更新されます。
- 以前のAzureポータルではJSONを直接編集する必要がありましたが、現在は不要です。

#### ② ロールをユーザーやグループに割り当て

1. Azure ポータル → **Microsoft Entra ID** → **エンタープライズアプリケーション**
2. 対象アプリを選択（「アプリの登録」で作成したアプリと同じ）。
3. **「ユーザーとグループ」** → **「ユーザー/グループの追加」**
4. 対象ユーザーまたはグループを選択し、作成した Admin または User ロールを割り当て。

---

### 2. ASP.NET Core 側の実装

#### ① `Program.cs` の最小構成


以下は、Microsoft Entra ID 認証を有効化し、アプリロールを利用するための最小限のコードです。

```csharp:Program.cs
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.Identity.Web;

var builder = WebApplication.CreateBuilder(args);

// Entra ID 認証を追加（appsettings.json の AzureAd セクションを参照）
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"));

// トークンの roles クレームをロールとして認識する設定
builder.Services.Configure<OpenIdConnectOptions>(OpenIdConnectDefaults.AuthenticationScheme, options =>
{
    options.TokenValidationParameters.RoleClaimType = "roles";
});

// 認可サービスとRazorページを追加
builder.Services.AddAuthorization();
builder.Services.AddRazorPages();

var app = builder.Build();

// 認証・認可ミドルウェアを有効化
app.UseAuthentication();
app.UseAuthorization();

app.MapRazorPages();

app.Run();
```

補足: Microsoft.Identity.Web パッケージを NuGet からインストールしてください（例: dotnet add package Microsoft.Identity.Web）。


#### ② `appsettings.json` の例

```json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "Domain": "yourtenant.onmicrosoft.com",
    "TenantId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "ClientId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "CallbackPath": "/signin-oidc"
  }
}
```

##### TenantId と ClientId の取得方法:

Azure ポータル → Microsoft Entra ID → アプリの登録 → 対象アプリを選択。
「概要」ページで アプリケーション (クライアント) ID（ClientId）と ディレクトリ (テナント) ID（TenantId）を確認。

##### トークンの確認方法:

デバッグ時にトークンを確認するには、ログイン後の User.Claims を出力（例: foreach (var claim in User.Claims) { Console.WriteLine($"{claim.Type}: {claim.Value}"); }）。
roles クレームに Admin や User が含まれていることを確認してください。


#### ③ ページごとのアクセス制御

```csharp
// Admin 専用ページ
[Authorize(Roles = "Admin")]
public class AdminPageModel : PageModel
{
    public void OnGet() { }
}

// User 専用ページ
[Authorize(Roles = "User")]
public class UserPageModel : PageModel
{
    public void OnGet() { }
}

// 両方アクセス可能
[Authorize(Roles = "Admin,User")]
public class CommonPageModel : PageModel
{
    public void OnGet() { }
}
```

---

### 3. 動作確認

1. Azure ポータルで Admin ロールを割り当てたユーザーでログイン → Admin ページにアクセス可能、User ページもアクセス可能（CommonPageModel の場合）。

1. User ロールのみのユーザーでログイン → User ページはアクセス可能、Admin ページは 403 Forbidden。


**注意点:**

認証エラー（例: 401 Unauthorized）が発生した場合は、appsettings.json の設定や NuGet パッケージのバージョンを確認してください。

---

## まとめ


- アプリロール方式は、Azure ポータルでの設定だけでロールをトークンに含め、コードをシンプルに保てます。
- [Authorize(Roles="...")] を使えば、ページや API のアクセス制御が簡単に実現可能です。
- ロールの追加・削除は Azure ポータルで完結し、運用フェーズでの変更が容易です。

**おすすめポイント**

- グループ方式に比べてコード量が減り、運用フェーズでの権限変更が大幅に効率化されます。
- ASP.NET Coreで新規開発する場合や Azure 環境をフルに活用する場合は、アプリロール方式がベストチョイスです。

