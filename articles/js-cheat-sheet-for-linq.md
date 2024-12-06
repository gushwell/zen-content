---
title: "C#プログラマーのためのJavaScriptチートシート(LINQ編)"
emoji: "✍️"
type: "tech" # tech: 技術記事 / idea: アイデア
topics:  ["csharp", "JavaScript"]
published: true
published_at: 2024-12-12 20:45
publication_name: zead
---

以下の記事の続編で、「#プログラマーのためのJavaScriptチートシート(LINQ編)」です。

https://zenn.dev/zead/articles/js-cheat-sheet-for-cs

## 概要

処理 | C#（LINQ） | JavaScript
----|------|-----------
フィルタリング | Where | filter
変換 | Select | map
検索 | First, FirstOrDefault | find, findIndex
スキップ/取得 | Skip, Take | slice
条件チェック | Any, All | some, every
並べ替え | OrderBy, OrderByDescending | sort
集約 | Aggregate | reduce

## フィルタリング: Where → filter

#### C#
```cs
var evenNumbers = numbers.Where(n => n % 2 == 0);
```

#### JavaScript

```js
let evenNumbers = numbers.filter(n => n % 2 === 0);
```

## 変換: Select → map
#### C#
```cs
var squares = numbers.Select(n => n * n);
```
#### JavaScript

```js
let squares = numbers.map(n => n * n);
```

## 検索: First, FirstOrDefault → find

#### C#
```cs
var firstEven = numbers.First(n => n % 2 == 0);
```

#### JavaScript

```js
let firstEven = numbers.find(n => n % 2 === 0);
```
FirstOrDefault相当:

```js
let firstOrDefault = numbers.find(n => n > 10) || 0; // デフォルト値: 0
```

## スキップと取得: Skip, Take → slice

#### C#
```cs
var skipTwo = numbers.Skip(2);
var takeTwo = numbers.Take(2);
```

#### JavaScript

```js
let skipTwo = numbers.slice(2); // 2つスキップ
let takeTwo = numbers.slice(0, 2); // 最初の2つ取得
```

## 条件チェック: Any, All → some, every

#### C#

```cs
bool hasEven = numbers.Any(n => n % 2 == 0);
bool allPositive = numbers.All(n => n > 0);
```

#### JavaScript

```js
let hasEven = numbers.some(n => n % 2 === 0); // 1つでも条件を満たすか
let allPositive = numbers.every(n => n > 0); // 全ての要素が条件を満たすか
```

## 並べ替え: OrderBy, OrderByDescending → sort

#### C#
```cs
var sorted = numbers.OrderBy(n => n);
var descending = numbers.OrderByDescending(n => n);
```
#### JavaScript

```js
let sorted = numbers.slice().sort((a, b) => a - b); // 昇順
let descending = numbers.slice().sort((a, b) => b - a); // 降順
```

注意: sortは破壊的メソッドなので、コピー（slice()）を作成するのが安全です。


## 集約: Aggregate → reduce

#### C#

```cs
var sum = numbers.Aggregate((acc, n) => acc + n);
```

#### JavaScript

```js
let sum = numbers.reduce((acc, n) => acc + n, 0);
```

## グループ化: GroupBy

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


## 複雑なクエリ例


#### C#
```cs
var results = people.Where(p => p.Age > 25)
                    .OrderBy(p => p.Name)
                    .Select(p => new { p.Name, p.Age });
```

#### JavaScript

```js
let results = people
  .filter(p => p.age > 25)             // フィルタリング
  .sort((a, b) => a.name.localeCompare(b.name)) // 並べ替え
  .map(p => ({ name: p.name, age: p.age }));    // 変換
```

localeCompareは言語を考慮した比較を行う。
