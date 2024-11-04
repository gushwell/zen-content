---
title: "SvelteKit入門: ルーティングとデータローディングについて理解しよう"
emoji: "🔰"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["svelte", "svelte5", "sveltekit"]
published: true
published_at: 2024-11-06 20:45
publication_name: zead
---

## はじめに

以下の記事で、Svelte/SvelteKitの環境構築について説明したので、今度は簡単なWebページを作成して、Svelteへの理解を深めたいと思います。


https://zenn.dev/zead/articles/first-sveltekit


## スケルトンプロジェクトの作成

2024年10月20日に待望のSvelte5が正式リリースされたので、この記事では、Svelte5を利用しています、

まずは、以下のコマンドで、npxをインストールします。記事執筆時点のバージョンは10.8.2でした。

```
npm install -g npx
```

npxを使い、Svelte5のプロジェクトを作成します。

```
npx sv create first-svelte5
```

以下、実行例です。

```
┌  Welcome to the Svelte CLI! (v0.5.7)
│
◇  Which template would you like?
│  SvelteKit minimal
│
◇  Add type checking with Typescript?
│  Yes, using Javascript with JSDoc comments
│
◆  Project created
│
◇  What would you like to add to your project?
│  prettier, eslint
│
◇  Which package manager do you want to install dependencies with?
│  npm
│
◆  Successfully setup integrations
│
◇  Successfully installed dependencies
│
◇  Successfully formatted modified files
│
◇  Project next steps ─────────────────────────────────────────────────────╮
│                                                                          │
│  1: cd first-svelte5                                                     │
│  2: git init && git add -A && git commit -m "Initial commit" (optional)  │
│  3: npm run dev -- --open                                                │
│                                                                          │
│  To close the dev server, hit Ctrl-C                                     │
│                                                                          │
│  Stuck? Visit us at https://svelte.dev/chat                              │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────╯
│
└  You're all set!
```

メッセージのとおり、first-svelte5ディレクトリへ移動し、`npm run dev -- --open`でアプリを起動してみます。

ブラウザが起動し、以下のようなページが表示されます。

![](https://storage.googleapis.com/zenn-user-upload/83b8b35a3cd3-20241021.png)


終了する場合は、コマンドラインで Ctrl+C とタイプします。

ここでは、終了せずに以降も動かし続けておいてください。

## 作成されたファイル群を見てみる

Visual Studio Codeで、プロジェクトのフォルダーを開きます。

![](https://storage.googleapis.com/zenn-user-upload/24bec997cec3-20241021.png)

srcフォルダーはアプリのソースコードを置く場所です。
src/app.html はページのテンプレートです。
src/routes はアプリのルート(routes) を定義します。

staticフォルダーにはアプリをデプロイするときに含めるべきアセット (favicon.png や robots.txt など) を置きます。

その他詳しいプロジェクトの構成は以下のページををご覧ください。

https://kit.svelte.jp/docs/project-structure

app.htmlには、

```html
<div style="display: contents">%sveltekit.body%</div>
```

という記述がありますが、SvelteKit が %sveltekit.body% を適切に置き換えます。

src/routes 内にあるすべての +page.svelte ファイルは、Webアプリのページを意味します。

このアプリでは、`src/routes/+page.svelte`ファイルが一つだけあり、これは / にマッピングされます。（src/routes直下のため）

## SvelteKitのルーティングを理解する

### aboutページを追加

aboutページを追加してみます。 routesの下にaboutフォルダーを作成し、その下に `+page.svelte`を作成し、以下のように記述します。

```svelte:about/+page.svelte
<nav>
    <a href="/">home</a>
    <a href="/about">about</a>
</nav>

<h1>about</h1>
<p>this is the about page.</p>
```

ファイルを保存し、

```
http://localhost:5173/about
```

にアクセスすれば、aboutページが表示されます。

![](https://storage.googleapis.com/zenn-user-upload/731dfbeeab6d-20241021.png)

### homeページを書き換える

次にルートのhomeページ（`routes/+page.svelte`）を書き変え、保存します。

```svelte:+page.svelte
<nav>
    <a href="/">home</a>
    <a href="/about">about</a>
</nav>

<h1>home</h1>
<p>this is the <strong>Home</strong> page.</p>
```

先ほどのaboutページのhomeリンクをクリックすると、`routes/+page.svelte`ページに遷移します。

![](https://storage.googleapis.com/zenn-user-upload/edd669be4a00-20241021.png)

### +layout.svelteでページを共通化する

先ほど作成した2つのページには、

```svelte
<nav>
    <a href="/">home</a>
    <a href="/about">about</a>
</nav>
```

とまったく同じコードがあります。これをき`+layout.svelte`で共通化します。

src/routesの下に、`+layout.svelte`を作成し、以下のように記述します。

```svelte:+layout.svelte
<script >
  const { children } = $props();

</script>
<nav>
  <a href="/">home</a>
  <a href="/about">about</a>
</nav>

{@render children()}

```

こうすることで、`+layout.svelte`の内容が、そのディレクトリ内のすべてのルート(routes)に適用されます。
`{@render children()}` の部分は、`+page.svelte`の内容に置き換わります。

２つの`+page.svelte`ファイルから、

```svelte
<nav>
    <a href="/">home</a>
    <a href="/about">about</a>
</nav>
```

の記述を削除し、ファイルを保存します。

homeとaboutのリンクをクリックし、ページが切り替わるか確認してください。

もし、aboutフォルダーにも、`+layout.svelte`があれば、aboutページは、`about/+layout.svelte`が適用されます。

## データのローディングについて理解する

これまでみてきたページは、固定的でデータによって変更される箇所がありませんでした。
次にデータによって変化するページを作成してみます。

### データを用意する

まずは、rouesにblogフォルダーを作成し、そこにdata.jsを作成します。ここでは、SvelteKitのチュートリアルサイトで使われているデータをそのまま流用しています。


```js:data.js
export const posts = [
  {
    slug: 'welcome',
    title: 'Welcome to the Aperture Science computer-aided enrichment center',
    content: '<p>We hope your brief detention in the relaxation vault has been a pleasant one.</p><p>Your specimen has been processed and we are now ready to begin the test proper.</p>'
  },
  {
    slug: 'safety',
    title: 'Safety notice',
    content: '<p>While safety is one of many Enrichment Center Goals, the Aperture Science High Energy Pellet, seen to the left of the chamber, can and has caused permanent disabilities, such as vaporization. Please be careful.</p>'
  },
  {
    slug: 'cake',
    title: 'This was a triumph',
    content: "<p>I'm making a note here: HUGE SUCCESS.</p>"
  }
];
```

実際は、APIなどで取得し、postsにデータが設定されることになるでしょう。ここではこの3つのBlog記事がposts配列がexportされます。

### サーバーでデータを取得する

次に、blogフォルダーに+page.server.jsファイルを作成します。

```js:+page.server.js
import { posts } from './data.js';

export function load() {
    return {
        summaries: posts.map((post) => ({
            slug: post.slug,
            title: post.title
        }))
    };
}
```

このJavaScriptのコードは、そのファイル名の通りサーバー側で実行されるコードです。ブラウザで実行されるコードではありません。  
先頭行の import文で、先ほどのdata.jsを利用できるようにしています。

load関数は、SvelteKitが自動で呼び出す関数です。そのページに遷移した時に呼び出されます。  
ここでは、map関数を使って、blog記事一覧を表示するための、titleとその記事を識別するslugの一覧を作成してます。

### 取得したデータをレンダリングする

さらに、blogフォルダーに`+page.svelte`ファイルを作成します。

```svelte:+page.svelte
<script>
    const { data } = $props();
</script>

<h1>blog</h1>

<ul>
    {#each data.summaries as { slug, title }}
        <li><a href="/blog/{slug}">{title}</a></li>
    {/each}
</ul>
```

先ほどのload関数で返されたデータが、

```html
<script>
    const { data } = $props();
</script>
```

によって、dataという名前で利用できるようになります。
$props()は、コンポーネント（拡張子.svelteファイル）が外部から受け取ることができる「プロパティ」を定義するために使用されます。  
load関数はデータの取得と準備を担当し、コンポーネントの`$props()`で宣言されたプロパティはそのデータを受け取って表示する役割を果たします。
ちょっと違和感のある書き方ですが、そういうものだと思ってください。

以下のコードで、ブログ記事の一覧を表示しています。

```
    {#each data.summaries as { slug, title }}
        <li><a href="/blog/{slug}">{title}</a></li>
    {/each}
```

`{#each ...} {/each}` がSvelteの制御文で、load関数で得たデータsummariesから一つずつデータを取り出し、slug, title変数に代入しています。

以下のコードで、取り出したslug, titleの値は、{slug}, {title}で参照され置き換わります。

```
    <li><a href="/blog/{slug}">{title}</a></li>
```


3つのファイルを保存し、

```
http://localhost:5173/blog
```

にアクセスしてみましょう。誤りがなかれば以下のように表示されるはずです。

![](https://storage.googleapis.com/zenn-user-upload/fce8bd94b216-20241021.png)

ここで、ブラウザのディベロッパーツールを起動し、blogのリクエストに対し、どんなレスポンスが返ってきているのか確認してみます。

一部を整形して以下に示します。

```html
  <h1 data-svelte-h="svelte-cvg234">blog</h1> 
  <ul>
    <li><a href="/blog/welcome">Welcome to the Aperture Science computer-aided enrichment center</a></li>
    <li><a href="/blog/safety">Safety notice</a></li>
    <li><a href="/blog/cake">This was a triumph</a></li>
  </ul> 
```

確かに、サーバー側で記事一覧がレンダリングされているのが確認できます。

### +layout.svelteを書き換える

`routes/+layout.svelte`を書き換えます。

```svelte:+layout.svelte
<script >
  const { children } = $props();

</script>
<nav>
  <a href="/">home</a>
  <a href="/about">about</a>
  <a href="/blog">blog</a>
</nav>

{@render children()}
```

これで、すべてのページで、

![](https://storage.googleapis.com/zenn-user-upload/073682df2202-20241021.png)

と表示されるようになるはずです。


## 動的なパラメーター付きのルート(routes)を作成する

### Blogの個々の記事を表示する

この状態では、Blog記事一覧ページで、記事をクリックしても、404エラーになってしまいます。

![](https://storage.googleapis.com/zenn-user-upload/6a60d304656e-20241021.png)

この時のURLは、

```
http://localhost:5173/blog/{slug}
```

で{slug}の箇所には、 `welcome`や、`safety` が入ります。

では、この`/blog/{slug}`のページを作成しましょう。

まず、blogフォルダーの下に`[slug]`フォルダーを作成します。`[` `]` も含めたフォルダー名とします。

この下に、`+page.server.js`と`+page.svelte`ファイルを作成します。

```js:/blog/[slug]/+page.server.js
import { error } from '@sveltejs/kit';
import { posts } from '../data.js';

export function load({ params }) {
    const post = posts.find((post) => post.slug === params.slug);

    if (!post) throw error(404);

    return {
        post
    };
}

```

load関数のparamsは、動的ルートパラメーターが含まれます。例えば、/posts/[id]のようなルートがあり、/posts/123というURLがアクセスされた場合、paramsオブジェクトには`{ id: '123' }`が含まれます。

この場合は、`/blog/[slug]`というルートですから、paramsオブジェクトには、`{ slug : 'welcome' }`といったデータが渡ります。

`params`という名前はSvelteKitが決めた名前で変更することはできません。



```svelte:/blog/[slug]/+page.svelte
<script>
  const { data } = $props();
</script>

<h1>{data.post.title}</h1>
<div>{@html data.post.content}</div>
```

`+page.svelte`ファイルは、load関数で取得したdataを `{xxxx}`でバインドしています。

なお、`{@html data.post.content}`の`data.post.content`には、htmlの文字列がそのまま入っているので、そのままHTMLとしてレンダリングします。

![](https://storage.googleapis.com/zenn-user-upload/461a56c5e0b4-20241021.png)


### ブログ記事ページのレイアウトを変更する

今のままだと、`routes/+layout.svelte`の情報が、ブログ記事のページにも適用されます。これを変更し、`routes/blog/[slug]`に`+layout.svelte`ファイルを追加し、ブログ記事だけに別のレイアウトを適用してみましょう。


```svelte:/blog/[slug]/+layout.svelte
<script>
    const { data, children } = $props();
</script>

<div class="layout">
  <main>
    {@render children()}
  </main>
</div>

<style>
  @media (min-width: 640px) {
      .layout {
            display: grid;
            gap: 2em;
            grid-template-columns: 1fr 16em;
      }
  }
</style>
```

これは、幅が640ピクセル以上の時に、右側に16em分の空白を確保し、残りでコンテンツを表示させる指定になります。

![](https://storage.googleapis.com/zenn-user-upload/f775c9d4d4f4-20241021.png)


### +layout.server.jsでServerの処理を共通化する

今度は、ブログ記事の右側に以下のような記事一覧を表示してみましょう。
すべての個別ページでも、ブログ記事の一覧データを取得する必要があります。

`src/routes/blog/+page.server.js` で行っているのと同じように、`src/routes/blog/[slug]/+page.server.js` の `load`関数から `summaries` を返すこともできますが、これでは同じことを繰り返すことになってしまいます。

そこで、代わりに、`src/routes/blog/+page.server.js` を `src/routes/blog/+layout.server.js` にリネームします。
こうすることで、`src/routes/blog/+layout.server.js`のload関数は、ブログ記事一覧のページ(`+page.svelte`)でもブログの個別記事(`+layout.svelte`)のページでも両方で動くようになります。

次に、個別記事のほうを修正します。すべての記事で共通ですので、`src/routes/blog/[slug]/+layout.svelte` を以下のように変更します。

```svelte:/blog/[slug]/+layout.svelte
<script>
    const { data, children } = $props();
</script>

<div class="layout">
  <main>
    {@render children()}
  </main>
  <aside>
    <h2>More posts</h2>
    <ul>
        {#each data.summaries as { slug, title }}
            <li>
                <a href="/blog/{slug}">{title}</a>
            </li>
        {/each}
    </ul>
  </aside>
</div>

<style>
  @media (min-width: 640px) {
      .layout {
          display: grid;
          gap: 2em;
          grid-template-columns: 1fr 16em;
      }
  }
</style>
```

asideタグが追加したタグになります。他は変更はありません。

先頭でdataプロパティを利用できるように宣言しています。

```
const { data, children } = $props();
```

このdata経由で、`+layout.server.js`で返る記事一覧が参照できるようになります。

`+page.server.js`で返すデータは、`+page.svelte`で参照し、`+layout.server.js`で返すデータは、`+layout.svelte`で参照するという対応関係になっています。

これで、再度Blogの個別記事を開くと、先ほど示したように、ページの右側に記事一覧が表示されます。


![](https://storage.googleapis.com/zenn-user-upload/56633e2a3948-20241021.png)


## 最後に

文章だけだと、難しく感じるかもしれませんが、ぜひ実際に手を動かしてやってみてください。それほど難しくはないことがわかると思います。

SvelteKitが定めたお約束がいくつかありますので、そこを押さえてしてしまえば、簡単にルーティングとデータローディングを実現できます。
