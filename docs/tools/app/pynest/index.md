# PyNest

[**PyNest**](https://github.com/PythonNest/PyNest) is designed to help structure
your APIs in an intuitive, easy to understand, and enjoyable way.

Asynchronous programming is a paradigm that facilitates non-blocking operations,
making it particularly suitable for I/O-bound tasks such as database interactions.
**PyNest**'s integration with SQLAlchemy 2.0 allows developers to manage database
operations without the overhead of traditional synchronous processing.
This integration not only enhances performance but also improves the scalability
and responsiveness of applications.

```shell
pip install pynest-api
pip install asyncpg
```

```shell
pynest create-nest-app -n MyAppName -db postgresql --is-async
```

```text
├── app.py
├── config.py
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── src
│    ├── __init__.py
```

## References

- [Asynchronous Magic: PyNest and SQLAlchemy 2.0 Drive a 25% Improvement in Python Apps Performance](https://medium.com/@itay2803/asynchronous-magic-pynest-and-sqlalchemy-2-0-drive-a-25-improvement-in-python-apps-performance-9e2724e9f198)
