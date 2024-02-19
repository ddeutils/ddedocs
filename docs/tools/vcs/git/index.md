---
icon: material/git
---

# Git

!!! quote inline end

    **Git** is an open source distributed version control system designed to handle
    everything from small to very large projects with speed and efficiency.

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

    !!! note

        Remove all untracked files that was created in working, `git clean -f`.

=== "Index/Staging"

    === "Add"

        ```console
        $ git add .
        $ git status
        On branch main
        ...
        Changes to be committed:
          (use "git rm --cached <file>..." to unstage)
              newfile:    demo.txt
        ```

    === "Restore"

        Restore Added file that was added from staging to working

        ```console
        # Restore Added file that was committed to repository, to working
        $ git retore --staged .
        ```

    === "Reset"

        Reset all files that was added to staging

        ```console
        $ git reset
        $ git prune
        ```

    === "Revert"

        Revert files that was added to staging and delete files in `object/`

        ```console
        $ git add .
        $ git rm --cached <filename>
        $ git prune
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

    === "Commit"

        ```console
        $ git commit -m "initial"
        [main (root-commit) 3c6d5a4] initial
        1 file changed, 1 insertion(+)
        create mode 100644 demo.txt
        ```

    === "Restore"

        Restore Changed file that was committed to repository

        ```console
        $ git restore .
        ```

    === "Reset"

        Re-position of HEAD to hash commit that was committed to repository

        ```console
        $ git reset --hard <commit-hash>
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

```console
$ git diff 073c HEAD
...
index 2a3ee71..84f5955 100644
...
```

??? note "Use `difftool`"

    ```console
    $ git config --global diff.tool vscode
    $ git config --global difftool.vscode.cmd "code -w -d \$LOCAL \$REMOTE"
    $ git difftool --staged
    ...
    Viewing (1/1): '<filename>'
    Lauch 'vscode' [Y/n]?

    $ git config --global difftool.prompt false
    $ git difftool --staged
    ```

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

=== "Delete"

    ```shell
    # Delete branch that does not any new commit
    $ git branch -d <branch_name>

    # Delete branch that was created new commit
    $ git branch -D <branch_name>
    $ git reflog expire --expire-unreachable=now --all
    $ git prune
    ```

    !!! note

        `git cleanup` for delete branches in local repository that was merged.

!!! note

    If you want to check out previous branch, you can use: `git checkout -`.

### Git Tag

**Git Tags** are used to capture the specific point in the history that is further
used to point to a released version. A tag does not change like a branch.

```console
$ git log --oneline
816998a <commit-message>
7c576ab <commit-message>
dd9a333 stable
...

# Switch HEAD to that commit
$ git switch --detach dd9a333
$ git tag alpha
$ git switch --detach alpha
```

```shell
$ git tag "<tag-name>" "<commit>"
$ git show "<tag-name>"
$ git tag --list
$ git tag -d "<tag-name>"
```

!!! note

    - Annotated tags - `git tag -a '<tag-name>' -m '<message>' HEAD`
    - Lightweight tags - `git tag <tag-name>`

```shell
$ git ls-remote --tags
$ git ls-remote --tags origin
$ git push --delete origin "<tag-name>"
$ git push origin :refs/tags/"<tag-name>"
```

> NOTE: If you want to push tag on local repository to remote, you will use `git push my_remote –tags`

### Git Stash

The `git stash` does hide all changes, stash the changes in a dirty working directory
away. The local repository will be clean because `git stash` will tell HEAD commit
hash revert to any commit (the latest commit always dirty).

=== "Stash"

    ```console
    $ touch file.txt
    $ git add .
    $ git stash
    Saved working directory and index state WIP on gh-pages: fe163ee update and done
    ```

    !!! note

        You can change the name of stash by this command: `git stash save "<name>"`,
        and stash included untracked file: `git stash -u`.

=== "List"

    ```console
    $ git stash list
    stash@{0}: WIP on gh-pages: fe163ee update and done

    $ ls file.txt
    ls: cannot access 'file.txt': No such file or directory
    ```

=== "Apply"

    ```console
    $ git stash apply
    $ ls file.txt
    file.txt

    $ git stash drop stash@{0}
    ```

    !!! note

        Above command, `git stash apply stash@{0}`, apply the latest stash to working
        area and staged area but difference with `git stash pop` because `pop` will
        delete stash history in list.

### Git Remote

=== "Set"

    ```shell
    $ git remote add origin https://github.com/username/myproject.git
    $ git remote -v
    origin  https://github.com/username/myproject.git (fetch)
    origin  https://github.com/username/myproject.git (push)
    ```

=== "Push"

    ```shell
    $ git push -u origin master
    Enumerating objects: 7, done.
    ...
    To https://github.com/username/myproject.git
     * [new branch]      master -> master
    Branch 'master' set up to track remote branch 'master' from 'origin'.
    ```

    !!! warning

        The command `git push origin master --force` for force push to remote repository
        that mean it does not use `git pull origin` command before push.

    !!! note

        Above remote is use `http` access, so it always pass username/password after
        `git push` command. The another way is
        [use ssh for connect to remote](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

=== "Pull"

    ```shell
    $ git fetch
    ...
    From https://github.com/username/myproject.git
       5a30adf..ad*****  master     -> origin/master

    $ git status
    On branch master
    Your branch is behind 'origin/master' by 1 commit, and can be fast-forwarded.
      (use "git pull" to update your local branch)

    nothing to commit, working tree clean
    ```

    ```shell
    $ git pull
    Updating 5a30adf..adfa804
    Fast-forward
     <filename> | 3 ++-
     1 file changed, 2 insertions(+), 1 deletion(-)
    ```

### Git Fork

Git Fork is the GitHub's feature for task owner of remote repository, it seems like
clone but the repository will be yours. If you want to sync update from original
repository to yours repository, you will add `upstream`.

```console
$ git remote add upstream https://github.com/<original_owner>/<original_repo>.git
$ git remote -v
origin  git@github.com:Phonbopit/bootstrap.git (fetch)
origin  git@github.com:Phonbopit/bootstrap.git (push)
upstream    git@github.com:Phonbopit/bootstrap.git (fetch)
upstream    git@github.com:Phonbopit/bootstrap.git (push)
```

```console
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
```

## Advance CMD

### Git Merge & Rebase

=== "Merge"

    - Will keep all commits history of the feature branch and move them into the master branch
    - Will add extra dummy commit.

    ```console
    $ git switch main
    $ git merge dev
    ```

=== "Merge Squash"

    - Will group all feature branch commits into one commit then append it in the front of the master branch
    - Will add extra dummy commit.

    ```console
    $ git merge --squash HEAD@{1}
    $ git checkout stable
    $ git merge --squash develop
    $ git commit -m "squash develop"
    ```

=== "Rebase"

    - Will append all commits history of the feature branch in the front of the master branch
    - Will NOT add extra dummy commit.

    ```console
    # Rebase all commit from dev branch to main branch
    $ git switch dev
    $ git rebase main
    $ git switch main
    $ git rebase dev
    $ git reflog expire --expire-unreachable=now --all
    $ git prune
    ```

### Git Conflict

!!! note

    Above command can use opposite option, like `git checkout --theirs config.yaml`.
    Or use it together with merge strategy,

    - `git merge --strategy-option ours`
    - `git merge --strategy-option theirs`

### Git Cherry Pick

Cherry Pick fixed file from dev to main branch

```shell
$ git add <fix-filename>
$ git commit -m "bug fix"
$ git switch main
$ git log dev --oneline
<commit-hash> (dev) bug fix
...
$ git cherry-pick <commit-hash>
```

## References

- TODO - [:simple-medium: Git commands I wish I knew earlier as a developer](https://levelup.gitconnected.com/git-commands-i-wish-i-knew-earlier-as-a-developer-a5f9f47d5644)
- [Frequently Used Git Commands](https://armno.in.th/2019/07/29/frequently-used-git-commands/)
- [Git is your Friend](https://medium.com/@pakin/git-%E0%B8%84%E0%B8%B7%E0%B8%AD%E0%B8%AD%E0%B8%B0%E0%B9%84%E0%B8%A3-git-is-your-friend-c609c5f8efea)
