# Git Revert Commit

## Revert commit from remote repository.

First you need to do a `git log` to find out which commit ID you want to revert.
For example, it is commit `abc123`. If you know that it's the last one, you can use a special identifier "HEAD".

Then you first revert it locally in your local "staging" branch:

```shell
git checkout staging
git revert abc123
git push origin staging
```

!!! note

    for the last commit in the log you would write `git revert HEAD`.

## Revert commit with make it gone.

In general the forced push is a bad practice, but keeping useless commits and
reverts around is not nice as well, so another solution would be to actually
create a new branch "staging2" and do your testing in that branch instead:

```shell
git checkout staging
git checkout -b staging2
git reset --hard HEAD^
git push
```

!!! note

    * https://stackoverflow.com/questions/50473587/revert-a-commit-on-remote-branch
    * https://stackoverflow.com/questions/4114095/how-do-i-revert-a-git-repository-to-a-previous-commit
