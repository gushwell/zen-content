---
title: "ASP.NET CoreにSerilogを導入する初心者向けガイド"
emoji: "🥣"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["aspnetcore", "csharp", "serilog"]
published: true
published_at: 2025-08-28 21:30
publication_name: zead
---

## はじめに

Serilogは、構造化されたログを簡単に記録できる強力なロギングライブラリです。これを使うことで、アプリケーションの動作を監視したり、問題をデバッグしたりする際に役立つ詳細なログを残せます。

この記事では、ASP.NET CoreアプリケーションにSerilogを導入する方法を、わかりやすく解説します。

なおこの記事は、Serilog公式サイトやSerilogのGitHubリポジトリのドキュメントを参考にしています。    

https://serilog.net/

https://github.com/serilog/serilog-aspnetcore



    
    
## なぜSerilogを使うのか？

ASP.NET Coreには標準のロギング機能がありますが、Serilogは以下のような利点があります。

- **構造化ログ**: ログを単なるテキストではなく、JSON形式などの構造化データとして保存可能。これにより、ログの検索や分析が容易に。
- **豊富な出力先**: コンソール、ファイル、データベース、クラウドサービスなど、さまざまな出力先（シンク）にログを送信可能。
- **カスタマイズ性**: ログに追加情報（例: マシン名やリクエスト情報）を簡単に付加できる。
- **ASP.NET Coreとの統合**: ASP.NET CoreのロギングAPIとシームレスに連携。

初心者でも簡単に利用開始できるので、早速始めてみましょう！

## ステップ1: プロジェクトの準備

まず、ASP.NET Coreプロジェクトが必要です。以下の手順で新しいプロジェクトを作成します（すでにプロジェクトがある場合はスキップ可能）。

1. **Visual Studioまたはターミナルでプロジェクトを作成**:
   ```bash
   dotnet new webapi -n SerilogSample
   cd SerilogSample
   ```

   この記事では、WebAPIプロジェクトで説明しますが、Razor Pages、MVCでも手順は同じです。


2. **プロジェクトをVisual Studioで開く**（必要に応じて）:
   ```bash
   code .
   ```

これで、基本的なASP.NET Core Web APIプロジェクトが準備できました。

## ステップ2: SerilogのNuGetパッケージをインストール

Serilogをプロジェクトに追加するには、必要なNuGetパッケージをインストールします。以下のコマンドをターミナルまたはVisual StudioのNuGetパッケージマネージャーで実行します。

```bash
dotnet add package Serilog.AspNetCore
dotnet add package Serilog.Sinks.Console
dotnet add package Serilog.Sinks.File
```

- **Serilog.AspNetCore**: ASP.NET CoreとSerilogを統合するためのパッケージ。
- **Serilog.Sinks.Console**: ログをコンソールに出力するためのシンク。
- **Serilog.Sinks.File**: ログをファイルに出力するためのシンク。

## ステップ3: Serilogの設定

Serilogを設定するには、`Program.cs`を編集します。以下は、基本的な設定例です。


```csharp:program.cs
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Serilogの設定
builder.Host.UseSerilog((context, configuration) =>
{
    configuration
        .WriteTo.Console() // コンソールにログを出力
        .WriteTo.File("Logs/log-.txt", rollingInterval: RollingInterval.Day) // ファイルにログを出力（日次ローテーション）
        .Enrich.FromLogContext() // コンテキスト情報を追加
        .MinimumLevel.Information(); // ログの最低レベルをInformationに設定
});

// サービスを追加
builder.Services.AddControllers();

var app = builder.Build();

// Serilogのリクエストロギングミドルウェアを追加
app.UseSerilogRequestLogging();

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```


### コードのポイント

- **UseSerilog**: Serilogをホストに統合します。
- **WriteTo.Console()**: ログをコンソールに出力。
- **WriteTo.File()**: ログを`Logs/log-.txt`に日次で保存（例: `log-20250718.txt`）。
- **Enrich.FromLogContext()**: ログにコンテキスト情報（例: リクエストID）を追加。
- **UseSerilogRequestLogging()**: HTTPリクエストのログを簡潔に記録するミドルウェア。

## ステップ4: ログを記録する

ログを記録するには、`ILogger<T>`をコントローラーやサービスに注入して使用します。以下は、簡単なコントローラーの例です。


```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace SerilogSample.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IActionResult Get()
        {
            _logger.LogInformation("天気予報APIが呼び出されました");
            _logger.LogWarning("これは警告ログの例です");
            
            var forecast = $"天気予報データ: Date = {DateTime.Now}, TemperatureC = 25, Summary = \"Sunny\"";
            _logger.LogInformation(forecast);

            return Ok(forecast);
        }
    }
}
```


### コードのポイント

- **ILogger<T>**: ASP.NET Coreの標準ロギングインターフェースを使用。Serilogが裏で処理。
- **LogInformation**: 通常の情報ログを記録。
- **LogWarning**: 警告ログを記録。


## ステップ5: アプリケーションを実行してログを確認

プロジェクトを実行します：

```bash
dotnet run
```

1. **APIテスト**:
   ブラウザやPostmanで`https://localhost:5001/WeatherForecast`にアクセスし、ログを確認。

2. **コンソールログ**:
   ターミナルにログが出力されます。例：
   ```
   [2025-07-27 16:38:12 INF] 天気予報APIが呼び出されました
   [2025-07-27 16:38:12 WRN] これは警告ログの例です
   [2025-07-27 16:38:12 INF] 天気予報データ: Date = 2025/07/27 14:14:22, TemperatureC = 25, Summary = "Sunny"
   ```

3. **ファイルログ**:
   `Logs`フォルダに`log-YYYYMMDD.txt`が作成され、同じログが記録されます。


## ステップ6: appsettings.jsonで設定を管理（オプション）

ログ設定をコードではなく`appsettings.json`で管理することもできます。以下は例です。

```json
{
  "Serilog": {
    "Using": [ "Serilog.Sinks.Console", "Serilog.Sinks.File" ],
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    },
    "WriteTo": [
      { "Name": "Console" },
      {
        "Name": "File",
        "Args": {
          "path": "Logs/log-.txt",
          "rollingInterval": "Day"
        }
      }
    ],
    "Enrich": [ "FromLogContext", "WithMachineName", "WithThreadId" ],
    "Properties": {
      "Application": "SerilogSample"
    }
  }
}

```

上記設定では、Microsoft, System名前空間のログは、Warning以上にフィルタリングしています。

上記設定を読み込むように`Program.cs`を変更します。


```csharp:program.cs
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

// Serilogの設定をappsettings.jsonから読み込む
builder.Host.UseSerilog((context, configuration) =>
{
    configuration.ReadFrom.Configuration(context.Configuration);
});

// サービスを追加
builder.Services.AddControllers();

var app = builder.Build();

app.UseSerilogRequestLogging();
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```


### ポイント

- **ReadFrom.Configuration**: `appsettings.json`のSerilogセクションを読み込み。
- **JSONフォーマッタ**: ログをJSON形式で保存し、構造化ログを活用。


## ステップ7: 構造化ログをファイルに出力する

Serilogで構造化ログをファイルに出力するには、ログをJSON形式などの構造化フォーマットで保存する設定を追加します。


### 1. 必要なNuGetパッケージのインストール

構造化ログをJSON形式でファイルに出力するには、Serilog.Formatting.Compactパッケージが必要です。以下のコマンドでインストールします：

```
dotnet add package Serilog.Formatting.Compact
```

ただし、すでにインストールしている Serilog.AspNetCore パッケージには、Serilog.Formatting.Compactパッケージが含まれていますので、上記コマンドは実行しなくても問題ありません。

Serilog.Formatting.Compact: ログをコンパクトなJSON形式（CLEF: Compact Log Event Format）で出力。

### 2. 構成ファイルの設定

appsettings.jsonの"WriteTo"を以下のように書き換えます。

```json:appsettings.json
    "WriteTo": [
      { "Name": "Console" },
      {
        "Name": "File",
        "Args": {
          "path": "Logs/log-.txt",
          "rollingInterval": "Day",
+         "formatter": "Serilog.Formatting.Compact.CompactJsonFormatter, Serilog.Formatting.Compact" // この行を追加
        }
      }
    ],
```

### 3. 構造化ログの記録

コントローラーで構造化ログを記録するには、ILogger<T>を使用してオブジェクトをログに含めます。以下は例です：

```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

namespace SerilogSample.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IActionResult Get()
        {
            var forecast = new { Date = DateTime.Now, TemperatureC = 25, Summary = "Sunny" };
            _logger.LogInformation("天気予報データ: {@Forecast}", forecast);
            return Ok(forecast);
        }
    }
}
```

#### ポイント

**{@Forecast}**: プレースホルダーの@はオブジェクトを構造化データとしてログに記録します。これにより、forecastオブジェクトのプロパティ（Date, TemperatureC, Summary）がJSON形式で保持されます。

### 4. ログファイルの確認

アプリケーションを実行（dotnet run）し、APIを呼び出すと、Logsフォルダにlog-YYYYMMDD.txtが作成されます。ログファイルの内容は以下のようなJSON形式になります：

```text
{"@t":"2025-07-22T05:16:55.4884051Z","@mt":"天気予報データ: {@Forecast}","@tr":"7961cb5b8e70a7475d1ecd4ecf0145ba","@sp":"eb124c7f42ecffb2","Forecast":{"Date":"2025-07-22T14:16:55.4883004+09:00","TemperatureC":25,"Summary":"Sunny"},"SourceContext":"SerilogTest.Pages.PrivacyModel","ActionId":"06f92c9e-ae65-43c0-b324-ec658cf8ccd5","ActionName":"/Privacy","RequestId":"0HNE8RROBGB7K:00000015","RequestPath":"/Privacy","ConnectionId":"0HNE8RROBGB7K","Application":"SerilogSample"}
```

整形したものを以下に示します。

```json
{
  "@t": "2025-07-27T05:16:55.4884051Z",
  "@mt": "天気予報データ: {@Forecast}",
  "@tr": "7961cb5b8e70a7475d1ecd4ecf0145ba",
  "@sp": "eb124c7f42ecffb2",
  "Forecast": {
    "Date": "2025-07-27T14:16:55.4883004+09:00",
    "TemperatureC": 25,
    "Summary": "Sunny"
  },
  "SourceContext": "SerilogTest.Pages.PrivacyModel",
  "ActionId": "06f92c9e-ae65-43c0-b324-ec658cf8ccd5",
  "ActionName": "/Privacy",
  "RequestId": "0HNE8RROBGB7K:00000015",
  "RequestPath": "/Privacy",
  "ConnectionId": "0HNE8RROBGB7K",
  "Application": "SerilogSample"
}
```

- @t: タイムスタンプ
- @mt: メッセージテンプレート
- Forecast: 構造化データとして保存されたオブジェクト
  このJSON形式は、ログ分析ツール（例: Seq、ELK Stack）で簡単に解析できます。


### 5. コードでSerilogの設定をする（オプション）

appsettings.jsonの代わりにProgram.csで構造化ログの設定をすることも可能です。

```csharp:program.cs
using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;
using Serilog;
using Serilog.Formatting.Compact;

var builder = WebApplication.CreateBuilder(args);

// Serilogの設定
builder.Host.UseSerilog((context, configuration) =>
{
    configuration
        .WriteTo.Console() // コンソールにも出力（オプション）
        .WriteTo.File(
            new CompactJsonFormatter(), // JSON形式でログをフォーマット
            "Logs/log-.txt", // ログファイルのパス（日次ローテーション）
            rollingInterval: RollingInterval.Day
        )
        .Enrich.FromLogContext() // コンテキスト情報を追加
        .MinimumLevel.Information(); // ログの最低レベル
});

// サービスを追加
builder.Services.AddControllers();

var app = builder.Build();

app.UseSerilogRequestLogging();
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

#### コードのポイント

- **CompactJsonFormatter**: ログをコンパクトなJSON形式で出力。これにより、ログが構造化データとして解析しやすくなります。
- **WriteTo.File**: Logs/log-.txtに日次でログファイルを作成（例: log-20250718.txt）。
Enrich.FromLogContext: リクエストIDやカスタムプロパティをログに追加。

---

## 補足情報

- カスタムプロパティ: LogContext.PushProperty("UserId", userId)でログにカスタムデータを追加可能。
- エラーログ: Log.Error(ex, "エラーが発生: {@Details}", details)で例外情報を構造化ログとして記録。

- ファイルサイズ: ログファイルが大きくなる場合、restrictedToMinimumLevelやfileSizeLimitBytesを設定して制御。

- パフォーマンス: 構造化ログはテキストログより少し処理コストが高いので、ログレベル（例: Information以上）を適切に設定。

- ログ解析ツール: JSONログは、SeqやElasticsearchなどのツールで簡単にインポートしてて分析可能。






