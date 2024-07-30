# Noted

This note will tell us about provisioning mkdocs on local for testing or hosting.

## Initialize `mkdocs`

```shell
mkdocs new .
```

## Serving

```shell
mkdocs serve
```

> [!NOTE]
> It will generate document to the url: http://127.0.0.1:8000/

> [!TIP]
> If you do not want to use auto reload, you can use `mkdocs serve --no-livereload`.

## Release Document

```shell
shelf vs bump date
```

## Document Template

```text
# Header

## :material-arrow-down-right: Getting Started

## Types

## :material-arrow-right-bottom: New-Topic

## :material-source-commit-end: Conclusion

## :material-playlist-plus: Read Mores
```

## :material-playlist-plus: Read Mores

- [How To Create STUNNING Code Documentation With MkDocs Material Theme](https://www.youtube.com/watch?v=Q-YA_dA8C20)
- [GitHub Gist - Markdown with `markdownlint`](https://gist.github.com/ahgraber/9ad4d0086a3f239f7872b7f33ebbe4c5#markdown-with-markdownlint)
