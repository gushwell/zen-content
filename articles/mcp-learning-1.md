---
title: "C#でMCP入門（STDIO方式編）- 書籍『MCP入門』のPythonコードを移植する(1)"
emoji: "🧰"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "mcp", "mcpサーバー", "ai", "dotnet" ]
published: true
published_at: 2025-12-18 08:30
publication_name: zead
---


## はじめに

今回から数回にわたり、[『MCP入門―生成AIアプリ本格開発』（技術評論社）](https://www.amazon.co.jp/MCP%E5%85%A5%E9%96%80%E2%80%95%E2%80%95%E7%94%9F%E6%88%90AI%E3%82%A2%E3%83%97%E3%83%AA%E6%9C%AC%E6%A0%BC%E9%96%8B%E7%99%BA-%E5%B0%8F%E9%87%8E-%E5%93%B2-ebook/dp/B0FWBTVP6Q)に掲載されている一部のソースコードを、C# に移植していく連載記事を書いていこうと思います。
著者の小野哲さんからは、移植および掲載の許可をいただいています。

本書は、MCPエコシステムを一通り学びながら実際に構築していくための一冊であり、MCP を体系的かつ実践的に身につけられるオススメの書籍です。

本連載の第1回となる今回は、第3章に掲載されている電卓 MCP サーバー（calculator_server.py）を C# で実装し直し、C# で MCP サーバーを作成する際の基本的な手順を学んでいきます。

元となった Python コードは、以下のリポジトリで公開されています。

https://github.com/gamasenninn/MCP_Learning

:::message
『MCP入門―生成AIアプリ本格開発』を読んでいない方にも理解できる内容にしたつもりです。
:::


## .NET AI アプリ テンプレートをインストールする

事前準備として、Microsoft.Extensions.AI.Templates パッケージをインストールします。
このパッケージは、AI駆動型アプリケーションの開発を簡素化するために設計された Microsoftが提供する .NET テンプレートパッケージであり、MCPサーバーの開発もサポートしています。

以下のコマンドを実行します。

```
dotnet new install Microsoft.Extensions.AI.Templates
```

## プロジェクトの作成

次に、C# の MCP サーバープロジェクトを作成します。筆者は、2025年秋に発表された .NET 10 を利用しています。

```
dotnet new mcpserver -n CalculatorServer
```

## CalculatorTools クラスを定義する

ここでは、MCP サーバーの本体となる CalculatorTools.csファイルをToolsフォルダに作成します。

```cs
using System.ComponentModel;
using ModelContextProtocol.Server;

namespace CalculatorServer.Tools;

/// <summary>
/// 電卓機能を提供するMCPツール
/// AI対応電卓のツール群
/// </summary>
public class CalculatorTools
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
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using CalculatorServer.Tools;

var builder = Host.CreateApplicationBuilder(args);

// すべてのログを stderr に送信するように設定します (MCP プロトコル メッセージには stdout が使用されます)。
builder.Logging.AddConsole(o => o.LogToStandardErrorThreshold = LogLevel.Trace);

// MCPサービスを追加します。使用するトランスポートは stdio です。
// ツールは、CalculatorToolsクラスを利用します。
builder.Services
    .AddMcpServer()
    .WithStdioServerTransport()
    .WithTools<CalculatorTools>();

await builder.Build().RunAsync();
```

## ビルド

準備が整ったので、ビルドして実行ファイルを作成します。

```
dotnet publish -c Release
```

`bin/Release/net8.0/publish/` に exe ファイルが作成されます。
この exe ファイルを実行するには、.NET Runtime は不要です。

## Claude Desktop に MCP サーバーを組み込む

#### exe ファイルを配置する

`C:\mcp-learning\mcpserver` フォルダーを作成し、ビルドで生成された CalculatorServer.exe をコピーします。

#### claude_desktop_config.json を編集する

Claude Desktop からこの C# 製 MCP 電卓サーバーを利用できるように、「ローカル stdio MCP サーバー」として登録します。ここでは Windows の手順を紹介します。

:::message
『MCP入門 - 生成AIアプリ本格開発』では、Claude Desktop を利用してMCPサーバーに接続していますので、この記事でもClaude Desktop を利用しています。
:::

`%APPDATA%\Claude\claude_desktop_config.json` を開き、以下のように記述します（存在しない場合はファイルを作成してください）。

```json
{
  "mcpServers": {
    "calculator": {
      "command": "C:\\mcp-learning\\mcpserver\\CalculatorServer.exe",
      "args": []
    }
  }
}
```

#### 組み込みの確認

Claude Desktop を起動し、[設定] → [開発者] ページを開きます。

![](https://storage.googleapis.com/zenn-user-upload/0286dd6e326f-20251205.png)

calculator サーバーが 青色で running と表示されていれば正常に組み込まれています。

![](https://storage.googleapis.com/zenn-user-upload/15ee9ad334a5-20251205.png)

## 実行してみる

次のプロンプトを入力して、動作を確認します。

```
今5000円手元にあります。年利5%ずつ増えると仮定して、複利計算すると5年後にはいくらになりますか？
```

実行結果で、作成した電卓 MCP サーバーの Power や Multiply ツールが利用されていれば成功です。

![](https://storage.googleapis.com/zenn-user-upload/672fdf57b46b-20251205.png)

## 最後に

C# でも Python と同様に MCP サーバーを実装できることが確認できました。

『MCP入門――生成AIアプリ本格開発』では、MCP の基礎から、サーバー構築、デバッグ方法、エラー時の対処まで丁寧に解説されていますので、興味のある方はぜひ読んでみてください。

今回は STDIO 方式の MCP サーバーを作成しましたが、次回は 第5章に掲載されている HTTP 通信方式の MCP サーバー を C# に移植してみようと思います。

---

本記事は、Qiita アドベントカレンダー「MCP Advent Calendar 2025」の18日目の記事です。
https://qiita.com/advent-calendar/2025/mcp
