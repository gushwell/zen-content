---
title: "Polyglot NotebooksでC#をVS Code上で手軽に動かす"
emoji: "🔔"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "vscode", "polyglot", "polyglotnotebook"]
published: true
published_at: 2024-12-21 21:20
publication_name: zead
---

## はじめに

C#でプログラムを書いていて、コードの断片をちょっと動かしてみたいと思ったことありませんか？

そんな時に便利なのが、VS Codeの拡張機能である「Polyglot Notebooks」です。

この記事では、Polyglot Notebooksの環境構築と簡単な使い方について説明しています。

## Polyglot Notebooksとは？

Polyglot Notebooksは、簡単に言えば、Jupyter Notebookの.NET版といったところでしょうか。

複数のプログラミング言語を1つのノートブック内でシームレスに使用できるツールで、.NET Interactiveを活用することでC#、F#、PowerShellなどを切り替えて利用可能です。、Python、JavaScript、SQLなどにも対応しています。各言語ごとにセルを分けて記述でき、データの共有や連携も簡単に行えます。Visual Studio Codeと統合されていて、データ解析やスクリプト作成、マルチプラットフォーム開発に適しています。

## 準備

1. .NET SDK をインストール

    https://dotnet.microsoft.com/ja-jp/download/dotnet

    筆者は、.NET8をインストールしています。

2. .NET interactiveをインストール

    ```
    dotnet tool install -g Microsoft.dotnet-interactive
    ```
3. Visual Studio Codeを起動し、Polyglot Notebooks をインストール
    ![alt text](image-13.png)

## Polyglot Notebooksを使ってみる

### C#を実行する

1. フォルダを作成し、そのフォルダをVS Codeで開く。

2. Ctrl+Alt+Window+Nをタイプ

    ![alt text](image-14.png)    

3. .dibを3択します。(.dib拡張子については後述します)

    ![alt text](image-15.png)

4. 言語を選択します。ここではC#を選びます。

    ![alt text](image-16.png)

5. ファイルが作成されます。適当な名前で保存しておきます。

    ![alt text](image-17.png)

6. コードを入力する欄がありますので、ここにC#のコードを入力します。
    ここでは以下のコードを入力。

    ```cs
    var a = 10;
    var b = 20;
    Console.WriteLine($"Sum: {a + b}");
    ```

7. コード入力欄の左にある▷マークをクリックするとコードを実行できます。
   以下、実行した結果です。

    ![alt text](image-18.png)

8. 別のコードを実行したい場合は、上部の 「＋Code」をクリックします。
    先ほどの下に新たなコード入力欄が現れます。

    ![alt text](image-19.png)

9. ここにコードを入れて、同様に左にある▷マークをクリックするとコードを実行できます。

10. 全てのコードを実行したい場合は、上部の「Run All」をクリックします。

![alt text](image-20.png)

### markdownを記入する

1. コード欄以外にカーソルを移動すると、Markdownを追加するボタンが現れます。

    ![alt text](image-21.png)

2. このボタンをクリックするとMarkdownを記入できる欄が追加されますので、ここで、コードの説明文などを記入します。

    ![alt text](image-22.png)

C#の動作をちょっと確認したい時とか、教育用に利用できそうですね。

## .dibファイルと.ipynbファイルの違い

#### 1. .dib（.NET Interactive Notebook）

- Polyglot Notebooks独自のファイル形式です。
- 軽量なMarkdown形式に基づいており、セルごとにコードやテキストを記述します。
- 言語ごとに異なるカーネル（例: C#、Python、F#など）を使用できます。
- Gitに保存する場合に適している..dibファイルは、通常のMarkdown形式に近いため、差分管理が容易です。


#### 2. .ipynb（Jupyter Notebook）

- Jupyter Notebookの標準形式です。
- JSON形式でデータを保存します。.dibよりも若干ファイルサイズがやや大きくなるかも。
- Jupyterカーネルで動作しますが、Polyglot Notebooksもこの形式をサポートします。
- Jupyter Notebook、JupyterLab、Google Colabなど、他のツールでも開くことができます。

## 最後に

.NET Interactive、Polyglot Notebooksはまだ知名度が低いと思いますが、簡単に環境構築できて、手軽にC#を実行できるので、C#のコード断片を動かすのに最適なツールだと思います。ドキュメントとして残せるのもいいですね。

