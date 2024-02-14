---
icon: material/git
---

# Git

!!! quote

    **Git** is a free and open source distributed version control system designed
    to handle everything from small to very large projects with speed and efficiency.

**Git** is the best version control tools for any developer, you can read the
[Official Documents](https://git-scm.com/).

- save and track different versions of your repositories
- coordinate changes across different teams without impacting the work of other collaborators
- share local copies of the same codebases as other developers when working offline
- isolate new fixes and features in development without impacting production

## Common Commands

### Git Hash

Git have build-in hash function that use for create file name in Git.

```console
$ git hash-object <filname>.<file-extension>
af5b63bf238bc06de68f6a2ac63f3ec8c7a0dfef
```

Or, you can create hash value with yourself

```console
$ echo -n "<type:[blob, tree, commit]> <content-length>\0<content-information>" \
  | shasum
af5b63bf238bc06de68f6a2ac63f3ec8c7a0dfef
```

You see the above hash process, Git does not create hash file name from the real
filename, but it uses content information in the file.

### Git Config

```console
$ git config --global user.name "username"
$ git config --global user.email "username@email.com"
$ git config --list
...
user.name=username
user.email=username@email.com
...
```

Configuration in Git can use: `git config` command line. The simple way to edit
Git configuration is using editor like **VS Code**, **Atom**, or **Vim** by Git
default.

```console
# Set Editor in Git config when you use -e option.
$ git config --global core.editor "code -w"
$ git config --global -e
hint: Waiting for your editor to close the file...
```

!!! note

    If you want to set Atom editor, use

    ```console
    $ git config --global core.editor "atom --wait"
    ```

!!! note

    The `git config` will override config values in local from global
    configuration.

    ```console
    $ git config "key" "value"
    $ git config --get "key"
    ```

## TODO

- [:simple-medium: Git commands I wish I knew earlier as a developer](https://levelup.gitconnected.com/git-commands-i-wish-i-knew-earlier-as-a-developer-a5f9f47d5644)
