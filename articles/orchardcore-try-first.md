---
title: "C#ベースのオープンソースCMS「Orchard Core」で作成する最初のWebサイト"
emoji: "🍑"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "aspnetcore", "orchardcore", "cms"]
published: true
published_at: 2024-05-31 08:12
publication_name: zead
---


[前回の記事](https://zenn.dev/zead/articles/orchardcore-setup)では、Orchard Coreの環境構築を行いました。
今回は、Orchard Core組み込みのCMSレシピを使い、ブログサイトを作成したいと思います。

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

データベースは、SQL Serverや、MySQLなどが選べますが、今回は、Sqliteを選択します。

[セットアップを完了する]ボタンをクリックします。

以下のページが表示されます。簡単ですね。

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

なお、今動いているOrchard Core CMSのモードは、"C#ベースのオープンソースCMS「Orchard Core」について"で紹介した「完全な CMS」モードです。このモードは、選択したテーマとテンプレートを使用してカスタム開発を行わずにサイトを構築することを目的としてます。

https://zenn.dev/zead/articles/f604f9ad31f941#3%E3%81%A4%E3%81%AEweb%E3%82%B5%E3%82%A4%E3%83%88%E6%A7%8B%E7%AF%89%E3%83%A2%E3%83%BC%E3%83%89

## ブログ記事を投稿してみる

では、さっそくブログ記事を投稿してみましょう。

左のメニューから[コンテンツ]-[コンテンツの項目]を選びます。

![](https://storage.googleapis.com/zenn-user-upload/2a5263b135f6-20240524.png)

右側のペインで、"Blog" のリンクをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/ab7a85c2c9a2-20240524.png)

ページが切り替わりますので、右上の[Create Blog Post]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/f197d235286c-20240524.png)

ここで記事を入力します。

![](https://storage.googleapis.com/zenn-user-upload/b9c7813920a6-20240528.png)

パーマリンクには、`blog/about-orchard-core` のように、先頭に`blog/`を指定します。

ページ下部には、[公開],[ドラフトの保存],[プレビュー]などのボタンがありますが、ここでは、[ドラフトの保存]ボタンをクリックし、下書き保存したいと思います。この段階ではまだ公開されていません。

[ドラフトの保存]ボタンをクリックすると、Blog投稿一覧画面に戻るので、ここで、先ほど入力した記事がどんなふうに表示されるのか、「Preview Draft」ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/853741a3dcb9-20240524.png)

すると、別タブでプレビューが見られます。別タブなので、確認したら閉じて問題ありません。

![](https://storage.googleapis.com/zenn-user-upload/86e22a90258f-20240524.png)

確認が済んだら、[操作]ボタンを押して、「Publish Draft」 をクリックします。これで記事が公開されました。

![](https://storage.googleapis.com/zenn-user-upload/59dcb4c3566d-20240524.png)

## ブログを確認

早速、ブラウザの別タブで、以下のURLを開きます。

```
https://localhost:5001
```

トップページに先ほどの記事が追加されているのが確認できます。

![](https://storage.googleapis.com/zenn-user-upload/8353eeabe2d6-20240524.png)

記事のリンクをクリックすれば、個別記事に移動します。

URLが、`/blog/<パーマリンク>`になっていることを確認してください。\<パーマリンク\>はブログ記事の入力時に指定した値です。

## Main Menuにメニュー項目を追加する

次にページ上部のMain Menuにカテゴリーページへ遷移するメニュー項目を追加してみましょう。再度、管理者の画面に移動してください。

左のメニューから「Main Menu」をクリックしし、右側のペインで、「メニューアイテムの追加」ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/d2ef91b4549c-20240527.png)

「コンテンツメニュー項目」の「追加」ボタンをクリックします。
![](https://storage.googleapis.com/zenn-user-upload/f7ad4e9c93fd-20240527.png)

ここで既存のページへのリンクを作成します。名前に"Categories"と入力し、[Selected　Content Item]から"Categories"を選択し、[公開]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/1afa80ca0aa4-20240527.png)

一覧に戻るので、再度「公開」ボタンをクリックします。

今度は、Ctrlキーを押しながら、右上の「Visit Site」ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/fc7be34b02ed-20240527.png)

サイトが別タブで開きます。

メニューに[CATEGORIES]が追加されたのが確認できますので、[CATEGORIES]リンクをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/05270e64ef0a-20240527.png)

Categoriesページに遷移したのが確認できるはずです。

![](https://storage.googleapis.com/zenn-user-upload/7d2134d7acdf-20240527.png)

## Profileページを追加する

次に独立した単一のページ(プロフィールページ)を作成し、上部メニューからアクセスできるようにします。

管理者メニューの[コンテンツの項目]をクリックし、右側のペインから、[New]ボタンをクリックし、[Article]を選びます。

![](https://storage.googleapis.com/zenn-user-upload/1da96e726bb0-20240527.png)

新規Articleのページが開きますので、ここでプロフィール情報を記入します。

![](https://storage.googleapis.com/zenn-user-upload/f068ab117619-20240527.png)

※ 先ほど追加したブログ記事とまったく関係ないプロフィールですが、ご容赦ください😅。

下にスクロールして、[Banner Image]の＋ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/563f07a0c6eb-20240527.png)

必要なら、ここで画像をアップロードします。表示した画像を選択し、OKボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/c21899f068c3-20240527.png)

Articleの編集ページに戻りますので、[公開]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/1563d01c5ace-20240527.png)

コンテンツの管理ページに戻ります。ここで、今作成したProfileの行があることを確認します。

![](https://storage.googleapis.com/zenn-user-upload/c9b1a8e481c3-20240527.png)

## Main MenuにProfileページへのリンクを追加する

先ほどCategoriesメニュー項目を追加しましたが、同じ要領でProfileへのメニュー項目を作成します。

![](https://storage.googleapis.com/zenn-user-upload/c42b1f71758d-20240527.png)

先ほどと同様、[Visit Site]アイコンをCtrlキーを押しながらクリックします。

Profileへのリンク項目が追加されていますので、このリンクをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/da55899683f9-20240527.png)

Profileページが開きます。

![](https://storage.googleapis.com/zenn-user-upload/2d5f74d2efc5-20240527.png)

## カテゴリを追加

今のままでは、Categoryは、Travelしか選択できません。カテゴリを追加してみます。

管理者メニューから[コンテンツ]-[Taxonomy]を選びます。

![](https://storage.googleapis.com/zenn-user-upload/af34dc4cf054-20240527.png)

Categories の[Edit]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/f77df5d1874e-20240527.png)

[Categoryを追加]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/76396da60c4f-20240527.png)

タイトルやアイコンを入力し、[公開]ボタンを押します。

![](https://storage.googleapis.com/zenn-user-upload/949850070954-20240527.png)

「Taxonomyを編集」のページへ戻るので、再度[公開]ボタンをクリックします。

これでカテゴリが追加されました。[コンテンツ]-[コンテンツの項目]を選び、右側の「Blog」の[List Items]ボタンをクリックします。

続けて[Create Blog Post]ボタンをクリックします。新規 Blog Postページが開きますので、下にスクロールすると、Category欄に先ほど追加したカテゴリー"Camera"が選択できるようになっています。

![](https://storage.googleapis.com/zenn-user-upload/6e95a603dc7c-20240527.png)

## ブログタイトルの変更

順番が逆になってしまいましたが、ブログタイトルを変更します。

管理者ページの左の[Blog]を選択し、右側の[Edit Blog]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/966165dd41c2-20240528.png)

ここで、タイトルとHtmlBodyを変更し、[公開]ボタンをクリックします。。

![](https://storage.googleapis.com/zenn-user-upload/e75443bd3acc-20240528.png)

サイトにアクセスすれば、以下のように変更されたのを確認できます。

![](https://storage.googleapis.com/zenn-user-upload/52adaa6fe9d7-20240528.png)

## 終わりに

Orchard CoreのBlogテーマを使うと、簡単にブログサイトを作成できることがわかりました。

さらに、記事を追加したり、カテゴリを追加したりして動きを確認してみてください。

**Orchard Coreに関する記事一覧は以下のページで確認できます。**

https://zenn.dev/zead/articles/orchardcore-list-of-article


