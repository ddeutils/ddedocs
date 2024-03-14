---
icon: material/language-rust
---

# Rust

**Rust** was created by [<u>Graydon Hoare</u>](https://github.com/graydon) in 2006,
who was working at [<u>Mozilla</u>](https://en.wikipedia.org/wiki/Mozilla) by the
time. It began as a personal project, driven by the desire to create
**a more secure and efficient language** for [<u>system-level programming</u>](https://en.wikipedia.org/wiki/Systems_programming).

In 2009, **Mozilla began sponsoring the project**. The goal was to create a language
that could power the next generation of **web applications** and **services**, particularly
in **performance-critical components of Firefox** and its layout engine,
[<u>**Servo**</u>](https://github.com/servo/servo/wiki/Servo-Layout-Engines-Report).

Rust drew inspiration from several existing languages. Its syntax has **similarities
to C++** but also incorporates features from languages like <u>**Erlang and Haskell**</u>,
especially in terms of its approach to **concurrency** and **memory safety**.

!!! quote "In general terms"

    **Rust** brings to the table a unique blend of features, **_primarily focusing
    on performance_**, in a similar way to **C++**, but with modern language features
    that **_make development safer_**.

## Safety

The key features that define safety in rust are:

- [Memory management (Ownership System)](#ownership---memory-management)
- [Borrowing and references](#borrowing-and-references)
- [Lifetimes](#lifetimes)
- [Error handling](#error-handling)

### Ownership - Memory management

_Ownership_ is a **set of rules that govern how a program manages memory**.
It refers to how different parts of the system’s memory are allocated and controlled.

Imagine having an assistant who periodically checks your desk, removing items
you’re done with so your workspace remains uncluttered and efficient.

All programs have to manage the way they use a computer’s memory while running.
Some languages have garbage collection that regularly looks for no longer-used
memory as the program runs; in other languages, the programmer must explicitly
allocate and free the memory.

**Ownership in Rust**:

Rust manages memory through a system of ownership with a set of rules that
the compiler checks. If any of the rules are violated, the program won’t
compile.

> **Ownership Rules**:
>
> - Each value in Rust has an _owner_.
> - There can only be one owner at a time.
> - When the owner goes out of scope, the value will be dropped.
>
> Read More: [:simple-medium: Rust Ownership - Explained for Beginners](https://medium.com/@vennilapugazhenthi/rust-ownership-explained-for-beginners-de70de16b099)

None of the features of ownership will slow down a Rust program while it’s
running.

This ensures that Rust programs not only benefit from enhanced memory safety
and efficiency but also maintain optimal runtime performance, as the ownership
model imposes no runtime overhead.

### Borrowing and References

Borrowing and references are fundamental concepts in Rust that work hand-in-hand
with the ownership system to ensure memory safety and data race protection
without the overhead of garbage collection.

### Lifetimes

### Error handling

## Speed

## Concurrency

## References

- [:simple-medium: Rust -- A New Titan in Data Science](https://medium.com/thedeephub/rust-a-new-titan-in-data-science-d449463078b2)
