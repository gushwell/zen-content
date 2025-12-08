---
title: "書籍『MCP入門 - 生成AIアプリ本格開発』のソースをC#に移植する・其の2"
emoji: "🧰"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "mcp", "mcpサーバー", "ai", "dotnet" ]
published: true
published_at: 2025-12-17 08:30
publication_name: zead
---


## はじめに

前回の記事の続きです。


今回は、[『MCP入門――生成AIアプリ本格開発』（技術評論社）](https://www.amazon.co.jp/MCP%E5%85%A5%E9%96%80%E2%80%95%E2%80%95%E7%94%9F%E6%88%90AI%E3%82%A2%E3%83%97%E3%83%AA%E6%9C%AC%E6%A0%BC%E9%96%8B%E7%99%BA-%E5%B0%8F%E9%87%8E-%E5%93%B2-ebook/dp/B0FWBTVP6Q)の第5章の掲載された`calculator_server_http.py' を C# へ移植します。

要は、前回の stdio 版の calculator_server.py を HTTP 版にしてみよう、ということです。

今回は HTTP 版ということで、ASP.NET Core を利用して HTTP 通信を行えるようにします。

元となった Python コードは、以下のリポジトリで公開されています。

https://github.com/gamasenninn/MCP_Learning

## .NET AI アプリ テンプレートをインストールする

事前準備として、Microsoft.Extensions.AI.Templates パッケージをインストールします。インストール済みの場合は、この手順はスキップしてください。

このパッケージは、AI 駆動型アプリケーションの開発を簡素化するために設計された、Microsoft が提供する .NET テンプレートパッケージであり、MCP サーバーの開発もサポートしています。

以下のコマンドを実行します。

```
dotnet new install Microsoft.Extensions.AI.Templates
```


## プロジェクトの作成

次に、C# の MCP サーバープロジェクトを作成します。筆者は、2025年秋に発表された .NET 10 を利用しています。

```
dotnet new mcpserver -n CalculatorServerHttp
```

## csprojファイルを変更する

`dotnet new mcpserver`コマンドで作成されるプロジェクトは、コンソールアプリケーションなので、CalculatorServerHttp.csprojファイルを編集します。

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <RuntimeIdentifiers>win-x64;win-arm64;osx-arm64;linux-x64;linux-arm64;linux-musl-x64</RuntimeIdentifiers>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>

    <!-- NuGetパッケージをMCPサーバーとして設定 -->
    <PackAsTool>true</PackAsTool>
    <PackageType>McpServer</PackageType>

    <!-- MCPサーバーを共有フレームワークに依存しない自己完結型アプリケーションとして設定 -->
    <SelfContained>true</SelfContained>
    <PublishSelfContained>true</PublishSelfContained>

    <!-- MCPサーバーを単一ファイル実行可能ファイルとして設定 -->
    <PublishSingleFile>true</PublishSingleFile>

    <!-- 推奨されるパッケージメタデータを設定 -->
    <PackageReadmeFile>README.md</PackageReadmeFile>
    <PackageId>SampleMcpServer</PackageId>
    <PackageVersion>0.1.0-beta</PackageVersion>
    <PackageTags>AI; MCP; server; http</PackageTags>
    <Description>MCP C# SDKを使用したMCPサーバー。</Description>
  </PropertyGroup>

  <!-- MCPサーバーの閲覧用に追加ファイルをインクルード -->
  <ItemGroup>
    <None Include=".mcp\server.json" Pack="true" PackagePath="/.mcp/" />
    <None Include="README.md" Pack="true" PackagePath="/" />
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="ModelContextProtocol" Version="0.4.0-preview.3" />
    <PackageReference Include="ModelContextProtocol.AspNetCore" Version="0.4.0-preview.3" />
  </ItemGroup>

</Project>
```

変更点は以下のとおりです。

- 1行目の`<Project Sdk="Microsoft.NET.Sdk">`を`<Project Sdk="Microsoft.NET.Sdk.Web">`に変更
- PackageReferenceに`Include="ModelContextProtocol.AspNetCore"`を追加


## CalculatorTools クラスを定義する

ここでは、MCP サーバーの本体となる CalculatorTools.csファイルをToolsフォルダに作成します。このクラスは、前回示したものと同じです。

```cs
using System.ComponentModel;
using ModelContextProtocol.Server;

namespace CalculatorServer.Tools;

/// <summary>
/// 電卓機能を提供するMCPツール
/// AI対応電卓のツール群
/// </summary>
internal class CalculatorTools
{
    [McpServerTool]
    [Description("2つの数値を加算（足し算）します。整数・小数に対応。金額計算、合計値の算出、累積計算などに使用。例：価格の合計、スコアの加算、距離の合算など。")]
    public double Add(
        [Description("加算する最初の数値")] double a,
        [Description("加算する2番目の数値")] double b)
    {
        return a + b;
    }

    [McpServerTool]
    [Description("2つの数値の差を計算（引き算）します。整数・小数に対応。差額計算、残高計算、変化量の算出などに使用。例：割引額の計算、在庫の減算、時間差の計算など。")]
    public double Subtract(
        [Description("減算する数値")] double a,
        [Description("減算される数値")] double b)
    {
        return a - b;
    }

    [McpServerTool]
    [Description("2つの数値の積（掛け算）を計算します。面積計算、単価×数量、累乗計算（同じ数を2回）などに使用。例：「100個買ったら合計いくら？」「5メートル四方の面積は？」")]
    public double Multiply(
        [Description("乗算する最初の数値")] double a,
        [Description("乗算する2番目の数値")] double b)
    {
        return a * b;
    }

    [McpServerTool]
    [Description("2つの数値の商（割り算）を計算します。比率計算、平均値算出、単価計算などに使用。ゼロ除算は自動的にエラー処理。例：「1人あたりの金額は？」「成功率は？」「時速を計算」")]
    public double Divide(
        [Description("除算する数値")] double a,
        [Description("除算される数値")] double b)
    {
        if (b == 0)
        {
            throw new ArgumentException("ゼロで割ることはできません");
        }
        return a / b;
    }

    [McpServerTool]
    [Description("累乗計算（aのb乗）を実行します。指数計算、複利計算、面積・体積の計算などに使用。例：「2の10乗は？」「年利5%で10年後は？」「立方体の体積」大きすぎる結果は自動的にエラー処理。")]
    public double Power(
        [Description("基数")] double a,
        [Description("指数")] double b)
    {
        try
        {
            return Math.Pow(a, b);
        }
        catch (OverflowException)
        {
            throw new InvalidOperationException("計算結果が大きすぎます");
        }
    }

    [McpServerTool]
    [Description("平方根（ルート）を計算します。距離計算、標準偏差、ピタゴラスの定理などに使用。負の数には対応していません（虚数は扱わない）。例：「100の平方根は？」「対角線の長さを求める」")]
    public double SquareRoot(
        [Description("平方根を計算する数値")] double a)
    {
        if (a < 0)
        {
            throw new ArgumentException("負の数の平方根は計算できません");
        }
        return Math.Sqrt(a);
    }

    [McpServerTool]
    [Description("円の面積を計算します（πr²）。半径から円の面積を算出。建築、デザイン、物理計算などに使用。例：「半径10cmの円の面積は？」「ピザのサイズを計算」結果は平方単位（半径がcmなら面積はcm²）。")]
    public double CircleArea(
        [Description("円の半径")] double radius)
    {
        if (radius < 0)
        {
            throw new ArgumentException("半径は正の数である必要があります");
        }
        return Math.PI * radius * radius;
    }
}
```

[McpServerTool]属性は、どのメソッドを MCP ツールとして公開するか」を示しています。

[Description]属性は、「そのツールが何をするものか、どんな場面で呼び出すべきなのか、その引数はどんな値を設定するのか」を LLMに説明するためのメタデータです。これを基にLLMはどのツール（メソッド）を呼び出すべきなのかを判断します。


## Program.cs の編集

Program.cs を次のように編集します。

```cs
using CalculatorServer.Tools;

var builder = WebApplication.CreateBuilder(args);

// すべてのログを stderr に送信するように設定します (MCP プロトコル メッセージには stdout が使用されます)。
builder.Logging.AddConsole(o => o.LogToStandardErrorThreshold = LogLevel.Trace);

// MCPサービスを追加します。使用するトランスポートは HTTP です。
// ツールは、CalculatorTools / RandomNumberTools クラスから明示的に登録します。
builder.Services
    .AddMcpServer()
    .WithHttpTransport()
    .WithTools<CalculatorTools>(); 

// CORS を有効化してクロスオリジンリクエストを許可します。
builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin()
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});

var app = builder.Build();

// CORS ミドルウェアを有効化します。
app.UseCors();

// MCP エンドポイントを /api/mcp にマッピングします。
app.MapMcp("/api/mcp");

await app.RunAsync();

```

## ビルド

準備が整ったので、ビルドして実行ファイルを作成します。

```
dotnet publish -c Release
```

`bin/Release/net10.0/publish/` に自己完結型の exe ファイルが作成されます。
この exe ファイルは、対象プラットフォーム用の .NET Runtime がインストールされていない環境でも実行できます。

:::message
今回は、csptojで、自己完結型の exe ファイルを生成するようにしています。
:::

## MCPサーバーを起動する

作成されたexeファイルを実行するか、プロジェクトのあるフォルダで、`dotnet run`でMCPサーバーを起動します。

```
p> dotnet run
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5000
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Production
info: Microsoft.Hosting.Lifetime[0]
      Content root path: E:\repos\GitHub\MCP_Learning\Chap05\CalculatorServerHttp

```


## MCP Inspectorを起動する

今回は、Claude Desktopではなく、MCP Inspectorを使ってみます。

MCP Inspector（Model Context Protocol Inspector）は、MCPサーバーのテストとデバッグに特化した開発者向けツールです。

以下のコマンドで起動すると、ブラウザが起動し、Inspectorのページが表示されます。

```
npx @modelcontextprotocol/inspector
```

:::message
はじめてこのコマンドを実行すると、インストールの確認メッセージが表示されますので、[y]で進んでください。
:::


## Inspectorで、CalculatorServerHttpに接続する。

左側の欄で、以下を設定し、Connectボタンをクリックします。

- Transport Type: Streamable Http
- URL: http:localhost:5000/api/mcp
- Connection Type: Direct

![](https://storage.googleapis.com/zenn-user-upload/8e3cc0e786ce-20251208.png)


## ツール一覧を表示する

接続したMCPサーバーにどんなツールがあるのか、一覧表示してみます。

上部の[Tools]ボタンをクリックし、[List Tools] をクリックします。

![](https://storage.googleapis.com/zenn-user-upload/42401b2ce223-20251208.png)


以下のように、ツール一覧が表示されます。

![](https://storage.googleapis.com/zenn-user-upload/e9cee0423218-20251208.png)

## ツールを呼び出してみる

ここでは、multiplyツールを呼び出してみます。一覧のmultiplyをクリックします。

右側にパラメータを入力する欄が現れますので、'a', 'b'に値を入れて、[Run Tool]ボタンをクリックします。

Tool Resultに、"63"と表示されればOKです。

![](https://storage.googleapis.com/zenn-user-upload/566904385914-20251208.png)

## 最後に

C# でも Http方式の MCP サーバーを実装できることが確認できました。

今回は、『MCP入門――生成AIアプリ本格開発』の第5章に掲載されているMCPサーバーをC#に移植しました。書籍によると、Claude Desktopは、Streamable-HTTP の MCP サーバーに “直接” 接続できないとのことで、MCP Inspectorで確認をしました。

書籍には、mcp-proxy を使って HTTP MCP サーバーをローカル MCP として見せる方法で、Claude Desktopから利用する方法も解説しています。興味のある方はぜひ読んでみてください。

次回は 第6章に掲載されている データベースと連携する MCP サーバー を C# に移植してみようと思います。
