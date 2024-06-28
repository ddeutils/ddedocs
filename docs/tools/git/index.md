---
icon: material/git
---

# Git

!!! quote inline end

    **Git** is an <u>Open Source Distributed Version Control System Designed</u>
    to handle everything from small to very large projects with speed and efficiency.

:material-git: **Git** is the best version control tools for any developer, you can read the
[Official Documents](https://git-scm.com/).

- Save and Track different versions of your repositories
- Coordinate changes across different teams without impacting the work of other collaborators
- Share local copies of the same codebases as other developers when working offline
- Isolate new fixes and features in development without impacting production

## :octicons-workflow-24: Workflow

```text
Initial ---> Working <--> Index/Staging <--> Repository
```

=== "Initial"

    ```text
    .git/
      ├───> hooks/
      ├───> info/
      ├───> objects/
      ├───> refs/
      ├───> config
      ├───> description
      ├───> FETCH_HEAD
      ├───> HEAD
      └───> index
    ```

=== "Working"

    ```text
    .git/
      ├───> hooks/
      ├───> info/
      ├───> objects/
      ├───> refs/
      ├───> config
      ├───> description
      ├───> FETCH_HEAD
      ├───> HEAD
      └───> index
    ```

=== "Index/Staging"

    ```text
    .git/
      ├───> ...
      ├───> objects/
      |       ├───> 19/
      |       |     └───> 10283f238bc06de68f6a2ac63f3ec8c7a0dfef
      |       ├───> info/
      |       └───> pack/
      ├───> ...
      └───> index
    ```

=== "Repository"

    ```text
    .git/
      ├───> ...
      ├───> objects/
      |     ├───> 3c/
      |     |     └───> 6d5a4...
      |     ├───> 19/
      |     |     └───> 10283f238bc06de68f6a2ac63f3ec8c7a0dfef
      |     ├───> info/
      |     └───> pack/
      ├───> ...
      └───> index
    ```

**Details**:

=== "Initial"

    When you want to create `.git` file in your local project, you can use:

    ```console
    $ git init
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

## :material-console-line: Common Command

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

Filtering your commit history:

- by date - `--before` or `--after`
- by message - `--grep`
- by author - `--author`
- by file - `-- ${filename}`
- by branch - `${branch-name}`

```console
$ git log --after="2021-7-1"
$ git log --after="2021-7-1" --before="2021-6-5"
$ git log --grep="refactor"
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
    $ git branch
    ```

    **Options**:

    - `-a`, `git branch -a`: List all branchs on local and remote

=== "Create"

    ```shell
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

### Git Checkout

```shell
# Revert all modified files to clean status
$ git checkout .

# Switch to previous branch
$ git checkout -

# Revert to specific commit
$ git checkout "<commit>"

# Revert to specific file and commit
$ git checkout "<commit>" <file-name>

# Create new branch in local repository from existing branch in remote repository
$ git checkout -b feature/xxx origin/feature/xxx
```

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

=== "Set Remote"

    ```shell
    $ git remote add origin https://github.com/username/myproject.git
    $ git remote -v
    origin  https://github.com/username/myproject.git (fetch)
    origin  https://github.com/username/myproject.git (push)
    ```

=== "Push to Remote"

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

=== "Fetch from Remote"

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

=== "Pull from Remote"

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

## :material-console-line: Advance Command

### Git Revert

Revert specific commit to new commit

```console
$ git revert "<commit>"
$ git revert -m 1 "<commit>"

# Revert merge change
$ git reset --hard HEAD^
```

### Git Merge & Rebase

[Merging vs Rebasing](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)

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

=== "Merge Rebase"

    - Will append all commits history of the feature branch in the front of the master branch
    - Will NOT add extra dummy commit.

    ```shell
    # Rebase all commit from dev branch to main branch
    $ git switch dev
    $ git rebase main
    $ git rebase --continue
    $ git switch main
    $ git merge dev
    $ git branch -d dev
    ```

    !!! note

        If you want to cancel the rebase process, you can use `git rebase --abort`.

### Git Rebase Self

Instead, use it for cleaning up your local commit history before merging it into
a shared team branch. `git rebase` will use for

- Change a commit message
- Delete/Reorder commits
- Combine multiple commits into one (squash)
- Edit/Split an existing commit into multiple new ones

!!! warning

    Do **NOT** use Interactive Rebase on commits that you've already pushed/shared
    on a remote repository.

```console
$ git rebase -i HEAD~3
pick adfa804 Update config.yaml
pick 81529d3 update config.yaml
pick 3d8cc7a Update config.yaml

# Rebase 5a30adf..ae76b2e onto 5a30adf (3 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup <commit> = like "squash", but discard this commit's log message
# x, exec <command> = run command (the rest of the line) using shell
# b, break = stop here (continue rebase later with 'git rebase --continue')
# d, drop <commit> = remove commit
# l, label <label> = label current HEAD with a name
# t, reset <label> = reset HEAD to a label
# m, merge [-C <commit> | -c <commit>] <label> [# <oneline>]
# .       create a merge commit using the original merge commit's
# .       message (or the oneline, if no original merge commit was
# .       specified). Use -c <commit> to reword the commit message.
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
#
# Note that empty commits are commented out
:q!

$ git rebase --abort
```

```console
$ git log --oneline
ae76b2e (HEAD -> master, origin/master) USE OURS ON CONFLICT FILE
81529d3 update config.yaml
3d8cc7a Update config.yaml
adfa804 Update config.yaml
5a30adf ADD CONFIG
4e133da YOUR MESSAGE
```

!!! note

    When you want to control commit with rebase, `git rebase master --interactive`

!!! note

    If you want to **squash** all commit together, you can use `git merge --squash "<branch>"`
    command. (Or `git rebase -i --autosquash`)

### Git Conflict

!!! note

    Above command can use opposite option, like `git checkout --theirs config.yaml`.
    Or use it together with merge strategy,

    - `git merge --strategy-option ours`
    - `git merge --strategy-option theirs`

### Git Cherry Pick

If you want to take some commit (such as bug fix commit) from another branch to
your branch (Allows you to select individual commits to be integrated).

Cherry Pick fixed file from dev to main branch

```shell
$ git add <fix-filename>
$ git commit -m "bug fix"
$ git switch main
$ git log dev --oneline
<commit-hash> (dev) bug fix
...
$ git cherry-pick "<commit-hash>"
```

!!! note

    git does not that delete commit from source branch and in your branch will be exists that commit in new id.

### Git Submodules

Git Submodule help you to develop main project together with subproject and separate
the commits of subproject from main project.

The file `.submodule` is configuration of `git submodule` that keep project’s URL,
local subdirectory, and subproject branches that was tracked.

=== "Add"

    ```console
    $ git submodule add -b master https://github.com/username/module sub-project
    $ git status
    On branch master
    Your branch is up to date with 'origin/master'.
    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)
          new file:   .gitmodules
          new file:   sub-project

    $ cd sub-project
    sub-project$ ls
    README.md ...
    ```

    ```console
    $ cat .gitmodules
    [submodule "sub-project"]
        path = sub-project
        url = https://github.com/username/sub-project.git
        branch = master
    ```

    !!! note

        When you already push, you will see submodule in main project repository
        and the submodule does not keep the source code but it keep hash commit
        number of submodule.

=== "Clone"

    ```shell
    $ git clone https://github.com/username/mainproject.git
    $ cd sub-project
    sub-project$ ls


    sub-project$ git submodule init
    sub-project$ git submodule update
    Cloning into '/username/mainproject/sub-project'...
    Submodule path 'sub-project': checked out 'a5635f67626c1c224e733fe407aaa132b5e5d1e3
    ```

    !!! note

        The `git clone --recurse-submodules "<repository-url>"` is auto initialize
        and update submodules.

    `git submodule update --init --recursive`

    ```shell
    $ cd sub-project/
    sub-project$ git fetch
    sub-project$ git merge origin/master
    Already up to date.
    ```

    !!! note

        `git submodule update --remote` will auto fetch and merge with track branch. If you do not set trank, you will use

        ```shell
        username/myproject$ git config -f .gitmodules submodule.sub-project.branch develop
        username/myproject$ cat .gitmodules
        [submodule "sub-project"]
         path = sub-project
         url = https://github.com/username/sub-project.git
         branch = develop
        ```

        Optional, `git submodule update --remote --merge` or `git submodule update --remote --rebase`

=== "Push"

    ```shell
    username/myproject/sub-project$ git commit -am 'update readme.md'
    username/myproject/sub-project$ git push

    username/myproject/sub-project$ cd ..
    username/myproject$ git commit -am 'update submodule'
    username/myproject$ git push
    ```

    > NOTE: You can push along with the main project, where the submodule is pushed before the main project is pushed using the command `git push — recurse-submodules=on-demand`

=== "Delete"

    ```shell
    username/myproject$ git submodule deinit -f sub-project
    > Cleared directory 'sub-project'
    > Submodule 'sub-project' (https://github.com/username/sub-project.git) unregistered for path 'sub-project'

    username/myproject$ rm -rf .git/modules/sub-project
    username/myproject$ git rm --cached sub-project
    > rm 'sub-project'

    username/myproject$ rm .gitmodules
    username/myproject$ git commit -am "REMOVED submodule"
    > [master 66b1703] removed submodule
    >  2 files changed, 5 deletions(-)
    >  delete mode 160000 sub-project

    username/myproject$ git push origin master
    ```

### Git Reflog

A protocol of HEAD Pointer movements. Reflog is a mechanism to record when the tip
of branches is updated. This command is to manage the information recorded in it.

ใช้แสดง Log ของการเปลี่ยนแปลงใน HEAD ของ Local Repository มันเหมาะสำหรับการค้นหางานที่สูญหายไป

```shell
username/myproject$ git reflog --all
> ae76b2e (HEAD -> master, origin/master) HEAD@{0}: rebase -i (abort): updating HEAD
> 81529d3 HEAD@{1}: rebase -i (start): checkout HEAD~3
> ae76b2e (HEAD -> master, origin/master) refs/remotes/origin/master@{0}: update by push
> ae76b2e (HEAD -> master, origin/master) refs/heads/master@{0}: commit (merge): USE OURS ON CONFLICT FILE
> ae76b2e (HEAD -> master, origin/master) HEAD@{2}: commit (merge): USE OURS ON CONFLICT FILE
> 81529d3 refs/heads/master@{1}: commit: update config.yaml
> 81529d3 HEAD@{3}: commit: update config.yaml
> adfa804 refs/heads/master@{2}: reset: moving to HEAD~1
> :
```

### Git Blame

Use to track change inline of file.

```console
$ git blame config.yaml
5a30adf5 (usernaem    2022-03-06 13:52:04 +0700 1) env:
adfa8044 (usernaemDEV 2022-03-06 19:30:39 +0700 2)   develop: "/dev"
adfa8044 (usernaemDEV 2022-03-06 19:30:39 +0700 3)   remote: "/remote"
81529d32 (usernaem    2022-03-07 11:19:06 +0700 4)   production: "/prod"
```

### Git Bisect

#### Start bisect

```shell
username/myproject$ git bisect start
username/myproject$ git bisect bad "<commit-start>"
username/myproject$ git bisect good "<commit-end>"
```

#### Unittest until the latest commit exists

```shell
username/myproject$ run app
username/myproject$ git bisect bad
> Bisecting: 7 revisions left to test after this (roughly 3 steps)
> [12sasa53261sdfas4235sdab721c2405abv0*****] COMMIT MESSAGE

...

username/myproject$ run app
username/myproject$ git bisect bad
> Bisecting: 0 revisions left to test after this (roughly 0 steps)
> [jk1p1634sda78v93kla13asdfscc23140030*****] COMMIT MESSAGE

username/myproject$ git bisect bad
> 5a30adf5d4f184fd4586891e26d6826ab66***** COMMIT MESSAGE
> commit 5a30adf5d4f184fd4586891e26d6826ab66*****
> Author: username <username@email.com>
> Date: Sun Jan 01 00:00:00 1999 +0700
>
>     COMMIT MESSAGE

username/myproject$ git show 5a30adf5d4f184fd4586891e26d6826ab66*****
```

#### If found the bug success, you should exit bisect first

```shell
username/myproject$ git bisect reset
```

!!! note

    `git bisect log` will show the log of bisect, should use this command before
    reset.

## :material-vector-link: References

- TODO - [:simple-medium: Git commands I wish I knew earlier as a developer](https://levelup.gitconnected.com/git-commands-i-wish-i-knew-earlier-as-a-developer-a5f9f47d5644)
- [Frequently Used Git Commands](https://armno.in.th/2019/07/29/frequently-used-git-commands/)
- [:simple-medium: Git is your Friend](https://medium.com/@pakin/git-%E0%B8%84%E0%B8%B7%E0%B8%AD%E0%B8%AD%E0%B8%B0%E0%B9%84%E0%B8%A3-git-is-your-friend-c609c5f8efea)
