---
title: ".NET Frameworkで発生した『System.Net.Http が見つからない』問題を解決した話"
emoji: "🧩"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["dotnet", "csharp", "nuget", "mysqlconnector", "systemnethttp"]
published: true
published_at: 2025-10-07 21:05
publication_name: zead
---

## はじめに


今回は、.NET Framework プロジェクトで発生した  
**System.Net.Http のアセンブリ競合問題**をどのように解決したかを紹介します。

### 🔥 発生したエラー

.NET Frameowrk4.7で開発していたアプリケーションを.NET Framework4.7.2に上げ、MySqlConnector パッケージを更新すると、アプリ実行時に次のエラーが発生しました。

```text
ファイルまたはアセンブリ 'System.Net.Http, Version=4.2.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a'、
またはその依存関係の 1 つが読み込めませんでした。
指定されたファイルが見つかりません。
```

一見「System.Net.Http.dll が無い」と言われていますが、実際には **アセンブリのバージョン競合** が原因でした。

---

## 背景

* ターゲットを **.NET Framework 4.7** から **.NET Framework 4.7.2**に変更
* 以前使用していた **MySqlConnector は 0.56**
* バージョンアップして **MySqlConnector 2.x 系**を導入した

すると内部で使用される `System.Net.Http` の依存関係が変わり、異なるバージョンの DLL を読み込もうとして混乱が起こりました。

---

## 最初の試み（失敗）

NuGet で `System.Net.Http` を追加し、Web.config にバージョンリダイレクトを追加しました。

```xml:Web.config
<dependentAssembly>
  <assemblyIdentity name="System.Net.Http" publicKeyToken="b03f5f7f11d50a3a" culture="neutral" />
  <bindingRedirect oldVersion="0.0.0.0-4.3.4.0" newVersion="4.3.4.0" />
</dependentAssembly>
```

この記述は、System.Net.HttpのVersion 0.0.0.0～4.3.4.0が要求されたら、newVersionで指定した 4.3.4.0 にリダイレクトする指定です。

しかし、今度は以下のようなエラーに変化。

```text
ファイルまたはアセンブリ 'System.Net.Http, Version=4.3.4.0' が見つかりません。
```

つまり、**別のバージョン競合を引き起こしてしまった**のです。

---

## 原因の本質

.NET Framework 4.7 以降では、
`System.Net.Http` はフレームワーク本体（GAC）に統合されています。

ところが、NuGet 経由で追加した System.Net.Http（4.3.x）は
**同名の別 DLL**（.NET Standard 用）で、GAC のものと競合してしまいます。

その結果、

> Version 4.0.0.0（GAC） vs Version 4.2.0.0（NuGet）

の衝突が起こり、ランタイムで「見つからない」と言われてしまったわけです。

:::message
.NET 8, .NET 10 などの .NET Core 以降の .NET では、GACは廃止されていて、各アプリケーションが必要なアセンブリを自分の実行フォルダ内に保持するので、.NET Frameworkよりも競合問題が激減しています。
:::

---

## 最終的な解決方法

結論から言うと、**NuGet 版 System.Net.Http を削除し、フレームワーク組み込みのものを使う** ことで解決しました。

### 1. NuGet の System.Net.Http を削除

Visual Studio の「ソリューション エクスプローラー」で：

```
→ 参照
   → System.Net.Http
```

を右クリックして「削除」。

### 2. csproj を以下のように修正

```xml
<Reference Include="System.Net.Http" />
```

👉 HintPath や Version の指定は **一切書かないこと**。 これでフレームワーク標準の System.Net.Http が参照されます。

---

### 3. 不要な DLL をクリーン

`bin` フォルダに `System.Net.Http.dll` が残っていたら削除します。

```powershell
dir bin\System.Net.Http.dll
```

存在する場合は手動で削除してから再ビルド。

---

### 4. MySqlConnector は安定版 0.57.0 を採用

ここは悩んだところなのですが、できるだけこれまで利用していたバージョンとの差異が少ない、0.57.0 採用することにしました。
このバージョンなら、.NET Framework 4.7.1～4.8 で安定動作します。

Visual StudioのNuGetパッケージマネージャでMySqlConnectorのバージョンを 0.57.0 に更新します。

これで以下のようのファイルが更新されるはずです。

```xml:package.config
  <package id="MySqlConnector" version="0.57.0" targetFramework="net472" />
```

```xml:.csproj
<Reference Include="MySqlConnector, Version=0.57.0.0, Culture=neutral, PublicKeyToken=d33d3e53aa5f8c92, processorArchitecture=MSIL">
  <HintPath>..\packages\MySqlConnector.0.57.0\lib\net471\MySqlConnector.dll</HintPath>
</Reference>
```

:::message
このプロジェクトでは、packages.configを利用したパッケージ管理を行っています、
:::

---

### 5. 依存アセンブリのリダイレクト設定

```xml:Web.config
<dependentAssembly>
  <assemblyIdentity name="System.Runtime.CompilerServices.Unsafe"
                    publicKeyToken="b03f5f7f11d50a3a" culture="neutral" />
  <bindingRedirect oldVersion="0.0.0.0-4.0.6.0"
                   newVersion="4.0.6.0" />
</dependentAssembly>
```

これで `System.Runtime` まわりの警告も消えました。


ちなみに、このプロジェクトでは、System.Runtime.CompilerServices.Unsafeはバージョン 4.7.1 を利用しています。

---

## 結果

* ✅ ビルド成功 
* ✅ 実行時エラーなし 
* ✅ MySqlConnector も正常動作 

最終的に `.NET Framework 4.7.2` の標準 System.Net.Http を利用する構成で安定しました。

---

## まとめ

| やること                                                    | 理由                |
| ------------------------------------------------------- | ----------------- |
| NuGet の System.Net.Http を削除                             | フレームワーク版と競合するため   |
| csproj に `<Reference Include="System.Net.Http" />` のみ残す | GAC 参照を明示         |
| bin の System.Net.Http.dll を削除                           | 古い DLL の残骸防止      |
| MySqlConnector 0.57.0 を使用                               | .NET 4.7.2 対応の安定版 |


.NET/.NET Frameworkのパッケージのバージョンを上げた時は、こういったパッケージのバージョン不一致で悩まされることもありますので、何かの参考になればと思い、この記事を公開しています。


