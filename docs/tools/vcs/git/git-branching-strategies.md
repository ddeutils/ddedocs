# Git Branching Strategies

[:material-youtube: Git - Branching Strategies Explained](https://www.youtube.com/watch?v=U_IFGpJDbeU)

## The Mainline branches

It's the simplest but most effective way for small teams. Because of working
only on the main branch. So this main branch has to be deployed/published
all the time.

For each developer will work on his local branch. If a develop process was
finished, it would merge a code to main branch.

- **master**

  The source code of `HEAD` always reflects a _production-ready_
  state.

- **develop**

  The source code of `HEAD` always reflects a state with the
  latest delivered development changes for the next release.

!!! note

    Sometime we will split tag version in `master` to `stable` for keeping
    only release tag change.

!!! warning

    For each feature, it should be small work. If it has long or more code
    change, it will affect to main branch and has more conflict code.

## The Supporting branches

### Feature branches

Manage code in separate branches for each feature. When developers complete
development and testing, they merge the code from the feature branch into the
integration branch. After that, another round of testing is conducted on the
integration branch. When everything is ready, the code is merged back into the
main branch.

Therefore, the state of the code on the main branch is always ready for
deployment/release.

- **May branch off from:** `develop`
- **Must merge back into:** `develop`
- **Branch naming convention:** anything except `master`, `develop`, `release-*`,
  `support-*`, or `hotfix-*`

!!! warning

    Things to be cautious about include the lifespan of feature branches or
    prolonged development. Maintaining them becomes increasingly difficult.

!!! example

    Creating a feature branch:

    ```console
    $ git checkout -b myfeature develop
    Switched to a new branch "myfeature"
    ```

    Incorporating a finished feature on develop:

    ```console
    $ git checkout develop
    Switched to branch 'develop'

    $ git merge --no-ff myfeature
    Updating ea1b82a..05e9557
    (Summary of changes)

    $ git branch -d myfeature
    Deleted branch myfeature (was 05e9557).

    $ git push origin develop
    ```

    !!! info

        The `--no-ff` flag causes the merge to always create a new commit
        object, even if the merge could be performed with a fast-forward.
        This avoids losing information about the historical existence of a
        feature branch and groups together all commits that together added
        the feature.

### Environment branches

- **May branch off from:** `master`
- **Must merge back into:** `Next environment`
- **Branch naming convention:** `testing`, `production`, `staging`,
  `pre-production`

### Release branches

Separate according to each version of the system. However, the main work
remains in the main branch.

But the problem that follows is the management and maintenance in each
branch or release, which, first of all, requires editing and merging into
the main branch and then using the Git feature called **Cherry Pick**.

To pick up the changes to different branches or releases. And if you make
changes in each branch or release, you must also Cherry Pick them to the
main branch.

This policy or working method is called **Upstream First**.

- **May branch off from:** `develop`
- **Must merge back into:** `develop` and `master`
- **Branch naming convention:** `release-*`

!!! example

    Creating a release branch:

    ```console
    $ git checkout -b release-1.2 develop
    Switched to a new branch "release-1.2"

    $ ./bump-version.sh 1.2
    Files modified successfully, version bumped to 1.2.

    $ git commit -a -m "Bumped version number to 1.2"
    [release-1.2 74d9424] Bumped version number to 1.2
    1 files changed, 1 insertions(+), 1 deletions(-)
    ```

    Finishing a release branch:

    ```console
    $ git checkout master
    Switched to branch 'master'

    $ git merge --no-ff release-1.2
    Merge made by recursive.
    (Summary of changes)

    $ git tag -a 1.2
    ```

    > You might as well want to use the -s or -u <key> flags to sign your
    > tag cryptographically.

    ```console
    $ git checkout develop
    Switched to branch 'develop'

    $ git merge --no-ff release-1.2
    Merge made by recursive.
    (Summary of changes)

    $ git branch -d release-1.2
    Deleted branch release-1.2 (was ff452fe).
    ```

### Hotfix branches

- **May branch off from:** `master`
- **Must merge back into:** `develop` and `master`
- **Branch naming convention:** `hotfix-*`

!!! example

    Creating the hotfix branch:

    ```console
    $ git checkout -b hotfix-1.2.1 master
    Switched to a new branch "hotfix-1.2.1"

    $ ./bump-version.sh 1.2.1
    Files modified successfully, version bumped to 1.2.1.

    $ git commit -a -m "Bumped version number to 1.2.1"
    [hotfix-1.2.1 41e61bb] Bumped version number to 1.2.1
    1 files changed, 1 insertions(+), 1 deletions(-)
    ```

    ```console
    $ git commit -m "Fixed severe production problem"
    [hotfix-1.2.1 abbe5d6] Fixed severe production problem
    5 files changed, 32 insertions(+), 17 deletions(-)
    ```

    Finishing a hotfix branch:

    ```console
    $ git checkout master
    Switched to branch 'master'

    $ git merge --no-ff hotfix-1.2.1
    Merge made by recursive.
    (Summary of changes)

    $ git tag -a 1.2.1
    ```

    > You might as well want to use the -s or -u <key> flags to sign your
    > tag cryptographically.

    ```console
    $ git checkout develop
    Switched to branch 'develop'

    $ git merge --no-ff hotfix-1.2.1
    Merge made by recursive.
    (Summary of changes)
    ```

    > The one exception to the rule here is that, **when a release branch
    > currently exists, the hotfix changes need to be merged into that
    > release branch, instead of** `develop`. Back-merging the bugfix into
    > the release branch will eventually result in the bugfix being merged
    > into `develop` too, when the release branch is finished. (If work in
    > `develop` immediately requires this bugfix and cannot wait for the
    > release branch to be finished, you may safely merge the bugfix into
    > `develop` now already as well.)

    ```shell
    $ git branch -d hotfix-1.2.1
    Deleted branch hotfix-1.2.1 (was abbe5d6).
    ```

### Support branches

- **May branch off from:** `tag`
- **Must merge back into:** `None`
- **Branch naming convention:** `support-*`

!!! example

    Creating the support branch:

    ```console
    $ git checkout -b support-1.2.1.1 v1.2.1
    Switched to a new branch "support-1.2.1.1"

    $ ./bump-version.sh 1.2.1.1
    Files modified successfully, version bumped to 1.2.1.1.

    $ git commit -a -m "Bumped version number to 1.2.1.1"
    [support-1.2.1.1 13ds7e2] Bumped version number to 1.2.1.1
    1 files changed, 1 insertions(+), 1 deletions(-)
    ```

    > Support branches would be created “on demand” when requested by
    > customers who are stuck on legacy releases and are not able to move
    > forward to current releases, but need security and other bug fixes.

## References

- [Successful Git Branch Model](https://nvie.com/posts/a-successful-git-branching-model/)
