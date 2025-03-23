---
title: "Svelte5でシンプルなモーダルコンポーネントを作る"
emoji: "⚙️"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["svelte", "svelte5" ]
published: true
published_at: 2025-03-23 21:15
publication_name: "zead"
---

# Svelte5でシンプルなモーダルコンポーネントを作る

## 1. はじめに

Svelteは、コンパイル時に不要なフレームワークのランタイムを削減し、軽量で高速なアプリケーションを作成できるフロントエンドフレームワークです。Svelteのコンポーネントは `.svelte` ファイルとして定義され、HTML・CSS・JavaScriptを統合して記述できるのが特徴です。これにより、シンプルな構造で直感的にUIコンポーネントを開発できます。

本記事では、Svelteでシンプルなモーダルコンポーネントを作成する方法を通じて、SvelteでUIコンポーネントを作成する基礎を紹介します。
モーダル（Modal）は、ユーザーの注意を引くためのポップアップウィンドウです。アラート、確認ダイアログ、フォームの表示などに使われます。

## 2. モーダルコンポーネントの作成

以下がシンプルなModalコンポーネントのコードです。 モーダルの開閉状態を管理し、親で指定した要素を表示できるようにします。

```svelte:Modal.svelte
<svelte:options runes={true} />
<script>
  let { show = false, onClose = () => {},children } = $props();

  function close() {
    onClose();
  }
</script>

{#if show}
  <div class="modal-overlay" >
    <div class="modal-content" >
      {@render children()}
      <button onclick={close}>閉じる</button>
    </div>
  </div>
{/if}

<style>
  .modal-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal-content {
    background: white;
    padding: 12px;
    border-radius: 4px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  }
</style>
```

### コードの説明

1. `<svelte:options runes={true} />`

```svelte
<svelte:options runes={true} />
```

Svelte 5のrunesモードを有効にしています。これにより、`$props()`や`@render`などの新しい記法を使えるようになります。

2. `<script>` ブロック

```svelte
<script>
  let { show = false, onClose = () => {}, children } = $props();

  function close() {
    onClose();
  }
</script>
```

- $props() 
    - 親コンポーネントから渡されたプロパティ（props）を取得するSvelte 5の新しい記法です。
- show (デフォルト: false)
    - モーダルの表示・非表示を制御するフラグ。親からこの値を変更することでモーダルの表示/非表示の制御をします。
- onClose (デフォルト: 空の関数) 
    - いわゆるイベントの定義で、モーダルを閉じる処理を実行する関数です。親コンポーネントから渡される想定をしています。
- children
    - モーダル内に表示するコンテンツ。
- close() 関数
    - `onClose()`を実行し、モーダルを閉じます。

3. テンプレート部分（モーダルの描画）

```svelte
{#if show}
  <div class="modal-overlay">
    <div class="modal-content">
      {@render children()}
      <button onclick={close}>閉じる</button>
    </div>
  </div>
{/if}
```

- `{#if show}`
    - showがtrueのときに、モーダルを表示します。
- `<div class="modal-overlay">`
    - モーダルの背景部分。クリックするとモーダルの中身が見えにくくなるよう、半透明の背景を適用しています。
- `<div class="modal-content">`
    - モーダルのメインコンテンツ部分です。
- `{@render children()}`
    - children()を呼び出し、親コンポーネントから渡された内容をモーダル内に表示しています。
- `<button onclick={close}>閉じる</button>`
    - 「閉じる」ボタンを押すと、close() 関数が実行され、onClose() が呼ばれます。


4. スタイル

```svelte
<style>
  .modal-overlay {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal-content {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
</style>
```

- .modal-overlay
    - 画面全体を覆う背景要素（半透明）。
    - `display: flex;` を使って中央に配置。
- .modal-content
    - モーダルの本体部分。
    - 背景色は白、角を丸め、影をつけることでモーダルらしく見せます。


## 3. 親コンポーネントでの使用

作成した `Modal.svelte` を親コンポーネントで使用してみます。

```svelte:App.svelte
<svelte:options runes={true} />
<script>
  import Modal from './Modal.svelte';
  let showModal = $state(false);
</script>

<button onclick={() => { showModal = true;  }}>モーダルを開く</button>
<Modal show={showModal} onClose={() => { showModal = false; }>
  <h2>モーダルのタイトル</h2>
  <p>ここに好きなコンテンツを追加できます。</p>
</Modal>
```

- `<button>` をクリックするとshowModalがtrueになり、モーダルが開きます。
- モーダルの「閉じる」ボタンを押すと、onCloseに指定されたcloseModal() が実行され、showModalがfalseになり、モーダルが閉じます。
- `<Modal>`の子要素がchildrenとしてModalコンポーネントに渡され、Modalコンポーネントの`{@render children()}`でレンダリングされます。

動かしてみましょう。

プログラムを動かし、「モーダルを開く」のボタンをクリックします。

![main page](/images/svelte-01.png)

以下のように、モーダルウィンドウが開きます。「閉じる」ボタンをクリックするとモーダルウィンドウが閉じます。

![modal window](/images/svelte-02.png)


うまく動いているようです。


## 4. 改良

「閉じる」ボタンが、Modalコンポーネント側にあると表示の自由度が妨げられますので、「閉じる」ボタンを親コンポーネントに移動します。

Modal.svelteを以下のように変更します。

```svelte:Modal.svelte
<svelte:options runes={true} />
<script>
  let { show = false,children } = $props();

</script>

{#if show}
  <div class="modal-overlay" >
    <div class="modal-content" >
      {@render children()}
    </div>
  </div>
{/if}

<style>
  ... 省略 ...
</style>
```

親コンポーネント側に閉じるボタンを移動します。

```svelte:App.svelte
<svelte:options runes={true} />
<script>
  import Modal from './Modal.svelte';
  let showModal = $state(false);

  function closeModal() {
    showModal = false;
  }

	function openModal() {
		showModal = true;
	}
</script>

<button onclick={openModal}>モーダルを開く</button>
<Modal show={showModal} >
	<div class="modal">
    <h2>モーダルのタイトル</h2>
    <p>ここに好きなコンテンツを追加できます。</p>
    <button class="button" onclick={closeModal}>閉じる</button>
	</div>
</Modal>
```

このようにすることで、以下のメリットが生まれます。

- コンポーネントの責務が明確になる
    -Modalは「モーダルの枠の見た目と表示制御」のみを担当し、「閉じるボタンの配置やデザイン」は親が管理する。
- ボタンのデザインや動作をカスタマイズしやすくなる
    - 「閉じる」以外のボタン（OK、キャンセルなど）も簡単に追加できる。
- 汎用性が上がる
    - 「閉じる」ボタンを必須にせず、用途に応じたカスタマイズが可能。

## 5. おまけ：アニメーションの追加

Svelteのin, out機能を使い、フェードイン・アウトを実装します。

以下のようにModal.svelteを変更します。`<script>`タグの先頭で、
Svelteの組み込みトランジションfadeをインポートしています。fadeは要素をフェードイン・フェードアウトさせるためのトランジション（要素が表示・非表示になるときに発生するアニメーション）です。

フェードイン・アウトの効果がわかるようにここでは、durationの値を大きめに設定しています。


```svelte:Modal.svelte
<svelte:options runes={true} />
<script>
  import { fade } from 'svelte/transition';
  let { show = false,children } = $props();

</script>

{#if show}
  <div class="modal-overlay" >
    <div class="modal-content" 
      in:fade={{ duration: 900 }} 
      out:fade={{ duration: 900 }} 
    >
      {@render children()}
    </div>
  </div>
{/if}

<style>
  ... 省略 ...
</style>
```

## 6. まとめ

ここで示したようにSvelteでUIコンポーネントを作成することはそれほど難しいことではありません。
Svelte独自の記法もありますが、THMLとJavaScriptの基本を理解しているなら、割とすんなりとこのコードを理解できるのではと思います。
興味にある方は、このコードをベースに、アラート、フォーム、確認ダイアログなどの機能を拡張してみてください！

ここで示したコードは、Svelte Playgroundで確認できます。

https://svelte.dev/playground/902be321e2ec4db295f5dcfeff9e3a77?version=5.25.2

