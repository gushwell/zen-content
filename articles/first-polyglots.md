---
title: "Polyglot NotebooksでC#とJavaScriptをVS Code上で手軽に動かす"
emoji: "🔔"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "vscode", "polyglot", "polyglotnotebook", "javascript"]
published: true
published_at: 2024-12-18 21:10
publication_name: "zead"
---

## はじめに

C#やJavaScriptなどでプログラムを書いていて、コードの断片をちょっと動かしてみたいと思ったことありませんか？

そんな時に便利なのが、VS Codeの拡張機能である「Polyglot Notebooks」です。

弊社のkotaprojさんが書いた記事「Semantic KernelのGetting Started」でもPolyglot Notebooksを利用しています。

https://zenn.dev/zead/articles/semantic_kernel_getting_started

この記事では、Polyglot Notebooksの環境構築と簡単な使い方について説明しています。

## Polyglot Notebooksとは？

Polyglot Notebooksは、簡単に言えば、Jupyter Notebookの.NET版といったところでしょうか。

複数のプログラミング言語を1つのノートブック内でシームレスに使用できるツールで、.NET Interactiveを活用することでC#、F#、PowerShellなどを切り替えて利用可能です。Python、JavaScript、SQLなどにも対応しています。

Visual Studio Codeと統合されており、データ解析やスクリプト作成、マルチプラットフォーム開発に適しています。

Polyglot Notebooksでは、各プログラミング言語ごとにセルを分けて記述でき、異なる言語で書かれたコードを同じノートブック内で実行し、データを共有することができます。

また、データ共有機能（`#!value`コマンド）を使うことで、セル間やノートブック間でデータを連携することも可能です（この記事では触れていません）。

## 準備

1. .NET SDKをインストールしていない場合は、.NET SDK をインストールします。

    https://dotnet.microsoft.com/ja-jp/download/dotnet

    .NET9, .NET8どちらでもお好みの方をインストールしてください。


2. .NET interactiveをインストール

    ```
    dotnet tool install -g Microsoft.dotnet-interactive
    ```
3. Visual Studio Codeを起動し、Polyglot Notebooks をインストール

    ![](https://storage.googleapis.com/zenn-user-upload/94d78156cf35-20241207.png)

## Polyglot Notebooksを使ってみる

### C#を実行する

1. フォルダを作成し、そのフォルダをVS Codeで開く。

2. Ctrl+Alt+Window+Nをタイプ（\[File\]-\[New File...\]メニューでも可）

3. Polyglot Notebook を選択

    ![](https://storage.googleapis.com/zenn-user-upload/db7ad42b32bc-20241207.png)


4. .dibを選択します。

    ![](https://storage.googleapis.com/zenn-user-upload/fb05d13ae077-20241207.png)

    :::message
    .dib拡張子については後述の「.dibファイルと.ipynbファイルの違い」で説明しています。
    :::

5. 言語を選択します。ここではC#を選びます。

    ![](https://storage.googleapis.com/zenn-user-upload/2985c60d1351-20241207.png)

6. ファイルが作成されます。適当な名前で保存しておきます。

7. コードを入力する欄(セル)がありますので、ここにC#のコードを入力します。

    ![](https://storage.googleapis.com/zenn-user-upload/1766ed2baca6-20241207.png)

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

1. コード欄(セル)の外側にカーソルを移動すると、Markdownを追加するボタンが現れます。

    ![](https://storage.googleapis.com/zenn-user-upload/50544fbe9e86-20241207.png)

2. このボタンをクリックするとMarkdownを記入できる欄(セル)が追加されますので、ここで、コードの説明文などを記入します。

    ![](https://storage.googleapis.com/zenn-user-upload/221a5d055ead-20241207.png)

C#の動作をちょっと確認したい時とか、教育用に利用できそうですね。

## 同じノートブック内でC#とJavaScriptを一緒に使う

Polyglot Notebooksは、複数のプログラミング言語を統合し、1つのノートブック内で異なる言語のコードを実行できる環境を提供します。各セルごとに使用する言語を指定できるため、C#やJavaScriptなどを組み合わせて利用できます。


手順を以下に示します。

:::message
すでに[Node.js](https://nodejs.org/en) がインストールされていることを前提にしています。
:::


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

.NET InteractiveやPolyglot Notebooksはまだ知名度が高くないかもしれませんが、簡単に環境を構築でき、C#やJavaScriptなどのコードを手軽に実行できるため、コードスニペットを試したり共有したりするのに最適なツールだと思います。また、実行結果とともにコードをドキュメントとして保存できる点も大きな利点ですね。

