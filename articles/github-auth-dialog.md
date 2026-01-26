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

Visual Studio  を使っていると、ある日突然、

![](/images/github-auth-dialog/image.png)

といった **GitHub の認証ダイアログが頻繁に表示される**ようになってしまいました。

GitHub Credential Manager（GCM）が、どのアカウント／トークンを使うか判断できずに、このダイアログが出るようになっていたようです。

本記事では、GitHub の認証ダイアログが何度も出る理由と対処法を解説します。

---

## どのような時にでるのか


仕事用アカウントと個人アカウントを同じPCで利用していると、この現象が出やすいですが、仕事用アカウントだけでもこの現象は起きるようです。

以下のような状況の時に、この現象が発生しやすいようです。

- HTTPSとSSHの両方で、Cloneしたことがある
- 複数のGitクライアントアプリを利用している
- コマンドでもGitHubを操作している
- Git Personal Access Tokenを利用

このような時に、以下の状況になると、認証ダイアログが出ます。

#### 1. Visual Studio と VS Code で認証方式が異なる

Visual Studio と VS Code は 同じ GitHub Credential Manager を使います。両方で GitHub リポジトリにアクセス（git fetch / pull / 拡張機能の API 呼び出しなど）すると、どのアカウント／トークンを使うか判断できず、この「Select an account」ダイアログが頻繁に出ます。

ツール	| 認証方式
---------|----------------
Visual Studio |	GitHub アカウント（OAuth）
VS Code	| PAT（または別アカウント）

同じ Git 操作でも「どれを使う？」と毎回聞かれます。

#### 2. GitHub 拡張機能が裏で API を叩いている

VS Code 側で以下が有効だと、操作していなくても認証が走ります。

- GitHub Pull Requests and Issues
- GitHub Copilot
- GitHub Repositories

Visual Studio も同様に、起動時やソリューション読み込み時に GitHub へアクセスします。

---

## なぜ利用するアカウントが一つなのに起きるのか

GitHub の資格情報は、

* アカウント単位
* リポジトリ単位

ではなく、

**「ツール × 認証方式 × URL 形式」単位** で保存されます。

そのため、同じ GitHub アカウントでも、使い方次第で資格情報がどんどん増えていくようです。

この資格情報が増えていくと、GitHub Credential Manager はどれを使ったらよいのか判断できなくなり、**毎回アカウント選択ダイアログが表示される** ようになります。

自動で整理してくれれば良いのですが、他ツールの資格情報を勝手に消すことはセキュリティ上できません。
そのため、**使うほど資格情報は足されるだけ** になります。

---

### 資格情報が増えていく典型パターン

#### ① Visual Studio で GitHub にサインイン

* Visual Studio の「GitHub でサインイン」を使用
* OAuth トークンが保存される

```
GitHub for Visual Studio - https://github.com/
```

---

#### ② HTTPS で clone / push した

* GitHub が PAT（Personal Access Token）を要求
* 入力すると Git が保存

```
git:https://github.com
git:https://username@github.com
```

OAuth があっても、別枠で保存される

---

#### ③ VS Code の Git 機能や GitHub 拡張を使った

* GitHub Pull Requests
* GitHub Repositories
* GitHub Copilot

これらは内部で API を呼び出すため、独自の資格情報を保存します。

```
gh:github.com:username
```


---

#### ④ URL の違いで別物として扱われる

Git は以下を **すべて別物** として扱います。

```
https://github.com
https://username@github.com
git@github.com
```

同じアカウントでも資格情報が分裂してしまいます。

---


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

### ③ Visual Studio、 VS Code で GitHub に再ログイン

1. Visual Studio を起動
2. 右上 → アカウント
3. GitHub でサインイン

### ④ VS Code も同じアカウントでログイン

1. VSCodeを起動
2. 左下のアカウントアイコンをクリック
3. 「Sign in with GitHub」または「Sign in to GitHub.com」を選択
4. ブラウザが自動で開くので、GitHubアカウントで通常のログイン


---

## おわりに

本記事が、

- GitHub 認証で困っている方
- Visual Studio と VS Code を併用している方

の参考になれば幸いです。
