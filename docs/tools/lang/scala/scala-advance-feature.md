# Scala Advance Feature

## Lazy Evaluation

```scala
class LazyEval {
    lazy val l = {
        println("lazy")
        9
    }
}

val x = new LazyEval;  // Does not print anything
println(y.l);
```

```text
lazy
9
```

- Method Lazy

```scala
def methodNormal(n: Int) {
    println("Normal");
    println(n);
}

def methodLazy(n: => Int) {
    println("Lazy");
    println(n);
}

val add = (a: Int, b: Int) => {
    print("Add");
    a + b;
}

methodNormal(add(5, 6));
methodLazy(add(5, 6));
```

```text
Add
Normal
11
Lazy
Add
11
```

## Multi-threading

```scala
class ThreadExample extends Thread {
    override def run() {
        for (i <- 0 to 3) {
            println(this.getName() + ":" + this.getPriority() + " - " + i);
            Thread.sleep(500);
        }
    }
}

var t1 = new ThreadExample();
var t2 = new ThreadExample();
var t3 = new ThreadExample();
t1.start();
t1.join();
t1.setName("First Thread:1");
t2.setName("Second Thread:10");
t1.setPriority(Thread.MIN_PRIORITY);
t2.setPriority(Thread.MAX_PRIORITY);
t1.start();
t2.start();
```

```text
0
1
2
3
First Thread:1 - 0
Second Thread:10 - 0
Second Thread:10 - 1
First Thread:1 - 1
Second Thread:10 - 2
First Thread:1 - 2
Second Thread:10 - 3
First Thread:1 - 3
```

- Thread Multitasking

```scala
class ThreadExample() extends Thread {
    override def run() {
        for (i <- 0 to 5) {
            println(i);
            Thread.sleep(500);
        }
    }
    def task() {
        for (i <- 0 to 5) {
            println(i);
            Thread.sleep(200);
        }
    }
}

var t1 = new ThreadExample();
t1.start();
t1.task();
```

```text
0
0
1
2
1
3
4
2
5
3
4
5
```
