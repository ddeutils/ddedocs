# Scenarios

This topic will provide solutions for Git scenario that you want to manage your
Git working find after do something mistake.

## :material-arrow-right-bottom: Reset Removed File

```console
$ rm -r README.md
$ git status
On branch master
Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        deleted:    README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

=== "Delete in Working"

    ```console
    $ git checkout README.md
    Updated 1 path from the index

    $ git status
    On branch master
    nothing to commit, working tree clean
    ```

    !!! note

        Same as `git restore --worktree README.md`

=== "Delete in Staged"

    ```console
    $ git add .
    $ git status
    On branch master
    Changes to be committed:
      (use "git restore --staged <file>..." to unstage)
            deleted:    README.md
    ```

    ```console
    $ git restore --source=HEAD --staged --worktree README.md
    $ git status
    On branch master
    nothing to commit, working tree clean
    ```

    !!! note

        If want to restore to before add to git will use `git restore --staged READMD.md`

=== "Delete in Local Repo"

    ```console
    $ git add .
    $ git commit -m "ACCIDENT COMMIT"
    [master 134bf16] ACCIDENT COMMIT
     1 file changed, 1 deletion(-)
     delete mode 100644 README.md

    $ git log
    commit 5882d01f453beecfec3f252141a9f1bd0761fc35 (HEAD -> master)
    Author: username <username@email.com>
    Date:   Sun Jan 01 00:00:00 1999 +0700

        ACCIDENT COMMIT

    commit 4e133da8b2b77cf9755095bf967d8be78a70c7b9
    Author: username <username@email.com>
    Date:   Sun Jan 01 00:00:00 1999 +0700

        YOUR MESSAGE
    ```

    === "`--soft` option"

        ```console
        $ git reset --soft HEAD~1
        $ git status
        On branch master
        Changes to be committed:
          (use "git restore --staged <file>..." to unstage)
                deleted:    README.md

        username/myproject$ git log
        commit 4e133da8b2b77cf9755095bf967d8be78a70c7b9 (HEAD -> master)
        Author: username <username@email.com>
        Date:   Sun Jan 01 00:00:00 1999 +0700

            YOUR MESSAGE
        ```

    === "`--hard` option"

        ```console
        $ git reset --hard HEAD~1
        HEAD is now at 4e133da YOUR MESSAGE

        $ git status
        On branch master
        nothing to commit, working tree clean

        username/myproject$ git log
        commit 4e133da8b2b77cf9755095bf967d8be78a70c7b9 (HEAD -> master)
        Author: username <username@email.com>
        Date:   Sun Jan 01 00:00:00 1999 +0700

            YOUR MESSAGE
        ```

    !!! note

        `git remove --cached README.md`

---

## :material-arrow-right-bottom: Reset `main` Branch

=== "Deleting `.git`"

    ```shell
    # Clone the project, e.g. `myproject` is my project repository
    $ git clone https://github/username/myproject.git
    $ cd myproject

    # Delete the `.git` folder
    $ git rm -rf .git

    # Now, re-initialize the repository
    $ git init
    $ git remote add origin https://github.com/heiswayi/myproject.git
    $ git remote -v

    # Add all the files and commit the changes
    $ git add --all
    $ git commit -am "Initial commit"

    # Force push update to the main branch of our project repository
    $ git push -f origin main
    ```

=== "Deleting Branch"

    Deleting the `.git` folder may cause problems in our git repository. If we want
    to delete all of our commits history, but keep the code in its current state.

    ```shell
    # Check out to a temporary branch
    $ git checkout --orphan "TEMP_BRANCH"

    # Add all the files
    $ git add -A

    # Commit the changes
    $ git commit -am "Initial commit"

    # Delete the old branch
    $ git branch -D main

    # Rename the temporary branch, "TEMP_BRANCH" to main
    $ git branch -m main

    # Finally, force update to our repository
    $ git push -f origin main
    ```

---

## :material-arrow-right-bottom: Revert Multi-Merge Commits

```shell
git checkout -b <new-branch-name> <revert-commit-id>
git merge --strategy=ours main
git checkout main
git merge <new-branch-name>
```
