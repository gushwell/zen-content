---
title: "C#でMCP入門（Webサーチ編）- 書籍『MCP入門』のPythonコードを移植する(7)"
emoji: "🧰"
type: "tech"
topics: ["csharp", "mcp", "mcpサーバー", "dotnet", "tavily"]
published: true
published_at: 2026-02-02 21:00
publication_name: zead
---

## はじめに

シリーズ第7回目の本記事では、[『MCP入門――生成AIアプリ本格開発』（技術評論社）](https://www.amazon.co.jp/MCP%E5%85%A5%E9%96%80%E2%80%95%E2%80%95%E7%94%9F%E6%88%90AI%E3%82%A2%E3%83%97%E3%83%AA%E6%9C%AC%E6%A0%BC%E9%96%8B%E7%99%BA-%E5%B0%8F%E9%87%8E-%E5%93%B2-ebook/dp/B0FWBTVP6Q)の第8章に掲載されているプログラム`universal_tools_server_web_2.py`を C# に移植します。(著者の小野哲さんからは、移植および掲載の許可をいただいています)

今回は、Web検索機能を提供するMCPサーバーを作成します。利用するサービスは、Tavilyです。

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
using System;
using System.Collections.Generic;

namespace Chap08WebSearchServer.Tools
{
    // Web検索 / Webページ取得で使う DTO をまとめたクラス
    public static class Dtos
    {
        // 単一の検索結果を表す DTO
        public record WebSearchResult
        {
            public string? Title { get; init; }
            public string? Url { get; init; }
            public string? Snippet { get; init; }
        }

        // WebSearch の応答 DTO
        public record WebSearchResponse
        {
            // 成功フラグ
            public bool Success { get; init; }
            // Tavily 等が返す要約的な answer（存在すれば）
            public string? Answer { get; init; }
            // 検索結果の配列
            public List<WebSearchResult>? Results { get; init; }
            // 元のクエリ
            public string? Query { get; init; }
            // エラー発生時のメッセージ（Success=false のときにセット）
            public string? Error { get; init; }
        }

        // GetWebpageContent の応答 DTO
        public record WebpageContentResponse
        {
            // 成功フラグ
            public bool Success { get; init; }
            // 取得元 URL
            public string? Url { get; init; }
            // ページタイトル
            public string? Title { get; init; }
            // 抽出した本文テキスト（必要であればトランケート済み）
            public string? Content { get; init; }
            // 指定長で切り捨てられたか
            public bool Truncated { get; init; }
            // エラー発生時のメッセージ（Success=false のときにセット）
            public string? Error { get; init; }
        }
    }
}
```

## MCPのToolsクラスを定義する


```cs
using System.ComponentModel;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using HtmlAgilityPack;
using ModelContextProtocol.Server;

namespace Chap08WebSearchServer.Tools
{
    /// <summary>
    /// 汎用Web検索とページ読取を提供するMCPツール
    /// </summary>
    public class WebTools
    {
        private static readonly string TAVILY_API_KEY = Environment.GetEnvironmentVariable("TAVILY_API_KEY") ?? string.Empty;

        private static readonly HttpClient _httpClient = new HttpClient();

        [McpServerTool]
        [Description("TavilyでWeb検索を実行します。")]
        public async Task<Dtos.WebSearchResponse> WebSearchAsync(
            [Description("検索クエリ")] string query,
            [Description("取得する最大結果数（デフォルト3）")] int numResults = 3)
        {
            // APIキー未設定時の即時応答
            if (string.IsNullOrEmpty(TAVILY_API_KEY))
            {
                return new Dtos.WebSearchResponse
                {
                    Success = false,
                    Error = "APIキーが未設定です"
                };
            }
    
            try
            {
                var payload = new Dictionary<string, object>
                {
                    ["api_key"] = TAVILY_API_KEY,
                    ["query"] = query,
                    ["max_results"] = numResults
                };
    
                var json = JsonSerializer.Serialize(payload);
                using var content = new StringContent(json, Encoding.UTF8, "application/json");
    
                // 同期的に呼び出す（MCPツールは同期でも動作する実装が多いので簡潔に）
                var response = await _httpClient.PostAsync("https://api.tavily.com/search", content);
                response.EnsureSuccessStatusCode();
    
                var respText = await response.Content.ReadAsStringAsync();
                using var doc = JsonDocument.Parse(respText);
                var root = doc.RootElement;
    
                // エラーチェック
                if (root.TryGetProperty("error", out var err))
                {
                    return new Dtos.WebSearchResponse
                    {
                        Success = false,
                        Error = err.GetString() ?? "unknown error"
                    };
                }
    
                // 結果を整形して DTO にマッピング
                var resultsList = new List<Dtos.WebSearchResult>();
                if (root.TryGetProperty("results", out var resultsElem) && resultsElem.ValueKind == JsonValueKind.Array)
                {
                    foreach (var r in resultsElem.EnumerateArray())
                    {
                        var title = r.TryGetProperty("title", out var t) ? t.GetString() ?? "" : "";
                        var url = r.TryGetProperty("url", out var u) ? u.GetString() ?? "" : "";
                        var contentStr = r.TryGetProperty("content", out var c) ? c.GetString() ?? "" : "";
                        var snippet = contentStr.Length > 400 ? contentStr.Substring(0, 400) : contentStr;
    
                        resultsList.Add(new Dtos.WebSearchResult
                        {
                            Title = title,
                            Url = url,
                            Snippet = snippet
                        });
                    }
                }
    
                var answer = root.TryGetProperty("answer", out var a) ? a.GetString() ?? "" : "";
    
                return new Dtos.WebSearchResponse
                {
                    Success = true,
                    Answer = answer,
                    Results = resultsList,
                    Query = query
                };
            }
            catch (Exception ex)
            {
                return new Dtos.WebSearchResponse
                {
                    Success = false,
                    Error = ex.Message
                };
            }
        }

        [McpServerTool]
        [Description("Webページの内容を取得してテキストを返します（スクリプトやスタイル除去）。")]
        public async Task <Dtos.WebpageContentResponse> GetWebpageContentAsync(
            [Description("取得するページのURL")] string url)
        {
            try
            {
                // ヘッダー指定（User-Agent）
                using var request = new HttpRequestMessage(HttpMethod.Get, url);
                request.Headers.UserAgent.ParseAdd("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36");
    
                var response = await _httpClient.SendAsync(request);
                response.EnsureSuccessStatusCode();
    
                var html = await response.Content.ReadAsStringAsync();
    
                var doc = new HtmlDocument();
                doc.LoadHtml(html);
    
                // script/style を完全に削除
                var nodesToRemove = doc.DocumentNode.SelectNodes("//script|//style");
                if (nodesToRemove != null)
                {
                    foreach (var n in nodesToRemove)
                    {
                        n.Remove();
                    }
                }
    
                // タイトル取得
                var titleNode = doc.DocumentNode.SelectSingleNode("//title");
                var title = titleNode != null ? titleNode.InnerText.Trim() : string.Empty;
    
                // テキスト抽出
                var text = doc.DocumentNode.InnerText ?? string.Empty;
    
                // クリーニング：行ごとにトリムして空の行を除去、その後連続空白を単一スペースにする
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
                // 連続スペースを1つに
                var cleaned = Regex.Replace(joined, @"\s{2,}", " ").Trim();
    
                var truncated = cleaned.Length > 2000;
                var content = truncated ? cleaned.Substring(0, 2000) : cleaned;
    
                return new Dtos.WebpageContentResponse
                {
                    Success = true,
                    Url = url,
                    Title = title,
                    Content = content,
                    Truncated = truncated
                };
            }
            catch (Exception ex)
            {
                return new Dtos.WebpageContentResponse
                {
                    Success = false,
                    Error = $"取得エラー: {ex.Message}"
                };
            }
        }
    }
}
```


### コードの解説

### 環境変数による API キー管理

API キーは環境変数 TAVILY_API_KEY から読み込んでいます。キー未設定時に即座に成功フラグ false を返しています。


### JSON 処理の方針

検索 API のレスポンスは JsonDocument でパースし、必要なフィールド（answer, results）のみ抽出して DTO へ整形しています。生レスポンスをそのまま渡すと LLM 側の負荷が増えるため、必要情報に絞り込むことが設計上有益です。

### HTML クレンジングの実務的工夫

ページ本文抽出では HtmlAgilityPack を用い、`<script>/<style>` を除去してから InnerText を取り、空行を削除、連続空白を圧縮する処理を行っています。さらに長さを 2000 文字に切り詰め、Truncated フラグを返す仕様にして、LLM 側での処理コストを制御しています。

実運用ではノイズをさらに減らすために以下の改善を検討すると良いでしょう。

- body 限定抽出: head やメタ情報、ナビゲーションが混入するのを避けるため、可能であれば body ノードのみを対象にテキストを抽出します。
- noscript / コメント除去: `<noscript>` や HTML コメントはノイズになることが多いので削除します。
- HTML エンティティのデコード: `&nbsp;` 等をデコードして可読なテキストにします（HtmlAgilityPack の HtmlEntity.DeEntitize を使用）。
- 段落単位の保持: p 要素ごとに分割して段落を維持すると、LLM に渡す際に文脈保持に有利です（段落間を1つの空行でつなぐ等）。
- 空白の正規化: 連続空白・改行を正規化して不要な改行を減らします。


### エラーハンドリング設計

失敗時は成功フラグを false にし、Error メッセージを返す形に統一しています（DTO の Success/Error）。これにより LLM がツールの呼び出し結果を判別しやすくなります。


## 6. Claude Desktop への組み込み（例）

Windows で Claude Desktop に組み込むときの `claude_desktop_config.json` の例です。


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
:::message
Windows版のClaude Desktopは、OS側で設定した環境変数を正しく取得できないようです。そのため、苦肉の策でclaude_desktop_config.jsonに環境変数を記述しています。本番運用する場合には、別の対策を検討してください。
:::

:::message
Claude Desktopで動作を検証する場合は、標準のWebサーチ機能が働かないように、「websearch_serverを使ってください」など質問を工夫して動作を確認してください。
:::
---

## 最後に

今回は、C#を使用してWeb検索を行うMCPサーバーを作成しました。実際の運用では、robots.txtの制御やレート制限なども考慮した実装が必要になると思われます。
また、長文のページを扱う場合の工夫も必要になるかもしれません。


次回は、第8章に掲載されている Pythonコードを実行するMCPサーバーを C#に移植してみようと思います。気が向いたらC#のコードを実行するMCPサーバーにするかもしれません。多分、次回が最終回となる予定です。

---

**これまでの記事**

- [C#でMCP入門（HTTP方式編）- 書籍『MCP入門』のPythonコードを移植する(1)](https://zenn.dev/zead/articles/mcp-learning-1)
- [C#でMCP入門（STDIO方式編）- 書籍『MCP入門』のPythonコードを移植する(2)](https://zenn.dev/zead/articles/mcp-learning-2)
- [C#でMCP入門（DB接続編）- 書籍『MCP入門』のPythonコードを移植する(3)](https://zenn.dev/zead/articles/mcp-learning-3)
- [C#でMCP入門（Weather API連携編）- 書籍『MCP入門』のPythonコードを移植する(4)](https://zenn.dev/zead/articles/mcp-learning-4)
- [C#でMCP入門（NEWS API連携編）- 書籍『MCP入門』のPythonコードを移植する(5)](https://zenn.dev/zead/articles/mcp-learning-5)
- [C#でMCP入門（IP情報連携編）- 書籍『MCP入門』のPythonコードを移植する(6)](https://zenn.dev/zead/articles/mcp-learning-6)
