# GO Basic Command Line

**Table of Content**:

- []()

## Installation and Setup

- Create `go.mod` file to your project

```shell
$ mkdir go-basic && cd go-basic
$ go mod init go-basic
```

- Create go file and `main` package

```go
package main

func main() {
    println("Hello World")
}
```

- Import format

```go
package main

import "fmt"

func main() {
    fmt.Printf("Hello %v\n", "World")
}
```

> **Warning**: \
> The GO is separate end of line with `;` and fix the `{}` syntax.

- Test run main package

```shell
go run main.go
```

## Declare in GO

`var` is mutable and `const` is immutable

```go
var x int  // declared but not used
```

```go
var x int
_ = x
```

```go
var x int = 10
print(x)
```

- Short declaration

```go
y := 10
```

> **Note**: \
> All variable in GO have default value, in GO it call **zero value**.

> **Note**: \
> When to use short declaration
>
> ```go
> package main
>
> var x int
>
> func main() {
>     y := 10
> }
> ```

## If Statement

```go
point := 50
if point >= 50 && point <= 100 {
    println("Pass")
} else if point >= 20 {
    println("Not Pass")
}
```

##For Loop

```go
values := []int{1, 2, 3, 4, 5}

for i := 0; i < len(values); i ++ {
    println(values[i])
}
```

```go
values := []int{10, 20, 30, 40}

for i, v := range values {
    println(i, v)
}
```

```text
0 10
1 20
2 30
3 40
```

> **Note**: \
> If you do not want to use index in for-each statement, you can use
>
> ```go
> for _, v := range values {
>     println(V)
> }
> ```

## While Loop

```go
values := []int{1, 2, 3, 4, 5}

i := 0
for i < len(values) {
    println(values[i])
    i++
}
```

## Array

```go
// array of int with size 3
var x [3]int = [3]int{1, 2, 3}

x := [3]int{1, 2, 3}

x := [...]int{1, 2, 3, 4}

// Create slice array
x := []int{1, 2, 3}
x = append(x, 4)
```

## Map

```go
var countries map[string]string

countries := map[string]string{}
countries["th"] = "Thailane"

country, ok := countries["jp"]
if !ok {
    println("No value")
    return
}
```

## Function

The scope of function is in `package`

```go
func main() {
    c, _ := add(10, 20)
    println(c)
}

func add(a, b int) (int, string) {
    return a + b, "Hello"
}
```

```go
x := func(a, b int) int {
    return a + b
}
value := x(10, 20)
println(value)
```

```go
func sum(a ...int) int {
    s := 0
    for _, v := range a {
        s += v
    }
    return s
}

s := sum(1, 2, 3, 4, 5)
println(s)
```

## High-order Function

```go
func cal(f func(int,int)int) {
    sumn := f(50, 10)
    println(sum)
}

cal(func(a, b int) int {
    return a + b
})
```

## Package

```text
project
    |-- customer
    |   |- customer.go
    |- go.mod
    |- main.go
```

```go
// customer.go
package customer

var Name = "Customer"
```

```go
// main.go
import "project/customer"

func main() {
    println(customer.Name)
}
```

> **Warning**: \
> In GO, if you want to export anything from another package, you should use pascal case like,
> `func Sum()` or `var Name = `

## Pointer

```go
var x, y int
x = 10
y = x

// return pointer in memory
println(&x)
println(&y)
```

```text
0xc0000140e0
0xc0000ae010
```

```go
var x int
x = 10

var y *int
y = &x

// return pointer in memory
println(&x)
println(y)
```

```text
0xc000122008
0xc000122008
```

> **Note**: \
> If you want to use value of pointer `y`, you can use `println(*y)`.

## Struct

Struct is a class without method in GO. Attribute in GO say with behavior.

```go
type Person struct {
    Name string
    Age int
}

func main() {
    x := Person{"Tom", 18}
    y := Person{Name: "Tom", Age: 18}
    z := Person{
        Name: "Tom",
        Age: 18,
    }

    println(x.Name)
    println(y.Age)
}
```

- Create Extension Method

```go
func Hello(p Person) string {
    return "Hello " + p.Name
}

println(Hello(x))
```

```go
func (p Person) Hello() string {
    return "Hello " + p.Name
}

println(Hello(x))
println(x.Hello())
```

- Create OOP in Struct

```go
package customer

type Person struct {
    name string
    age int
}

func (p Person) GetName() string {
    return p.name
}

func (p *Person) SetName() string {
    p.name = name
}

func (p Person) GetAge() int {
    return p.age
}
```

```go
x := customer.Person{}
x.SetName("Tom")
println(x.GetName())
```

```text
Tom
```

## References

- https://www.youtube.com/watch?v=JbIS97exQnQ
- https://github.com/avelino/awesome-go
