---
title: "GitHub Copilot の利用方法（Visual Studio 2022 向け）"
emoji: "✈"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["visualstudio2022", "visualstudio", "githubcopilot"]
published: true
published_at: 2025-05-11 20:45
publication_name: "zead"
---

## はじめに

このドキュメントは、Visual Studio 2022 上で GitHub Copilot を使い始める方を対象にしています。
基本的な使い方から、チャット機能や便利なコマンドまで、順を追ってわかりやすく解説します。

### 事前に以下をご確認ください：

- Visual Studio 2022 がインストールされていること

- GitHub Copilot 拡張機能がインストールされ、有効化されていること

- GitHub アカウント で Copilot の利用契約が完了していること

セットアップがまだの方は、まず Visual Studio の拡張機能管理画面から
「GitHub Copilot」を検索してインストールし、GitHub アカウントでサインインしてください。


## コード補完

GitHub Copilot を有効にすると、コード入力中に自動で提案が表示されます。

- **提案を受け入れる**：`Tab` キー  
- **提案をスキップする/拒否する**：`Esc` キー

### 補完の例

```csharp
// メソッドのシグネチャを入力したとき
int CalculateDaysBetweenDates(

// コメントを入力したとき
var doc = XDocument.Load("index.xhtml");
// find all images

// メソッドやクラスの一部を入力したとき
JsonSerializer.
```

### コメントの自動生成

`///` を入力して `Enter` を押すと、Copilot がコメントの候補を提案します。

### 代替候補の切り替え

- `Alt + .`：次の提案に切り替え  
- `Alt + ,`：前の提案に戻る


## Copilot Chat

### 2種類のチャット方法

#### インラインチャット（エディタ内）

- `Alt + /` で表示  
- コード編集の流れを止めずに質問できます  

![インラインチャット](https://storage.googleapis.com/zenn-user-upload/e5b55be9600d-20250508.png)

#### チャットウインドウ（専用パネル）

- Visual Studio の右上にある Copilot アイコンをクリックし、「チャットウィンドウを開く」を選択。 

![チャットウインドウ](https://storage.googleapis.com/zenn-user-upload/8b7aad8c76c5-20250508.png)

- よく使うショートカット：
  - `Ctrl + N`：新しいスレッドを作成
  - `Ctrl + Shift + T`：過去スレッドのドロップダウン表示

### モデルの選択

ウィンドウ右下の **AIモデルピッカー** から選択可能。  
通常は **GPT-4o** がデフォルトで設定されています。

![モデルピッカー](https://storage.googleapis.com/zenn-user-upload/899c1f80bb7f-20250508.png)
---

### スラッシュコマンド `/`

簡単なコマンドで、プロンプトを入力せずに共通タスクを実行できます。

| コマンド      | 内容                                                                 |
|---------------|----------------------------------------------------------------------|
| `/doc`        | コメントの自動生成（選択中コードまたは指定範囲）                   |
| `/explain`    | コードの説明                                                         |
| `/fix`        | バグ修正やリファクタリング                                           |
| `/generate`   | 質問に基づくコード生成（スペル注意: "gener**a**te" ではなく "gener**e**te"） |
| `/help`       | Copilot Chat の使い方ヘルプ                                          |
| `/optimize`   | パフォーマンス改善                                                   |
| `/tests`      | 単体テストの生成                                                     |

---

### ハッシュコマンド `#`

ファイル・クラス・メソッドをチャット内で直接指定できます。

例：
- `#BasketService.cs`：ファイル全体を参照
- `#AddItemToBasket`：メソッドを参照（ファイルと組み合わせて `#BasketService.cs の #AddItemToBasket` も可能）

---

### アットコマンド `@`

スコープやコンテキストを指定できます。

| コマンド       | 内容                                      |
|----------------|-------------------------------------------|
| `@GitHub`      | リポジトリ全体を参照                     |
| `@Workspace`   | ソリューション全体を対象にする           |
| `@VS`          | Visual Studio に関する質問                |

> その他の拡張機能は [GitHub Marketplace](https://github.com/marketplace?type=apps&copilot_app=true) からインストール可能

#### 気になる拡張機能

- Docker for GitHub Copilot  

    https://github.com/marketplace/docker-for-github-copilot

- Mermaid Chat  

    https://github.com/marketplace/mermaid-chart

---

### チャット使用例

| 質問例                                               | 対象コンテキスト                       |
|------------------------------------------------------|----------------------------------------|
| `#MyFile.cs の目的は何ですか: 66-72`                | ファイルの特定行範囲                   |
| `#BasketService.cs のテストはどこにありますか?`     | 指定ファイル全体                       |
| `/#BasketService.cs 内の #AddItemToBasket を説明`   | メソッド単体                           |
| `この @workspace にバスケットの削除メソッドは？`    | ソリューション全体                     |
| `#TestCalculator が正しく動いているか確認するには？` | テストメソッドの動作検証               |
| `#BasketService と #OrderService の違いは？`         | 両クラスを比較                         |
| `#AddItemToBasket は私の @workspace のどこに？`     | メソッドの位置特定                     |



### スレッド管理と昇格

#### スレッドの使い分け

- 関連する質問を続ける → 同一スレッドで継続  
- 新しい話題 → [新しいスレッドを作成] をクリックして開始

#### インラインチャットの昇格

インラインチャットをウィンドウに「昇格」させることで、履歴と文脈を保持できます。

- `[チャット ウィンドウで続行]` をクリック  
  ![昇格](https://storage.googleapis.com/zenn-user-upload/4d0f36054dbc-20250508.png)
---

### カスタム命令の有効化

1. **[Tools] > [Options] > [GitHub] > [Copilot]** にアクセス  
2. 「(プレビュー) カスタム命令を `.github/copilot-instructions.md` ファイルから読み込む」を有効化  
3. リポジトリのルートに `.github/copilot-instructions.md` を作成し、前提条件や指示を自由に記述可能

※ ただし、Visual Studio 2022ではまだ、正常に動作していない模様。(Visual Studio 2022 Version 17.13.6で確認)


## おわりに

GitHub Copilot を活用することで、日々の開発作業をより効率的かつ快適に進めることができます。

本ドキュメントで紹介した使い方やコマンドを参考に、ぜひご自身のプロジェクトに取り入れてみてください。

さらに詳しい機能や最新情報については、GitHub Copilot の公式ドキュメント もあわせてご確認ください。

https://docs.github.com/ja/copilot

