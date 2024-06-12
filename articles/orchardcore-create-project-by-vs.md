---
title: "C#ベースのオープンソースCMS「Orchard Core」のプロジェクトをVisual Studioで作成する"
emoji: "🍐"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "aspnetcore", "orchardcore", "cms"]
published: true
published_at: 2024-06-12 08:10
publication_name: zead
---

dotnet コマンドでプロジェクトを作成する手順は以下の記事で紹介しましたが、Visual Studio を使ってもプロジェクトを作成することができます。


https://zenn.dev/zead/articles/orchardcore-setup


以下の2つの方法があります。

1. プロジェクトテンプレートを使う方法
2. 空のプロジェクトから作成する方法

この2つの方法について手順を示します。

2つの方法ともに、Orchard Core CMSのテンプレートのインストールが済んでいることが前提となります。

テンプレートは、以下のコマンドでインストールできます。

```
dotnet new install OrchardCore.ProjectTemplates::1.8.3
```


## 1. プロジェクトテンプレートを使う方法

Visual Studioを起動し、「新しいプロジェクトの作成」を選択します。

![](https://storage.googleapis.com/zenn-user-upload/543d79b383a3-20240606.png)

新しいプロジェクトの作成ダイアログで、"orchard"と入力し、見つかったテンプレートから「Orchard Core Cms Web App」を選びます。

![](https://storage.googleapis.com/zenn-user-upload/9a8a676f5cf9-20240606.png)

プロジェクト名を入力し、[次へ]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/55ce6df8ac1d-20240606.png)

追加情報ダイアログは、.NET8.0が選ばれていることを確認し、[作成]ボタンをクリックすます。

![](https://storage.googleapis.com/zenn-user-upload/6deb2e003e79-20240606.png)

これで、プロジェクトが作成されました。F5でデバッグ起動すると以下のようなセットアップページが開きます。

![](https://storage.googleapis.com/zenn-user-upload/7ef67b7c2ed4-20240606.png)



---

## 2. 空のプロジェクトから作成する方法

Visual Studio を起動し、「新しいプロジェクトの作成」を選択します。  
新しいプロジェクトの作成ダイアログで、"ASP.NET Core"と入力し、見つかったテンプレートから「ASP.NET Core（空）」を選びます。

![](https://storage.googleapis.com/zenn-user-upload/d190a627d23f-20240606.png)

プロジェクト名を入力し、\[次へ\]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/f8ca141d877d-20240606.png)

追加情報ダイアログは、.NET8.0が選ばれていることを確認し、\[作成\]ボタンをクリックすます。

![](https://storage.googleapis.com/zenn-user-upload/7062f1e7e5c4-20240606.png)


プロジェクトが作成されたら、ソリューションエクスプローラーで,「ソリューションのNuGetパッケージの管理」を選びます。

![](https://storage.googleapis.com/zenn-user-upload/11f56b400de1-20240606.png)


"OrchardCore.Application.Cms.Targets"パッケージをインストールします。
似たようなパッケージがあるので間違わないようにしてください。

![](https://storage.googleapis.com/zenn-user-upload/cc264d6b45f7-20240606.png)

パッケージがインストールできたら、Program.cs を以下のように書き換えます。

※ やっとC#プログラマーっぽい内容になった(笑)


```cs:program.cs
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOrchardCms();

var app = builder.Build();

if (!app.Environment.IsDevelopment()) {
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}

app.UseStaticFiles();
app.UseOrchardCore();

app.Run();
```

F5キーでデバッグ開始すれば、セットアップページが表示されます。

![](https://storage.googleapis.com/zenn-user-upload/7ef67b7c2ed4-20240606.png)


## 終わりに

以上で、Visual Studioを使いOrchard Coreのプロジェクトを作成する方法の説明は終わりです。
C#でWebアプリケーションを開発したことがあれば、何も難しいことはありませんね。


次回は、Orchard CoreをAzureにデプロイする方法について紹介します。
