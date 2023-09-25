Advance Git
===========

> TOPICS:
> - [Checkout and Revert](#git-checkout-and-revert)
>   - [Checkout](#checkout)
>   - [Revert](#revert)
> - [Reset Scenarios](#reset-scenarios)
>   - [Scenario: Working Area](#scenario-1-delete-file-in-working-area)
>   - [Scenario: Staged Area](#scenario-2-delete-file-and-add-to-staged-area)
>   - [Scenario: Local Repository](#scenario-3-delete-file-and-commit-to-local-repository)
> - [Reset `master` Branch](#reset-master-branch)
> - [Rebase](#git-rebase)
> - [Search and Find](#search-and-find)
> - [submodules](#git-submodules)
> - [Cherry Picking](#cherry-picking)
> - [The Reflog](#the-reflog)
> - [](#git-blame)
> - [Git Bisect](#git-bisect)

---

Git Checkout and Revert
-----------------------

### Checkout

```shell
# Revert all modified files to clean status
username/myproject$ git checkout .

# Switch to previous branch
username/myproject$ git checkout -

# Revert to specific commit
username/myproject$ git checkout "<commit>"

# Revert to specific file and commit
username/myproject$ git checkout "<commit>" <file-name>

# Create new branch in local repository from existing branch in remote repository
username/myproject$ git checkout -b feature/xxx origin/feature/xxx
```

### Revert

```shell
# Revert specific commit to new commit
username/myproject$ git revert "<commit>"
username/myproject$ git revert -m 1 "<commit>"

# Revert merge change
username/myproject$ git reset --hard HEAD^
```


Reset Scenarios
---------------

If you have accident, like `rm -r README.md`

```shell
username/myproject$ git status
> On branch master
> Changes not staged for commit:
>   (use "git add/rm <file>..." to update what will be committed)
>   (use "git restore <file>..." to discard changes in working directory)
>         deleted:    README.md
>
> no changes added to commit (use "git add" and/or "git commit -a")
```

### Scenario 1: delete file in working area

```shell
username/myproject$ git checkout README.md
> Updated 1 path from the index

username/myproject$ git status
> On branch master
> nothing to commit, working tree clean
```

> NOTE: Same as `git restore --worktree README.md`

### Scenario 2: delete file and add to staged area

```shell
username/myproject$ git add .
username/myproject$ git status
> On branch master
> Changes to be committed:
>   (use "git restore --staged <file>..." to unstage)
>         deleted:    README.md
```
```shell
username/myproject$ git restore --source=HEAD --staged --worktree README.md
username/myproject$ git status
> On branch master
> nothing to commit, working tree clean
```

> NOTE: If want to restore to before add to git will use `git restore --staged READMD.md`

### Scenario 3: delete file and commit to local repository

```shell
username/myproject$ git add .
username/myproject$ git commit -m "ACCIDENT COMMIT"
> [master 134bf16] ACCIDENT COMMIT
>  1 file changed, 1 deletion(-)
>  delete mode 100644 README.md

username/myproject$ git log
> commit 5882d01f453beecfec3f252141a9f1bd0761fc35 (HEAD -> master)
> Author: username <username@email.com>
> Date:   Sun Jan 01 00:00:00 1999 +0700
>
>     ACCIDENT COMMIT
>
> commit 4e133da8b2b77cf9755095bf967d8be78a70c7b9
> Author: username <username@email.com>
> Date:   Sun Jan 01 00:00:00 1999 +0700
>
>     YOUR MESSAGE
```

#### `--soft` option

```shell
username/myproject$ git reset --soft HEAD~1
username/myproject$ git status
> On branch master
> Changes to be committed:
>   (use "git restore --staged <file>..." to unstage)
>         deleted:    README.md
>
> username/myproject$ git log
> commit 4e133da8b2b77cf9755095bf967d8be78a70c7b9 (HEAD -> master)
> Author: username <username@email.com>
> Date:   Sun Jan 01 00:00:00 1999 +0700
>
>     YOUR MESSAGE
```
### `--hard` option

```shell
username/myproject$ git reset --hard HEAD~1
> HEAD is now at 4e133da YOUR MESSAGE

username/myproject$ git status
> On branch master
> nothing to commit, working tree clean
>
> username/myproject$ git log
> commit 4e133da8b2b77cf9755095bf967d8be78a70c7b9 (HEAD -> master)
> Author: username <username@email.com>
> Date:   Sun Jan 01 00:00:00 1999 +0700
>
>     YOUR MESSAGE
```

> `git remove --cached README.md`

Reset `master` Branch
---------------------

### First Method

```shell
# Clone the project, e.g. `myproject` is my project repository
username/myproject$ git clone https://github/username/myproject.git

# Since all of the commits history are in the `.git` folder, we have to remove it
username/myproject$ cd myproject

# And delete the `.git` folder:
username/myproject$ git rm -rf .git

# Now, re-initialize the repository:
username/myproject$ git init
username/myproject$ git remote add origin https://github.com/heiswayi/myproject.git
username/myproject$ git remote -v

# Add all the files and commit the changes:
username/myproject$ git add --all
username/myproject$ git commit -am "Initial commit"

# Force push update to the master branch of our project repository:
username/myproject$ git push -f origin master
```

> NOTE: You might need to provide the credentials for your GitHub account.

### Second Method

Deleting the `.git` folder may cause problems in our git repository. If we want to delete all of our commits history, but keep the code in its current state, try this:

```shell
# Check out to a temporary branch
username/myproject$ git checkout --orphan "TEMP_BRANCH"

# Add all the files
username/myproject$ git add -A

# Commit the changes
username/myproject$ git commit -am "Initial commit"

# Delete the old branch
username/myproject$ git branch -D master

# Rename the temporary branch, "TEMP_BRANCH" to master
username/myproject$ git branch -m master

# Finally, force update to our repository
username/myproject$ git push -f origin master
```

> NOTE: This will not keep our old commits history around. But if this doesn't work, try the next method below.

Git Rebase
----------

Instead, use it for cleaning up your local commit history before merging it into a shared team branch. `git rebase` will use for
 - Change a commit's message
 - Delete/Reorder commits
 - Combine multiple commits into one
 - Edit/Split an existing commit into multiple new ones

> NOTE: Do __NOT__ use Interactive Rebase on commits that you've already pushed/shared on a remote repository.

```shell
username/project$ git rebase -i HEAD~3
> pick adfa804 Update config.yaml
> pick 81529d3 update config.yaml
> pick 3d8cc7a Update config.yaml
>
> # Rebase 5a30adf..ae76b2e onto 5a30adf (3 commands)
> #
> # Commands:
> # p, pick <commit> = use commit
> # r, reword <commit> = use commit, but edit the commit message
> # e, edit <commit> = use commit, but stop for amending
> # s, squash <commit> = use commit, but meld into previous commit
> # f, fixup <commit> = like "squash", but discard this commit's log message
> # x, exec <command> = run command (the rest of the line) using shell
> # b, break = stop here (continue rebase later with 'git rebase --continue')
> # d, drop <commit> = remove commit
> # l, label <label> = label current HEAD with a name
> # t, reset <label> = reset HEAD to a label
> # m, merge [-C <commit> | -c <commit>] <label> [# <oneline>]
> # .       create a merge commit using the original merge commit's
> # .       message (or the oneline, if no original merge commit was
> # .       specified). Use -c <commit> to reword the commit message.
> #
> # These lines can be re-ordered; they are executed from top to bottom.
> #
> # If you remove a line here THAT COMMIT WILL BE LOST.
> #
> # However, if you remove everything, the rebase will be aborted.
> #
> # Note that empty commits are commented out
> :q!

username/project$ git rebase --abort
```

```shell
username/project$ git log --oneline
> ae76b2e (HEAD -> master, origin/master) USE OURS ON CONFLICT FILE
> 81529d3 update config.yaml
> 3d8cc7a Update config.yaml
> adfa804 Update config.yaml
> 5a30adf ADD CONFIG
> 4e133da YOUR MESSAGE
```

> NOTE: When you want to control commit with rebase, `git rebase master --interactive`

> NOTE: If you want to `squash` all commit together, you can use `git merge --squash "<branch>"` command. (Or `git rebase -i --autosquash`)

Search and Find
---------------

Filtering your commit history
- by date - `--before` or `--after`
- by message - `--grep`
- by author - `--author`
- by file - `-- ${filename}`
- by branch - `${branch-name}`

```shell
$ git log --after="2021-7-1"
$ git log --after="2021-7-1" --before="2021-6-5"
$ git log --grep="refactor"
```

Git Submodules
--------------

Git Submodule help you to develop main project together with sub-project and separate the commits of sub-project from main project.

The file `.submodule` is configuration of `git submodule` that keep project’s URL, local subdirectory, and sub-project branchs that was tracked.

### Add submodules to Local Repository

```shell
username/myproject$ git submodule add -b master https://github.com/username/module sub-project
username/myproject$ git status
> On branch master
> Your branch is up to date with 'origin/master'.
> Changes to be committed:
>   (use "git reset HEAD <file>..." to unstage)
>       new file:   .gitmodules
>       new file:   sub-project

username/myproject$ cd sub-project
username/myproject/project$ ls
> README.md ...
```

```shell
username/myproject$ cat .gitmodules
> [submodule "sub-project"]
>     path = sub-project
>     url = https://github.com/username/sub-project.git
>     branch = master
```

> NOTE: When you already push, you will see submodule in main project repository and the submodule does not keep the source code but it keep hash commit number of submodule.


### Clone Remote Repository which included submodules

```shell
username/mainproject$ git clone https://github.com/username/mainproject.git
username/myproject$ cd sub-project
username/myproject$ ls
>

username/mainproject/sub-project$ git submodule init
username/myproject/sub-project$ git submodule update
> Cloning into '/username/mainproject/sub-project'...
> Submodule path 'sub-project': checked out 'a5635f67626c1c224e733fe407aaa132b5e5d1e3
```

> NOTE: `git clone --recurse-submodules "<repository-url>"` is auto initialize and update submodules.

`git submodule update --init --recursive`

```shell
username/myproject$ cd sub-project/
username/myproject/sub-project$ git fetch
username/myproject/sub-project$ git merge origin/master
> Already up to date.
```

> NOTE: `git submodule update --remote` will auto fetch and merge with track branch. If you do not set trank, you will use
> ```shell
> username/myproject$ git config -f .gitmodules submodule.sub-project.branch develop
> username/myproject$ cat .gitmodules
> [submodule "sub-project"]
>  path = sub-project
>  url = https://github.com/username/sub-project.git
>  branch = develop
> ```
> Optional, `git submodule update --remote --merge` or `git submodule update --remote --rebase`

### Push updated submodule to Remote

```shell
username/myproject/sub-project$ git commit -am 'update readme.md'
username/myproject/sub-project$ git push

username/myproject/sub-project$ cd ..
username/myproject$ git commit -am 'update submodule'
username/myproject$ git push
```

> NOTE: You can push along with the main project, where the submodule is pushed before the main project is pushed using the command `git push — recurse-submodules=on-demand`

### Delete submodule

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

Cherry-Picking
--------------

If you want to take some commit (such as bug fix commit) from another branch to your branch (Allows you to select individual commits to be integrated).

```shell
username/myproject$ git cherry-pick "<commit>"
```

> NOTE: git does not that delete commit from source branch and in your branch will be exists that commit in new id.

The Reflog
----------

A protocol of HEAD Pointer movements. Reflog is a mechanism to record when the tip of branches are updated. This command is to manage the information recorded in it.

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

Git Blame
---------

ใช้ดูว่ามีใครที่เข้ามาเปลี่ยนแปลง อะไร และ เมื่อใด ใน my_file

```shell
username/myproject$ git blame config.yaml
> 5a30adf5 (korawica    2022-03-06 13:52:04 +0700 1) env:
> adfa8044 (KorawichSCG 2022-03-06 19:30:39 +0700 2)   develop: "/dev"
> adfa8044 (KorawichSCG 2022-03-06 19:30:39 +0700 3)   remote: "/remote"
> 81529d32 (korawica    2022-03-07 11:19:06 +0700 4)   production: "/prod"
```

Git Bisect
----------

### Start bisect

```shell
username/myproject$ git bisect start
username/myproject$ git bisect bad "<commit-start>"
username/myproject$ git bisect good "<commit-end>"
```

### Unittest until the latest commit exists

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

### If found the bug success, you should exit bisect first

```shell
username/myproject$ git bisect reset
```

> NOTE: `git bisect log` will show the log of bisect, should use this command before reset.

HOOKS
-----

`git hooks` ชุดของคำสั่งที่ Git จะเรียก ก่อนหรือหลังคำสั่งหลักใดๆ เช่น commit, push

Git hooks เป็นสิ่งที่ติดตัวมากับ Git อยู่แล้วไม่ต้องไปดาวโหลดอะไรมาลงเพิ่มและ Git hooks นั้นเป็นฟีเจอร์ที่จำทำงานแบบ local หรือเฉพาะเครื่องของคนๆนั้นเท่านั้น

> NOTE:
> ```shell
> $ git config --global core.hooksPath /path/to/my/centralized/hooks
> $ git config --local core.hooksPath /path/to/my/centralized/hooks
> ```

 Let’s have a look what kind of local hooks we have in our repository’s .git/hooks folder :
├── applypatch-msg.sample
├── commit-msg.sample
├── post-update.sample
├── pre-applypatch.sample
├── pre-commit.sample
├── prepare-commit-msg.sample
├── pre-rebase.sample
└── update.sample


### Post Receive

`git config receive.denycurrentbranch ignore`

post-receive จะทำหน้าที่คือ เมื่อ push เข้า origin master เมื่อไร code จะถูก update อัตโนมัติ
และคำสั่งภายใน ./git/hooks/post-receive ก็จะถูกรัน

โดยคำสั่งใน post-receive จะทำงานหลังจากที่เรามีการใช้คำสั่ง git push ดังนั้นหากเราต้องการจะทำอะไรหลังจาก push โค้ดเสร็จ

#### Scenario 01: trigger jenkins

หลังจากที่มีการสร้าง job ใน Jenkins เราสามารถสั่งให้ Jenkins รันคำสั่ง build project ผ่านลิงค์ได้ ซึ่งลิงค์จะอยู่ในรูปแบบ ลิงค์ในการสั่ง build project ใน Jenkins http://jenkins-server/job/projectname/build

```shell
#!/bin/sh
curl http://jenkins-server/job/projectname/build
```

#### Scenario 02:

เป็นการบอกว่า เมื่อมีการ git push เข้ามา ให้ส่ง source code ไปยัง /var/www/domain.com

```shell
#!/bin/sh
git –work-tree=/var/www/domain.com –git-dir=/var/repo/site.git checkout -f
```

### Scenario 03:

```shell
#!/bin/sh
git checkout -f
touch restart.txt
```

---

`git commit --fixup "<commit>"`

`git commit --squash "<commit>"`

`git subtree`

`git subrepo`

`git show-ref`
