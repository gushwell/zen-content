---
title: "『改訂新版 実戦で役立つC#プログラミングのイディオム/定石&パターン』を出版します"
emoji: "📘"
type: "idea" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "dotnet"]
published: true
published_at: 2024-07-22 21:10
publication_name: zead
---


『実戦で役立つC#プログラミングのイディオム/定石&パターン』の改訂版を執筆しましたので、ちょっとお知らせです。

2024年7月25日発売予定です。

https://www.amazon.co.jp/dp/4297143070


## 改訂のきっかけなど

初版が2017年3月3日に刊行されたので、そこから数えるとすでに7年以上が経過していることになります。

初版は、C#6.0＋.NET Framework4.6をベースにした本ですが、普遍的な内容も多く盛り込んでいましたので、プログラミングの本としては随分と寿命の長い本になったと思います。購入していただいた方々のおかげです。本当にありがたい限りです。

しかし、この7年間でC#の世界は大きく進化しました。とくに.NET Frameworkから.NET Coreおよび.NET 5以降への移行が大きな変革をもたらしたと言えます。また、Windowsはもちろん、Linux, macOSでも動作するマルチプラットフォーム対応になりました。C#の文法も、null参照許容型、レコード型、パターンマッチングなどさまざまな機能が追加され、より表現力に磨きがかかっています。

そんな外部変化があり、「C#もいろいろ進化してるし、そろそろ改訂版を出したいなー」と数年前から思っていたのですが、その前に出した[『C#コードレシピ集』](https://www.amazon.co.jp/C-%E3%82%B3%E3%83%BC%E3%83%89%E3%83%AC%E3%82%B7%E3%83%94%E9%9B%86-%E5%87%BA%E4%BA%95-%E7%A7%80%E8%A1%8C/dp/4297122650/)が産みの苦しみだったので、本を書くのはもういいや、という気持ちになっていたのも影響してなかなか手をつけられませんでした。

2023年の8月にやっと重い腰を上げ、改訂作業を開始したのですが、いかんせん書くスピードが遅いので、結局この本も改訂版にもかかわらず出版するのに1年くらいかかってしまいました。

本当は、.NET8が出たらすぐにこの本も出したいと思っていたのですが...


## 改訂新版で何が変わったのか

今回の改訂では、以下のような方針で臨みました。

- 「C#のより良い書き方」、「.NETのクラスの活用」、「オブジェクト指向プログラミング」、「良いコードを書く指針」という4つの柱はそのま残す
- ただし、章立ては見直し、必要なら章の追加、削除も行う
- 内容は C#12 .NET8をベースにし、サンプルコードやコラムも含め全ての内容を見直す

その結果、改訂版では、以下の章を新設/構成変更を行いました。

- 最新のC#のクラスにまつわる文法を解説する第5章「クラスに関するイディオム」
- C#のさらなる優れた機能を収録した第16章「C#を使いこなす」
- .NETの便利な小技を集めたAppendix「その他のプログラミングの定石」

結果、null許容参照型、レコード型、タプル、パターンマッチングなどC#7.0以降に取り入れられた機能をいろいろ追加するとともに、旧版では盛り込めなかった、列挙型、ジェネリックス、拡張メソッド、反復子、属性についても説明することにしました。

また、「第13章 実戦オブジェクト指向プログラミング」では、オブジェクトコンポジションや依存性の注入についても説明するようにしました。

一方、旧版の以下の2つの章は収録を見送りました。

- 「XMLファイルの操作」
- 「Entity Frameworkによるデータアクセス」

これらを入れたら、500ページを優に超える本になってしまうので...

※ 「XMLファイルの操作」の章では、LINQ to XMLについてかなり詳しく説明していたのですが、当時と比べてXMLを利用する機会も減ったので、改訂新版ではLINQ to XMLには触れずに、「第12章 シリアル化、逆シリアル化」でXMLのシリアル化、デシリアル化を説明するだけにしました。

※ Entity Framework Coreについては、拙著『[C#コードレシピ集](https://www.amazon.co.jp/dp/4297122650/)』で扱っているので、もし興味があれば、そちらを参照していただければと思います。

それ以外でも、いろいろと追加、変更をしていますし、サンプルコードはほぼ全面見直しを行なっているので旧版をお持ちになっている方にも読んでいただける内容になったと思います。

また、本書は豊富なコラムがあることも特徴のひとつかなと思っています。本文の説明の流れでは入れ込むことが難しい内容だけど、知っていると嬉しい内容をコラムで説明しています。コラムについても削除・追加をしています。内容はもめっちゃ初心者向けの話題から中級者向けの話題までいろいろ取り揃えています。

## 目次とコラム一覧

以下、改訂新版の目次とコラムの一覧です。

### 改訂新版の目次

**Part 1 ［準備編］**
Chapter 1　オブジェクト指向プログラミングの基礎
Chapter 2　C#でプログラムを書いてみよう
Chapter 3　ラムダ式とLINQの基礎

**Part 2 ［基礎編］**
Chapter 4　基本イディオム
Chapter 5　クラスに関するイディオム
Chapter 6　文字列の操作
Chapter 7　配列とList\<T\>の操作
Chapter 8　ディクショナリの操作
Chapter 9　日付，時刻の操作

**Part 3 ［実践編］**
Chapter 10　ファイルの操作
Chapter 11　正規表現を使った高度な文字列処理
Chapter 12　シリアル化、逆シリアル化
Chapter 13　LINQを使いこなす
Chapter 14　非同期/並列プログラミング

**Part4 ［ステップアップ編］**
Chapter 15　実践オブジェクト指向プログラミング
Chapter 16　C#を使いこなす
Chapter 17　スタイル，ネーミング，コメント
Chapter 18　良いコードを書くための指針

Appendix その他のプログラミングの定石


### コラムの一覧（順不同）

- オブジェクトとインスタンス
- 前置++と後置++の違い
- 浮動小数点型の比較
- オブジェクトどうしの比較
- 文字列は不変オブジェクト
- foreachやforのループの中でリスト要素を削除してはいけない
- constのバージョン管理問題
- グローバルusing
- DateOnly構造体とTimeOnly構造体
- ボックス化とボックス化解除
- 文字エンコーディングを指定したファイル出力
- LINQの集合演算子
- LINQのDefaultIfEmptyメソッド
- Zipメソッドの使い方
- lock構文で排他制御
- typeof演算子とGetTypeメソッド
- record型とwith式
- 正規表現パターンには逐語的リテラル文字列を使う
- 正規表現エンジンのキャッシュ
- 行頭、行末の意味を変更し複数モードにする（正規表現）
- 大文字・小文字を区別せずにマッチさせる（正規表現）
- ECMAScript準拠の動作を有効にする（正規表現）
- プログラミングの一般原則
- コンパイラの警告は無視してはいけない
- Visual Studioのデバッグの基本
- プロジェクトに新しいクラスを追加する
- usingディレクティブを自動で挿入する
- コードスニペットでプロパティを楽々定義
- Visual Studioの[名前変更]機能
- XMLコメントとVisual Studio
- Visual Studioのコードメトリックスの使い方
