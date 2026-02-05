---
title: "C#でMCP入門（Webサーチ編）- 書籍『MCP入門』のPythonコードを移植する(7)"
emoji: "🧰"
type: "tech"
topics: ["csharp", "mcp", "mcpサーバー", "dotnet", "tavily"]
published: true
published_at: 2026-02-09 21:00
publication_name: zead
---

## はじめに

シリーズ第7回目（最終回）の本記事では、[『MCP入門――生成AIアプリ本格開発』（技術評論社）](https://www.amazon.co.jp/MCP%E5%85%A5%E9%96%80%E2%80%95%E2%80%95%E7%94%9F%E6%88%90AI%E3%82%A2%E3%83%97%E3%83%AA%E6%9C%AC%E6%A0%BC%E9%96%8B%E7%99%BA-%E5%B0%8F%E9%87%8E-%E5%93%B2-ebook/dp/B0FWBTVP6Q)の第8章に掲載されているプログラム`universal_tools_server_web_2.py`を C# に移植します。(著者の小野哲さんからは、移植および掲載の許可をいただいています)

今回は、Web検索機能をMCPサーバーを作成します。利用するサービスは、Tavilyです。

https://api.tavily.com/search


:::message
『MCP入門―生成AIアプリ本格開発』を読んでいない方にも理解できる内容にしたつもりです。
:::

元となった Python コードは、以下のリポジトリで公開されています。

https://github.com/gamasenninn/MCP_Learning

なお、本記事では、プロジェクトの作成手順やセットアップ手順は過去回に委ね、本質的な設計決定と注意点に絞って説明します。

過去の回へのリンクは、本記事の最後に掲載しています。

---

## 1. 実装する２つのツール

**検索（外部検索 API へ問い合わせ）: WebSearch()**

Tavily の検索 API（https://api.tavily.com/search）を使い、JSON を受け取って要約（answer）と検索結果リストを返す。

**ページ読取（指定 URL の本文抽出）: GetWebpageContent()**

HtmlAgilityPack を用いて HTML からスクリプト/スタイルを除去し、本文テキストを抽出・クリーニングして返却（長さは最大 2000 文字で切り詰め）。

## 2. DTOクラスの定義

上記ツールの戻り値を表すDTOクラスを定義します。


```cs
namespace Chap08WebSearchServer.Tools;

// Web検索 / Webページ取得で使う DTO をまとめたクラス
// コメントは日本語で記述し、Chap07 のスタイルに合わせて record を使用する。

public static class Dtos
{
    // 単一の検索結果を表す DTO
    public record WebSearchResult(
        string? Title,
        string? Url,
        string? Snippet
    );

    // WebSearch の応答 DTO
    public record WebSearchResponse(
        // 成功フラグ
        bool Success,
        // Tavily 等が返す要約的な answer（存在すれば）
        string? Answer,
        // 検索結果の配列
        List<WebSearchResult>? Results,
        // 元のクエリ
        string? Query,
        // エラー発生時のメッセージ（Success=false のときにセット）
        string? Error
    );

    // GetWebpageContent の応答 DTO
    public record WebpageContentResponse(
        // 成功フラグ
        bool Success,
        // 取得元 URL
        string? Url,
        // ページタイトル
        string? Title,
        // 抽出した本文テキスト（必要であればトランケート済み）
        string? Content,
        // 指定長で切り捨てられたか
        bool Truncated,
        // エラー発生時のメッセージ（Success=false のときにセット）
        string? Error
    );
}
```

## MCPのToolsクラスを定義する


```cs
// 必要な名前空間をインポート
using System.ComponentModel;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using HtmlAgilityPack;
using ModelContextProtocol.Server;

namespace Chap08WebSearchServer.Tools;
/// <summary>
/// 汎用Web検索とページ読取を提供するMCPツール
/// </summary>
// Web検索とページ取得を提供するツールクラス
public class WebTools
{
    // Tavily APIキーを環境変数から取得
    private static readonly string TAVILY_API_KEY = Environment.GetEnvironmentVariable("TAVILY_API_KEY") ?? string.Empty;

    // HTTPクライアントのインスタンスを共有
    private static readonly HttpClient _httpClient = new HttpClient();

    // Web検索を実行するMCPツールメソッド
    [McpServerTool]
    [Description("TavilyでWeb検索を実行します。")]
    public Dtos.WebSearchResponse WebSearch(
        [Description("検索クエリ")] string query,
        [Description("取得する最大結果数（デフォルト3）")] int numResults = 3,
        CancellationToken ct = default)
    {
        // APIキー未設定時の即時応答
        if (string.IsNullOrEmpty(TAVILY_API_KEY))
        {
            return new Dtos.WebSearchResponse(false, null, null, null, "APIキーが未設定です");
        }
    
        try
        {
            // APIリクエストのペイロードを作成
            var payload = new Dictionary<string, object>
            {
                ["api_key"] = TAVILY_API_KEY,
                ["query"] = query,
                ["max_results"] = numResults
            };

            // JSONにシリアライズしてHTTPコンテンツを作成
            var json = JsonSerializer.Serialize(payload);
            using var content = new StringContent(json, Encoding.UTF8, "application/json");
    
            // Tavily APIにPOSTリクエストを同期的に送信
            var response = _httpClient.PostAsync("https://api.tavily.com/search", content, ct).GetAwaiter().GetResult();
            response.EnsureSuccessStatusCode();
    
            // レスポンスを文字列として読み込み、JSONドキュメントにパース
            var respText = response.Content.ReadAsStringAsync(ct).GetAwaiter().GetResult();
            using var doc = JsonDocument.Parse(respText);
            var root = doc.RootElement;

            // APIレスポンスのエラーをチェック
            if (root.TryGetProperty("error", out var err))
            {
                return new Dtos.WebSearchResponse(false, null, null, null, err.GetString() ?? "unknown error");
            }
    
            // 検索結果をリストに収集
            var resultsList = new List<Dtos.WebSearchResult>();
            if (root.TryGetProperty("results", out var resultsElem) && resultsElem.ValueKind == JsonValueKind.Array)
            {
                foreach (var r in resultsElem.EnumerateArray())
                {
                    // 各結果からタイトル、URL、コンテンツを抽出
                    var title = r.TryGetProperty("title", out var t) ? t.GetString() ?? "" : "";
                    var url = r.TryGetProperty("url", out var u) ? u.GetString() ?? "" : "";
                    var contentStr = r.TryGetProperty("content", out var c) ? c.GetString() ?? "" : "";
                    // スニペットを400文字以内に制限
                    var snippet = contentStr.Length > 400 ? contentStr.Substring(0, 400) : contentStr;
    
                    resultsList.Add(new Dtos.WebSearchResult(title, url, snippet));
                }
            }

            // APIからの回答を抽出
            var answer = root.TryGetProperty("answer", out var a) ? a.GetString() ?? "" : "";
    
            // 成功レスポンスを構築
            return new Dtos.WebSearchResponse(true, answer, resultsList, query, null);
        }
        catch (Exception ex)
        {
            // エラーが発生した場合の失敗レスポンス
            return new Dtos.WebSearchResponse(false, null, null, null, ex.Message);
        }
    }

        // Webページの内容をテキストとして取得するMCPツールメソッド
    [McpServerTool]
    [Description("Webページの内容を取得してテキストを返します（スクリプトやスタイル除去）。")]
    public Dtos.WebpageContentResponse GetWebpageContent(
        [Description("取得するページのURL")] string url, CancellationToken ct = default)
    {
        try
        {
            // HTTPリクエストを作成し、User-Agentヘッダーを設定
            using var request = new HttpRequestMessage(HttpMethod.Get, url);
            request.Headers.UserAgent.ParseAdd("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36");
    
            // リクエストを送信（同期的に）
            var response = _httpClient.SendAsync(request, ct).GetAwaiter().GetResult();
            response.EnsureSuccessStatusCode();
    
            // HTMLコンテンツを読み込み（同期的に）
            var html = response.Content.ReadAsStringAsync(ct).GetAwaiter().GetResult();
    
            // HtmlAgilityPackでHTMLをパース
            var doc = new HtmlDocument();
            doc.LoadHtml(html);

            // スクリプトとスタイル要素を削除してクリーンなHTMLにする
            var nodesToRemove = doc.DocumentNode.SelectNodes("//script|//style");
            if (nodesToRemove != null)
            {
                foreach (var n in nodesToRemove)
                {
                    n.Remove();
                }
            }
    
            // ページタイトルを抽出
            var titleNode = doc.DocumentNode.SelectSingleNode("//title");
            var title = titleNode != null ? titleNode.InnerText.Trim() : string.Empty;
    
            // すべてのテキストコンテンツを抽出
            var text = doc.DocumentNode.InnerText ?? string.Empty;

            // テキストをクリーンアップ：改行で分割し、空行を除去、トリムして結合
            var lines = text.Split(new[] { '\r', '\n' }, StringSplitOptions.RemoveEmptyEntries);
            var cleanLines = new List<string>();
            foreach (var line in lines)
            {
                var trimmed = line.Trim();
                if (!string.IsNullOrEmpty(trimmed))
                {
                    cleanLines.Add(trimmed);
                }
            }
            var joined = string.Join(" ", cleanLines);
            // 連続する空白を単一のスペースに正規化
            var cleaned = Regex.Replace(joined, @"\s{2,}", " ").Trim();

            // コンテンツを2000文字以内に制限
            var truncated = cleaned.Length > 2000;
            var content = truncated ? cleaned.Substring(0, 2000) : cleaned;
    
            // 成功レスポンスを返す
            return new Dtos.WebpageContentResponse(true, url, title, content, truncated, null);
        }
        catch (Exception ex)
        {
            // 取得失敗時のエラーレスポンス
            return new Dtos.WebpageContentResponse(false, null, null, null, false, $"取得エラー: {ex.Message}");
        }
    }
}
```


### コードの解説

### 環境変数による API キー管理

API キーは環境変数 TAVILY_API_KEY から読み込んでいます（実装箇所: Chap08/WebSearchServer/Tools/WebTools.cs）。Claude Desktop 等で起動する場合、OS の環境変数が渡らないケースがあるため、前回記事のように起動設定に明示的に env を書くなどの対応が必要です。

表示例: 実装ではキー未設定時に即座に成功フラグ false を返す設計（早期失敗で LLM 側の誤作動を防ぐ）。

### JSON処理の方針

検索 API のレスポンスは JsonDocument でパースし、必要なフィールド（answer, results）のみ抽出して DTO へ整形しています（WebSearch() 内処理）。生レスポンスをそのまま渡すと LLM 側の負荷が増えるため、必要情報に絞り込むことが設計上有益です。

### HTMLクレンジングの工夫

ページ本文抽出では HtmlAgilityPack を用い、`<script>/<style>` を除去してから InnerText を取り、空行を削除、連続空白を圧縮する処理を行っています（GetWebpageContent()）。さらに長さを 2000 文字に切り詰め、Truncated フラグを返す仕様にして、LLM 側での処理コストを制御しています。

### エラーハンドリング設計

失敗時は成功フラグを false にし、Error メッセージを返す形に統一しています（DTO の Success/Error）。これにより LLM がツールの呼び出し結果を判別しやすくなります（WebSearch の error パス: Chap08/WebSearchServer/Tools/WebTools.cs）。


## 6. MCPサーバーのの組み込み（例）

mcpサーバーを組み込むjsonファイルの例です。

```json
{
  "mcpServers": {
    "websearch_server": {
      "command": "C:\\mcp-learning\\mcpserver\\WebSearchServer.exe",
      "args": [],
      "env": {
        "TAVILY_API_KEY": "ここにAPIキーを書く"
      }
    }
 }
}
```


---

### 実行例

Claude Desktopで確認しようとしたのですが、なぜかうまくMCPツールを認識してくれませんでした。そのため、普段活用しているKilo Code（VSCodeの拡張機能）から呼び出してみました。


「C#の概要をWebで調べて300文字程度にまとめてください。」


![](/images/mcp-learning-7/image.png)

---

## 最後に

今回は、C#を使用してWeb検索を行うMCPサーバーを作成しました。実際の運用では、robots.txtの制御やレート制限なども考慮した実装が必要になると思われます。
また、長文のページを扱う場合の工夫も必要になるかもしれません。

既存のMCPクライアントを利用する場合は、Web検索機能は標準で備わっていることが多いので、必要ないかもしれませんが、MCPクライアントも含め自作した場合には作成する価値はあると思います。

書籍『MCP入門』では、

- **第8章の後半**: Pythonのコードを実行させるMCPサーバーの説明
- **第9章**: MCPホストを自作する
- **第10章**: MCPエージェント（AIエージェント）を作成する

と続きます。興味のある方は、是非書籍を読んでいただければと思います。

「C#でMCP入門（Webサーチ編）- 書籍『MCP入門』のPythonコードを移植する」のシリーズは、今回の記事を最終回としたいと思います。


---

**記事目次**

- [C#でMCP入門（HTTP方式編）- 書籍『MCP入門』のPythonコードを移植する(1)](https://zenn.dev/zead/articles/mcp-learning-1)
- [C#でMCP入門（STDIO方式編）- 書籍『MCP入門』のPythonコードを移植する(2)](https://zenn.dev/zead/articles/mcp-learning-2)
- [C#でMCP入門（DB接続編）- 書籍『MCP入門』のPythonコードを移植する(3)](https://zenn.dev/zead/articles/mcp-learning-3)
- [C#でMCP入門（Weather API連携編）- 書籍『MCP入門』のPythonコードを移植する(4)](https://zenn.dev/zead/articles/mcp-learning-4)
- [C#でMCP入門（NEWS API連携編）- 書籍『MCP入門』のPythonコードを移植する(5)](https://zenn.dev/zead/articles/mcp-learning-5)
- [C#でMCP入門（IP情報連携編）- 書籍『MCP入門』のPythonコードを移植する(6)](https://zenn.dev/zead/articles/mcp-learning-6)
- [C#でMCP入門（Webサーチ編）- 書籍『MCP入門』のPythonコードを移植する(7)](https://zenn.dev/zead/articles/mcp-learning-7) 
