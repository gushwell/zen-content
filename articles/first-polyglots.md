---
title: "Polyglot NotebooksでC#をVS Code上で手軽に動かす"
emoji: "🔔"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "vscode", "polyglot", "polyglotnotebook"]
published: true
published_at: 2024-12-16 21:10
publication_name: "zead"
---

## はじめに

C#でプログラムを書いていて、コードの断片をちょっと動かしてみたいと思ったことありませんか？

そんな時に便利なのが、VS Codeの拡張機能である「Polyglot Notebooks」です。

弊社のkotaprojさんが書いた記事「Semantic KernelのGetting Started」でもPolyglot Notebooksを利用しています。
https://zenn.dev/zead/articles/semantic_kernel_getting_started

この記事では、Polyglot Notebooksの環境構築と簡単な使い方について説明しています。

## Polyglot Notebooksとは？

Polyglot Notebooksは、簡単に言えば、Jupyter Notebookの.NET版といったところでしょうか。

複数のプログラミング言語を1つのノートブック内でシームレスに使用できるツールで、.NET Interactiveを活用することでC#、F#、PowerShellなどを切り替えて利用可能です。Python、JavaScript、SQLなどにも対応しています。各言語ごとにセルを分けて記述でき、データの共有や連携も簡単に行えます。Visual Studio Codeと統合されていて、データ解析やスクリプト作成、マルチプラットフォーム開発に適しています。

## 準備

1. .NET SDK をインストール

    https://dotnet.microsoft.com/ja-jp/download/dotnet

    筆者は、.NET8をインストールしています。

2. .NET interactiveをインストール

    ```
    dotnet tool install -g Microsoft.dotnet-interactive
    ```
3. Visual Studio Codeを起動し、Polyglot Notebooks をインストール

    ![](https://storage.googleapis.com/zenn-user-upload/94d78156cf35-20241207.png)

## Polyglot Notebooksを使ってみる

### C#を実行する

1. フォルダを作成し、そのフォルダをVS Codeで開く。

2. Ctrl+Alt+Window+Nをタイプ

    ![](https://storage.googleapis.com/zenn-user-upload/db7ad42b32bc-20241207.png)

3. .dibを3択します。(.dib拡張子については後述します)

    ![](https://storage.googleapis.com/zenn-user-upload/fb05d13ae077-20241207.png)

4. 言語を選択します。ここではC#を選びます。

    ![](https://storage.googleapis.com/zenn-user-upload/2985c60d1351-20241207.png)

5. ファイルが作成されます。適当な名前で保存しておきます。

    ![](https://storage.googleapis.com/zenn-user-upload/1766ed2baca6-20241207.png)


6. コードを入力する欄(セル)がありますので、ここにC#のコードを入力します。
    ここでは以下のコードを入力。

    ```cs
    var a = 10;
    var b = 20;
    Console.WriteLine($"Sum: {a + b}");
    ```

7. コード入力欄(セル)の左にある▷マークをクリックするとコードを実行できます。
   以下、実行した結果です。

    ![](https://storage.googleapis.com/zenn-user-upload/ccefb49b94f5-20241207.png)

8. 別のコードを実行したい場合は、上部の 「＋Code」をクリックします。
    先ほどの下に新たなコード入力欄(セル)が現れます。

    ![](https://storage.googleapis.com/zenn-user-upload/afdbb938a090-20241207.png)

9. ここにコードを入れて、同様に左にある▷マークをクリックするとコードを実行できます。

10. 全てのコードを実行したい場合は、上部の「Run All」をクリックします。

    ![](https://storage.googleapis.com/zenn-user-upload/e2009816fc7c-20241207.png)

### markdownを記入する

1. コード欄以外にカーソルを移動すると、Markdownを追加するボタンが現れます。

    ![](https://storage.googleapis.com/zenn-user-upload/50544fbe9e86-20241207.png)

2. このボタンをクリックするとMarkdownを記入できる欄が追加されますので、ここで、コードの説明文などを記入します。

    ![](https://storage.googleapis.com/zenn-user-upload/221a5d055ead-20241207.png)

C#の動作をちょっと確認したい時とか、教育用に利用できそうですね。

## 同じノートブック内でC#とJavaScriptを一緒に使う

Polyglot Notebooksは異なるプログラミング言語を統合して、1つのノートブックで異なる言語のコードを実行できる環境を提供します。各言語はセルごとに分けて使用し、それぞれのセルに言語を指定することで、C#やJavaScriptを組み合わせて使えます。

手順を以下に示します。

1. 前述同様、上部の 「＋Code」をクリックします。コードを入力する欄（セル）が追加されます。

    ![](https://storage.googleapis.com/zenn-user-upload/2e6fd0211912-20241207.png)

2. 次に、セルの右下の「csharp - C# Script」をクリックします。ここでJavaScriptを選択すれば、JavaScriptを実行できるセルに切り替わります。

    ![](https://storage.googleapis.com/zenn-user-upload/3bccab7e907d-20241207.png)

3. 以下のコードを入れてみます。

    ```js
    const numbers = [
    [ 1,2,3 ],
    [ 4,5,6]
    ];
    const results = numbers.flatMap(n => n);
    console.log(results);
    ```

4. 左にある▷マークをクリックするとコードを実行できます。

5. 以下のような結果が表示されます。

    ```
    [1,2,3,4,5,6]
    ```

## .dibファイルと.ipynbファイルの違い

#### 1. .dib（.NET Interactive Notebook）

- Polyglot Notebooks独自のファイル形式です。
- 軽量なMarkdown形式に基づいており、セルごとにコードやテキストを記述します。
- 言語ごとに異なるカーネル（例: C#、Python、F#など）を使用できます。
- Gitに保存する場合に適しています。.dibファイルは、通常のMarkdown形式に近いため、差分管理が容易です。


#### 2. .ipynb（Jupyter Notebook）

- Jupyter Notebookの標準形式です。
- JSON形式でデータを保存します。.dibよりも若干ファイルサイズがやや大きくなるかも。
- Jupyterカーネルで動作しますが、Polyglot Notebooksもこの形式をサポートします。
- Jupyter Notebook、JupyterLab、Google Colabなど、他のツールでも開くことができます。

## 最後に

.NET Interactive、Polyglot Notebooksはまだ知名度が低いと思いますが、簡単に環境構築できて、手軽にC#を実行できるので、C#のコード断片を動かすのに最適なツールだと思います。ドキュメントとして残せるのもいいですね。

