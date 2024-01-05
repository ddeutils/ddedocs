---
icon: simple/scala
---

# Scala

https://medium.com/odds-team

## Installation

We should to install 2 components for running scalar on local:

1) [Java JDK](https://www.oracle.com/java/technologies/downloads/)
2) [Scalar](https://www.scala-lang.org/download/)

```text
project-directory
|
|---> build.sbt
|---> MyMain.scalar
```

```shell
sbt run
```

## Main Object

```scala
object MainObject {
    def main(args: Array[String]) = {
        ...
    }
}
```
