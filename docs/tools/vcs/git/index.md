---
icon: material/git
---

# Git

!!! quote inline end

    **Git** is a free and open source distributed version control system designed
    to handle everything from small to very large projects with speed and efficiency.

**Git** is the best version control tools for any developer, you can read the
[Official Documents](https://git-scm.com/).

- Save and Track different versions of your repositories
- coordinate changes across different teams without impacting the work of other collaborators
- share local copies of the same codebases as other developers when working offline
- isolate new fixes and features in development without impacting production

## Workflow

```text
Initial ---> Working ---> Index/Staging ---> Repository
```

=== "Initial"

    When you want to create `.git` file in your local project, you can use:

    ```console
    $ git init
    ```

    ```text
    .git/
      |---> hooks/
      |---> info/
      |---> objects/
      |---> refs/
      |---> config
      |---> description
      |---> FETCH_HEAD
      |---> HEAD
      |---> index
    ```

    Another command, `git init –bare` will create and keep only configuration
    values of version control without source code.

=== "Working"

    ```console
    $ echo -e "Hello World" > demo.txt
    $ git hash-object demo.txt
    1910283f238bc06de68f6a2ac63f3ec8c7a0dfef
    ```

    ```console
    $ git status
    On branch main

    ...

    Untracked files:
      (use "git add <file>..." to ...)
          demo.txt

    nothing added to commit but untracked files present (use "git add" to track)
    ```

=== "Index/Staging"

    ```console
    $ git add .
    $ git status
    On branch main

    ...

    Changes to be committed:
      (use "git rm --cached <file>..." to unstage)
          newfile:    demo.txt
    ```

    ```text
    .git/
      |---> ...
      |---> objects/
      |       |---> 19/
      |       |     |---> 10283f238bc06de68f6a2ac63f3ec8c7a0dfef
      |       |---> info/
      |       |---> pack/
      |---> ...
    ```

    ```console
    $ git ls-files
    demo.txt
    ```

    !!! note

        The file in `object/` was compressed, and you will see value in this file
        when you use `zlib` like: `blob 11<nil>Hello World`.

    !!! note

        `git add -p <file>`, this command will split changed file to hunks of code for
        review and what to do with that hunk,

        such as `y n q a d / j J g e ?`.

        * `-y`: (yes) for add that hunk to staged zone
        * `-n`: (no) ignore to add this hunk
        * `-q`: (quit) quit this interactive with mode `git add -p`
        * `-s`: (split) divide this hunk to smaller hunks

    !!! note "Sub-Folder"

        This command, `git add :/`, using when you stay in sub-folder of working
        area and want to add all changed files include outside to staged status.

=== "Repository"

    ```console
    $ git commit -m "initial"
    [main (root-commit) 3c6d5a4] initial
    1 file changed, 1 insertion(+)
    create mode 100644 demo.txt
    ```

    ```text
    .git/
    |---> ...
    |---> objects/
    |     |---> 3c/
    |     |     |---> 6d5a4...
    |     |---> 19/
    |     |     |---> 10283f238bc06de68f6a2ac63f3ec8c7a0dfef
    |     |---> info/
    |     |---> pack/
    |---> ...
    ```

    ```console
    # Get type of Git file
    $ git cat-file -t 3c6d
    commit

    # Get content of Git file
    $ git cat-file -p 3c6d
    tree a611c6cc...
    author ...
    ...

    $ git cat-file -p a611
    100644 blob 1910283f238bc06de68f6a2ac63f3ec8c7a0dfef    demo.txt
    ```

    !!! note

        In commit hash file, Git will add `parent` information if you add new commit
        after first commit.

        ```console
        $ git cat-file -p 463f
        tree 9f3dc...
        parent 3c6d5a4...
        ...
        ```

    !!! note

        The `git commit --amend` or `git commit --amend -m "YOUR MESSAGE"` command use
        for create new commit replace the latest commit.

        ```console
        $ git commit -am "<message>"
        $ git add .
        $ git commit --amend
        ```

        This solution use only local repository, before push branch to remote repository.
        If it is not any changed file to Staged, this command will allow you to edit
        the latest Commit Message.

    !!! note

        `git ldm` for list history commits that you do in local repository before daily
        standup meeting.

## Common CMD

### Git Hash

Git have build-in hash function that use for create file name in Git.

```console
$ git hash-object <filname>.<file-extension>
af5b63bf238bc06de68f6a2ac63f3ec8c7a0dfef
```

??? note "Manual Hash"

    ```console
    $ echo -n "<type:[blob, tree, commit]> <content-length>\0<content-information>" \
      | shasum
    af5b63bf238bc06de68f6a2ac63f3ec8c7a0dfef
    ```

You see the above hash process, Git does not create hash file name from the real
filename, but it uses content information in the file.

### Git Config

The `git config` will override config values in local from global configuration.

=== "Config"

    ```console
    $ git config user.name "username"
    $ git config --get user.name
    $ git config --list
    ```

=== "Global"

    ```console
    $ git config --global user.name "username"
    $ git config --global user.email "username@email.com"
    $ git config --list
    ```

=== "Local"

    ```console
    $ git config --local user.name "username"
    $ git config --local user.email "username@email.com"
    $ git config --list
    ```

???+ example "Config Editor"

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

### Git Log

```console
# Set Disable Git Log pager
$ git config --globlal pager.log false
$ git log
commit 3c6d5a4... (HEAD -> main)
Author: ...
...
```

### Git Diff

### Git Branch

=== "List"

    ```console
    # List local branchs
    $ git branch

    # List all branchs on local and remote
    $ git branch -a
    ```

=== "Create"

    ```console
    # Create new branch
    $ git branch <branch-name>

    # Create new branch and switch HEAD to this branch
    $ git checkout -b <branch-name>

    # Support on Git version >= 2.2.3
    $ git switch -c <branch-name>
    ```

## References

- TODO - [:simple-medium: Git commands I wish I knew earlier as a developer](https://levelup.gitconnected.com/git-commands-i-wish-i-knew-earlier-as-a-developer-a5f9f47d5644)
