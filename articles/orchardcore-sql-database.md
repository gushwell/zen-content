---
title: "Azure SQL Databaseを利用する"
emoji: "🍋"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["azure", "visualstudio","aspnetcore", "orchardcore", "csharp"]
published: true
published_at: 2024-07-11 21:20
publication_name: zead
---

## はじめに

この記事では、Azure SQL Databaseの利用手順を示します。
例としてOrchard CoreのプログラムからAzure SQL Databaseに接続します。

※ この記事は、C#ベースのオープンソースCMS「Orchard Core」の紹介する一連の記事のうちの一つですが、「Orchard Core」に依存した部分は、記事後半の「Orchard CoreからSQL Databaseを利用する」以降だけなので、Azure SQL Databaseのリソースの作成手順は一般的な内容となっています。

## Azure SQL Databaseとは

Azure SQL Databaseは、Microsoft SQL Server データベース エンジンの最新の安定したバージョンを利用できるフルマネージドのPaaSデータベースエンジンです。

高可用性、バックアップ、その他の一般的なメンテナンス操作が組み込まれていて、データベースエンジンとオペレーティングシステムの更新は、すべて自動で行われます。

この記事書く際に知ったのですが、

> SQL Server の最新機能のリリースは Azure SQL Database から始まり、その後 SQL Server 自体に対してリリースされます。 

なんだそうです。へー知りませんでした。

## 2つの購入モデル

SQL Database には、2つの異なる購入モデル (仮想コアベースの購入モデルと DTUベースの購入モデル) があります。

**仮想コアベースの購入モデル**では、仮想コアの数、メモリの量、およびストレージの容量と速度を選択できます。また、仮想コアベースの購入モデルでは、既存の SQL Server ライセンスを活用して、SQL Server 向けの Azure ハイブリッド特典を使い、コストを削減することもできます。


**DTUベースの購入モデル**では、データベースのパフォーマンスを簡単に選択できるように設計されたモデルです。DTUは、コンピューティング、メモリ、およびI/Oリソースの総合的な測定単位です。選択するDTUの値によって料金が異なります。小規模データベースから大規模で高負荷な処理をこなすデータベースまで様々なプランが用意されています。

今回は比較的安価に利用できるDTUベースの購入モデルを利用します。


## Azure Portalで SQL Databseのリソースを作成する

### リソースの作成を開始する

まずは、Azure PotalでApp Serviceのリソースを作成します。  
ここでは、Azureのサブスクリプションとリソースグループの作成は済んでいるものとします。
リソースグループの作成については、以下を参照してください。

https://learn.microsoft.com/ja-jp/azure/azure-resource-manager/management/manage-resource-groups-portal


Azure Portal を開き、リソースグループを開き[作成]ボタンを押します。

![](https://storage.googleapis.com/zenn-user-upload/92812223a3a2-20240612.png)

MarketPlaceのページが開きますので、左側の一覧でデータベースを選択し、右側のサービス一覧から「SQL Database」をクリックします。

![](https://storage.googleapis.com/zenn-user-upload/53d2cd56f951-20240624.png)

続いて、プランが「SQL Database」であることを確認し、[作成]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/4b5f5c76dc7b-20240624.png)


### SQL データベースの作成

以下のページが開きます。
ここで、データベース名を入力したら、サーバーの[新規作成]のリンクをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/913c5d8737e3-20240624.png)


「SQL Databaseサーバーの作成」ページが開きます。
ここで、サーバー名と場所、認証方法を入力します。

![](https://storage.googleapis.com/zenn-user-upload/fe07f85ecd82-20240624.png)

認証方法は、ここではみなさんお馴染みの「SQL認証」を選びました。ここで設定したサーバー管理者のログインとパスワードがDB接続時のID/パスワードになります。

セキュリティ的には、Microsoft Entra専用認証を使用するのがおすすめとのことです。

なお、SQL Databaseサーバーとは、その名の通り、SQLデータベースをホストする論理サーバーです。複数のSQL Databaseを管理することができます。

必要な項目を入力したら[OK]ボタンをクリックします。

先ほどの「SQLデータベースの作成」のページに戻りますので、ワークロード環境を選択（ここでは「開発」にチェック）したら、コンピューティングとストレージの[データベースの構成]リンクをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/3fba6a201dff-20240624.png)


次のページで、サービスレベルを選択し、[適用]ボタンをクリックします。
ここでは、一番安価なDTUモデルのBasicを選択しました。

![](https://storage.googleapis.com/zenn-user-upload/28fdfcc29928-20240624.png)

再び、「SQLデータベースの作成」のページに戻りますので、「バックアップストレージの冗長性」でいずれかを選択し、[確認および作成]ボタンをクリックします。
開発用なら、「ローカル冗長バックアップストレージ」を選んでおけばいいかなと思います。

![](https://storage.googleapis.com/zenn-user-upload/349671da9c11-20240624.png)


「確認および作成」タブに移りますので内容を確認し、[作成]ボタンをクリックします。

デプロイが開始され、しばらくすると下記の画面に切り替わります。

![](https://storage.googleapis.com/zenn-user-upload/46fe318c7cb0-20240624.png)

### ネットワークの設定の変更

次に、ネットワークの設定を行います。作成したSQL Databaseサーバーのリソースに移動します。

左側メニューで「ネットワーク」を選択すると、右側のペインがネットワークの設定ページに切り替わります。

今回は、「選択したネットワーク」にチェックを入れ、ページ下にある「Azureサービスおよびリソースにこのサーバーへのアクセスを許可する」にチェックを入ました。
このデータベースを利用するアプリケーションOrchard CoreもAzureで動作（ App Serviceで動かす）するため、ここにチェックを入れています。
場合によっては、IPアドレスで制限しても良いと思います。

[保存]ボタンをクリックし、設定を保存します。


![](https://storage.googleapis.com/zenn-user-upload/e14c17a87efe-20240624.png)

次に、左側から「SQL database」の項目をクリックします。以下の画面になりますので、ここで先ほど作成した「SQL databases」をクリックします。
なお、ひとつSQL Databaseサーバーに複数のSQL Serverデータベースを作成できますので、複数ある場合はここの複数のデータベースが表示されることになります。

![](https://storage.googleapis.com/zenn-user-upload/6e0f0c9f93af-20240624.png)

以下のページに遷移しますでの、[データベース接続文字列の表示]リンクをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/e6930801a3ec-20240624.png)

データベースの接続文字列が確認できます。このSQL接続文字列をコピーして、アプリケーションに設定すればデータベースを利用できるようになります。今回は、SQL認証を選んだので、下の「ADO.NET（SQL認証）」の接続文字列をコピーします。

![](https://storage.googleapis.com/zenn-user-upload/f6d3cee4f07f-20240624.png)

以上で、Azure SQL Databaseのリソースの作成と設定は完了です。

## Orchard CoreからSQL Databaseを利用する

それでは、ASP.NET Coreで作成されたCMSであるOrchard CoreからこのDBに接続してみます。
すでに、AzureにOrchard Coreのプログラムがデプロイされているものとします。

なお以下の記事で、Orchard CoreをAzure App Serviceにデプロイする手順を示しています。

https://zenn.dev/zead/articles/orchardcore-app-service

ローカルでセットアップを行わない状態で、Orchard CoreのプロジェクトをAzure App Serviceにデプロイすると、以下のセットアップのページが表示されます。

![](https://storage.googleapis.com/zenn-user-upload/f573a96b1dbc-20240624.png)

このセットアップページで、データベースの種類を「Sql Server」にして、接続文字列に先ほどコピーした接続文字列（パスワードを変更したもの）を設定してセットアップすれば、DBに接続され、必要なテーブルが自動で作成されます。

以下のページが表示されればAzure SQL databaseへの接続は成功です。

![](https://storage.googleapis.com/zenn-user-upload/a54a72e42f51-20240624.png)








