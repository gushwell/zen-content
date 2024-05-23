---
title: "C#ベースのオープンソースCMS「Orchard Core」の環境構築"
emoji: "🍎"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "aspnetcore", "orchardcore"]
published: true
published_at: 2024-05-23 08:00
publication_name: zead
---

[前回の記事](https://zenn.dev/zead/articles/f604f9ad31f941)では、Orchard Coreの概要を説明したので、今回はOrchard Coreをインストールし、起動するまでを説明します。

前回の記事
<https://zenn.dev/zead/articles/f604f9ad31f941>

## .NET 8 SDKのインストール

以下のサイトからそれぞれの環境に合わせて.NET 8 SDKをインストールします。

<https://dotnet.microsoft.com/ja-jp/download/dotnet/8.0>

この記事では、Windowsでの環境構築を前提とします。

## Orchard Core CMSのテンプレートのインストール

.NET Core SDK をインストールしたら、次のコマンドを入力して、Orchard Core Web アプリケーションを作成するためのテンプレートをインストールします。

```cli
dotnet new install OrchardCore.ProjectTemplates::1.8.3
```

以下のような結果が表示されればOKです。

```cli
次のパッケージがインストールされます:
   OrchardCore.ProjectTemplates::1.8.3

成功: OrchardCore.ProjectTemplates::1.8.3により次のテンプレートがインストールされました。
テンプレート名            短い名前     言語  タグ
------------------------  -----------  ----  --------------------
Orchard Core Cms Module   ocmodulecms  [C#]  Web/Orchard Core/CMS
Orchard Core Cms Web App  occms        [C#]  Web/Orchard Core/CMS
Orchard Core Mvc Module   ocmodulemvc  [C#]  Web/Orchard Core/Mvc
Orchard Core Mvc Web App  ocmvc        [C#]  Web/Orchard Core/Mvc
Orchard Core Theme        octheme      [C#]  Web/Orchard Core/CMS
```

なお、最新のバージョンは、公式のドキュメントページに書いてあります。

<https://docs.orchardcore.net/en/latest/#status>

![](https://storage.googleapis.com/zenn-user-upload/e3633662ed99-20240522.png)

## Lombiq Orchard Visual Studio 拡張機能のインストール（オプション）

Visual Studioを利用するC#開発者は、Visual Studioを起動し、Lombiq Orchard Visual Studio 拡張機能をインストールします。インストールしなくても大丈夫です。この記事ではこの拡張機能は利用しません。

![](https://storage.googleapis.com/zenn-user-upload/6c8b89112116-20240522.png)

まだOrchard Coreを使いこなせていないので、この拡張機能で何ができるのか不明です(^^;)

これで環境構築は完了です。簡単ですね。

## サンプルCMSの作成

正しく環境構築ができたか確認します。

プロジェクトを作成したいディレクトリへ移動し、以下のコマンドでOrchard Coreアプリケーションプロジェクトを作成します。

```cli
dotnet new occms -n OrchardCoreSample
```

正常に終了すると、以下が表示されます。

```cli
テンプレート "Orchard Core Cms Web App" が正常に作成されました。
```

OrchardCoreSampledディレクトリには以下のようなファイルとフォルダが作成されます。

![](https://storage.googleapis.com/zenn-user-upload/7891f557c2c8-20240522.png)

次のコマンドでOrchardCoreSampleフォルダへ移動します

```cli
cd OrchardCoreSample
```

以下のコマンドでOrchardCoreプログラムを起動します。

```cli
dotnet run
```

しばらくすると、以下のメッセージが表示されます。

```cli
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: https://localhost:5001
2024-05-22 09:30:24.2798|INFO|Microsoft.Hosting.Lifetime|Now listening on: https://localhost:5001
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5000
2024-05-22 09:30:24.2980|INFO|Microsoft.Hosting.Lifetime|Now listening on: http://localhost:5000
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
2024-05-22 09:30:24.2980|INFO|Microsoft.Hosting.Lifetime|Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Development
2024-05-22 09:30:24.2980|INFO|Microsoft.Hosting.Lifetime|Hosting environment: Development
info: Microsoft.Hosting.Lifetime[0]
      Content root path: C:\Users\gushwell\zenn\OrchardCoreSample
2024-05-22 09:30:24.2980|INFO|Microsoft.Hosting.Lifetime|Content root path: C:\Users\gushwell\zenn\OrchardCoreSample
```

ブラウザを起動し、以下のURLへアクセスします。

```
https://localhost:5001/
```

以下のページが表示されればOKです。

![](https://storage.googleapis.com/zenn-user-upload/4bb6e3255b12-20240522.png)

これで、Orchard Coreの環境設定は完了です。

次の記事では、ここで作成したプロジェクトでサンプルのCMSサイトを構築する予定です。
