---
title: "GitHub Copilot Editsの利用方法（Visual Studio 2022 向け）"
emoji: "🚀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["visualstudio2022", "visualstudio", "githubcopilot"]
published: true
published_at: 2025-05-14 08:45
publication_name: "zead"
---

## はじめに

このドキュメントは、Visual Studio 2022 上で GitHub Copilot のEdits機能を使い始める方を対象にしています。 基本的な使い方を順を追って解説します。

事前に以下をご確認ください：

- Visual Studio 2022 がインストールされていること
- GitHub Copilot 拡張機能がインストールされ、有効になっていること
- GitHub アカウントで Copilot の利用契約が完了していること

セットアップがまだの方は、まず Visual Studio の拡張機能管理画面から「GitHub Copilot」を検索してインストールし、GitHub アカウントでサインインしてください。

GitHub Copilotのコード補完とチャット機能については、以下の記事で説明していますので、こちらも参照していただければと思います。

https://zenn.dev/zead/articles/githubcopilot-vs2022

## GitHub Copilot Editsとは

GitHub Copilot Editsは、チャットとインラインチャットの長所を組み合わせた機能で、 会話型のフローとファイル群に対するインラインでの変更を同時に扱えます。

Copilot Editsでは、編集対象のファイルを指定し、自然言語で変更をリクエストできます。

## Copilot Editsの特徴

Copilot Editsの最大の特徴は、開発者が主導権を持ってファイルを変更できる点です。  
変更内容を確認しながら、求める解決策に到達するまで何度も調整が可能です。

また、プレビュー機能により、影響を受けるファイルと提案された変更内容を正確に把握できます。 
変更の取り消し（ロールバック）も可能なため、安心して利用できます。

## Copilot Chat との違い

Microsoft公式サイトでは、ChatとEditsの使い分けについて以下のように説明されています。

項目 | Copilot Chat | Copilot Edits
------|-------------|----------
主な使用例 | プログラミングの概念を理解し、コードについて質問し、コードを生成するための**汎用的な会話型インターフェース** | コードレビュー、ファイル内プレビュー、ロールバック機能を備えた、**マルチファイル編集に特化したインターフェース**
提案されたコードのプレビュー | 各コードブロックをソリューション内のファイルに**手動で適用し**、差分を確認 | 提案されたコード差分を各ファイルに**自動で適用し**、理解を容易にする
コードレビュー体験 | ファイルの変更を**まとめて**承認または拒否 | ファイル内の**個別のコードチャンク**を受け入れまたは拒否
バージョン管理 | 既存のバージョン管理を利用 | 編集したファイルの変更を追跡し、**ロールバック**可能（チェックポイントはVisual Studio終了まで保持）

## Copilot Editsの簡単な使い方

1. Visual Studio の右上にある Copilot アイコンをクリックし、「チャットウィンドウを開く」を選択します。\
    ![](https://storage.googleapis.com/zenn-user-upload/0848a0e81f09-20250513.png)
    
2. 「新しいEditsスレッドの作成」アイコンをクリックします。\
    ![](https://storage.googleapis.com/zenn-user-upload/1615ba7fa3bb-20250513.png)

3. 自然言語でプロンプトを入力します。\
    ファイル、ソリューション、エラー、シンボルを #コマンドで具体的に指定できます。

4. Copilot の提案を確認し、承認または拒否を行います。

## 簡単な利用例

それでは、実際にEdits機能を使ってみましょう。

### プロンプトの入力

今回は、Consoleアプリプロジェクト（SampleApp.csproj）を作成し、Program.cs ができた状態からスタートします。

Copilot Editsを起動し、以下のプロンプトを入力します。

```
#SampleApp.csproj BMIを計算するクラスを作成して。
```

![](https://storage.googleapis.com/zenn-user-upload/67decec376fc-20250513.png)

BMICalculator.cs が生成され、Program.cs にも変更が加えられます。  
この時点では提案のみなので、状況により承諾または拒否を選択します。

### 提案を確認する

「イテレーション1」に表示されている BMICalculator.cs をクリックします。

![](https://storage.googleapis.com/zenn-user-upload/9b0c53ded0f8-20250513.png)

Visual Studio の編集ウィンドウに BMICalculator.cs（提案されたコード）が表示されます。

### 提案を拒否する

提案を拒否する場合は、Alt＋Delキーを押します。  
または、コードウィンドウ上部の「Alt+Del」と表示されたボタンをクリックしても同様です。

この例では、クラス全体が1つのチャンクになっているため、Alt＋Delを押すとクラス全体が拒否されます。

### 提案を受け入れる

提案を承諾するには、Tabキーを押します。  
または、コードウィンドウ上部の「Tab」と表示されたボタンをクリックしても承諾できます。

特定のソースファイルへの変更をまとめて受け入れる場合は、GitHub Copilot Editsウィンドウの「ファイルの変更を受け入れる」アイコンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/2ca2a232875b-20250513.png)

Program.csも含めて提案されたすべてを承諾するには、「すべてを承諾する」ボタンをクリックします。
ここでは、「すべてを承諾する」ボタンをクリックして、すべてを受け入れてみます。

ソリューションエクスプローラーを開くと、プロジェクトに BMICalculator.cs が追加されていることを確認できます。

![](https://storage.googleapis.com/zenn-user-upload/ddc3b87ac3ac-20250513.png)

※ファイルはまだ保存されていないため、適宜保存してください。

### 既存のクラスを変更する

次に、BMICalculator.cs に変更を加えます。

プロンプトに以下を入力します。

```
#BMICalculator.cs GetBMICategoryの戻り値を独自定義のenum型に変更してください。enumの名前はわかりやすいものにしてください。
```

Copilotウインドウに、提案されたファイル一覧（ここでは、BMICalculator.csのみ）が表示されますので、青い BMICalculator.cs 部分をクリックします。

![](https://storage.googleapis.com/zenn-user-upload/c763788ab421-20250513.png)

編集ウィンドウに変更案が表示されます。  
GetBMICategoryを呼び出しているGetFormattedBMIResultも、ちゃんと変更されているのが確認できます。

![](https://storage.googleapis.com/zenn-user-upload/7ee3fb6e0875-20250513.png)

### 提案されたコードをさらに変更する

BMICategory列挙型を別ファイルに移動してみましょう。

以下を入力します。

```
BMICategory列挙型を新しいファイルに作成して移動してください。
```

BMICategory.cs が生成されますので、提案を確認して受け入れます。

続いて、BMICalculator.cs の変更提案も確認します。  
複数チャンクに分かれている場合は、Tabキーを押しながら承諾していきます。  
一括で受け入れる場合は「ファイルの変更を受け入れる」アイコンをクリックします。

### ビルドして実行する

ビルドして実行してみましょう。

以下は実行結果です。

![](https://storage.googleapis.com/zenn-user-upload/458d63f607cb-20250513.png)


### さらに既存ファイルを編集する

実行結果の **カテゴリ：Normal** は日本人にはわかりにくいですね。  
日本語でわかりやすく表記してみましょう。

以下のプロンプトを入力します。

```
#SampleApp.csproj GetFormattedBMIResultメソッドでは、BMICategory列挙型をそのまま文字列にしています。これを日本語に翻訳し、より分かりやすい文字列を返すように変更してください。
```

![](https://storage.googleapis.com/zenn-user-upload/4d2da4d455cb-20250513.png)

GetFormattedBMIResult が上記のように変更されました。これを受け入れて再度実行します。

![](https://storage.googleapis.com/zenn-user-upload/970323937589-20250513.png)

うまく日本語化できました。

---

## 最後に

GitHub Copilot Editsを使うことで、**単なるコード生成**にとどまらず、**既存コードの改善やリファクタリングも自然言語で直感的に行える**ようになります。  
Visual Studioとの連携により、提案された内容を細かく確認・調整できるため、実際のプロジェクトでも安心して活用できると思います。

本記事では簡単な例を中心に紹介しましたが、さらに複雑な編集や、プロジェクト全体にわたる大規模なリファクタリングも可能です。  
ぜひ、GitHub Copilot Editsの機能を最大限に活用し、日々の開発効率を向上させてください。



