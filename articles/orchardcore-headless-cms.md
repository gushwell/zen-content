---
title: "C#ベースのオープンソースCMS「Orchard Core」をヘッドレスCMSとして利用する"
emoji: "🌰"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  [ "orchardcore", "cms", "headlesscms", "csharp", "graphql"]
published: true
published_at: 2024-08-21 21:10
publication_name: zead
---

Orchard Coreシリーズの最初の記事で説明しましたが、Orchard　CoreはヘッドレスCMSとして利用することも可能です。

https://zenn.dev/zead/articles/f604f9ad31f941

この記事では、OrchardCoreをヘッドレスCMSとして利用する方法について説明します。

## ヘッドレス(Headless) CMS とは

ヘッドレス(Headless) CMSは、バックエンド専用のコンテンツ管理システムです。
 「ヘッドレス（Headless）」という用語は、フロントエンド (ヘッド) をバックエンド (ボディ) から取り除くという考え方から来ています。
ヘッドレスCMSはコンテンツ リポジトリとして機能し、RESTful API やGraphQL APIを介してコンテンツを任意のデバイスに表示することができます。

そのため、ヘッドレスCMS にとってコンテンツがどこにどのように表示されるかは重要ではありません。その代わりに、構造化されたコンテンツの保存と配信のみに重点を置いています。   

フロントエンドはヘッドレスCMSとは疎結合のため、使い慣れたWebテクノロジー(VueやReact, Svelteなど)を使ってウェブサイトを構築することができます。


## GraphQLを利用可能にするための手順
 
ここでは、Orchard をヘッドレスCMSとして設定するためのステップバイステップのガイドを示します。  

### ステップ 1: プロジェクトをセットアップする   

#### Visual Studioの場合

Visual Studio を使用して、新しい .NET Core Web アプリ プロジェクトを作成します。テンプレートを選択する必要はありません。
デフォルトでは空のテンプレートを選択できます。プロジェクトが作成されたら、Orchard Core CMS パッケージをプロジェクトに追加します。  

NuGetを使い、プロジェクトファイルに  「OrchardCore.Application.Cms.Targets」パッケージをインストールします。

#### コマンドラインの場合

以下のコマンドを実行します。`OrchardCoreHeadless`は任意の名前です。

```
dotnet new occms -n OrchardCoreHeadless
cd OrchardCoreHeadless
dotnet run
```

### ステップ 2: Program.cs ファイルを更新して、Orchard CMS を使用するようにアプリケーションを構成する。
  
コマンドラインの場合は、すでにこのようになっています。

```cs
using OrchardCore.Logging;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseNLogHost();
builder.Services.AddOrchardCms();

var app = builder.Build();

if (!app.Environment.IsDevelopment()) {
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseOrchardCore();

app.Run();
```

### ステップ 3: アプリケーションを起動し、新しいサイトをセットアップする   

アプリケーションを実行し、サイト名、管理者の資格情報、タイムゾーンなどを入力して新しいサイトを設定します。
Orchard Core は、コンテンツ、テーマ、ビューを設定しない Blank Site レシピを提供します。このレシピは、Orchard CoreをヘッドレスCMSとして設定するためのコンテンツ管理機能を提供します。  
通常、ヘッドレスCMS サイトを作成するには、[レシピ] ドロップダウンで、[Blank site] を選択しますが、この記事では説明の都合で、いつものように[Blog]レシピを使うこととします。

なお、Blank siteでサイトを作成すると、以下のページが表示されますが、問題ありません。

![](https://storage.googleapis.com/zenn-user-upload/754dd8a7b40d-20240807.png)

### ステップ 4: コンテンツ タイプとコンテンツ アイテムを作成する    

Adminページを開き、コンテンツ タイプとそのコンテンツ タイプ内にフィールドを作成する必要があります。

システム内には複数のコンテンツ タイプが存在する可能性があります。たとえば、サイトにはホームページ、ブログ アイテム、製品ページのコンテンツ タイプなどが含まれる場合があります。

コンテンツ タイプを作成したら、サイト データを追加できます。

各コンテンツ アイテムはコンテンツ タイプに基づくドキュメントであり、フィールドとそれらのフィールドに追加されるデータを定義します。 

コンテンツの基礎は、以下の記事で簡単に説明しています。

https://zenn.dev/zead/articles/orchardcore-contents-basics

この基礎が理解できれば、独自のコンテンツを定義することができるはずです。

なお、この記事では、Blog記事を取得する例を示しています。

### ステップ 5: フロントエンド アプリケーションの API を有効にする  

#### GraphQL モジュールを有効にする

GraphQLとは、簡単に言えば、データを取得・更新するためのクエリ言語です。
クライアントは、このGraphQLを利用し、CMSシステムからデータを取得します。

GrapQLの概要は、以下のページも参考にしてください。

https://zenn.dev/zead/articles/first-graphql

以下のページで、GraphQL モジュールを有効にします。

![](https://storage.googleapis.com/zenn-user-upload/029dc071007f-20240807.png)

すると、GraphQL メニュー項目が表示されます。 

![](https://storage.googleapis.com/zenn-user-upload/f43b0384bcd0-20240807.png)

GraphQLメニューで開くこのページは、GraphQLエンドポイントの汎用エクスプローラーです。このページで GraphQL クエリをテストすることができます。このクエリは、CMS システムからデータを取得するために使用されます。   

![](https://storage.googleapis.com/zenn-user-upload/7c2c754a7dd4-20240807.png)


## GraphQL API を使用する

### 認証なしで利用できるようにする

アプリケーションで GraphQL API エンドポイントを GraphQL クエリとともに使用して、CMS からデータを取得します。  

GraphQL クエリを使用すると、必要なものだけを取得できます。アプリケーションでレンダリングする必要があるコンテンツ項目とフィールドを定義すると、それらのフィールドのみが返されるため、アプリケーションは非常に軽くて高速になります。   

これが完了すると、ヘッドレスCMS は、GraphQL API を通じて選択したフロントエンド アプリケーションと統合できるようになります。 

まずは、認証なしで利用できるようにしてみます。

Orchard Coreの管理者ページで、[ロール]を選び、Anonimouseを見つけ、[編集]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/2805422942a6-20240807.png)


[Execute GraphQL]の[許可]にチェックを入れ、[保存]をクリックします。

![](https://storage.googleapis.com/zenn-user-upload/4fa5aaf686d8-20240807.png)

### Graph QLを利用してみる

以下は、"[Altair GraphQL Client](https://altairgraphql.dev/)"の実行画面です。あとで、Postmanでの利用例も示します。

![](https://storage.googleapis.com/zenn-user-upload/4647dfb3d5fa-20240807.png)

ここでは、以下のようなクエリを実行しています。(BlogレシピのBlog記事のデータを取得しています)

```graphql
{
  blogPost {
    tags {
      taxonomyContentItemId
    }
    subtitle
    displayText
    markdownBody {
      markdown
    }
  }
}
```

### OpenIDで認証し、クエリを呼び出す


まずは、OPenIDの[OpenID Authorization Server],[OpenID Token Validation]の2つの機能を有効にします。

![](https://storage.googleapis.com/zenn-user-upload/dc1f0f7d9fb5-20240807.png)


次に、OpenID Serverの設定を行います。
[Allow Client Credentials Flow]にチェックを入れます。

![](https://storage.googleapis.com/zenn-user-upload/62629c05ceb6-20240807.png)



下へスクロールして更新ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/ff2fe4f216ff-20240807.png)

次に、このGraphQLを呼び出した際のロールを設定します。ここでは、Adminstratoeを指定していますが、本当ならもっと弱い権限のロールを使った方が良いでしょう。
[Execute GraphQL]の[許可]にチェックを入れ、[保存]をクリックします。

![](https://storage.googleapis.com/zenn-user-upload/e7263a2a66cb-20240807.png)

次に、クライアントアプリケーションの設定を行います。
メニュー[OpenID Connect]-[Applications]を選び、[Add an application]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/6991f1f6d90a-20240807.png)

Create a new application のページが開くので、ここでクライアントIDやシークレット値を入力します。

![](https://storage.googleapis.com/zenn-user-upload/7b600ccbddc7-20240807.png)

##### クライアントID

決まった桁数はありませんが、通常は8～128文字程度の範囲で設定します。
クライアントIDは一意であり、人間が識別しやすい文字列であれば十分です。

##### クライアントシークレット

最小桁数: 多くのプロバイダーは16文字以上を推奨していますが、セキュリティを考慮して32文字以上を推奨します。
最大桁数: 実際の制限はプロバイダーによりますが、通常は64文字～128文字程度までサポートされています。

ここでは以下のような値を入力しました

項目 | 値
-----|----------
Client Id | orchard-core-sample-client  
Display Name | orchard-core-sample-client  
Type | Confidential client  
Client Secrets | 90ri1anLF18bSeOMFLU5U4N8kV86TuSU  
Flows | [Allow Client Credentials Flow]にチェック  
Client Credentials Roles | Administratorにチェック  
 

### Postmanで呼び出してみる

まずは、tokenを取得します。以下に、Postmanの実行結果を示します。

```
Method:Post  
URL:https://localhost:5001/connect/token  
Content-Type:application/x-www-form-urlencoded  
Body:grant_type=client_credentials&client_id=orchar-core-sample-client&client_secret=90ri1anLF18bSeOMFLU5U4N8kV86TuSU
```

![](https://storage.googleapis.com/zenn-user-upload/85139847cc13-20240807.png)

![](https://storage.googleapis.com/zenn-user-upload/43db9e39317d-20240807.png)

![](https://storage.googleapis.com/zenn-user-upload/dbc565da710e-20240807.png)



これで、JWT（access_token）が返るので、JWTを使い、以下のようにGraphQLを呼び出します。


リクエストの設定:

```
HTTPメソッドを POST に設定します。  
URLを設定します。例: http://localhost:5000/api/graphql  
ヘッダーの設定: Content-Type=application/json   
リクエストボディの設定:

 {
  blogPost {
    tags {
      taxonomyContentItemId
    }
    subtitle
    displayText
    markdownBody {
      markdown
    }
  }
 }
```

JWTの設定: 

![](https://storage.googleapis.com/zenn-user-upload/357898a2437b-20240807.png)

GraphQLのクエリをBodyに設定: 

![](https://storage.googleapis.com/zenn-user-upload/a85c833eeb1e-20240807.png)

クエリの結果: 

![](https://storage.googleapis.com/zenn-user-upload/8d90ce09b582-20240807.png)


GraphQLを使うと、クライアントからOrchard Coreのコンテンツを取得できることがわかりました。

## Orchard Core ヘッドレスCMSの利点

最後に、Orchard Core をヘッドレスCMSとして利用する際の利点を示します。

### 1.柔軟性

OrchardをヘッドレスCMSとして使用することで、組織内で利用可能な技術的専門知識に基づいてアプリケーションのフロントエンドを決定し、設計できます。
さらに、同じコンテンツリポジトリを使用して、デバイスごとに異なる技術スタックを使用してコンテンツを表示することもできます。

### 2.コントロール

コンテンツ・リポジトリを完全にコントロールし、APIを使用してデータをさまざまなシステムに送信することができます。

### 3.適応性

デジタル革命が本格化する中、新しいマーケティング・コミュニケーション・プラットフォームが出現している。1つのプラットフォームを使ってコンテンツを管理しながら、望むだけ多くのマーケティング・チャンネルを簡単に更新・追加することができます。

### 4.時間と資源の節約

Orchardには、コンテンツを管理するための幅広い機能、ユーザーの役割、その他多くの機能が搭載されており、コストやリソースを節約することができます。

**Orchard Coreに関する記事一覧は以下のページで確認できます。**

https://zenn.dev/zead/articles/orchardcore-list-of-article

