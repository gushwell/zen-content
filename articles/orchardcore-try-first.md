---
title: "C#ベースのオープンソースCMS「Orchard Core」で最初のWebサイト"
emoji: "🍑"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "aspnetcore", "orchardcore"]
published: false
published_at: 2024-07-03 08:10
publication_name: zead
---


[前回の記事](https://zenn.dev/zead/articles/orchardcore-setup)では、Orchard Coreの環境構築を行いました。
今回は、既存のCMSレシピを使い、Orchard Coreのサイトを作成したいと思います。

前回の記事
https://zenn.dev/zead/articles/orchardcore-setup

## Orchard Coreのサイト設定

前回同様、作成したOrchardCoreプロジェクトのディレクトリに移動し、以下のコマンドでOrchard Coreを起動します。

```cli
dotnet run
```

ブラウザで、`https://localhost:5001/`を開くと、以下のページが表示されます。


![](https://storage.googleapis.com/zenn-user-upload/e5d03bd64ccf-20240523.png)

以下のような値を入力します。

サイトの名前: MyBlog
レシピ: Blog
データベースの種類: Sqlite
スパーユーザー：admin
メールアドレス: あなたのメールアドレス
パスワード: 任意　（英大文字、英小文字、数字、記号からなるパスワード）

サーバーは、SQL Serverや、MySQLなどが選べますが、今回は、Sqliteを選択します。

[セットアップを完了する]ボタンをクリックします。

以下のページが表示されます。

![](https://storage.googleapis.com/zenn-user-upload/862c6fff6ce2-20240523.png)

## 管理者ページに移動する

以下のURLを開いて管理者ページに移動します。

```
https://localhost:5001/admin
```

ログインページが開くので、先ほどのユーザ名と、パスワードでログインします。

![](https://storage.googleapis.com/zenn-user-upload/13977c405b82-20240523.png)


管理者ページが開きます。

## 日本語表示に切り替える

ここで、まず日本語表示に切り替えます。左のメニューで、[Configuration]-[Features]を選んでください。

右側のペインで機能を有効化/無効化できるページが開きます。

![](https://storage.googleapis.com/zenn-user-upload/90e47764e58b-20240524.png)


ここで、検索欄に、"Locali"と入力し、表示された[Localization]の[Enable]ボタンをクリックします。

ボタンのラベル等が日本語になったのが確認できます。

![](https://storage.googleapis.com/zenn-user-upload/c23cb9f89293-20240524.png)

ただ、残念ながら日本語化されているのは全体の30%ほどのようです。
翻訳されていない箇所を日本語化する方法は別の記事で紹介したいと思います。


なお、今動いているOrchard Core CMSのモードは、「C#ベースのオープンソースCMS「Orchard Core」について」で紹介した「完全な CMS」モードです。このモードは、選択したテーマとテンプレートを使用してカスタム開発を行わずにサイトを構築することを目的としてます。


## ブログ記事を投稿してみる

では、さっそくブログ記事を投稿していましょう。

https://zenn.dev/zead/articles/f604f9ad31f941#3%E3%81%A4%E3%81%AEweb%E3%82%B5%E3%82%A4%E3%83%88%E6%A7%8B%E7%AF%89%E3%83%A2%E3%83%BC%E3%83%89

左のメニューから[コンテンツ]-[コンテンツの項目]を選びます。

![](https://storage.googleapis.com/zenn-user-upload/2a5263b135f6-20240524.png)

右側のペインで、"Blog" のリンクをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/ab7a85c2c9a2-20240524.png)

ページが切り替わりますので、右上の[Create Blog Post]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/f197d235286c-20240524.png)


ここで記事を入力し、「ドラフトの保存」ボタンをクリックします。この段階ではまだ公開されていません。

![](https://storage.googleapis.com/zenn-user-upload/a33c8eb48994-20240524.png)

Blog投稿一覧画面に戻るので、ここで、先ほど入力した記事がどんなふうに表示されるのか、「Preview Draft」ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/853741a3dcb9-20240524.png)

すると、別タブでプレビューが見られます。別タブなので、確認したら閉じて問題ありません。

![](https://storage.googleapis.com/zenn-user-upload/86e22a90258f-20240524.png)

確認が済んだら、[操作]ボタンを押して、「Publish Draft」 をクリックします。これで記事が公開されました。

![](https://storage.googleapis.com/zenn-user-upload/59dcb4c3566d-20240524.png)

## ブログを確認

早速、ブラウザの別タブで、以下のURLを開きます。

https://localhost:5001


トップページに先ほどの記事が追加されているのが確認できます。

![](https://storage.googleapis.com/zenn-user-upload/8353eeabe2d6-20240524.png)

記事のリンクをクリックすれば、個別記事に移動します。

