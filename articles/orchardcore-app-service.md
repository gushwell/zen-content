---
title: "Visual StudioからAzure App Serviceにプログラムをデプロイする"
emoji: "🍋"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["azure", "visualstudio", "csharp", "aspnetcore", "orchardcore"]
published: true
published_at: 2024-06-24 08:00
publication_name: zead
---

## はじめに

この記事では、Orchard Coreのプロジェクトを例に、Visual StudioからAzure App Serviceにデプロイする方法を説明します。

Azure App Service は、WebアプリケーションやWebAPIをホストするためのフルマネージドPaaS (サービスとしてのプラットフォーム) です。
サーバーレスコンピューティング環境を提供し、自動スケーリング、セキュリティ、統合認証などの機能が備わっています。デプロイはGit、GitHub、Docker、Visual Studioなどから行うことができ、効率的なアプリケーション管理が可能です。

Orchard Coreのプロジェクトを例にとりますが、C#で作成したWebアプリケーションならば、今回の方法でVisual Studioから簡単にデプロイすることが可能です。

Orchard Coreのプロジェクトを作成する記事
https://zenn.dev/zead/articles/orchardcore-create-project-by-vs

## Azure Portalで App Serviceのリソースを作成する

全てぼ作業をVisual Studioから行えるのですが、Azureのリソースの作成は、Azure Portalで行うこととします。

### リソースの作成を開始する

まずは、Azure PotalでApp Serviceのリソースを作成します。  
ここでは、Azureのサブスクリプションとリソースグループの作成は済んでいるものとします。
リソースグループの作成については、以下を参照してください。

https://learn.microsoft.com/ja-jp/azure/azure-resource-manager/management/manage-resource-groups-portal


Azure Portal を開き、リソースグループを開き[作成]ボタンを押します。

![](https://storage.googleapis.com/zenn-user-upload/92812223a3a2-20240612.png)

MarketPlaceのページが開きますので、検索欄に"web"と入力し、検索された「Web　アプリ」をクリックします。
「Azureサービスのみ」にチェックを入れると探しやすくなると思います

![](https://storage.googleapis.com/zenn-user-upload/19c35b1edd30-20240612.png)

続いて、プランが「Web APP」であることを確認し、[作成]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/4a753b4dd685-20240612.png)

### Webアプリの情報を入力

以下のページが開きます。

![](https://storage.googleapis.com/zenn-user-upload/56245a8bd072-20240612.png)

ここで、以下を入力して、[確認および作成]ボタンをクリックします。

- インスタンスの名前： 任意（ここでは、orchard-code-demo）  
- ランタイムスタック: .NET8 (LTS)  
- オペレーティングシステム: Linux  
- 地域: 任意  
- Linuxプラン: そのままでもOK (新規作成で任意の名前指定することをオススメします)  
- 価格プラン: 任意 (ここではFree F1を選択)   

### Webアプリの情報確認と作成開始

"確認および作成"のタブページに移動します。エラーがなければ、作成ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/b9b9b6b6eaa5-20240619.png)

### デプロイ開始

作成ボタンをクリックすると、デプロイが始まります。

![](https://storage.googleapis.com/zenn-user-upload/a3133810c1a3-20240612.png)

デプロイが完了すると、以下の表示に切り替わります。これでApp ServiceのリソースがAzureに作成されました。


![](https://storage.googleapis.com/zenn-user-upload/c5890ccd29ab-20240612.png)

しばらく待っても、表示が切り替わらない場合は、ページを更新してみてください。

![](https://storage.googleapis.com/zenn-user-upload/c0bf66e706e3-20240612.png)


## Azure App Serviceの設定を変更

作成したApp Serviceのページに移動し、左側のメニューで[設定]-[構成]を選びます。  
ここで、「SCM基本認証の発行資格」にチェックをし、設定を[保存]します。

![](https://storage.googleapis.com/zenn-user-upload/06cee89594b2-20240612.png)

この設定は、Visual Studioからデプロイするのに必要となります。

以上で、Azure Portal側の作業は終了です。

## Visual Studioでプログラムを発行する

### Orchard Coreのプロジェクトを作成

既存のプロジェクトをそのま利用しても良いですが、ここでは新規にプロジェクトを作成します。プロジェクトの名前はなんでもOKです。

```
 dotnet new occms -n OrchardCoreAzure
```

Visual Studioで作成したプロジェクトを開き、正しくビルドできるか確認します。

ここでは、Orchard Coreのプロジェクトを作成しましたが、通常のASP.NET Coreのアプリケーションでも問題ありません。


### 発行プロファイルの作成

次に、ソリューションエクスプローラーのプロジェクトを右クリックして、[発行]を選びます。

![](https://storage.googleapis.com/zenn-user-upload/232f652082b5-20240612.png)

Azureを選択し、[次へ]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/c4af70a19e12-20240612.png)

Azure App Service (Linux)を選択し、[次へ]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/5358db7e5091-20240612.png)

先ほどAzure Portalで作成した Azure App Serviceを選択し、[完了]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/2e28812df5d3-20240619.png)

次の画面（省略）で[閉じる]ボタンをクリックします。これで発行プロファイルが作成されました。
一度、発行プロファイルを作成すれば、この設定がPCに保存されますので、発行する際に再利用することができます。

### Azureへの発行

先ほどの画面で[完了]ボタンをクリックすると、発行のページに移りますので、ここで、[発行]ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/a08ea956c6c7-20240612.png)

Azureへの公開が開始されます。

![](https://storage.googleapis.com/zenn-user-upload/b1758db1e51e-20240612.png)

公開が正常に終了すると、Azure App ServiceにデプロイしたWebアプリケーションが起動するとともに、ブラウザが起動しアプリケーションのページが開きます。

今回のOrchard Coreの場合は、以下の画面が表示されます。

![](https://storage.googleapis.com/zenn-user-upload/69093660a9bf-20240612.png)

以上で、Azure App Serviceのデプロイが終了しました。


---

## 次にやること（Orchard Coreの場合）

セットアップの画面が出たら、セットアップを開始します。
確認した範囲では、このセットアップ画面でデータベースにSQLiteを選んでもそれなりに動いてくれているようでした。
しかし、Azure App ServiceでのSQLiteの利用は推奨されていません。  

次回は、今回作成したOrchard Coreのサイトで、Azure SQL Databaseを利用する方法について見ていこうと思います。






