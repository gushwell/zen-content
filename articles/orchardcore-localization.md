---
title: "C#ベースのオープンソースCMS「Orchard Core」の日本語化"
emoji: "🍏"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  [ "orchardcore", "cms", "aspnetcore", "csharp"]
published: true
published_at: 2024-07-21 21:10
publication_name: zead
---

この記事では、C#ベースのオープンソースCMS「OrchardCore」の日本語化について説明します。


## 日本語表示に切り替える

以下の記事でも説明しましたが、まずは、OrchardCoreの設定を変更し、Localizationの機能を有効化します。

https://zenn.dev/zead/articles/orchardcore-try-first

簡単な手順を再度記載します。

管理者ページを開いたら、[Configuration]-[Features]を選んでください。右側のペインに機能を有効化/無効化できるページが開きます。

ここで、検索欄に、"Locali"と入力し、表示された[Localization]の[Enable]ボタンをクリックします。これでLocalizationの機能が有効になり、表示が日本語に切り替わります。

ただ、残念ながら日本語化されているのは全体の30%ほどのようです。翻訳されていない箇所を日本語化する手順を以下で説明します。

## 日本語化の準備　（csprojファイルの編集）

Orchard Coreのプロジェクトフォルダーの下にLocalizationフォルダーがあることを確認します。

csprojファイルに以下の記述を追加します。

```
  <ItemGroup>
    <Content Include="Localization\**">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
    </Content>
  </ItemGroup>
```

## 日本語へ翻訳作業

Localization用のファイルは、以下のフォルダーにあります。

```
Localization/ja
```

このフォルダーの中に、Orchardのモジュール単位に、以下のような拡張子.po ファイルが存在すします。

```
OrchardCore.Admin.po
OrchardCore.AdminDashboard.po
OrchardCore.AdminMenu.po
OrchardCore.Alias.po
OrchardCore.Apis.GraphQL.po
OrchardCore.ArchiveLater.po
... 以下省略 ...
```

POファイル（Portable Objectファイル）は、ソフトウェアのローカライズにおいて使用されるテキストファイル形式で、以下のような形式で翻訳データが記述されています。

```
msgctxt "OrchardCore.Admin.DeploymentStartup"
msgid "Exports the admin settings."
msgstr "管理者設定をエクスポート"
```

msgctxtは、そのテキストの使用箇所を示します。
msgidにはオリジナルの英語のテキスト、msgstrが翻訳されたテキストです。

上記の例は、日本語化されているますが、以下のようにmsgstrが空文字のものは、日本語化されていません。

```
msgctxt "OrchardCore.AdminMenu.Controllers.MenuController"
msgid "Admin menu updated successfully."
msgstr ""
```

これを日本語化するには、このファイルを直接変更してもうまくいきません。OrchardCoreでは、リビルドや発行をすると、オリジナルのファイルに戻ってしまいます。

本来ならば、以下のサイトで日本語化に貢献するのがよいのですが、

https://crowdin.com/project/orchard-core

これがOrchard Coreのパッケージに取り込まれるには時間がかかってしまいます。筆者もかなりの数の翻訳をこのサイトで行いましたが、現時点ではOrchardCore本体には取り込まれていません。

そのため、すぐに自分のOrchardCoreプロジェクトを日本語化したい場合は、以下の手順で日本語化を行います。


#### 1. STEP1

プロジェクトのLocalizationフォルダーに、ja.poファイルを作成します。

```
ja.po
```

このファイルはUTF-8で作成してください。

なお、このファイルはプロジェクトに含めることができません。そのため、Visual Studioのソリューションエクスプローラーからみられるようにするには、ソリューションエクスプローラーの[すべてのファイルを表示]アイコンをONにする必要があります。

![](https://storage.googleapis.com/zenn-user-upload/bb5eae301db4-20240715.png)


これで、ja.poファイルをダブルクリックすれば、ja.poファイルを開くことができる。

![](https://storage.googleapis.com/zenn-user-upload/0b197c238529-20240715.png)



#### 2. STEP2

Localization/jaフォルダーの.poファイルから、日本語化したい箇所を見つけ出します。
長い英文の場合は、検索機能を使えば比較的簡単に見つかりますが、`Edit`や`Content`のような単語の場合は探すのが大変です。
モジュールごとにファイルが分かれているので、モジュール名から「このファイルかな」と類推することはできますが、そのpoファイルに該当の単語/文章が見つからない場合は、地道に該当箇所を見つけるしかないです。

見つかったら、msgctxt, msgid, msgstr の3行をコピーし、ja.po ファイルに張り付けます。それから以下のようにmsgstrの箇所を翻訳後の日本語文字列に置き換えます。


```
msgctxt "OrchardCore.AdminMenu.Controllers.MenuController"
msgid "Admin menu updated successfully."
msgstr "管理者メニューは正常に更新されました。"
```

msgctxtが一致していないと、意図した箇所が日本語化されないので注意してください。


#### 3. STEP3

ビルドし、再実行し正しく日本語化できたか確かめます。


以上が日本語化の手順です。

#### 制限事項

すでに日本語化されているものは、ja.poファイルに書いても置き換えることができません。その場合は、以下のサイトで、日本語化に貢献する必要があります。

```
https://crowdin.com/project/orchard-core
```

やってみてはいないのですが、実行環境でLocalizationを有効にした後に、オリジナルのpoファイルを編集し、実行環境にコピーすれば大丈夫かなとも思います。


**Orchard Coreに関する記事一覧は以下のページで確認できます。**

https://zenn.dev/zead/articles/orchardcore-list-of-article