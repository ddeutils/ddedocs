# Git Commit Release

This topic will talk about how to write commit message in best practice way.
That mean it will reuse this message for tracking and grouping changes for
`CHANGELOG.md` file.

## Common message

A git commit common message should have a format like:

```console
$ git commit -am "<type>(<scope>): <short-summary-in-present-tense>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>"
```

`<short-summary>`

: - use the imperative, present tense: "change" not "changed" nor "changes" - don't capitalize first letter - no dot (.) at the end

`<type>`

: - `feat`: Features : A new feature. - `fix`: Bugfixes : A bug fix. - `docs`: Documents : Documentation changes. - `style`: Style : Changes that do not affect the meaning of the code
(white-space, formatting, missing semi-colons, etc). - `refactor`: Refactor : A code change that neither fixes a bug nor adds a feature. - `perf`: Improved performance : A code change that improves performance. - `test`: Testing : Changes to the test framework. - `build`: Build : Changes to the build process or tools. - `dep`: Dependencies and Removals : Changes or update dependencies

`<scope>`

: An optional keyword that provides context for where the change was made.
It can be anything relevant to your package or development workflow
(e.g., it could be the module or function name affected by the change).

    Different text in the commit message will trigger PSR to make different
    kinds of releases:

    A `<type>` of fix triggers a patch version bump, e.g.

    ```shell
    git commit -m "fix(mod_plotting): fix confusing error message in plot_words"
    ```

    A `<type>` of feat triggers a minor version bump, e.g.

    ```shell
    git commit -m "feat(package): add example data and new module to package"
    ```

    The text `BREAKING CHANGE:` in the footer will trigger a major release, e.g.

    ```shell
    git commit -m "feat(mod_plotting): move code from plotting module to pycounts module

    BREAKING CHANGE: plotting module won't exist after this release."
    ```

`<body>`

: Just as in the subject, use the imperative, present tense: "change" not
"changed" nor "changes". The body should include the motivation for the
change and contrast this with previous behavior.

`<footer>`

: The footer should contain any information about **Breaking Changes** and is
also the place to [reference GitHub issues that this commit closes](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue).

    **Breaking Changes** should start with the word `BREAKING CHANGE:` with a space or two newlines.

    !!! note

        Any line of the commit message cannot be longer than 100 characters.
        This allows the message to be easier to read on GitHub as well as in
        various git tools.

## Revert message

If the commit reverts a previous commit, it should begin with `revert:`,
followed by the header of the reverted commit.

In the body it should say: `This reverts commit <hash>.`, where the hash is the
SHA of the commit being reverted.

The git revert command will undo only the changes associated with a specific commit

## CHANGELOG.md

the CHANGELOG file like release note for developer can see changes history for any tag version.

If we set up the commit message and already create release for our project, we
can generate a `CHANGELOG.md` file for show the tracking change histories.

We will use `git log` command to show commit message histories.

```shell title="bash script"
#!/usr/bin/env bash
# refs: https://stackoverflow.com/questions/40865597/generate-changelog-from-commit-and-tag
previous_tag=0
for current_tag in $(git tag --sort=-creatordate)
do
if [ "$previous_tag" != 0 ]; then
    tag_date=$(git log -1 --pretty=format:'%ad' --date=short ${previous_tag})
    printf "## ${previous_tag} (${tag_date})\n\n"
    git log ${current_tag}...${previous_tag} \
      --pretty=format:'*  %s [View](https://bitbucket.org/projects/test/repos/my-project/commits/%H)' \
      --reverse | grep -v Merge
    printf "\n\n"
fi
previous_tag=${current_tag}
done
```

```shell
sh change-log-builder.sh > CHANGELOG.md
```

```markdown title="CHANGELOG.md"
## v1.1.0 (2017-08-29)

- Adds IPv6 support [View](http...)
- Adds TreeMaker class and its test. [View](http...)

## v1.0.9 (2017-08-22)

- Updates composer.json.lock [View](http...)

## v1.0.8 (2017-08-22)

- Adds S3Gateway as substitute class [View](http...)
- Remove files no more used [View](http...)
```

In the `CHANGELOG.md` file that will group by typing,

```markdown title="CHANGELOG.md"
## Version 0.1.0

...

**Features**

- `#2094 <https://github.com/<organize>/<project>/pull/2094>`\_
  Add `response()` method for closing a stream in a handler
- `#2097 <https://github.com/<organize>/<project>/pull/2097>`\_
  Allow case-insensitive HTTP Upgrade header
- `#2104 <https://github.com/<organize>/<project>/pull/2104>`\_
  Explicit usage of CIMultiDict getters
- `#2109 <https://github.com/<organize>/<project>/pull/2109>`\_
  Consistent use of error loggers
- `#2114 <https://github.com/<organize>/<project>/pull/2114>`\_
  New `client_ip` access of connection info instance
- `#2133 <https://github.com/<organize>/<project>/pull/2133>`\_
  Implement new version of AST router

  - Proper differentiation between `alpha` and `string` param types
  - Adds a `slug` param type, example: `<foo:slug>`

**Bugfixes**

- `#2119 <https://github.com/<organize>/<project>/pull/2119>`\_
  Fix classes on instantiation for `Config`

...
```

## References

- [Angular Developers Commit](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits)
- [Python Package: 07 Releasing Versioning](https://py-pkgs.org/07-releasing-versioning.html)
