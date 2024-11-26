---
title: "C#プログラマーのためのJavaScriptチートシート"
emoji: "✍️"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "javascript"]
published: true
published_at: 2024-11-21 21:00
publication_name: zead
---

タイトルの通り、C#プログラマーのためのJavaScriptチートシートです。

C#に慣れているプログラマーがJavaScriptの書き方を効率的に学べるように、2つの言語の書き方をまとめています。LINQ編は別記事で公開します。

## 基本構文

概要 | C# | JavaScript
----|------|-----------
変数宣言 | `int x = 10;` | `let x = 10;`<br>`const y = 20;`
条件分岐 | `if (x > 0) { … }` | `if (x > 0) { … }`
for | `for (int i = 0; i < 10; i++) { … }` | `for (let i = 0; i < 10; i++) { … }`
while | `while (n < 10) { … }` | `while (n < 10) { … }`
等値判定 | `a == b` | `a === b`
不一致判定 | `a != b` | `a !== b`

C#ではローカル変数にreadonlyは使えない。
JavaScript の場合 `a == b`, `a != b`は自動型変換をしてくれる。

## 型と型システム

JavaScriptは動的型付け言語で、型を明示的に宣言しない。
一方、C#は静的型付けで型を厳密に管理する。（varを使っても型が管理される）

C# | JavaScript
----|---------------
`int x = 10;` | `let x = 10;`
`string name = "Hello";` | `let name = "Hello";`
`bool isTrue = true;` | `let isTrue = true;`

JavaScriptの特殊な値：

- undefined: 変数が未定義。
- null: 値が存在しない。
- NaN: 数値として不正な値。

### 型の判定

型 | C# | JavaScript
----|------|-----------
文字列 | `value is string` | `typeof value === "string"`
数値 | `value is int` | `typeof value === "number" && !isNaN(value)`
真偽値 | `value is bool` | `typeof value === "boolean"`
日時 | `value is DateTime` | `value instanceof Date`
配列 | `value is Array` | `value instanceof Array`
null | `value is null` | `value === null`

JavaScriptの数値には、整数、実数の区別がない。
isで統一されているC#は便利。

## 関数

#### C#

```cs
int Add(int x, int y) {	
  return x + y;	
}
```

#### JavaScript

```js
function add(x, y) {
  return x + y;
}
```

## ラムダ式/アロー式

#### C#

```cs
var triple = (int n) => n * 3;
var result = triple(5);
```

#### JavaScript

```js
const triple = (n) => n * 3;
const result = triple(5);
```

## 文字列操作

ほぼほぼ同じ感覚で使える。

内容 | C# | JavaScript
----|------|-----------
文字列の連結 | `str1 + str2` | `str1 + str2`
部分文字列の取得 | `str.Substring(startIndex, length)` | `str.substring(startIndex, endIndex)`
文字列の長さ取得 | `str.Length` | `str.length`
文字列の検索 | `str.IndexOf("searchString")` | `str.indexOf('searchString')`
文字列の置換 | `str.Replace("old", "new")` | `str.replace('old', 'new')`
文字列の分割 | `str.Split('delimiter')` | `str.split('delimiter')`
大文字に変換 | `str.ToUpper()` | `str.toUpperCase()`
小文字に変換 | `str.ToLower()` | `str.toLowerCase()`
空白の削除 | `str.Trim()` | `str.trim()`
先頭空白の削除 | `str.TrimStart()` | `str.trimStart()`
末尾空白の削除 | `str.TrimEnd()` | `str.trimEnd()`
特定文字列で始まるか? | `str.StartsWith("prefix")` | `str.startsWith('prefix')`
特定文字列で終わるか? | `str.EndsWith("suffix")` | `str.endsWith('suffix')`
特定文字列を含むか? | `str.Contains("substring")` | `str.includes('substring')`
文字列の挿入 | `str.Insert(index, "newText")` | `str.slice(0, index) + 'newText' + str.slice(index)`
文字列が空か? | `string.IsNullOrEmpty(str)` | `!str === \|\| str === ''`
文字列が空または空白か? | `string.IsNullOrWhiteSpace(str)` | `!str \|\| str.trim() === ''`

## 数値に関わる操作

内容 | `C#` | `JavaScript`
----|------|-----------
文字列を数値に変換 | `int.Parse("123")` <br> `double.Parse("123.45")` | `parseInt("123")` <br> `parseFloat("123.45")`
数値を文字列に変換 | `num.ToString()` | `num.toString()`
四捨五入 | `Math.Round(num)` | `Math.round(num)`
切り上げ | `Math.Ceiling(num)` | `Math.ceil(num)`
切り捨て | `Math.Floor(num)` | `Math.floor(num)`
絶対値 | `Math.Abs(num)` | `Math.abs(num)`
平方根 | `Math.Sqrt(num)` | `Math.sqrt(num)`
累乗 | `Math.Pow(base, exponent)` | `Math.pow(base, exponent) または base ** exponent`
最大値を取得 | `Math.Max(val1, val2, ...)` | `Math.max(val1, val2, ...)`
最小値を取得 | `Math.Min(val1, val2, ...)` | `Math.min(val1, val2, ...)`
数値を丸めて小数点以下を制限 | `Math.Round(num, decimals)` | `num.toFixed(decimals)`
整数部分を取得 | `Math.Truncate(num)` | `Math.trunc(num)`
符号を取得（正:1, 負:-1, 0:0） | `Math.Sign(num)` | `Math.sign(num)`
無限大か確認 | `double.IsInfinity(num)` | `num === Infinity または num === -Infinity`
NaNか確認 | `double.IsNaN(num)` | `isNaN(num) または Number.isNaN(num)`
型変換（int ↔ double） | `(int)num` <br> `(double)num` | `Number(num)`
乱数生成（0以上1未満） | `new Random().NextDouble()` | `Math.random()`
範囲指定の乱数生成 | `new Random().Next(min, max)` | `Math.floor(Math.random() * (max - min) + min)`


## コレクション

JavaScriptは、配列/リストの区別はない。

説明 | C# | JavaScript
----|-----|----------
初期化 | `int[] numbers = [ 1, 2, 3 ];`    | `let numbers = [1, 2, 3];`
List宣言 | `var list = new List<int>();`    | `let list = [];`
要素取得 | `var n = numbers[1];`  | `let n = numbers[1];`
末尾追加 | `list.Add(4);`  | `list.push(4);`
末尾削除 | `list.RemoveAt(list.Count - 1);`  | `list.pop();`
先頭挿入 | `list.Insert(0, value);` | `list.unshift(value);`
先頭削除 | `list.RemoveAt(0);` | `list.shift();`
指定位置削除 | `list.RemoveAt(2);` | `list.splice(2, 1);`
コレクション追加 | `list.GetRange(start, count)` |	`arr.slice(start, end)`
部分コレクション取得 | `foreach(var x in list) { … }` | `for (let x of list) { … }`
全要素操作 | `foreach(var x in list) { … }` | `for (let x of list) { … }`
全要素操作 | `list.ForEach(x => { … });` | `list.forEach(x => { … });`
検索 | `var n = list.Find(x => x == value);` | `const n = list.find(x => x === value);`
空にする | `list.Clear();` | `arr.length = 0;`

## 匿名クラス/オブジェクト

#### C#

```cs
var person = new { Name = "Alice", Age = 25 };
```

#### JavaScript

```js
let person = { name: "Alice", age: 25 };
```

## クラスとオブジェクト

#### C#

```cs
class Person {
  public string Name { get; set; } = "";
  public int Age { get; set; } = -1;
  public Person(string name, int age) {
    Name = name;
    Age = age;
  }
  public void Print() {
    Console.WriteLine($"{Name}({Age}歳)");
  }
}
```

#### JavaScript

```js
class Person {
  name = '';
  age = -1;
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
  print() {
    console.log(`${name}(${age}歳)`);
  }
}
```

JavScriptでは、name, ageをプロパティとして実装したいなら厳密には以下のようなコードになる。

```js
class Person {
  #name = '';
  #age = -1;
  constructor(name, age) {
    this.#name = name;
    this.#age = age;
  }
  get name(){ return this.#name }
  set name(str) { this.#name = str }
  get age() { return this.#age }
  set age(num) {this.#age = num }
  print() {
    console.log(`${this.#name}(${this.#age}歳)`);
  }
}
```

上記getter/setterのコードは[いぬいぬさんのコメント](https://zenn.dev/link/comments/fc0d2ad91b942d)より追記

Personクラスの使い方はpublicフィールドと同じ

```js
let p = new Person('Alice', 18);
console.log(p.name); 
console.log(p.age); 
```


JavaScriptのそれ以外のクラスの要素

```js
class MyClass {
  // 静的フィールド
  static myStaticField = "bar";
  // 静的メソッド
  static myStaticMethod() {
    // 静的メンバーのアクセスにはクラス名が必要
    console.log(MyClass.myStaticField);
  }
  // 静的ブロック
  static {
    // 静的初期化コード
  }
  // プライベートフィールド
  #myPrivateField = "baz";
  // メソッド、静的フィールド、静的メソッドも #で「プライベート」形式になる
}
```


## 例外処理

#### C#

```cs
throw new Exception("Parameter is not a number!");
```

#### JavaScript

```js
throw new Error('Parameter is not a number!');
```

#### C#

```cs
try {
  int result = 10 / 0;
} catch (Exception ex) {
  Console.WriteLine(ex.Message);
}
```

#### JavaScript

```js
try {
  let result = 10 / 0;
} catch (error) {
  console.log(error.message);
}
```

## 非同期処理


#### C#

```cs
Console.WriteLine("start");
var msg = await EchoAsync("hello");
Console.WriteLine(msg);

// 2秒後にmsgを返す
async Task<string> EchoAsync(string msg) {
  await Task.Delay(2000);
  return msg;
}
```

#### JavaScript

```js
async function main() {
  console.log('start');
  const msg = await echo('hello');
  console.log(msg);
}

// 2秒後にmsgを返す
async function echo(msg) {
  // Promiseの使い方を示すためにあえてこのコードにしている。
  return new Promise(async resolve => {
    await delay(2000);
    resolve(msg);
  });
}

async function delay(n) {
  await new Promise(r => setTimeout(r, n));
} 
```

上記 echoは、本来なら以下のコードで良い。

```js
async function echo(msg) {
  await delay(2000);
  return msg;
}
```



