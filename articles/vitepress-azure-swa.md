---
title: "GitHub ActionsでVitePressサイトをAzure Static Web Appsに簡単デプロイ"
emoji: "🚀"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["vitepress", "githubactions", "azure", "staticwebapps"]
published: true
published_at: 2024-09-15 21:02
publication_name: zead
---

## 前提

- 開発環境: Windows 11
- Node, npm、npxがインストール済み

## VitePressとは

VitePressは、VuePressの後継として開発されたViteベースの静的サイトジェネレーター（SSG）です。

VuePressと同様にMarkdownで簡単にコンテンツを作成できます。

技術ドキュメントやブログを効率よく作成・管理するツールとして広く利用されています。

また、カスタマイズ性が高く、軽量であるためパフォーマンスにも優れていると評価されています。

https://vitepress.dev/


## VitePressをインストール

まずは、VitePressをインストイールします。

以下のコマンドの実行します。（ここでは、vitepressというフォルダーを作成しています。）


```
mkdir vitepress
cd vitepress
npm init -y
npm i -D vitepress
```

## VitePressプロジェクトを作成

続いて、以下のコマンドを実行します。

```
npx vitepress init
```

VitePressプロジェクトを作成するための質問が表示されるので、例えば、以下のように答えます。


![](https://storage.googleapis.com/zenn-user-upload/024a36503a11-20240816.png)

## 動かして見る

```
npm run docs:dev
```

以下のメッセージの通り、`http://localhost:5173/` にアクセスします。

```
> vp@1.0.0 docs:dev
> vitepress dev docs


  vitepress v1.3.2

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help

```

以下のようなページが表示されば成功です。

![](https://storage.googleapis.com/zenn-user-upload/a984453fad86-20240816.png)


## Nodeのバージョンを v18に変更


順番が逆かもしれませんが、この記事を書いている時点では、Azure Static Web AppsでサポートするNode v20はプレビュー版なので、v18を利用するようにします。

### nvm-windowsをインストールします。

[npm-windowsのGitHubのページ](https://github.com/coreybutler/nvm-windows/releases)から`npm-setup.exe`をダウンロードして実行します。

### Node v18をインストールして切り替え

nvm-windowsをインストールしたら、以下を実行します。

```
nvm install 18.20.4
nvm use 18.20.4
```

### VitePressのpackage.jsonを編集

nodeのバージョンを指定します。

```json
{
  "name": "devguideline",
  "version": "1.0.0",
  "engines": {
      "node": "18.x"
  },
  ...
```


## Azure Static Web Appsにデプロイする

### package.jsonの編集

続いて、package.jsonのscriptに以下の行を追加します。


```json
    "build": "vitepress build docs"
```

### GitHubにプッシュする

GitHubにリポジトリーを作成し、このプロジェクトをプッシュします。

### Azure Static Web Appsのリソースを作成する

Azureポータルを開いて、Azure Static Web Appsのリソースを作成します。

リソースを作成する「静的 Web アプリの作成」の画面では、

「デプロイの詳細」の「ソース」でGitHubを選択し、「組織」「リポジトリ」「分岐」で、デプロイ対象のGitHubリポジトリとブランチを選択します。  

「ビルドの詳細」では、以下のように設定します。

- 「ビルドのプリセット」: vuepress 
- アプリの場所: /
- APIの場所:  空白
- 出力先: docs/.vitepress/dist

※ VitePressは、vuePressから派生した製品なので、vuePressを指定して問題ありません。

### CI/CD用のymlを編集

Azure Static Web Appsのリソースが作成されたら、GitHubのリポジトリをプルします。

azure-static-web-apps-abcd-glacier-0d129700.ymlのようなファイル(ファイル名は同じではありませんが、ymlファイルは一つだけなので間違うことはないです)が、.github/workflowフォルダーに作成されています。

このファイルに以下の行を追加します。

```
      - name: Set up Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
```

追加する場所は、以下の直後になります。

```
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
          lfs: false
      // ここに追加

```

再度、GitHubにプッシュします。

これで、正常にビルドアクションが走り、VitePressのプロジェクトがデプロイされるはず... だと思ったのですが、GitHub Actionsで

```
sh: 1: vitepress: Permission denied
```

のエラーになってしまいます。仕方ないので、ymlファイルに以下の記述をして対応しました。


```
      - run: npm install
      - name: Fix vitepress permissions
        run: chmod +x ./node_modules/.bin/vitepress
      - name: Build And Deploy
```

真ん中の2つの行を挿入しています。

再度、GitHubリポジトリにプッシュします。正常にビルドアクションが走り、VitePressのプロジェクトがデプロイされました。

なお、GitHubリポジトリのActionタブを開けば、デプロイの結果を見ることができます。

## VitePressサイトの確認

Azureポータルで、当該Azure Static Web Appsのリソースページを開きます。

概要ページにURLが書いてありますので、このURLを開けばサイトを見ることができます。


![](https://storage.googleapis.com/zenn-user-upload/a984453fad86-20240816.png)



