---
title: "C#ベースのオープンソースCMS「Orchard Core」のコンテンツ管理の基礎"
emoji: "🍒"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "aspnetcore", "orchardcore", "cms"]
published: true
published_at: 2024-06-09 21:10
publication_name: zead
---

[前回の記事](https://zenn.dev/zead/articles/orchardcore-try-first)では、既存のレシピを使いブログサイトを作成しました。

https://zenn.dev/zead/articles/orchardcore-try-first

今回は、前回作成したブログサイトを例にCMSシステムの根幹であるコンテンツ管理について見ていこうと思います。
この記事では、ローカライズの機能を有効化せずに、英語表示のままで説明をしています。

## コンテンツ関連の用語

Orchard Coreの管理者ページでコンテンツに関する定義がどうなっているかを見る前に、Orchard Coreのコンテンツに関わる用語について簡単に説明しておきます。

#### コンテンツアイテム (Content Item)

Orchard Core のコンテンツ管理システム（CMS）で管理される基本単位です。コンテンツアイテムは、さまざまな種類の情報を含むことができます。  
コンテンツアイテムの例としては、ページ、ブログ投稿、製品情報などがあります。多くの場合、それらはサイト上の固有のURL(アドレス)に関連付けられています。

#### コンテンツタイプ (Content Type)

コンテンツタイプは、コンテンツアイテムを生成するためのクラスのようなものです。コンテンツアイテムはコンテンツタイプのインスタンスに例えることができます。コンテンツアイテムは、コンテンツタイプの定義にしたがって生成されます。  
コンテンツタイプは、コンテンツアイテムを構成するコンテンツパーツとコンテンツフィールドを持つことができます。

#### コンテンツパーツ (Content Part)

コンテンツパーツは、コンテンツタイプの要素で、コンテンツタイプ間で再利用できます。例えば、TitlePart、HtmlBodyPart、ListPartなどがあります。

#### コンテンツフィールド　(Content Field)

コンテンツフィールドは、基本データ (文字列、整数、日付など) を格納するものと考えてください。例えば、DateField、TextField、NumericField、HtmlField、LinkField、MediaFieldなどがあります。  
コンテンツフィールドはコンテンツパーツに複数アタッチできます。また、コンテンツフィールドは、ちょっと変わった方法でコンテンツタイプにアタッチすることもできます。
コンテンツタイプまたはコンテンツパーツには、同じ種類の複数のフィールドが関連付けられている場合があります。

## コンテンツアイテムを見てみる

Blog Post（コンテンツアイテム）にはどんな要素があるのかを確認してみましょう。

1. Orchard Coreの管理者ページを開き、左のBlogメニューをクリックします。
2. 「Man must explore, and this is exploration at its greatest」のポストをクリックします。
3. 以下のようなページが開きます。 　

![](https://storage.googleapis.com/zenn-user-upload/778800bfc04c-20240605.png)

ここで開いたBlogの記事は、コンテンツアイテムにあたります。
Orchard Coreでは複数種類のコンテンツアイテムを扱うことができます。Blog Post(ブログ記事)の他に Main MenuやAboutページなどもコンテンツアイテムになります。

ブログ記事の中には、「Title」「Permalink」「MarkdownBody」「Subtitle」「Nabber Image」「Tags」「Category」などの要素があります。

ブログ記事がこれらの要素から成り立っているということになります。これらはコンテンツパーツかコンテンツフィールドのどちらかです。

これらの要素（「Title」「Permalink」「MarkdownBody」など）は、コンテンツタイプで定義されています。

## コンテンツタイプを見てみる

Orchard Coreではサイトに何を表示するかは「Content」メニューで管理しています。
左のメニューの「Content」をクリックしてみましょう。以下のようなメニューが展開されます。

![](https://storage.googleapis.com/zenn-user-upload/2cc226901be8-20240605.png)

ここで、「Content Definition」-「Content Type」をクリックします。以下のようにコンテンツタイプの一覧が表示されます。

![](https://storage.googleapis.com/zenn-user-upload/92c5876cff1e-20240605.png)

コンテンツタイプは、コンテンツアイテムのクラス定義のようなものです。そのインスタンスがコンテンツアイテムです。  
ここで、「Blog Post」をクリックしましょう。

このページではブログの投稿がどのように機能するかの青写真が示されます。先ほど見たBlog Postのページは個々のブログ記事（コンテンツアイテム）で、こちらは、コンテンツタイプのページになります。

![](https://storage.googleapis.com/zenn-user-upload/e1003487d43b-20240605.png)

このページのコンテンツタイプの定義を変更するとコンテンツアイテムの動作に影響を与えます。

このページの各項目について順に見ていきましょう。

#### Technical Name/Dispolay Name

全てのコンテンツタイプにはDisplay Name(表示名)があります。Display Nameはその名の通り、画面に表示される名前です。 　
Technical Nameは、表示名から自動で作成されます。Technical NameはURLに利用されます。

#### Description

そのコンテンツタイプを説明する文

#### メタデータ

コンテンツタイプには以下に示すメタデータが含まれています。

メターデータ名 | 説明
--------------|---------------
Creatable | このコンテンツタイプのインスタンスを UI（Content-Content Typsの当該コンテンツタイプのページ）から作成できるかどうかを決定します。
Listable | このコンテンツタイプのインスタンスがUI（Content Itemsメニュー）を通じて一覧表示できるかどうかを決定します。
Draftable | このコンテンツタイプがドラフト版（下書き）をサポートするかどうかを決定します。
Versionable | このコンテンツタイプがバージョニングをサポートするかどうかを決定します。（前のバージョンに戻すことも、削除されたコンテンツを復活させることもできます。）
Securable | このコンテンツタイプがカスタムパーミッション（コンテンツの編集権限など）を持つことができるかどうかを決定します。

#### Parts

コンテンツパーツは、コンテンツタイプの構成要素です。Orchard Coreが柔軟でカスタマイズ可能なのは、このコンテンツパーツのおかげです。

![](https://storage.googleapis.com/zenn-user-upload/81e84605f936-20240605.png)

Titleはコンテンツパーツで、ブログ記事の構成要素です。またコンテンツパーツは、別のコンテンツタイプの構成要素とすることもできますので、Titleパーツは、Pageコンテンツタイプなど他のコンテンツタイプでも利用されています。

AutorouteはPermalinkに該当するパーツで、そのコンテンツのURLが決定されます。

MarkdownBodyは、Markdown記法が可能なブログ記事の本文を提供します。

一番下に、Blog Postというパーツがありますが、これは後述します。

#### Fields

これ以外の構成要素として、Subtitle, Banner Imageなどがありますが、これらはコンテンツフィールドです。これらコンテンツフィールドは、コンテンツパーツにアタッチされています。

![](https://storage.googleapis.com/zenn-user-upload/d22292f76586-20240605.png)

コンテンツフィールドをコンテンツタイプで利用するには、コンテンツタイプと同名のコンテンツパーツが必要です。「Blog Post」という奇妙なコンテンツパーツがありますが、ここにコンテンツフィールドがアタッチされ、「Blog Post」コンテンツタイプで利用できるようになっています。

## コンテンツパーツとコンテンツフィールドの違い

同じコンテンツパーツを一つのコンテンツタイプに含めることはできません。例えば、複数のTitleコンテンツパーツを、Blob Postコンテンツタイプに含めることはできません。常にひとつだけです。

一方、コンテンツフィールドは、同じ種類のものを一つのコンテンツタイプに複数含めることができます。Blog Postでも、Taxonomy Fieldを複数持っています。これらを区別するために、Tags, Categoryという名前をつけています。

コンテンツパーツはある機能を持った大きな塊であり、場合によっては複数のデータを持つこともできます。

コンテンツフィールドはもっと小さな機能を表すのに使われます。通常は一つのデータだけを保持します。

ほとんどのシナリオでは、組み込みのコンテンツパーツとコンテンツフィールドで間に合いますが、独自のコンテンツパーツや独自のコンテンツフィールドを定義することもできます。この場合はC#での開発が必要となります。

## コンテンツパーツとコンテンツフィールドの定義順

管理者ページで、Blog Postを新規追加/編集する場合の表示順番は、コンテンツタイプのPartsの順序になります。  

そのため、Title, Autoroute, MarkdownBody, Blog Postの順に表示れます。Blog Postにアタッチされているフィールドも、Fieldsで表示されている順番になります。

つまり、Subtitle, Banner Image, Tags, Categoryの順です。例えば、Fieldsの要素をD&Dで順番を変更して、「Save」ボタンを押せば、「Edit Blog Post」「New Blog Post」のページの入力項目順序が変更されます。

## 終わりに

今回は、Orchard Coreのコンテンツ管理についての基礎を説明しました。

**Orchard Coreに関する記事一覧は以下のページで確認できます。**

https://zenn.dev/zead/articles/orchardcore-list-of-article