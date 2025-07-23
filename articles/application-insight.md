---
title: "ASP.NET CoreでAzure Monitor OpenTelemetryを使いログを出力する"
emoji: "🔬"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "aspnetcore", "opentelemetry",  "applicationinsight", "azure"]
published: true
published_at: 2025-07-23 21:05
publication_name: zead
---

## はじめに

Azure Monitor の Application Insights は OpenTelemetry に対応しており、.NETアプリからログ・トレース・メトリクスを直接送信できます。

この記事では、ASP.NET CoreアプリケーションからOpenTelemetryを使ってAzure Application Insightsにログを送信する基本的な手順を示します。

OpenTelemetry についは、こちらを参照してください。
https://opentelemetry.io/ja/docs/what-is-opentelemetry/


## 前提条件

* ASP.NET Core アプリ（.NET 8以降）を作成します。
* Azure 上にApplication Insights リソースを用意します。まだなければ Azure Portal などから作成してください。
* Application Insights から接続文字列（Connection String）を取得できるようにしておきます（後述）。

## 必要な NuGet パッケージの追加

まず、ASP.NET CoreプロジェクトにAzure Monitor 用のOpenTelemetryパッケージをインストールします。次のコマンドを実行してください。

```bash
dotnet add package Azure.Monitor.OpenTelemetry.AspNetCore
```

* `Azure.Monitor.OpenTelemetry.AspNetCore` は ASP.NET Core アプリ向けの OpenTelemetry 拡張パッケージです。

これにより、アプリで OpenTelemetry 機能を利用できるようになります。

## プログラムコードの設定

`Program.cs` を編集して OpenTelemetry を有効化します。`Azure.Monitor.OpenTelemetry.AspNetCore` 名前空間をインポートし、`AddOpenTelemetry().UseAzureMonitor()` メソッドを呼び出すと、Azure Monitor への送信設定が有効になります。

```csharp:program.cs
using Azure.Monitor.OpenTelemetry.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.このサンプルでは、Razor Pagesを利用
builder.Services.AddRazorPages();

// OpenTelemetry を追加し、UseAzureMonitor() で Application Insights への送信を有効化
builder.Services.AddOpenTelemetry().UseAzureMonitor();

var app = builder.Build();

... 省略 ...


app.Run();
```

この設定だけで、ASP.NET Core の自動インストルメンテーションが有効になり、HTTP リクエストや既定のメトリクスなどのテレメトリが収集されます。

## ログ出力の設定

アプリ内で `ILogger<T>` を使ってログを出力すれば、OpenTelemetry で収集できます。たとえば、次のようにRazor Page Modelやコントローラーなどでログを記述します。

```csharp
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;

namespace ApplicationInsightsTest.Pages;
public class IndexModel : PageModel {
    private readonly ILogger<IndexModel> _logger;

    public IndexModel(ILogger<IndexModel> logger) {
        _logger = logger;
    }

    public void OnGet() {

    }

    public void OnPost(string action) {
        switch (action) {
            case "LogError":
                _logger.LogError("This is an error log.");
                break;
            case "LogWarning":
                _logger.LogWarning("This is a warning log.");
                break;
            case "LogInformation":
                _logger.LogInformation("This is an information log.");
                break;
            case "LogDebug":
                _logger.LogDebug("This is a debug log.");
                break;
            default:
                _logger.LogInformation("No action specified.");
                break;
        }
    }
}

```

cshtmlでは、以下のようにボタンを定義しておます。

```cshtml
<form method="post">
    <button type="submit" class="btn btn-info" name="action" value="LogInformation">Info</button>
    <button type="submit" class="btn btn-danger" name="action" value="LogError">Error</button>
    <button type="submit" class="btn btn-warning" name="action" value="LogWarning">Warning</button>
    <button type="submit" class="btn btn-secondary" name="action" value="LogDebug">Debug</button>
</form>
 ```   

## Application Insights への接続設定

ログやトレースを送信するために、Application Insights リソースの「接続文字列（Connection String）」をアプリに設定します。接続文字列は Azure Portal の Application Insights リソース \[概要\] タブで確認できます。「接続文字列」欄のコピーアイコンでクリップボードにコピーすることが出来ます。

![](https://storage.googleapis.com/zenn-user-upload/83cb1fab6691-20250718.png)


取得した接続文字列は、環境変数（APPLICATIONINSIGHTS_CONNECTION_STRING）でアプリに渡します。

```
APPLICATIONINSIGHTS_CONNECTION_STRING=<Your Connection String>
```

開発時は、`.NET` の `appsettings.json` に次のように記述しても構いません。ただ、実際の開発環境ではユーザシークレット（secrets.json）の機能を使うことをお勧めします。


```json
{
  "AzureMonitor": {
    "ConnectionString": "<Your Connection String>"
  }
}
```

上記の設定例では、コード内で `UseAzureMonitor(options => options.ConnectionString = "...")` とする方法と同等に、接続文字列を指定できます。設定は優先順があり、コードで指定した場合が最も優先され、次いで環境変数、最後に設定ファイルが適用されます。

運用環境では環境変数での設定が推奨されます。


## データの確認

アプリを実行した後、Azure Portal の Application Insights リソースでデータが受信されているか確認します。

ログやリクエストの情報が表示されるまで数分かかることがあります。これで ASP.NET Core アプリから OpenTelemetry を使ってログ・トレース・メトリクスが Application Insights に送信されるようになります。

![](https://storage.googleapis.com/zenn-user-upload/a35bf18e3494-20250718.png)

![](https://storage.googleapis.com/zenn-user-upload/8c98b47bde8e-20250718.png)

Kusto 照会言語 (KQL)で必要な情報だけを抽出することも可能です（詳細は省略）。


## サンプリングを有効にする

サンプリングを有効にしてトレースデータの量を減らすと、コストを削減することができます。 

サンプリングを有効にするには、以下のようにコードを書き換えます。

```csharp:program.cs
// Add Azure Monitor via OpenTelemetry
builder.Services.AddOpenTelemetry().UseAzureMonitor(options => {
    // Set the sampling ratio to 10%. This means that 10% of all traces will be sampled and sent to Azure Monitor.
    options.SamplingRatio = 0.1F;
});
```

SamplingRatio は0 から 1 の間の値を設定します。レート 0.1 は、トレースの約10%が送信されることを意味します。

なお、サンプリングは主にトレース（リクエストや依存関係などのテレメトリーデータ）に適用されます。アプリケーションから出力されたログとメトリックは、サンプリングの影響を受けません。つまり、アプリケーションから出力されたログデータはサンプリングによって間引かれることなく、すべてAzure Monitorに送信されます。

しかし、ログの量が多い場合、Azure Monitorのコストやリソース使用量が増える可能性があるため、ログの出力量を適切に管理することが必要です。


## インストルメンテーションのカスタマイズ

Azure Monitor OpenTelemetry には、ASP.NET Core、HttpClient用の .NET OpenTelemetry インストルメンテーションが含まれています。 これらのインストルメンテーションをカスタマイズしたり、独自に追加のインストルメンテーションを手動で追加したりできます。

以下にそのサンプルコードを示します。

### AspNetCoreTraceInstrumentationOptions のカスタマイズ

```cs
builder.Services.AddOpenTelemetry().UseAzureMonitor();
builder.Services.Configure<AspNetCoreTraceInstrumentationOptions>(options =>
{
    options.RecordException = true;
    options.Filter = (httpContext) =>
    {
        // only collect telemetry about HTTP GET requests
        return HttpMethods.IsGet(httpContext.Request.Method);
    };
});
```

上記コードでは、以下の設定を行っています。

- HTTP GET リクエストに限定してトレースを収集。
    POST や PUT リクエストなどはこの設定では無視されます。
- 例外が発生した場合は、その情報も記録するように設定。


### HttpClientTraceInstrumentationOptions のカスタマイズ

```cs
builder.Services.AddOpenTelemetry().UseAzureMonitor();
builder.Services.Configure<HttpClientTraceInstrumentationOptions>(options =>
{
    options.RecordException = true;
    options.FilterHttpRequestMessage = (httpRequestMessage) =>
    {
        // only collect telemetry about HTTP GET requests
        return HttpMethods.IsGet(httpRequestMessage.Method.Method);
    };
});
```

上記コードでは、以下の設定を行っています。

- アプリケーション内部から HttpClient で送信される HTTP リクエストのトレースを収集。
- その中でも GET メソッドのみを対象。
- 例外が発生した場合は、それもトレース情報として記録。

---

以上の手順で .NET 8 の ASP.NET Core アプリから OpenTelemetry を使ってログを出力し、Azure Monitor Application Insights に送信できるようになります。


## 参考資料

##### Azure Monitor の公式ドキュメント:  
- [.NET、Node.js、Python、Java アプリケーション用の Azure Monitor OpenTelemetry を有効にする](https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-enable)  
- [Azure Monitor OpenTelemetry を設定する](https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-configuration)
- [.NET Application Insights SDK から Azure Monitor OpenTelemetry に移行する](https://learn.microsoft.com/ja-jp/azure/azure-monitor/app/opentelemetry-dotnet-migrate?tabs=aspnetcore)
