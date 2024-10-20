---
title: "SvelteKit入門 簡単なWEBページの作成を作成してみよう"
emoji: "🔰"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["svelte", "sveltekit"]
published: true
published_at: 2024-11-03 21:20
publication_name: zead
---

## はじめに

以下の記事で、Svelte.SvelteKitの環境構築について説明したので、今度は簡単なWebページを作成して、Svelteへの理解を深めたいと思います。


https://zenn.dev/zead/articles/first-sveltekit


## スケルトンプロジェクトの作成

npm createコマンドでプロジェクトを作成します。この記事では、最新のSvelte5（正式リリースはまだ）を利用したいと思います。

```
 npm create svelte@latest first-svelte
```

プロジェクト作成のための質問に答えます。

テンプレートはSkeltonを選びます。

![image](uploads/33ceebba3c5dbdb8e73a5fe6206a6e17/image.png)


TypeScriptはNoを選びます。

![image](uploads/ef48b5fb665e81e5ce895f942976c7f6/image.png)

追加オプションは、以下のように上の3つをONにします。

![image](uploads/926dfe9ca87f327152bde56336656de1/image.png)

プロジェクトが作成されると、次に何をしたら良いかが表示されます。

```
Next steps:
  1: cd first-svelte
  2: npm install
  3: git init && git add -A && git commit -m "Initial commit" (optional)
  4: npm run dev -- --open
```

順に実行します。

ローカルサーバーが起動時、ブラウザに作成したアプリが表示されます。

![image](uploads/903b7ebb5208145b9b95886b8c9f68b7/image.png)

コマンドラインで、q+[enter]でローカルサーバーを終了します。

ここでは、終了せずに以降も動かし続けておいてください。

## 作成されたファイル群を見てみる

Visual Studio Codeで、プロジェクトのフォルダを開きます。

![image](uploads/f097f7a67db1dd70ac968db989960648/image.png)

srcフォルダはアプリのソースコードを置く場所です。src/app.html はページのテンプレートで、src/routes はアプリのルート(routes) を定義します。

staticフォルダにはアプリをデプロイするときに含めるべきアセット (favicon.png や robots.txt など) を置きます。

その他詳しいプロジェクトの構成は以下のページををご覧ください。

[プロジェクト構成](https://kit.svelte.jp/docs/project-structure)

app.htmlには、

```html
<div style="display: contents">%sveltekit.body%</div>
```

という記述がありますが、SvelteKit が %sveltekit.body% を適切に置き換えます。

src/routes 内にあるすべての +page.svelte ファイルは、アプリのページを作成します。

このアプリでは、現在ページが1つあり (src/routes/+page.svelte)ます。これは / にマッピングされます。

## aboutページを追加

aboutページを追加してみます。 routesの下にaboutフォルダを作成し、その下に `+page.svelte`を作成し、以下のように記述します。

```svelte
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

![image](uploads/0a8ed1518b660bf6edf736edcc16f6a6/image.png)

## homeページを書き換える

ではルートのhomeページ（routes/+page.svelte）を書き変え、保存します。

```svelte
<nav>
    <a href="/">home</a>
    <a href="/about">about</a>
</nav>

<h1>home</h1>
<p>this is the <strong>Home</strong> page.</p>
```

先ほどのaboutページのhomeリンクをクリックすると、`routes/+page.svelte`ページに遷移します。

![image](uploads/70ce29305f13831d74c5c4d27c49a4df/image.png)


## +layout.svelteで共通化する

先ほど作成した2つのページには、

```svelte
<nav>
    <a href="/">home</a>
    <a href="/about">about</a>
</nav>
```

とまったく同じコードがあります。これをき+layout.svelteで共通化します。

src/routesの下に、+layout.svelteを作成し、以下のように記述します。

```svelte
<nav>
    <a href="/">home</a>
    <a href="/about">about</a>
</nav>

<slot />

```

こうすることで、+layout.svelteの内容が、そのディレクトリ内の全てのルート(routes)に適用されます。
<slot /> の部分は、+page.svelteの内容に置き換わります。

２つの+page.svelteファイルから、

```svelte
<nav>
    <a href="/">home</a>
    <a href="/about">about</a>
</nav>
```

の記述を削除し、ファイルを保存します。

homeとaboutのリンクをクリックし、ページが切り替わるか確認してください。

もし、aboutフォルダにも、+layout.svelteがあれば、aboutページは、about/_layout.svelteが適用されます。

## Blog記事一覧ページを作成する

これまでみてきたページは、固定的でデータによって変更される箇所がありませんでした。
次にデータによって変化するページを作成してみます。

### data.js

まずは、rouesにblogフォルダを作成し、そこにdata.jsを作成します。これは、SvelteKitのチュートリアルサイトで使われているデータです。


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

### blog/+page.server.js

次に、blogフォルダに+page.server.jsファイルを作成します。

```js
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

このJavaScriptのコードは、その名の通り、サーバー側で実行されるコードです。  
importで、先ほどのdata.jsを利用できるようにしています。

load関数は、SvelteKitが自動で呼び出す関数です。そのページに遷移した時に呼び出されます。  
ここでは、map関数を使って、blog記事一覧を表示するための、titleとその記事を識別するslugの一覧を作成してます。

### blog/+page.svelte

さらに、blogフォルダに_page.svelteファイルを作成します。

```
<script>
    export let data;
</script>

<h1>blog</h1>

<ul>
    {#each data.summaries as { slug, title }}
        <li><a href="/blog/{slug}">{title}</a></li>
    {/each}
</ul>
```

先ほどのload関数で返されたデータが、

```
<script>
    export let data;
</script>
```

によって、dataという名前で利用できるようになります。このexportはJavaScriptのexportとは意味が異なります。  
コンポーネント（拡張子.svelteファイル）が外部から受け取ることができる「プロパティ」を定義するために使用されます。  
load関数はデータの取得と準備を担当し、コンポーネントの`export let`で宣言されたプロパティはそのデータを受け取って表示する役割を果たします。
ちょっと違和感のある書き方ですが、そういうものだと思ってください。


以下のコードで、ブログ記事の一覧を表示しています。

```
    {#each data.summaries as { slug, title }}
        <li><a href="/blog/{slug}">{title}</a></li>
    {/each}
```

`{#each ...} {/each}`　がSvelteの制御文で、load関数で得たデータsummariesから一つずつデータを取り出し、slug, title変数に代入しています。

以下のコードで、取り出したslug, titleの値は、{slug}, {title}で参照され置き換わります。

```
    <li><a href="/blog/{slug}">{title}</a></li>
```


3つのファイルを保存し、

```
http://localhost:5173/blog
```

にアクセスしてみましょう。誤りがなかれば以下のように表示されるはずです。

![image](uploads/e12e52650b3d68a3b7ae33eb07db5629/image.png)

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

routes/+layout.svelteを書き換えます。

```svelte
<nav>
    <a href="/">home</a>
    <a href="/about">about</a>
    <a href="/blog">blog</a>
</nav>

<slot />
```

これで、全てのページで、

![image](uploads/db2c68d203922627330ab00fdf78c3c5/image.png)

と表示されるようになるはずです。


## Blogの個々の記事を表示する

この状態では、Blog記事一覧ページで、記事をクリックしても、404エラーになってしまいます。

![image](uploads/f05f1ceecb4b61d94bc3254f7913119f/image.png)

この時のURLは、

```
http://localhost:5173/blog/{slug}
```

で{slug}の箇所には、 `welcome`や、`safety` が入ります。

では、この`/blog/{slug}`のページを作成しましょう。

まず、blogフォルダに下に`[slug]`フォルダを作成します。`[` `]` も含めたフォルダ名とします。

この下に、`+page.server.js`と`+page.svelte`ファイルを作成します。


##### +page.server.js

```js
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

load関数のparamsは、動的ルートパラメータが含まれます。例えば、/posts/[id]のようなルートがあり、/posts/123というURLがアクセスされた場合、paramsオブジェクトには`{ id: '123' }`が含まれます。

この場合は、`/blog/[slug]`というルートですから、paramsオブジェクトには、`{ slug : 'welcome' }`といったデータが渡ります。

`params`という名前はSvelteKitが決めた名前で変更することはできません。


##### +page.svelte

```svelte
<script>
    export let data;
</script>

<h1>{data.post.title}</h1>
<div>{@html data.post.content}</div>
```

`+page.svelte`ファイルは、load関数で取得したdataを `{xxxx}`でバインドしています。

なお、`{@html data.post.content}`は、`data.post.content`には、htmlの文字列がそのまま入っているので、そのままHTMLとしてレンダリングします。

### ブログ記事ページのレイアウトを変更する

今のままだと、`routes/+layout.svelte`の情報が、ブログ記事のページにも適用されます。これを変更し、`routes/blog/[slug]`に`+layout.svelte`ファイルを追加し、ブログ記事だけに別のレイアウトを適用してみましょう。


```
<script>
    export let data;
</script>

<div class="layout">
    <main>
        <slot />
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

これは、幅が、640ピクセル以上の時に、右側に16em分の空白を確保し、残りでコンテンツを表示させる指定になります。

## +layout.server.jsでServerの処理を共通化する

今度は、ブログ記事の右側に以下のような記事一覧を表示してみましょう。

![image](uploads/1aad5c43a869818431732d2d18982573/image.png)

このページでも、ブログ記事の一覧データを取得する必要があります。

src/routes/blog/+page.server.js で行っているのと同じように、src/routes/blog/[slug]/+page.server.js の load 関数から summaries を返すこともできますが、これでは同じことを繰り返すことになってしまいます。

そこで、代わりに、src/routes/blog/+page.server.js を src/routes/blog/+layout.server.js にリネームします。
こうすることで、src/routes/blog/+layout.server.jsのload関数は、ブログ記事一覧でもmブログの個別記事のページでも両方で動くようになります。

次に、個別記事のほうを修正します。全ての記事で共通ですので、src/routes/blog/[slug]/+layout.svelte を以下のように変更します。

```svelte
<script>
    export let data;
</script>

<div class="layout">
    <main>
        <slot />
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

先頭でdataプロパティを利用できるように宣言していますが、このdata経由で、+layout.server.jsで返る記事一覧が参照できるようになります。

```
  export let data;
```

+page.server.jsで返すデータは、+page.svelteで参照し、+layout.server.jsで返すデータは、+layout.svelteで参照するという対応関係になっています。

これで、再度Blogの個別記事を開くと、先ほど示したように、ページの右側に記事一覧が表示されます。


