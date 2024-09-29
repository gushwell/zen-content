---
title: "初めてのSvelteKit(環境構築、プロジェクト作成、実行、プロジェクト構成)"
emoji: "🏃‍♀️"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["svelte", "sveltekit"]
published: true
published_at: 2024-10-01 21:20
publication_name: zead
---

## 準備

### Node.jsのインストール

Windowsの場合は、以下の手順で、Node.jsをインストールします。

1. [Node.jsの公式サイト](https://nodejs.org/en)にアクセスします。
1. 「LTS（Long Term Support）」バージョンをダウンロードします。
1. ダウンロードしたインストーラーを実行し、画面の指示に従ってインストールを完了します。  
    すべてデフォルト値のままでOKです。

これで、npmコマンドを利用できるようになります。

コマンドプロンプトで、以下のコマンドでインストールできたか確認します。

```
node --version
npm --version
```

### VSCode拡張機能のインストール

　Visual Studio Codeに、`Svelte for VS Code` 拡張機能をインストールします。

![](https://storage.googleapis.com/zenn-user-upload/cd22fd05c37b-20240911.png)

## 初めてのSvelte/SvelteKit

### デモプロジェクト作成方法

```
npm create svelte@latest my-app
```

いくつかの質問に答えます。以下はその質問に答えた後の実行例です。  
ここでは、Svelteのデモアプリを選択し、TypeScriptのサポートはOffにしています。

```
Need to install the following packages:
create-svelte@6.3.10
Ok to proceed? (y) y

> npx
> create-svelte my-app

create-svelte version 6.3.10

┌  Welcome to SvelteKit!
│
◇  Which Svelte app template?
│  SvelteKit demo app
│
◇  Add type checking with TypeScript?
│  No
│
◇  Select additional options (use arrow keys/space bar)
│  Add ESLint for code linting, Add Prettier for code formatting
│
└  Your project is ready!

Install more integrations with:
  npx svelte-add

Next steps:
  1: cd my-app
  2: npm install
  3: git init && git add -A && git commit -m "Initial commit" (optional)
  4: npm run dev -- --open

To close the dev server, hit Ctrl-C

Stuck? Visit us at https://svelte.dev/chat
```

上記メッセージの通り、コマンドを実行します。

```
cd my-app
npm install
git init && git add -A && git commit -m "Initial commit" (optional)
npm run dev -- --open
```

gitコマンドはオプションです。gitでソース管理する場合に実行してください。

### デモプロジェクトの実行

`npm run dev -- --open` コマンドを実行すると、コンソールに以下のような出力がされます。

```
> my-app@0.0.1 dev
> vite dev --open

Forced re-optimization of dependencies

  VITE v5.4.3  ready in 767 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

ブラウザが起動し、`http://localhost:5173/` が開きます。

以下のようなページが表示されればOKです。

![](https://storage.googleapis.com/zenn-user-upload/f7abdc4c3925-20240911.png)

ーボタン、＋ボタンを教えて動きを確認してください。


コマンドプロンプトの画面で、`q[enter]`とタイプすれば、ブログラムが終了します。

## ソースコードを確認してみよう

### 作成したプロジェクトのフォルダーとファイル

VSCodeでmy-appフォルダーを開いた時のフォルダーです（src/routesを展開した状態）。

![](https://storage.googleapis.com/zenn-user-upload/d3b0acaf763d-20240911.png)

`+page.svelte`や`Counter.svelte`がsvelteのファイルで、ここにHTMLやJavaScript、cssが記述されています。

注目すべきは、app.html、+layout.svelte、および +page.svelte の３つのファイルです。

### 注目すべきフォルダー

#### src/lib

ライブラリコード（ユーティリティとコンポーネント）が含まれており、$libエイリアス経由でインポートできます。

#### src/routes

ページコンポーネントやそのページ内で利用されるコンポーネントやJavaScriptファイルなどが含まれています。

#### static

robots.txtやfavicon.pngのように、そのまま提供される静的アセットはここにおきます。


### 注目すべきファイル

#### svelte.config.js

このファイルには、Svelte および SvelteKit の構成が含まれています。

#### app.html

app.html は、SvelteKitアプリケーションの基本的なHTMLテンプレートです。

このファイルは、アプリケーション全体のHTML構造を定義し、SvelteKitが動的にコンテンツを挿入するためのプレースホルダーを提供します。

```html
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <link rel="icon" href="%sveltekit.assets%/favicon.png" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        %sveltekit.head%
    </head>
    <body data-sveltekit-preload-data="hover">
        <div style="display: contents">%sveltekit.body%</div>
    </body>
</html>
```

%sveltekit.head% の箇所に、SvelteKitが動的に `<head>` セクションを挿入します。各ページやレイアウトコンポーネントで定義された `<svelte:head>` タグ内の内容が挿入されます。

%sveltekit.body% の箇所には、SvelteKitが動的に `<body>` セクションを挿入します。`+layout.svelte` の内容が挿入されます。


#### +layout.svelte
+layout.svelte は、特定のルートや一連のルートに共通するレイアウトを定義するためのファイルです。

このファイルは、ナビゲーションバー、フッター、サイドバーなど、複数のページで共通して使用される要素を含むことができます。

```html
<script>
    import Header from './Header.svelte';
    import '../app.css';
</script>

<div class="app">
    <Header />

    <main>
        <slot />
    </main>

    <footer>
        <p>visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to learn SvelteKit</p>
    </footer>
</div>
...

```

このファイルの `<slot />` に、対応するページコンポーネントの内容が挿入されます。

#### +page.svelte

+page.svelte は、特定のルートに対応するページコンポーネントを定義するためのファイルです。

このファイルは、特定のURLパスに対応するコンテンツを提供します。簡単な例を示します。

```html
<script>
  export let data;
</script>

<h1>Welcome to the Home Page</h1>
<p>This is the content of the home page.</p>
```

src/routesの直下の +page.svelte は、`/` のurlに対尾するページファイルになります。
このファイルが、+layout.svelte の`<slot />`の箇所に挿入されることになります。


`export let data;` は、SvelteKitがこのページに渡すデータを受け取るための変数です。個人的にはこのexportがすごく気持ち悪いですが...  
（次期バージョンのSvelte5ではこのあたりが改善されるようです。）

### SvelteKitのルーティング

SvelteKitもルーティングは、「ファイルベースルーティング」（File-based Routing）です。ディレクトリ構造とURLパスが対応しているルーティングの仕組みが採用されています。

例えば、このデモプロジェクトの場合は、以下のようなディレクトリ構造になっています。

```
src/
  routes/
    +page.svelte
    about/
      +page.svelte
    sverdle/
      +page.svelte
```

この場合、対応するURLは以下のようになります。

url | ファイル
----|------
/     | src/routes/+page.svelte
/about | src/routes/about/+page.svelte
/sverdle | src/routes/sverdle/+page.svelte

SvelteKitでは、`+page.svelte`というファイル名は決まっているので、変更することはできません。



