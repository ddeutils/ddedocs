# Dependencies Wheel

**Table of Contents**:

- [What Is a Python Wheel?](#what-is-a-python-wheel)

## Use-case: Deploy to On-premise

This will use when you want to compress all dependencies from internet-able machine
to non-internet-able machine

- Pack the dependencies to `.whl` files to wheels folder

  ```shell
  pip wheel -w wheels -r requirements.txt
  ```

- Install `.whl` files in wheel folder

  ```shell
  pip install --no-index --find-links=wheels/ -r requirements.txt
  ```

## What Is a Python Wheel?

A Python `.whl` file is essentially a ZIP (`.zip`) archive with a specially crafted
filename that tells installers what Python versions and platforms the wheel will
support.

A wheel is a type of [**built distribution**](https://packaging.python.org/en/latest/glossary/#term-built-distribution).
In this case, built means that the wheel comes in a ready-to-install format and
allows you to skip the build stage required with source distributions.

> **Note**: \
> It’s worth mentioning that despite the use of the term built, a wheel doesn't
> contain `.pyc` files, or compiled Python bytecode.

A wheel filename is broken down into parts separated by hyphens:

```text
{dist}-{version}(-{build})?-{python}-{abi}-{platform}.whl
```

## References

- https://realpython.com/python-wheels/
