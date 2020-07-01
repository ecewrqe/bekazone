# javascript詳細解説
[TOC]

### 配列
#### mapとfilter
反復メソット使い方
``` javascript
arr.map(calback);
arr.map((currentValue, currentIntex, object_array)=>{})->arr
arr.filter(callback);
arr.filter(callback: (currentValue, currentIntex, object_array)=>{})->arr
arr.every(callback: (currentValue, currentIntex, object_array)=>{})->arr
arr.reduce(calback: (accumulator, currentvalue2, currentIndex1, object_array))->arr
arr.foreach(callback: (currentValue))

```
mapは一つcallback引数を使って、callbackではこの配列の各要素の値、インデックスとオブジェクトとしての三つの引数を伴って呼び出される
callbackは配列の順番通り、各要素に対して一度呼び出し、そして新しい配列作り出す
``` javascript
var arr1 = [1,4,5,10];
var arr10 = arr1.map((num, index) => num + index); // [ 1, 5, 7, 13 ]
```

filter処理した結果は下
``` javascript
var arr1 = [1,4,5,10];
var arr10 = arr1.filter((num) => num > 5) // [10]
```

reduce/reduceRight
引数は前回返り値と今の値

everyすべての値はcallbackの条件と相応しければtrue、反則false

#### foreach
``` javascript
var arr1 = [1,4,5,10];
arr1.forEach(function (num) {
    console.log(num);
    return num;
});
```

### 関数
javascriptにおけるすべての関数は実際はFunctionオブジェクト
#### Functionオブジェクト
``` javascript
var sum = new Function("a", "b", "return a + b");
console.log(sum(1, 2)); // 3
```
構文
```
new Function(arg1,arg2,...,function_body)
```
#### Functionのメソッド
Function.prototype.arguments
関数に渡された引数に一致する配列です、
``` javascript
var func = new Function("name", "...arg", "return arguments");
console.log(func("車", 1, 2, 3, 4));
// { '0': '車', '1': 1, '2': 2, '3': 3, '4': 4 }
```
Function.prototype.length
期待された関数の引数の長さ
``` javascript
var func = new Function("name", "email", "...arg", "return arguments");
console.log(func.length);  // 2
```
Function.prototype.name
```
console.log(func.name);  // anonymous(匿名)
function func2(){}
console.log(func.name); // func2
```

call, apply, bind
### 非同期
async function



非同期処理の最終的な完了処理

``` javascript
var promise1 = new Promise(function(resolve, reject) {
  setTimeout(function() {
    resolve('foo');
  }, 300);
});

promise1.then(function(value) {
  console.log(value);
  // expected output: "foo"
});

console.log(promise1);
// expected output: [object Promise]
```

### 正規表現
```
/pattern/flags
new RegExp(pattern, flags)
RegExp(pattern, flags)
```
`g`グローバルマッチ, `i`大文字と小文字を無視する, `m`複数行に渡るマッチ、`u`unicode文字のマッチを支持する
``` javascript
String.match(reg)
```


### プロトタイプ

### window.Storage
```
var localStorage =window.localStorage;
```