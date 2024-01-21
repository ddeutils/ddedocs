# Common Scenarios

## Normal Push from Local to Remote

```console
$ git status
$ git add .
$ git log --oneline
$ git commit -am "<commit-message>"
$ git push origin
```

- Git fetch only for `main` branch

```console
$ git fetch origin main
$ git merge FETCH_HEAD
```
