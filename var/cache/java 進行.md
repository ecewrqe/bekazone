- version
  SE: standard edition
  EE: enterprise edition

java13 & java8

[java document](https://docs.oracle.com/en/java/javase/13/ "java document")

jshellコマンド
/var, /module, /list
/imports

type:
java.lang.Double
java.lang.Float
java.lang.String
java.lang.Integer
java.lang.Boolean
java.lang.Byte
java.lang.Enum
java.lang.Class

Integer.parseInt()
Float.parseFloat()
Object.toString()

Math: java.lang.Math
System: java.lang.System

System.out.print
System.in.read
- assert
1, `assert 条件: メッセージ`
2, `try{throw}catch(){}, throws`, class: `AssertionError`
```
try{
	if(size.length != 2){
		throw new AssertionError("may the size length is not equal 2");
	}else{
		throw new Exception("other exception");
	}
}catch (AssertionError e){
	System.out.println(e);
}
```
```
throw Exception => catch => function throws => catch => ... => catch => Main function throws
```

#### class and interface
subclass extend class
subclass implement interface
- class modifiers
public, private, protected, abstract, static, final, strictfp

#### import


#### Collection
Collection is a root interface
- Collection's method:
```
Boolean add(E e)
Boolean remove(E e)
void clear()
Boolean is_empty()
Boolean contain(Object o) : Returns true if this collection contains the specified element
Boolean equals(Object o)
int hash_code()
Iterator<E> iterator()
Spliterator<E> spliterator()
Object[] toArray()
Stream<E> stream()
```
- Vector's method
```

```
- deque's method
```
add: <head: addFirst(o), offerFirst(o), push(o), tail: addLast(o), offerLast(o)>
remove: <head: removeFirst(), pollFirst(), pop(), tail: removeLast(), pollLast()>
examine: <head: getFirst(), peekFirst(), peek(), tail: getLast(), peekLast()>
```



