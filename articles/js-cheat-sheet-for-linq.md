---
title: "C#プログラマーのためのJavaScriptチートシート(LINQ編)"
emoji: "✍️"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "JavaScript"]
published: true
published_at: 2024-12-09 20:45
publication_name: "zead"
---

## はじめに

以下の記事の続編です。

https://zenn.dev/zead/articles/js-cheat-sheet-for-cs

この記事では、C#プログラマーのためがJavaScriptでコレクション操作をする時に、どう書いたら良いのかをまとめています。
JavaScriptでLINQのような操作ができるライブラリには、Linq.js, ix.js, remeda, lodashなどがありますが、ここではこれらのライブラリを使わずに、JavaScriptのネイティブ機能だけを使った方法を示します。



## 概要

C#（LINQ） | JavaScript | 説明
----|------|-----------
`Where(predicate)` | `filter(predicate)`|条件に一致する要素をフィルタリング
`First/FirstOrDefault(predicate)` | `find(predicate)` | 条件に一致する最初の要素を取得
`Last/LastOrDefault(predicate)` | `reverse().find(predicate)` | 条件に一致する最初の要素を取得
`Skip(count)`	 | `slice(count)`	| 最初の指定された数の要素をスキップ
`Take(count)`	 | `slice(count)`	| 最初の指定された数の要素を取得
`Any(predicate)` | `some(predicate)` |条件に一致する要素が1つでも存在するか
`All(predicate)` | `every(predicate)` | 全ての要素が条件を満たすか
`Select(selector)` | `map(selector)` | 各要素を変換
`OrderBy(keySelector)` | `sort((a, b) => keySelector(a) - keySelector(b))` | 昇順で並べ替え
`OrderByDescending(keySelector)` | `sort((a, b) => keySelector(b) - keySelector(a))` | 降順で並べ替え
`Count()` | `array.length` | 要素の数を取得
`Sum(selector)` | `reduce((sum, x) => sum + x, 0)` | 要素の合計を計算
`Average(selector)` | `reduce((sum, x) => sum + x, 0) / array.length`|要素の平均を計算
`Aggregate(func)` | `reduce(func)` |集計操作を実行
`GroupBy(keySelector)` | `reduce((map, x) => { let key = keySelector(x); (map[key] = map[key]` | グループ化
`Concat(sequence)` | `concat(sequence)`	| 2つの配列を連結
`SelectMany(selector)` | `flatMap(selector)`	| ネストされた配列を平坦化して変換

## クエリの例

以下、良く利用すると思われるコードをC#とJavaScriptで示します。

### フィルタリング: Where → filter

#### C#
```cs
var evenNumbers = numbers.Where(n => n % 2 == 0);
```

#### JavaScript

```js
const evenNumbers = numbers.filter(n => n % 2 === 0);
```

### 変換: Select → map

#### C#
```cs
var squares = numbers.Select(n => n * n);
```
#### JavaScript

```js
const squares = numbers.map(n => n * n);
```

### 検索: First, FirstOrDefault → find

#### C#
```cs
var firstEven = numbers.First(n => n % 2 == 0);
```

#### JavaScript

```js
const firstEven = numbers.find(n => n % 2 === 0);
```

findメソッドは、テスト関数を満たす値がない場合は、 undefined を返します。そのため、FirstOrDefault相当のコードは以下のようになります。


```js
const firstOrDefault = numbers.find(n => n > 10) || 0; // デフォルト値: 0
```

### スキップと取得: Skip, Take → slice

#### C#
```cs
var skipTwo = numbers.Skip(2);
var takeTwo = numbers.Take(2);
```

#### JavaScript

```js
const skipTwo = numbers.slice(2); // 2つスキップ
const takeTwo = numbers.slice(0, 2); // 最初の2つ取得
```

### 条件チェック: Any, All → some, every

#### C#

```cs
bool hasEven = numbers.Any(n => n % 2 == 0);
bool allPositive = numbers.All(n => n > 0);
```

#### JavaScript

```js
const hasEven = numbers.some(n => n % 2 === 0); // 1つでも条件を満たすか
const allPositive = numbers.every(n => n > 0); // 全ての要素が条件を満たすか
```

### 並べ替え: OrderBy, OrderByDescending → sort

#### C#
```cs
var sorted = numbers.OrderBy(n => n);
var descending = numbers.OrderByDescending(n => n);
```
#### JavaScript

```js
const sorted = numbers.slice().sort((a, b) => a - b); // 昇順
const descending = numbers.slice().sort((a, b) => b - a); // 降順
```

注意: sortは破壊的メソッドなので、コピー（slice()）を作成するのが安全です。


### 集約: Aggregate → reduce

#### C#

```cs
var sum = numbers.Aggregate((acc, n) => acc + n);
```

#### JavaScript

```js
const sum = numbers.reduce((acc, n) => acc + n, 0);
```

### グループ化: GroupBy → reduce

JavaScriptにはGroupByに相当する標準メソッドがないため、reduceを使って実装します。

#### C#

```cs
var grouped = numbers.GroupBy(n => n % 2 == 0 ? "Even" : "Odd");
```
#### JavaScript

```js
const numbers = [ 1,2,3,4,5,6,7,8,9,10 ];
const grouped = numbers.reduce((acc, n) => {
    const key = n % 2 === 0 ? "Even" : "Odd";
    if (!acc[key]) acc[key] = [];
    acc[key].push(n);
    return acc;
}, {});

console.log(grouped['Even']);
console.log(grouped['Odd']);
```

**結果:**
```
2,4,6,8,10
1,3,5,7,9
```

### 平坦化: SelectMany → flatMap

#### C#

```cs
var numbers = new List<List<int>>
{
    new List<int> { 1, 2, 3 },
    new List<int> { 4, 5, 6 }
};
var results = numbers.SelectMany(n => n);
Console.WriteLine(string.Join(", ", results));
```

#### JavaScript

```js
const numbers = [
  [ 1,2,3 ],
  [ 4,5,6]
];
const results = numbers.flatMap(n => n);
console.log(results);
```

**結果**

```
1,2,3,4,5,6
```

#### C#

```cs
var people = new List<Person>
{
    new Person { Name = "Alice", Hobbies = new List<string> { "reading", "traveling" } },
    new Person { Name = "Bob", Hobbies = new List<string> { "cycling", "trekking" } }
};
var hobbies = people.SelectMany(person => person.Hobbies);
Console.WriteLine(string.Join(", ", hobbies));
```

#### JavaScript

```js
const people = [
  { name: "Alice", hobbies: ["reading", "traveling"] },
  { name: "Bob", hobbies: ["cycling", "trekking"] },
];
const hobbies = people.flatMap(person => person.hobbies);
console.log(hobbies);
```

**結果**

```
reading,traveling,cycling,trekking
```

### メソッドチェーンの例


#### C#
```cs
var results = people.Where(p => p.Age > 25)
                    .Select(p => new { p.Name, p.Age })
                    .OrderBy(p => p.Name);
```

#### JavaScript

```js
const people = [ 
  { name: 'alice', age: 28 },
  { name: 'Bob', age: 25 },
  { name: 'Charlie', age: 30 },
  { name: 'Diana', age: 22 }];
const results = people
  .filter(p => p.age > 25)             // フィルタリング
  .map(p => ({ name: p.name, age: p.age }))    // 変換
  .sort((a, b) => a.name.localeCompare(b.name)); // 並べ替え
for (const p of results ) {
  console.log(p.name, p.age);
}
```

localeCompareは言語を考慮した比較を行います。

**結果**
```
alice 28
Charlie 30
```



## 最後に

JavaScriptのネイティブな機能だけでも、それなりにLINQと同じようなことが可能だとわかりました。しかし、どうしてもC#のLINQと比べると見劣りしてしまいます。

LINQに慣れたプログラマーの場合は、ix.jsなどのライブラリの利用も検討したほうが良いかもしれません。

#### ix.js
https://reactivex.io/IxJS/

#### Linq.js
http://linqjs.codeplex.com/

#### remeda
https://remedajs.com

#### lodash
https://lodash.com
