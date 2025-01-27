---
title: "ASP.NET CoreプロジェクトにSvelteを組み込む (SvelteKitは使わない)"
emoji: "🤝"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["svelte", "aspnetcore", "csharp" ]
published: true
published_at: 2025-01-27 20:45
publication_name: "zead"
---

## はじめに

記事：「ASP.NET CoreプロジェクトにSvelteを組み込む」では、ASP.NET Core APIプロジェクトにSvelteKitを組み込み、フロントエンドとしてSvelteを使えるようにしました。

https://zenn.dev/zead/articles/sveltekit-aspnetcore

この記事では、SvelteKitを使わずに、SvelteのみをASP.NET Core APIプロジェクトに組み込む方法について説明します。


## ASP.NET Core Web APIプロジェクトの作成

まずは、Visual StudioでASP.NET Core Web APIプロジェクトを作成します。

![](https://storage.googleapis.com/zenn-user-upload/7d549ba1cc50-20250114.png)

ここでは名前を`SvelteAspNetCore`としました。

## Svelteのプロジェクトを追加

1. タームナルを開いて、作成したC#のプロジェクトのフォルダーに移動します。ソリューションフォルダーではなく、プロジェクトフォルダーなので間違えないようにしてください。

2. 以下のコマンドを実行します。
    
    ```
    npm create vite@latest
    ```

3. 質問に答えます。これによりSveltreKitを含まないSvelteだけのプロジェクトが作成されます。

    ```
    Project name: ... ClientApp
    Package name: ... clientapp
    Select a framework: » Svelte
    Select a variant: » JavaScript
    ```

4. Svelteプロジェクトの作成が終わったら、以下のコマンドを実行

    ```
    cd clientapp
    npm install
    ```

5. パッケージのインストールが終わると、Visual Studioのソリューションエクスプローラーは以下のようになります。

    ![](https://storage.googleapis.com/zenn-user-upload/7398478677d7-20250114.png)


    この構造により、ASP.NET CoreプロジェクトとSvelteアプリケーションを同じリポジトリで管理しやすくなります。
    
    
6. vite.config.jsを以下のように書き換えます。

    ```js
    import { defineConfig } from 'vite'
    import { svelte } from '@sveltejs/vite-plugin-svelte'

    export default defineConfig({
      plugins: [svelte()],
      build: {
        outDir: '../wwwroot',
        emptyOutDir: true
      }
    })
   ```

   これでビルド時の出力フォルダーをwwwrootにしています。

7. ClientAppフォルダーで、以下のコマンドでSvelteプロジェクトをビルドします。

    ```
    npm run build
    ```

8. wwwrootフォルダーが作成されたことを確認します。

    ![](https://storage.googleapis.com/zenn-user-upload/6b7ee826d574-20250114.png)

9. 続いて、以下のコマンドでSvelteアプリだけを動かしてみます。

    ```
    npm run dev
    ```

10. `http://localhost:5173/` にアクセスします。

    以下のページが表示されればOKです。

    ![](https://storage.googleapis.com/zenn-user-upload/d73791532a0f-20250114.png)


## ASP.NET Coreでsvelteをホストする

### Program.csの変更

ASP.NET CoreのホストでSvelteが動作するよう、Program.csを以下のように変更します。追加するのは、+記号のある2行です。  

```cs
        app.UseHttpsRedirection();
        app.UseAuthorization();
+       app.UseStaticFiles();  
        app.MapControllers();
+       app.MapFallbackToFile("index.html");
        app.Run();
```

MapFallbackToFile は、特定のルートが見つからない場合に指定されたファイルにフォールバックするために使用されます。
これにより、サーバー側(C#側)で特定のルートが見つからない場合でも、index.htmlにルーティングされ、クライアント側のルーティングが行われるようになります。


### SvelteAspNetCore.csprojファイルの変更

C#のビルド時に、Svelte側もビルドするよう以下をSvelteAspNetCore.csprojファイルに追加します。

```xml
  <Target Name="NpmBuild" BeforeTargets="Build">
    <Message Text="#Start npm run build" Importance="high" />
    <RemoveDir Directories="wwwroot" />
    <Exec Command="npm run build" WorkingDirectory="./ClientApp" />
  </Target>
```

### デバッグで動作確認

F5キーでデバッグ実行してみます。

APIの動作確認をするSwaggerのページが表示されますが、ブラウザのURLを 

```
https://localhost:7096/
```

に変えてみます。（ポート番号は環境によて異なるかもしれません）

これで、再度Svelteのページが表示されればOKです。

![](https://storage.googleapis.com/zenn-user-upload/92dec24d2a53-20250114.png)

### デバッグの初期URLを変更

デバッグするたびに、ブラウザのアドレス欄のURLを変更するのは面倒なので、初期URLを変更しSvelteのページが開くように変更します。
swaggerのページを開きたい場合は、直接以下のURLを開くこととします。

```
https://localhost:7096/swagger/index.html
```

プロジェクトのプロパティ画面を開き、デバッグ設定ダイアログを開き、URL欄をクリアします。

![](https://storage.googleapis.com/zenn-user-upload/edfe11d7ca3f-20250114.png)


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

### Svelteのルーティングの設定

SvelteKitを使わないため、このままではルーティングができません。そのため、`svelte-routing`を利用することとします。

https://github.com/EmilTholin/svelte-routing

以下のコマンドで、インストールします。

```
npm i -D svelte-routing
```

### Svelteにページを追加


#### Menu.svelte

ClientApp/src/pagesフォルダーを作成し、その下に Menu.svelteファイルを新規作成します。これが最初に表示されるページとなります。

```html
<script>
</script>

<nav>
  <a href="/weather-forcast">Weather</a>
</nav>

<style>
</style>
```

#### WeatherForecast.svelte

続いて、WeatherForecast APIを呼び出し、その結果を表示するページを作成します。

以下のように、ClientApp/src/pagesフォルダーの下に WeatherForecast.svelteファイルを新規作成します。

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


#### App.svelte

App.svelteを以下のように変更します。`<Router>`タグは、svelte-routingが提要するタグです。`<Router>`タグの中身が、それぞれのpathで示したSvelteコンポーネント（svelteファイル）で切り替わることになります。svelte-routingの使い方は、公式サイトなどで確認してください。


```html
<script>
  import { Route, Router } from "svelte-routing";
  import Menu from './pages/Menu.svelte';
  import WeatherForecast from './pages/WeatherForecast.svelte';
</script>

<main>
    <h1>Asp.Net Core + Svelte</h1>
    <Router>
      <Route path="" component={Menu} exact />
      <Route path="/weather-forcast" component={WeatherForecast} />
    </Router>
</main>

<style>
  h1 {
    margin: 0;
    padding: 0;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    text-align: center;
  }
</style>
```

SvelteKitの場合は、すべてのページのファイル名が`+page.svelte`になりますが、svelte-routingでは自由度が高いので、ルーティングとsvelteファイルの関係を自由に定義することができます。ページを追加するたびに`<Route>`タグを追加しないといけないのが面倒ですが、筆者はプログラムを作成しpagesフォルダーのファイルから自動で`<Route>`タグを追加するようにしています。
package.jsonを編集し、このプログラムを`npm run build`時に実行するようにすれば、自動化することも可能です。

### 動作確認

それでは、ビルドして、F5で実行してみます。

起動すると、以下のページが表示されます。

![](https://storage.googleapis.com/zenn-user-upload/720def1b4fb7-20250114.png)

ここで、Weatherのリンクをクリックすると以下の表示に変化します。APIが呼ばれその結果を表示していることを確認できます。

![](https://storage.googleapis.com/zenn-user-upload/d92497d09f73-20250114.png)


:::message
実際の開発では、`vite build --watch` を実行しておいて、Svelte側もホットリロードに対応させると良いでしょう。
:::

