---
title: "Visual StudioとVS CodeでGitHubの認証ダイアログが何度も出る原因と解決方法"
emoji: "🔒"
type: "tech"
topics: ["VisualStudio", "github", "vscode"]
published: true
published_at: 2026-02-09 21:00
publication_name: zead
---

## はじめに

Visual Studio や VS Code を使っていると、突然 「Select an account」 のような GitHub の認証ダイアログが何度も表示され続けることがあります。
これは単なる不具合ではなく、GitHub Credential Manager（GCM） が複数の資格情報のどれを使うべきか判断できなくなることで発生します。
この記事では、

- なぜ認証ダイアログが何度も出るのか
- どういう環境で起きやすいのか
- どう対処すればよいのか

を、なるべく分かりやすく解説しようと思います。

---

## どんな状況で発生しやすい？

以下の条件が揃っていると、発生頻度が高くなるようです。

- 仕事用・個人用など 複数の GitHub アカウント を同じ PC で利用
- HTTPS と SSH の両方で clone したことがある
- 複数の Git クライアントを併用（VS、VS Code、Git Bash など）
- GitHub 拡張機能を VS Code で利用
  （GitHub PRs、Repositories、Copilot など）

これらにより、PC 内に 複数の GitHub 資格情報が蓄積され、GCM が選択に迷い始めます。

### アカウントが一つでも発生するのか？

仕事用アカウントと個人アカウントを同じPCで利用していると、この現象が出やすいですが、仕事用アカウントだけでもこの現象は起きるようです。

GitHub の資格情報は、「アカウント単位ではなく「ツール × 認証方式 × URL 形式」単位で保存される」という仕組みになっています。
以下のように、同じアカウントでも別物として扱われます：


例 | 認証方式等
-------|------
https://github.com | 標準 HTTPS
https://username@github.com | 埋め込みユーザー名
git@github.com | SSH
PAT / OAuth の違い | 認証方式が異なる

その結果、資格情報が次々と増え、最終的に GCM は

「どれを使えばいいんだ？」

となり、毎回聞きにくる状態が発生します。

### 資格情報が増えていく典型パターン

**① Visual Studio で GitHub にサインイン（OAuth）**

- Visual Studio は GitHub OAuth を利用
-「GitHub for Visual Studio」という名前で資格情報が保存される

**② Git 操作で HTTPS を利用すると PAT を要求**

- clone / push 時に GCM が PAT を保存
- OAuth とは別枠として扱われる

**③ VS Code の GitHub 拡張が API を叩く**

以下の拡張機能は内部で独自に API を叩くようです

- GitHub Pull Requests and Issues
- GitHub Repositories
- GitHub Copilot

これらが追加で資格情報を保存。

**④ URL 形式の違いでさらに分裂**

Git は、URL の書き方が少しでも違うと、完全に別のサーバーとして扱います。

- https://github.com
- https://username@github.com
- git@github.com

Git は全部別物扱いです。
結果、GCM の「同一アカウント」が内部ではバラバラに保存されます。


---

## 対処方法

### ① 現在の状態を確認する

PowerShellで以下のコマンドをタイプします。

```
cmdkey /list | findstr github
```

例えば、以下のように複数の github.com 関連エントリが表示されるはずです。

```
ターゲット: LegacyGeneric:target=https://github.com/ 
ターゲット: LegacyGeneric:target=git:https://github.com 
ターゲット: LegacyGeneric:target=gh:github.com:your-name 
ターゲット: LegacyGeneric:target=GitHub for Visual Studio - https://your-name@github.com/ 
ターゲット: LegacyGeneric:target=git:https://your-name@github.com 
ターゲット: LegacyGeneric:target=git:https://Personal Access Token@github.com
```


### ② GitHub 関連資格情報を一度すべて削除

```
cmdkey /delete:LegacyGeneric:target=https://github.com/
cmdkey /delete:LegacyGeneric:target=git:https://github.com 
cmdkey /delete:LegacyGeneric:target=gh:github.com:your-name 
cmdkey /delete:LegacyGeneric:target=GitHub for Visual Studio - https://your-name@github.com/ 
cmdkey /delete:LegacyGeneric:target=git:https://your-name@github.com 
cmdkey /delete:LegacyGeneric:target=git:https://Personal Access Token@github.
```

**※ 実際の一覧を見て、github.com を含むものだけ削除してください。**

### ③ Visual Studio、 VS Code で GitHub に再ログイン

1. Visual Studio を起動
2. 右上 → アカウント
3. GitHub でサインイン

### ④ VS Code も同じアカウントでログイン

1. VSCodeを起動
2. 左下のアカウントアイコンをクリック
3. 「Sign in with GitHub」を選択
4. ブラウザが自動で開くので、GitHubアカウントで通常のログイン


---

## おわりに

GitHub の認証ダイアログが頻繁に表示される原因は、
「資格情報の分裂と蓄積」 にあることがほとんどです。
原因を理解して整理すれば、問題は高い確率で解決します。

本記事が、

- GitHub 認証で困っている方
- Visual Studio と VS Code を併用している方

の参考になれば幸いです。
