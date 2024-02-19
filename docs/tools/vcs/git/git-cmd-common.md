# Git Commands

## Git Edit Workflow

```console
# Remove all files that was created in working
$ git clean -f

# Revert files that was added to staging and delete files in object/
$ git add .
$ git rm --cached <filename>
$ git prune

# Reset all files that was added to staging
$ git reset
$ git prune

# Restore Changed file that was committed to repository
$ git restore <filename>

# Restore Added file that was committed to repository, to working
$ git retore --staged <filename>
```

!!! note

    `git rm -r --cached "<folder>"` or `git rm --cached <file>` to stop tracking a
    file you need to remove it from the index.

!!! note

    `git clean` - for delete untracked file with options,

    * `-f`: Force delete
    * `-n`: Dry-run, that mean git will pop up the cleaned file

```console
# Delete files and auto add this files to staging
$ git rm <filename>

# Reset all files that was added to working
$ git reset --hard

# Re-position of HEAD to hash commit that was committed to repository
$ git reset --hard <commit-hash>
HEAD is now at <commit-hash> <commit-message>

$ git config --global core.pager cat
$ git reflog

# Delete reflog of mistake commit that created after HEAD
$ git reflog expire --expire-unreachable=now --all
$ git reflog
$ git prune
```

## Git Diff & Difftool

Create new file, <filename>, in your local Git staging area.

```console
$ git add <filename>
$ git diff --staged
diff --git a/<filename> b/<filename>
new file mode 100644
index 0000000..2a3ee71
--- /dev/null
+++ b/<filename>
...

$ git commit -m "add <filename>"
[main (root-commit) 073c83f] add <filename>
...
```

If you edit <filename> again and run `git diff` command:

```console
$ git diff
diff --git a/<filename> b/<filename>
index 2a3ee71..84f5955 100644
--- a/<filename>
+++ b/<filename>
...

$ git add <filename>
$ git diff --staged
diff --git a/<filename> b/<filename>
index 2a3ee71..84f5955 100644
...
```

```console
$ git diff 073c head
...
index 2a3ee71..84f5955 100644
...
```

Use `difftool` if you want to editable the diff files

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

## Git Branch

List all branches:

```console
$ git branch
* main
```

Create new branch:

```shell
# Create new branch
$ git branch <branch-name>

# Create new branch and switch HEAD to this branch
$ git checkout -b <branch-name>

# Support on Git version >= 2.2.3
$ git switch -c <branch-name>
```

> **Note**: \
> If you want to check out previous branch, you can use: `git checkout -`

Delete branch:

```shell
# Delete branch that does not any new commit
$ git branch -d <branch_name>

# Delete branch that was created new commit
$ git branch -D <branch_name>
$ git reflog expire --expire-unreachable=now --all
$ git prune
```

> **Note**: \
> `git cleanup` for delete branches in local repository that was merged.

## Git Merge & Rebase

### Merge

```console
# Merge change from dev branch to current main branch
$ git log main --oneline
$ git switch main
$ git merge dev

# Merge change from dev branch to current main branch that edit same files
$ git merge dev
...
CONFLICT (content): Merge conflict in <filename>
...

$ git add <filename>
$ git commit -m "Edit conflict from dev branch"
```

### Rebase

```shell
# Rebase all commit from dev branch to main branch
$ git switch dev
$ git rebase main
$ git switch main
$ git rebase dev
$ git reflog expire --expire-unreachable=now --all
$ git prune
```

### Squash Merge

```shell
$ git merge --squash HEAD@{1}
$ git checkout stable
$ git merge --squash develop
$ git commit -m "squash develop"
```

!!! note

    - **Merge commits**:
      - Will keep all commits history of the feature branch and move them into the master branch
      - Will add extra dummy commit.
    - **Rebase and merge**:\
      - Will append all commits history of the feature branch in the front of the master branch
      - Will NOT add extra dummy commit.
    - **Squash and merge**:\
      - Will group all feature branch commits into one commit then append it in the front of the master branch
      - Will add extra dummy commit.

    Read More: [What is the difference between squash and rebase](https://stackoverflow.com/questions/2427238/what-is-the-difference-between-merge-squash-and-rebase/2427520#2427520)

## Git Cherry Pick

```shell
# Cherry Pick fixed file from dev to main branch
$ git add <fix-filename>
$ git commit -m "bug fix"
$ git switch main
$ git log dev --oneline
<commit-hash> (dev) bug fix
...
$ git cherry-pick <commit-hash>
```

## Git Tag

**Git Tags** are used to capture the specific point in the history that is further
used to point to a released version. A tag does not change like a branch.

```shell
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

> **Note**:
>
> - Annotated tags - `git tag -a '<tag-name>' -m '<message>' HEAD`
> - Lightweight tags - `git tag <tag-name>`

```shell
$ git ls-remote --tags
$ git ls-remote --tags origin
$ git push --delete origin "<tag-name>"
$ git push origin :refs/tags/"<tag-name>"
```

> NOTE: If you want to push tag on local repository to remote, you will use `git push my_remote –tags`

## Git Stash

The `git stash` does hide all changes, stash the changes in a dirty working directory
away. The local repository will be clean because `git stash` will tell HEAD commit
hash revert to any commit (the latest commit always dirty).

```shell
$ touch file.txt
$ git add .
$ git stash
Saved working directory and index state WIP on gh-pages: fe163ee update and done

$ git stash list
stash@{0}: WIP on gh-pages: fe163ee update and done

$ ls file.txt
ls: cannot access 'file.txt': No such file or directory
```

```shell
$ git stash apply
$ ls file.txt
file.txt

$ git stash drop stash@{0}
```

> **Note**: \
> You can change the name of stash by this command: `git stash save "<name>"`.

> **Note**: \
> Above command, `git stash apply stash@{0}`, apply the latest stash to working
> area and staged area but difference with `git stash pop` because `pop` will
> delete stash history in list.

> **Note**: \
> `git stash -u`: stash included untracked file

## Git Remote

```shell
$ git remote add origin https://github.com/username/myproject.git
$ git remote -v
origin  https://github.com/username/myproject.git (fetch)
origin  https://github.com/username/myproject.git (push)
```

```shell
$ git push -u origin master
Enumerating objects: 7, done.
...
To https://github.com/username/myproject.git
 * [new branch]      master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.
```

> **Note**: \
> `git push origin master --force` for force push to remote repository that mean
> does not use `git pull origin` command before push.

> **Note**: \
> About command `git push -u origin master` has options detail:
>
> - `-u`/`--set-upstream-to` - for remember this `origin master` parameters, next you will use only `git push` command
> - `origin` - alias name of remote repository, that mean can remote more than one repository
> - `master` - target branch name want to push

> **Note**: \
> `git push origin HEAD` for push a new feature branch created in the local repository
> along with creating a new branch with the same name on the remote repository.

```shell
$ git log
commit 5a30adf5d4f184fd4586891e26d6826ab66***** (HEAD -> master, origin/master)
Author: username <username@email.com>
Date:   Sun Jan 01 00:00:00 1999 +0700

    ADD CONFIG

commit 4e133da8b2b77cf9755095bf967d8be78a7*****
Author: username <username@email.com>
Date:   Sun Jan 01 00:00:00 1999 +0700

    YOUR MESSAGE
```

> **Note**: \
> Above remote is use `http` access, so it always pass username/password after `git push` command. \
> The another way is [use ssh for connect to remote](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

### Git Pull from Remote

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

> **Note**: \
> The `git pull` command is combine between `git fetch` and `git merge` commands together.

### Conflict with Remote

While team edit a file, `config.yaml`, from local repository and remote repository
in the same line of file.

```yaml
# Local Repository
env:
  develop: "/dev"
  remote: "/remote"
  production: "/prd"
```

```yaml
# Remote Repository
env:
  develop: "/dev"
  remote: "/remote"
  staging: "/stg"
```

#### CASE: `git pull` to Local Repository

```shell
$ git add .
$ git commit -m "EDIT config.yaml"
$ git merge origin/master
Auto-merging config.yaml
CONFLICT (content): Merge conflict in config.yaml
Automatic merge failed; fix conflicts and then commit the result.

username/myproject$ git status
On branch master
Your branch and 'origin/master' have diverged,
and have 1 and 1 different commits each, respectively.
  (use "git pull" to merge the remote branch into yours)

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   config.yaml

no changes added to commit (use "git add" and/or "git commit -a")
```

```yaml
# Local Repository
env:
  develop: "/dev"
  remote: "/remote"
<<<<<<< HEAD
  production: "/prd"
=======
  staging: "/stg"
>>>>>>> origin/master
```

```console
$ git mergetool
# Display in terminal
# ╔═══════╦══════╦════════╗
# ║       ║      ║        ║
# ║ LOCAL ║ BASE ║ REMOTE ║
# ║       ║      ║        ║
# ╠═══════╩══════╩════════╣
# ║                       ║
# ║        MERGED         ║
# ║                       ║
# ╚═══════════════════════╝
This message is displayed because 'merge.tool' is not configured.
See 'git mergetool --tool-help' or 'git help config' for more details.
'git mergetool' will now attempt to use one of the following tools:
tortoisemerge emerge vimdiff
Merging:
config.yaml

Normal merge conflict for 'config.yaml':
  {local}: modified file
  {remote}: modified file
Hit return to start merge resolution tool (vimdiff):
$ :diffg RE
$ :wqa
```

!!! note

    * `LOCAL` – this is file from the current branch
    * `BASE` – common ancestor, how file looked before both changes
    * `REMOTE` – file you are merging into your branch
    * `MERGED` – merge result, this is what gets saved in the repo

> **Note**:
>
> - `diffg RE` - remote change
> - `diffg BA` - base change
> - `diffg LO` - local change

```shell
$ git commit -m "EDIT CONFLICTS"
$ git clean -f
Removing config.yaml.orig
```

#### CASE: `git push` to Remote Repository

```console
$ git push
To https://github.com/username/myproject.git.git
 ! [rejected]        master -> master (non-fast-forward)
error: failed to push some refs to 'https://github.com/username/myproject.git.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. Integrate the remote changes (e.g.
hint: 'git pull ...') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

$ git fetch origin
$ git pull origin master
From https://github.com/username/myproject.git
 * branch            master     -> FETCH_HEAD
Auto-merging config.yaml
CONFLICT (content): Merge conflict in config.yaml
Automatic merge failed; fix conflicts and then commit the result.
```

```shell
$ git checkout --ours config.yaml
Updated 1 path from the index

$ git status
On branch master
Your branch and 'origin/master' have diverged,
and have 1 and 1 different commits each, respectively.
  (use "git pull" to merge the remote branch into yours)

You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   config.yaml
```

> **Note**: \
> Above command can use opposite option, like `git checkout --theirs config.yaml`. \
> Or use it together with merge strategy,
>
> - `git merge --strategy-option ours`
> - `git merge --strategy-option theirs`

```shell
$ git add config.yaml
$ git status
On branch master
Your branch and 'origin/master' have diverged,
and have 1 and 1 different commits each, respectively.
  (use "git pull" to merge the remote branch into yours)

All conflicts fixed but you are still merging.
  (use "git commit" to conclude merge)

$ git commit -m "USE OURS ON CONFLICT FILE"
$ git push
...
To https://github.com/username/myproject.git.git
   3d8cc7a..ae76b2e  master -> master
```

```shell
$ git config --global alias.hist "log --oneline --graph --decorate --all"
$ git hist
 *   ae76b2e (HEAD -> master, origin/master) USE OURS ON CONFLICT FILE
 |\
 | * 3d8cc7a Update config.yaml
 * | 81529d3 update config.yaml
 |/
 * adfa804 Update config.yaml
 * 5a30adf ADD CONFIG
 * 4e133da YOUR MESSAGE
```

> **Note**: \
> `HEAD` is the pointer that keep all commits, most recent commit.
> In common case, `HEAD` points to the latest commit with `SHA` code.
>
> ```shell
> ...
> $ git show HEAD
> Merge: 81529d3 3d8cc7a
> Author: username <username@mail.com>
> ...
>     USE OURS ON CONFLICT FILE
> ...
> ```

## Git Fork

Git Fork is the GitHub's feature for task owner of remote repository, it seems like
clone but the repository will be yours. If you want to sync update from original
repository to yours repository, you will add `upstream`.

```shell
$ git remote add upstream https://github.com/<original_owner>/<original_repo>.git
$ git remote -v
origin  git@github.com:Phonbopit/bootstrap.git (fetch)
origin  git@github.com:Phonbopit/bootstrap.git (push)
upstream    git@github.com:Phonbopit/bootstrap.git (fetch)
upstream    git@github.com:Phonbopit/bootstrap.git (push)
```

```shell
$ git fetch upstream
$ git checkout master
$ git merge upstream/master
```

## References

- https://armno.in.th/2019/07/29/frequently-used-git-commands/
- https://medium.com/@pakin/git-%E0%B8%84%E0%B8%B7%E0%B8%AD%E0%B8%AD%E0%B8%B0%E0%B9%84%E0%B8%A3-git-is-your-friend-c609c5f8efea
