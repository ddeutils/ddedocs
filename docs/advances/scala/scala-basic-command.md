# Scalar Basic Command Line

**Table of Contents**:

- [While Loop]()
- [For Loop]()
- [Pattern Matching]()
- [Break]()
- [Function]()
- [Higher-Order Function]()
- [String]()
- [Option]()
- [Exception]()

## While Loop

- Method 01: Common while loop

```scala
var x = 0;
while (x < 10) {
    println("x = " + x );
    x += 1;
}
```

- Method 02: Switch while loop to the end of doing (do-while)

```scala
var x = 0;
do {
    println("x = " + x );
    x += 1;
} while (x < 10);
```

## For Loop

```scala
for (i <- 1 to 5) {
    println("i using to " + i);
}
```

> **Note**: \
> We can use `1.to(5)`, `1 until 6`, or `1.until(6)` for represent range of number from 1 to 5.\
> Optional, if you want to step this range, you can use `by` like `for(i<-1 to 10 by 2)`.

- Loop

```scala
for (i <- 1 to 9; j <- 1 to 3) {
    println("i using until " + i + " " + j);
}
```

```text
i using until 1 1
i using until 1 2
i using until 1 3
i using until 2 1
...
```

- Using `List`

```scala
val lst = List(1, 2, 3, 78, 9);';
for (i <- lst; if i < 6) {
    println("i using Filters " + i);
}
```

```scala
lst.foreach(print)
// 123789
```

```scala
lst.foreach((element:Int) => print(element + " "))
// 1 2 3 78 9
```

- Pass for loop into val

```scala
val result = for {i <- lst; if i < 6} yield {
    i * i
}
println("result = " + result);
```

```text
result = List(1, 4, 9)
```

## Break

```scala
import scala.util.control.Breaks._

// Breakable method to avoid exception
breakable {
    for (i <- 1 to 10 by 2) {
        if (i == 7)
            break
        else
            println("i using to " + i)
    }
}
```

## Pattern Matching

```scala
def search(a: Any): Any = a match {
    case 1  => println("One");
    case "Two" => println("Two");
    case "Hello" => println("Hello");
    case _ => println("No");
}
```

```scala
val i = 7;
i match {
    case 1 | 3 | 5 | 7 | 9 => println("odd");
    case 2 | 4 | 6 | 8 => println("even");
}
```

## Function

```scala
def add(x: Int, y: Int): Int = {
    return x + y;
}
```

```scala
def subtract(x: Int, y: Int): Int = {
    x - y;
}
```

```scala
def multiply(x: Int, y: Int): Int = x * y;
```

```scala
def devide(x: Int, y: Int) = x / y;
```

> **Note**: \
> You can ignore to write `return` in last line of function body that will auto
> use the last line to return.

```scala
object Math {
    def square(x: Int) = x * x;
}

// Use method function of object with space seperator
println(Math square 3);
```

- Recursion Function

```scala
// We can set default value to `y` parameter
def plusRecursion(x: Int, y: Int = 40): Int = {
    if (y == 0)
        0
    else
        x + plusRecursion(x, y - 1)
}
```

## Higher-Order Function

- Passing a Function as Parameter

```scala
def math(x: Double, y: Double, f: (Double, Double) => Double): Double = f(x, y);
```

```scala
val result = math(50, 20, (x, y) => x max y);
```

```scala
def math(x: Double, y: Double, z: Double, f: (Double, Double) => Double): Double = f(f(x, y), z);
```

```scala
val result = math(50, 20, 10, (x, y) => x + y);
```

> **Note**: \
> You can use wild-card like `math(50, 20, 10, _ + _);`

- Function Composition

```scala
def addTwo(x: Int): Int = x + 2;
def multiplyTwo(x: Int): Int = x * 2;
```

```scala
val result = multiplyTwo(addTwo(10));
```

- Anonymous (lambda) Function

```scala
// Anonymous function by using => (rocket)
val result = (x: Int, y: Int) => x + y;
```

```scala
// Anonymous function by using _ (underscore) wild-card
val result = (_: Int) + (_: Int)
```

- Multiline Expression

```scala
def add(x: Int, y: Int) = {
    x +
    y
}
```

```scala
def add(x: Int, y: Int) = {
    (x
    + y)
}
```

- Partially Applied Function

```scala
val sum(x: Int, y: Int, z: Int) => x + y + z;
```

```scala
val f = sum(10, 20, _: Int);
val result = f(200);
```

- Closures

```scala
var number = 10;
val add = (x: Int) => x + number;

def main(args: Array[String]) {
    number = 100;
    println(add(20)); // stdout will show 120
}
```

```scala
val add = (x: Int) => {
    number = x + number;
    number;
}

def main(args: Array[String]) {
    number = 100;
    println(add(20)); // stdout will show 120
    println(number); // stdout will show 120
}
```

- Function Currying

```scala
def add(x: Int)(y: Int) = {
    x + y;
}
```

```scala
val result = add(10)(10);
```

```scala
val add40 = add(40)_;
val result = add40(100);
```

> **Note**: \
> You can write with oneline like `def add (x: Int) = (y: Int) => x + y;`, and
> Change to use with `val add20 = add(20)`

- Nested Function

```scala
def add(x: Int, y: Int, z: Int) = {
    def addTwo(a: Int, b: Int) = {
        a + b;
    }
    addTwo(x, addTwo(y, z));
}
```

- Function with Variable Length Parameters

```scala
def addAll(args: Int*) = {
    var sum = 0;
    for (a <- args) sum += a;
    sum;
```

```scala
val result = addAll(1, 2, 3, 4, 5);
```

## String

```scala
val str1: String = "Hello World";
val str2: String = " Max";
```

```scala
str1.length();  // 11
str1.concat(str2);  // Hello World Max
str1 + str2;  // Hello World Max
str1.equals(str2);  // false
str1.compareTo(str2);  // -7
str1.substring(0, 5);  // Hello
```

- String Interpolation

```scala
var s1 = "Scala string example";
var version = 2.12;

println(f"This is $s1%s, scala version is $version%2.2f");  // This is Scala string example, scala version is 2.12
```

## Option

```scala
val lst = List(1, 2, 3);
val map = Map(1 -> "Tom", 2 -> "Sara");
val opt: Option[Int] = None;
```

```scala
lst.find(_ > 3);  // None
lst.find(_ > 2);  // Some(3)
map.get(1);  // Some(Tom)
map.get(3);  // None
```

```scala
lst.find(_ > 2).get;  // 3
map.get(1).get;  // Tom
map.get(3).getOrElse("No name found");  // No name found
```

## Exception

- Try Catch

```scala
class ExceptionExample {
    def divide(a: Int, b: Int) = {
        try {
            a / b;
            var arr = Array(1,2);
            arr(10);
        } catch {
            case e: ArithmeticException => println(e)
            case ex: Throwable => println("found a unknown exception: " + ex)
        } finally {
            println("Finally block always executes")
        }
        println("Rest of the code is executing...");
    }
}

var e = new ExceptionExample();
e.divide(100, 0);
e.divide(100,10)
```

```text
java.lang.ArithmeticException: / by zero
Finally block always executes
Rest of the code is executing...
found a unknown exception: java.lang.ArrayIndexOutOfBoundsException: 10
Finally block always executes
Rest of the code is executing...
```

- Throw keyword

```scala
class ExceptionExample {
    def validate(age: Int) = {
        if (age < 18)
            throw new ArithmeticException("You are not eligible")
        else println("You are eligible")
    }
}

var e = new ExceptionExample();
e.validate(10);
```

```text
java.lang.ArithmeticException: You are not eligible
```
