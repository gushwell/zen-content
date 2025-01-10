---
title: "ASP.NET CoreプロジェクトにSvelteKitを組み込む"
emoji: "🤝"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["svelte", "sveltekit", "aspnetcore", "csharp" ]
published: true
published_at: 2025-01-13 20:45
publication_name: "zead"
---

## はじめに

ASP.NET CoreのフロントにSvelteを使いたいので、同一プロジェクト内でASP.NET Core Web APIとSvelteを扱えるようにする手順を示します。

ここでは、SvelteKit側はSPA(Single Page Application)の形態で利用することとします。


## ASP.NET Core Web APIプロジェクトの作成

まずは、Visual StudioでASP.NET Core Web APIプロジェクトを作成します。

![](https://storage.googleapis.com/zenn-user-upload/583f0cc948d6-20250109.png)

ここでは名前を`SvelteAspNetApi`としました。

追加情報のダイアログは、以下のように設定しました。ここではコンテナのサポートは無効にしています。必要に応じて有効のチェックをつけてください。

![](https://storage.googleapis.com/zenn-user-upload/0a79f2b2ae9a-20250109.png)

## SvelteKitのプロジェクトを追加

タームナルを開いて、作成したC#のプロジェクトのフォルダに移動します。ソリューションフォルダではなく、プロジェクトフォルダなので間違えないようにしてください。

ここでは、Svelteの公式ドキュメント通りにnpxコマンドを利用します。

https://svelte.jp/docs/svelte/getting-started

1. まず、以下のコマンドを実行します。
    
    ```
    npx sv create ClientApp
    ```

2. 最初のテンプレートの選択では、「SvelteKit minimal」を選びます。

![](https://storage.googleapis.com/zenn-user-upload/1427e1008120-20250109.png)

3. 言語の選択では、JavaScriptを選択します。

![](https://storage.googleapis.com/zenn-user-upload/dcf2ea72ba17-20250109.png)


4. パッケージマネージャの選択では、npmを選択します。

![](https://storage.googleapis.com/zenn-user-upload/5e2890433fe5-20250109.png)


※ それ以外の選択ではお好みの選択でOKです。

5. SvelteKitのプロジェクトが作成されたら、以下のようにタイプしてパッケージをインストールします。

    ```
    cd ClientApp
    npm install
    npm install --save-dev @sveltejs/adapter-static
    ```

Visual Studio のソリューションエクスプローラーを開くと、ClientAppフォルダが追加されたのが確認できます。

![](https://storage.googleapis.com/zenn-user-upload/788ed4210dde-20250109.png)


## svelte.config.jsの編集

ASP.NET CoreのホストでSvelteKitが動作するよう、svelte.config.jsを以下のように変更します。  
svelte.config.jsは、ClientAppフォルダの直下にあります。

```js
import adapter from '@sveltejs/adapter-static';

/** @type {import('@sveltejs/kit').Config} */
const config = {
    kit: {
        adapter: adapter({
            pages: '../wwwroot',
            assets: '../wwwroot',
            fallback: 'index.html'
        })
    }
};

export default config;
```

これは、Svelteのソースをビルドした際にファイルをASP.NET Coreのwwwrootフォルダに出力するためです。

## Svelteの動作確認

ここで、Svelteのプロジェクトが動作するか確認してみます。
以下のコマンドをタイプします。

```
npm run build
```

正常に終了すれば、Visual StudioのソリューションエクスプローラーのSvelteAspNetApiプロジェクトにwwwrootフォルダが追加されているのが確認できます。

続いて、以下のコマンドを実行します。

```
npm run dev
```

以下のように表示されますので、http://localhost:5173/　にアクセスします。
```
  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

以下のページが表示されればOkです。

![](https://storage.googleapis.com/zenn-user-upload/3c3d95cb4204-20250109.png)

`q[Enter]` でnpm run devで動かしたプログラムを終了させます。


## C#プロジェクトの変更

続いて、C#のプロジェクト側の対応をします。

Program.csを以下のように書き換えます。追加するのは+メークがついた3行です。

```cs

namespace SvelteAspNetApi;

public class Program {
    public static void Main(string[] args) {
        var builder = WebApplication.CreateBuilder(args);

        // Add services to the container.

        builder.Services.AddControllers();
        // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();

        var app = builder.Build();

        // Configure the HTTP request pipeline.
        if (app.Environment.IsDevelopment()) {
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        app.UseHttpsRedirection();
+       app.UseStaticFiles();
+       app.UseRouting();
        app.UseAuthorization();

        app.MapControllers();

+       app.MapFallbackToFile("index.html");

        app.Run();
    }
}
```

これで、Visual Studioからデバッグ実行してみます。

APIの動作確認をするSwaggerのページが表示されますが、ブラウザのURLを 

```
https://localhost:7096/
```

に変えてみます。（ポート番号は環境によて異なるかもしれません）

これで、再度Svelteのページが表示されればOKです。


![](https://storage.googleapis.com/zenn-user-upload/3c3d95cb4204-20250109.png)


Svelteのプログラムが、ASP.NET Coreのホストで動作していることが確認できました。

## API連携をしてみる

### C#のWeatherForecastControllerを変更

まずは、APIのルーティングとSvelteのルーティングを区別するために、このプロジェクトではC#で作成するAPIは、

```
https://localhost:7096/api/....
```

のように必ず、apiで始まるようにします。

サンプルで作成されたWeatherForecast APIのコードを変更します。[Route]属性の引数を`"api/[controller]"`に変更します。

```cs
using Microsoft.AspNetCore.Mvc;

namespace SvelteAspNetApi.Controllers;
[ApiController]
[Route("api/[controller]")]
public class WeatherForecastController : ControllerBase 
```

### Svelteに新規ページを追加

続いて、Svelte側にWeatherForecast APIを呼び出し、その結果を表示する新しいページを作成します。

以下のように、ClientApp/src/routes フォルダにweatherフォルダを作成し、その下に +page.svelteファイルを新規作成します。

![](https://storage.googleapis.com/zenn-user-upload/7723f1f60583-20250109.png)


+page.svelte を以下のように記述します。

```html
<script>
  import { onMount } from 'svelte';

  let data = [];

  onMount(async () => {
    const response = await fetch('/api/WeatherForecast');
    data = await response.json();
  });
</script>

<h1>Data from API</h1>
{#each data as item}
  <div>
    <span>{item.date}</span>
    <span>{item.temperatureC}</span>
    <span>{item.temperatureF}</span>
    <span>{item.summary}</span>
  </div>
{/each}
```

このページでは、WeatherForecast APIを呼び出して、取得したデータを {#each}構文で表示しています。


続いて、ClientApp/src/routes/+page.svelteに以下のようなリンクタグを追加します。(これは、最初から存在する+page.svelteファイルです)

```html
<div>
    <a href="/weather">FetchData</a>
</div>
```

### プロジェクトファイルを変更

このままですと、Svelte側に変更を加えるたびに、`npm run build`を実行しなければなりません。C#側をビルドした時に、一緒のSvelteのソースをビルドできると便利です。

以下のコードを`SvelteAspNetApi.csproj`ファイルに追加します。

```xml
  <Target Name="NpmBuild" BeforeTargets="Build">
    <Message Text="#Start npm run build" Importance="high" />
    <RemoveDir Directories="wwwroot" />
    <Exec Command="npm run build" WorkingDirectory="./ClientApp" />
  </Target>
```


### デバッグの初期URLを変更

デバッグするたびに、ブラウザのアドレス欄のURLを変更するのは面倒なので、初期URLを変更しSvelteのページが開くように変更します。
swaggerのページを開きたい場合は、直接以下のURLを開くこととします。

```
https://localhost:7096/swagger/index.html
```

プロジェクトのプロパティ画面を開き、デバッグ設定ダイアログを開き、URL欄をクリアします。

![](https://storage.googleapis.com/zenn-user-upload/3ace292576c4-20250109.png)


## 実行してみる

それでは、Visual Studio からデバッグ実行してみます。

最初に以下のページが表示されます

![](https://storage.googleapis.com/zenn-user-upload/706cdc86d671-20250109.png)

FetchDataのリンクをクリックすると、先ほど作成したページが表示されます。

![](https://storage.googleapis.com/zenn-user-upload/b682c34b699b-20250109.png)


APIを呼び出し、その結果を表示しているのを確認できます。

:::message
実際の開発では、`vite build --watch` を実行しておいて、Svelte側もホットリロードに対応させると良いでしょう。
:::


## csprojファイルを編集し、発行にも対応させる

最後に、csprojファイルを編集して、発行にも対応させます。以下の行を追加してください。


```xml
  <ItemGroup>
    <Content Update="wwwroot\**" CopyToPublishDirectory="Never" />
    <Content Update="ClientApp\**" CopyToPublishDirectory="Never" />
  </ItemGroup>

  <Target Name="CopyPublish" AfterTargets="Publish">
    <Message Text="## Copy Vite build output" Importance="high" />
    <Exec Command="xcopy /f /s /e /y $(ProjectDir)wwwroot\* $(PublishDir)\wwwroot" />
  </Target>
```

これは、dotnetの発行の機能をそのまま利用すると、wwwrootにあるファイルをうまくコピーできないためです。
発行時の対象フォルダから除外して、xcopyコマンドで強制的にコピーしています。

