[TOC]

[**document**](https://developer.mozilla.org/ja/docs/Web/JavaScript "**document**")

[**Domとjquery**](/blog-backend/blog-view/?id=58 "Domとjquery")

----
Javascript无块级作用域
Javascript采用函数作用域
Javascript作用域链  (由内向外找)
Javascript作用域在执行之前已经创建
声明提前

在预编译时函数内部变量就已经声明，都是undefined，调用时再赋值
- Exception
try,catch,finally, throw
----
## 関数
function(param1, param2,...rest){statements}

(function(){statements})()
アロー関数
(param1, param2...)=>{statements}
(param1, param2,...rest)=>{statements}

new Function(param1, param2,...)~~~~

#### function methods
Function.prototype.length
関数の引数の長さ
Function.prototype.name
関数名前
Function.prototype.arguments
関数に渡された引数に一致する配列です
```
(function(a,b){console.log(arguments[0])})(1,2)  # 1
```

#### call and apply
Function.prototype.call(this_obj, arg1, arg2...)
Function.prototype.apply(this_obj, [arg1, arg2])

## オブジェクトとプロトタイプ
new就是给this赋值，直接调用函数就是执行函数，new的时候函数内部创建了一个新的this，一边执行函数一边给this赋值。返回给变量的是this。
给this赋值方法，是this的方法。每次创建对象都会创建一次。


newはオブジェクトを作るキーワード、functionでオブジェクトを作る時にはfunction本体はオブジェクトのコンストラクタ関数としながら、functionのprototypeはオブジェクトをクリエイトする；クラスはコンストラクタはconstructor関数で指定する、クラスのprototypeは同様な役割でオブジェクトを作る
オブジェクトの\_\_proto\_\_はfunction.prototype同値、
function.\_\_proto\_\_⇔Object.prototype

functionにとってはFunctionで作ったオブジェクトである、Functionはfunctionのクラス、またはテンプレート、そしてFunctionはObjectで作ったオブジェクトである、そういうわけで
function.\_\_proto\_\_⇔Function.prototype
Function.prototype.\_\_proto\_\_⇔Object.prototype

クラスで定義する


Personクラス定義した時には一つインスタンスを定義した
```
function Person(name, age){
    this.name = name;
    this.age = age;
}

function Teacher(name, age, course) {
    // Person.call(this, name, age);
    Person.apply(this, [name, age]);
    this.course = course;
}

var t01 = new Teacher("tougou", 23, "language");
console.log(t01.constructor);
```

- Objectのプロパティ
クラスを継承本質はオブジェクトを継承する
Object.defineProperty(obj, property, attributes)
object.defineProperties(obj, {property01: value01, ...})
Object.deleteProperty(obj, property)
Object.getOwnPropertyDescriptors(obj, property)
Object.getOwnPropertyNames(obj, property)
Object.getPrototypeOf(obj) ==> obj.\_\_proto\_\_ ==> class.prototype
prototypeObj.isPrototypeof(obj) -> bool
Object.create(obj) -> new_obj

Object.assign(target, source)
ソースのプロパティをターゲットにペーストする、ソースはターゲット同じプロパティに覆う


## builtins

#### builtin 関数
- 整数と文字列転換
parseInt(other), parseFloat(other)

- encodeとdecode
encode: 文字列`你好，世界！`を`%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81`転換
decode: 文字列`%E4%BD%A0%E5%A5%BD%EF%BC%8C%E4%B8%96%E7%95%8C%EF%BC%81`を`你好，世界！`の転換
encodeURL(string), decodeURL(string)
encodeURLComponent, decodeURLComponent
`encodeURLComponent`は`encodeURL`より特殊文字を転換することが出来る、
例えば`ASCII字母、数字、~!@#$&*()=:/,;?+'`

setInteval(function, second)
setTimeout(function,second)
#### String

string.tolowercase()
string.touppercase()

- slice(substring):
string.subStr(start, length)
string.subString(start, stop)

- マッチ機能:
string.endswitch(string)->bool
string.startswitch(string)->bool
string.split

- 正規表現マッチ：
string.search(regex)->object
string.match(regex)->object
```
0: "sss"
groups: undefined
index: 0
input: "sss,ddd"
length: 1
# 0:<match_result>, 1:<group0>, 2:<group1>, index:<start_index>, input:<source_string>, length:<length>
```
string.replace(regex, value)->result_string
value: $1, $2, $... is regex group index


#### Arrayと配列類
- add item
array.pop(i)/array.push(i)/array.unshift(i)/array.shift(i)

- slice
array.slice(start, stop, step)

iterator
array.map(callback)->array, callback: function(i){}
array.filter(callback)->array, callback: function(i){}
array.foreach(callback), callback: function(i){}

##### map
```
d1 = new Map()
d1.set("name","alex")
d1.has("name")
d1.get("name")
d1.delete("name")
d1.size
```

##### set
```
s1 = new Set()
res: Set(0) {}
s2 = new Set([2,3,4])
res:Set(3) {2, 3, 4}

s1.add(3)
s1.delete(3)
s1.has(4)    //是否有项
res:true

s1.keys()
SetIterator {12, 15, 1}
s1.values()
SetIterator {12, 15, 1}
```


### 非同期
async function
传统异步解决方案：回掉函数+事件


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
});~~~~

console.log(promise1);
// expected output: [object Promise]
```
ajax异步控制
```
$.ajax({
    async:false,
});
```

### 正規表現
```
/pattern/flags
new RegExp(pattern, flags)
RegExp(pattern, flags)

/.../g   全局匹配
/.../i    不区分大小写
/.../m   多行匹配
```
`g`グローバルマッチ, `i`大文字と小文字を無視する, `m`複数行に渡るマッチ、`u`unicode文字のマッチを支持する
new RegExp(string) -> regexp
// -> regexp

regexp.test()
regexp.exec()

