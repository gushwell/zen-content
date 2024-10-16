---
title: "GitHubの通知をChrome拡張機能で受け取る"
emoji: "🔔"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["github", "chrome拡張機能"]
published: true
published_at: 2024-10-20 21:20
publication_name: zead
---

## はじめに

GitHubからの通知をSlackで受け取る方法もありますが、仕事では別のコミュニケーションツールをメインに利用しているので、未読があるかどうかだけでも簡単に確認したいなーと調べていたら、まさにぴったりのChrome拡張機能「Notifier for GitHub」があるのを知りました。


この拡張機能は、GitHub通知の未読数を表示する拡張機能です。以下にその設定について説明します。

## 拡張機能のインストールと設定

1. 以下のページからChrome拡張をインストールします。

    https://chromewebstore.google.com/detail/notifier-for-github/lmjdlojahmbbcodnpecnjnmlddbkjhnn?hl=ja

    ![](https://storage.googleapis.com/zenn-user-upload/745ee5808950-20241016.png)

2. 以下の設定画面で、「create token」リンクをクリックします。  
   private リポジトリの場合は2つめの「create token」を選びます。

![](https://storage.googleapis.com/zenn-user-upload/8fc19690624f-20241016.png)

3. GitHubのログインが求められるのでログインします。ログインすると以下の画面が表示されます。

    ![](https://storage.googleapis.com/zenn-user-upload/45ac36553e9c-20241016.png)

4. Expiration を設定する。ここでは「no expiration」にしています。

5. 「Select Scopes」で通知の範囲を指定します。最低でも「repo」にはチェックを入れます。

6. 下にスクロールし「Generate token」ボタンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/1cf9f2f02c30-20241016.png)

7. tokenが生成されるので、コピーします。（必要ならファイル等へ保存しておく）

    ![](https://storage.googleapis.com/zenn-user-upload/f17c5dcd3ce4-20241016.png)

8. 拡張機能「Notifier for GitHub」のダイアログへ戻り、コピーしたtokenを「Token」欄に貼り付蹴ます。

![](https://storage.googleapis.com/zenn-user-upload/e77b79864d8a-20241016.png)


9. 上記スクショの通り、チェックを入れるて閉じます。

10. Chromeの拡張機能アイコンをクリックします。

![](https://storage.googleapis.com/zenn-user-upload/b52b0e4d637a-20241016.png)

11. Notifier for GitHub をピン留めします。

![](https://storage.googleapis.com/zenn-user-upload/df8b5e2fa585-20241016.png)


以上で設定は完了です。

## 通知を確認する

1. GitHubで未読の通知があると、以下のようにChromeの拡張機能アイコンに未読数が表示されます。

![](https://storage.googleapis.com/zenn-user-upload/8e0e15177f0f-20241016.png)


2. Notifier for GitHub のアイコンをクリックすると、GitHubのNotificationのページが開きます。

    ![](https://storage.googleapis.com/zenn-user-upload/c2c881ede691-20241016.png)

