---
title: "C#でMCP入門（NEWS API連携編）- 書籍『MCP入門』のPythonコードを移植する(5)"
emoji: "📰"
type: "tech"
topics: ["csharp", "mcp", "mcpサーバー", "ai", "dotnet", "newsapi"]
published: true
published_at: 2026-01-26 21:30
publication_name: zead
---

## はじめに

シリーズ第5回目の本記事では、[『MCP入門――生成AIアプリ本格開発』（技術評論社）](https://www.amazon.co.jp/MCP%E5%85%A5%E9%96%80%E2%80%95%E2%80%95%E7%94%9F%E6%88%90AI%E3%82%A2%E3%83%97%E3%83%AA%E6%9C%AC%E6%A0%BC%E9%96%8B%E7%99%BA-%E5%B0%8F%E9%87%8E-%E5%93%B2-ebook/dp/B0FWBTVP6Q)の第7章に掲載されているプログラム`newsapi_server.py`を C# に移植します。(著者の小野哲さんからは、移植および掲載の許可をいただいています)

:::message
『MCP入門―生成AIアプリ本格開発』を読んでいない方にも理解できる内容にしたつもりです。
:::


書籍『MCP入門』では、[NewsAPI](https://newsapi.org/)を利用して、ニュースを取得していましたが、本記事では、ニュース提供サービス NewsData.io を使って最新ニュース取得やキーワード検索を行う MCP サーバー（NewsServer）を C# で実装します。


---

## 何をするサーバーか（概要）

NewsServer の役割は、外部のニュース API（NewsData.io）を呼び出して得られた JSON を MCP ツールの戻り値としてそのまま返すことです。MCP クライアント（例: Claude Desktop）は返却された構造化データを利用してユーザーに自然言語で応答します。

具体的には次のツールを提供します：

- SearchNewsByCategory: カテゴリ／国ごとの最新ニュース取得
- SearchNewsByKeyword: キーワード検索によるニュース取得

:::message
書籍『MCP入門』では、get_latest_news、search_newsというメソッド名でしたが、SearchNewsByCategory、SearchNewsByKeywordと名前を変えています。メソッドの目的は変えていません。
:::


---

## NewsData.ioの の API キーを用意する

事前に NewsData.io のサイトから API キーを取得しておきます。

https://newsdata.io/

1. サイトにアクセスし、Loginリンクをクリックします。

2. Sign up here リンクをクリックします。

3. サインアップが完了するとダッシュボードページが表示されますので、左メニューのAPI Key項目をクリックします。

4. APIキーをメモしておきます。


---

## プロジェクトの作成

以下のコマンドで、MCP サーバープロジェクトとして作成します。

```bash
dotnet new mcpserver -n NewsServer
```

:::message
書籍『MCP入門』では、WeatherServerに、NewsServerのツールを追加していますが、こｎ記事では単独のNewsServer MCPサーバーを作成します。
:::


このプロジェクトでは、ＸＸＸパッケージを使いますので、インストールします。

```
nuget add  xxxxxx
```

---


## DTOクラスの定義

まずは、MCP経由でJSONとして返却される公開DTOクラスを定義します。C#のレコード型を利用しています。
元のPythonのコードは型定義をしていませんが、C#の良さを出すために、できるだけ忠実にC#の型に移植しています。

Toolsフォルダに、Dtos.csファイルを作成し、Dtosクラスを定義します。




---


## NewsDataTools.csの作成

Toolsフォルダに、NewsDataTools.csファイルを作成し、NewsDataToolsクラスを定義します。
このクラスは、NewsData.io API と連携してニュースを取得するツールクラスです。


NewsDataTools クラスには以下のツールが実装されています：

- SearchNewsByCategory: カテゴリ／国ごとの最新ニュース取得
- SearchNewsByKeyword: キーワード検索によるニュース取得

 [McpServerTool]属性、[Description]属性を使うのはこれまでと同じです。

今回作成したメソッドは、API の生レスポンスをそのまま返しています。もしかしたら、返すデータを絞った方が良いかもしれません。そのほうが、LLMでの負荷が軽くなると思われます。

---


## エントリポイント: Program.cs

エントリポイントとなる `Program.cs`を編集し、NewsDataToolsクラスをツールとして登録します。


## ビルドと実行

### ビルド

以下のコマンドでビルドします。

```
dotnet publish -c Release
```

`bin\Release\net10.0\win-x64\publish\`にexeファイルが作成されます。
この exe ファイルは、対象プラットフォーム用の .NET Runtime がインストールされていない環境でも実行できます。

### 実行ファイルとデータベースファイルをコピー

特定のフォルダに以下のファイルをコピーします。ここでは、`C:\mcp-learning\mcpserver`フォルダにコピーすることとします。

1. NewsServer.exe
1. NewsServer.pdb

### claude_desktop_config.jsonを編集

Claude Desktopに組み込んで動作を確認します。
`%APPDATA%\Claude\claude_desktop_config.json` を開き、以下のように記述します。前回の記事で作成したWeatherServerも一緒に組み込んでいます。

OPENWEATHER_API_KEY、NEWSDATA_API_KEYには、事前に取得したAPIキーを設定します。

```json
{
 "mcpServers": {
    "weather_server": {
      "command": "C:\\mcp-learning\\mcpserver\\WeatherServer.exe",
      "args": [],
      "env": {
        "OPENWEATHER_API_KEY": "ここにAPIキーを書く"
      }
    },
    "news_server": {
      "command": "C:\\mcp-learning\\mcpserver\\NewsServer.exe",
      "args": [],
      "env": {
        "NEWSDATA_API_KEY": "ここにAPIキーを書く"
"
      }
    }
}
```

:::message
Windows版のClaude Desktopは、OS側で設定した環境変数を正しく取得できないため、claude_desktop_config.jsonに環境変数を記述します。
:::

```


### Claude Desktopで確認

Claude Desktopを起動して、以下のような質問を投げてみます。

「最新のテクノロジーニュースを教えて」

「明日、シンガポールに行くので、シンガポールの天気とニュースを教えて」




## データフロー（概要）

ユーザー（質問） → Claude Desktop（LLM） → MCP Server（NewsServer） → NewsData.io API → MCP Server → Claude Desktop → ユーザー

概略図:
sequenceDiagram
    participant User
    participant Claude
    participant MCPServer
    participant newsdataAPI

    User->>Claude: 「最新のテクノロジーニュースを教えて」
    Claude->>MCPServer: SearchNewsByCategory(category="technology", country="us")
    MCPServer->>newsdataAPI: HTTP GET /latest?apikey=...&category=technology
    newsdataAPI-->>MCPServer: JSON レスポンス
    MCPServer-->>Claude: デシリアライズした構造化データ
    Claude-->>User: 要約して回答

---


## 最後に

この章では、C#を使用して外部 API と連携する MCPサーバーの作成方法について説明しました。
MCPツールが、何を受け取り何を返すべきなのかを見極めることができれば、あとは通常のWebAPIの呼び出しと変わりないことがわかりました。


次回は、第7章に掲載されている 位置情報API(IP-API)と連携する MCPサーバー" を C#に移植してみようと思います。


---

**これまでの記事**

[C#でMCP入門（HTTP方式編）- 書籍『MCP入門』のPythonコードを移植する](https://zenn.dev/zead/articles/mcp-learning-1)
[C#でMCP入門（STDIO方式編）- 書籍『MCP入門』のPythonコードを移植する](https://zenn.dev/zead/articles/mcp-learning-2)
[C#でMCP入門（DB接続編）- 書籍『MCP入門』のPythonコードを移植する](https://zenn.dev/zead/articles/mcp-learning-3)
[C#でMCP入門（WebAPI編）- 書籍『MCP入門』のPythonコードを移植する](https://zenn.dev/zead/articles/mcp-learning-4)



## 主要コードの読みどころ（抜粋説明）

- ツールの定義は次のメソッドにあります（詳細はファイル参照）：
  - [`Chap07/NewsServer/Tools/NewsDataTools.cs`](Chap07/NewsServer/Tools/NewsDataTools.cs:1) の `SearchNewsByCategory` と `SearchNewsByKeyword`。
- DTO 型は `Dtos.ApiResponse` を中心に受け取る形で実装されています（[`Chap07/NewsServer/Tools/Dtos.cs`](Chap07/NewsServer/Tools/Dtos.cs:1)）。

重要な実装箇所を簡単に要約します。

- SearchNewsByCategory:
  - category, country, limit といった引数を受け取り、NewsData.io の `/latest` エンドポイントへリクエストを投げます。
  - 内部で取得件数を `Math.Clamp()` により 1〜10 の範囲に正規化しています。

- SearchNewsByKeyword:
  - q（キーワード）と language, limit を受け取ります。キーワードが空の場合は例外を投げます。
  - limit は内部で 1〜20 の範囲に制限しています。

- MakeApiRequestAsync<T>:
  - URL を受け取り GET リクエストを投げ、成功時に JSON を受け取って `JsonSerializer.Deserialize<T>` でデシリアライズします。
  - リクエスト URL はデバッグのため stderr に出力されます（`Console.Error.WriteLine`）。

これらの挙動はすべて実装ファイルで確認できます: [`Chap07/NewsServer/Tools/NewsDataTools.cs`](Chap07/NewsServer/Tools/NewsDataTools.cs:1) 。

---

## エントリポイント（Program.cs）の設定

MCP サーバーの起動点である `Program.cs` では、MCP サーバーの登録とツールの公開を行っています。主要なポイントは次の通りです：

- ロギングを stderr に送る設定（MCP メッセージは stdout を使うため）を行う。
- MCP サーバーの追加: `.AddMcpServer().WithStdioServerTransport().WithTools<NewsDataTools>()` のようにツールを登録する。

実際の登録コードは [`Chap07/NewsServer/Program.cs`](Chap07/NewsServer/Program.cs:1) を参照してください。

---

## ビルドとデプロイ手順

1. プロジェクトのビルド（パブリッシュ）  
   リポジトリルートで次のコマンドを実行し、公開用の実行ファイルを作成します。  
   （ここでは dotnet の一般的手順を説明しています。プロジェクト名やターゲットは環境に合わせてください）

   - dotnet publish -c Release

   出力は `bin\Release\net10.0\win-x64\publish\` に生成されます。

2. 実行ファイルと必要なファイルをコピー  
   例: `C:\mcp-learning\mcpserver` フォルダに次をコピーします。
   - NewsServer.exe
   - NewsServer.pdb（必要に応じて）
   - その他ランタイムファイル（単一ファイル publish の場合は exe だけでも動作します）

3. Claude Desktop の設定  
   `%APPDATA%\Claude\claude_desktop_config.json` を開き、`mcpServers` に NewsServer を追加します。環境変数 `NEWSDATA_API_KEY` は claude_desktop_config.json の `env` セクションに記述することを推奨します（Windows 上の Claude Desktop は OS 環境変数が取り扱いにくいため）。

   例（抜粋）：
   ```
   {
     "mcpServers": {
       "news_server": {
         "command": "C:\\mcp-learning\\mcpserver\\NewsServer.exe",
         "args": [],
         "env": {
           "NEWSDATA_API_KEY": "ここに NewsData.io の API キーを書く"
         }
       }
     }
   }
   ```

---

## 実際に試す（想定されるプロンプト）

Claude Desktop などのクライアントから次のような問いかけを行います。

- 「最新のテクノロジーニュースを教えて」  
  → `SearchNewsByCategory(category: "technology", country: "us", limit: 5)` が呼ばれ API 結果が返ります。

- 「'quantum computing' に関する最近の記事を教えて」  
  → `SearchNewsByKeyword(query: "quantum computing", language: "en", limit: 10)` が呼ばれます。

返却された JSON（`Dtos.ApiResponse` 相当）はクライアント側で要約して自然言語の回答に変換されます。

---

## データフロー（概要）

ユーザー（質問） → Claude Desktop（LLM） → MCP Server（NewsServer） → NewsData.io API → MCP Server → Claude Desktop → ユーザー

概略図:
sequenceDiagram
    participant User
    participant Claude
    participant MCPServer
    participant newsdataAPI

    User->>Claude: 「最新のテクノロジーニュースを教えて」
    Claude->>MCPServer: SearchNewsByCategory(category="technology", country="us")
    MCPServer->>newsdataAPI: HTTP GET /latest?apikey=...&category=technology
    newsdataAPI-->>MCPServer: JSON レスポンス
    MCPServer-->>Claude: デシリアライズした構造化データ
    Claude-->>User: 要約して回答

---

## 開発上の注意点と改善案

- レスポンスの正規化  
  - 現状は API の生レスポンスを返しています。将来的には独自のサマリ DTO を作成して記事タイトル・要約・公開日などを抽出して返すと、LLM 側での後処理が楽になります。

- キャッシュの導入  
  - ニュースは頻繁に更新されますが、短時間で大量の同一問い合わせが来ると API レートに達する可能性があります。MemoryCache 等で短時間キャッシュを挟む設計が有効です。

- フォールトトレランス  
  - API の失敗時には意味のある例外や空の結果を返すようにし、クライアントで再試行や代替処理ができるようにするべきです。

- レート制限通知  
  - API が 429 を返した場合に専用の例外型を返し、クライアント側でリトライ遅延を行わせる設計も検討できます。

---

## 参考ファイル

- ツール本体: [`Chap07/NewsServer/Tools/NewsDataTools.cs`](Chap07/NewsServer/Tools/NewsDataTools.cs:1)
- DTO 定義: [`Chap07/NewsServer/Tools/Dtos.cs`](Chap07/NewsServer/Tools/Dtos.cs:1)
- エントリポイント: [`Chap07/NewsServer/Program.cs`](Chap07/NewsServer/Program.cs:1)
- 併読: DB編 [`mcp-learning-3.md`](mcp-learning-3.md:1)、Weather API 編 [`mcp-learning-4.md`](mcp-learning-4.md:1)

---

## おわりに

本稿では、NewsData.io を使った NewsServer の C# 実装の要点をまとめました。MCP ツールとしては「外部 API を呼んで構造化データを返す」ことが中心であり、API キー管理、HTTP クライアント再利用、レスポンスの取り扱いが重要です。実コード（[`Chap07/NewsServer/Tools/NewsDataTools.cs`](Chap07/NewsServer/Tools/NewsDataTools.cs:1)）を読みながら、自分の用途に合わせてレスポンス整形やキャッシュを追加してみてください。