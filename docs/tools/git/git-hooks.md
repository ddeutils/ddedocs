# Git Hooks

`git hooks` ชุดของคำสั่งที่ Git จะเรียก ก่อนหรือหลังคำสั่งหลักใดๆ เช่น commit, push

Git hooks เป็นสิ่งที่ติดตัวมากับ Git อยู่แล้วไม่ต้องไปดาวโหลดอะไรมาลงเพิ่มและ Git hooks นั้นเป็นฟีเจอร์ที่จำทำงานแบบ
local หรือเฉพาะเครื่องของคนๆนั้นเท่านั้น

!!! note

    ```shell
    $ git config --global core.hooksPath /path/to/my/centralized/hooks
    $ git config --local core.hooksPath /path/to/my/centralized/hooks
    ```

Let’s have a look what kind of local hooks we have in our repository’s `.git/hooks`
folder :

```text
.git/hooks
  ├── applypatch-msg.sample
  ├── commit-msg.sample
  ├── post-update.sample
  ├── pre-applypatch.sample
  ├── pre-commit.sample
  ├── prepare-commit-msg.sample
  ├── pre-rebase.sample
  └── update.sample
```

### Post Receive

`git config receive.denycurrentbranch ignore`

post-receive จะทำหน้าที่คือ เมื่อ push เข้า origin master เมื่อไร code จะถูก update อัตโนมัติ
และคำสั่งภายใน ./git/hooks/post-receive ก็จะถูกรัน

โดยคำสั่งใน post-receive จะทำงานหลังจากที่เรามีการใช้คำสั่ง git push ดังนั้นหากเราต้องการจะทำอะไรหลังจาก push โค้ดเสร็จ

=== "Scenario 01: trigger jenkins"

    หลังจากที่มีการสร้าง job ใน Jenkins เราสามารถสั่งให้ Jenkins รันคำสั่ง build project ผ่านลิงค์ได้ ซึ่งลิงค์จะอยู่ในรูปแบบ ลิงค์ในการสั่ง build project ใน Jenkins http://jenkins-server/job/projectname/build

    ```shell
    #!/bin/sh
    curl http://jenkins-server/job/projectname/build
    ```

=== "Scenario 02"

    เป็นการบอกว่า เมื่อมีการ git push เข้ามา ให้ส่ง source code ไปยัง /var/www/domain.com

    ```shell
    #!/bin/sh
    git --work-tree=/var/www/domain.com --git-dir=/var/repo/site.git checkout -f
    ```

=== "Scenario 03"

    ```shell
    #!/bin/sh
    git checkout -f
    touch restart.txt
    ```

## Jira with Git

Reference: [Hook story ID from Jira](https://medium.com/@kennwuttisasiwat/%E0%B9%80%E0%B8%95%E0%B8%B4%E0%B8%A1-story-id-%E0%B8%94%E0%B9%89%E0%B8%B2%E0%B8%99%E0%B8%AB%E0%B8%99%E0%B9%89%E0%B8%B2-commit-message-%E0%B8%AD%E0%B8%B1%E0%B8%95%E0%B9%82%E0%B8%99%E0%B8%A1%E0%B8%B1%E0%B8%95%E0%B8%B4-%E0%B8%94%E0%B9%89%E0%B8%A7%E0%B8%A2-git-hook-13b8129efb76)

Jira is software management tool. ไม่ว่าจะเป็นการใช้ Development life cycle แบบไหนก็แล้วแต่ เช่น Agile, Scrum, Waterfall โดยแต่ละงานที่ถูกสร้างขึ้นมาจะเรียกว่า Ticket

ถ้าสังเกตทุก ticket จะมี auto-increment number ให้เช่น JIRA-1 JIRA-2 JIRA-3 ซึ่งในบทความนี้จะขอเรียกหมายเลขข้างต้นนี้ว่า “Story-ID” (บางที่อาจจะเรียก Ticket-ID, Jira-ID, etc.)

ในเหตุการณ์จริงสมมติว่ามี branch ที่ถูกทำงานอยู่พร้อมๆกัน 4 branch ในแต่ละ branch เกิด commit ขึ้นประมาณ 5–20 commits
ถ้าสมมติว่า merge รวมกัน จะเกิดปัญหา commit จากทั้ง 4 branch จะถูกนำมาเรียงตามลำดับการเกิดขึ้น (timestamp) แล้วเมื่อเราต้องการจะ trace กลับไปปัญหาคือ ยากและค่อนข้างเสียเวลา

ในบางการทำงานจึงนิยมที่จะต้องใส่ `[STORY-ID] Commit message`
Story-ID ต่อหน้าชื่อคอมมิทเพื่อง่ายต่อการแกะรอยย้อนกลับ

ซึ่งในบทความนี้เราจะเจาะลงไปใช้ hook ที่ชื่อว่า “prepare-commit-msg” ซึ่งเป็น hook ที่จะถูกเรียกใช้หลังจากที่เราสั่ง commit -m หรือใส่ message นั่นเอง
โดยที่ hook นี้จะสามารถนำ message ที่เราใส่ขึ้นมา modify ก่อนที่จะทำการเขียนลงไปได้

### Create script in `.git/hooks/prepare-commit-msg.sh`

we simply rename `prepare-commit-msg.sample` to `prepare-commit-msg`, paste the script listed below and ensure that the file is executable.

#### Example01

```shell
#!/bin/bash

# This way you can customize which branches should be skipped when
# prepending commit message.
if [ -z "$BRANCHES_TO_SKIP" ]; then
   BRANCHES_TO_SKIP=(master develop test)
fi
BRANCH_NAME=$(git symbolic-ref --short HEAD)
BRANCH_NAME="${BRANCH_NAME##*/}"
BRANCH_EXCLUDED=$(printf "%s\n" "${BRANCHES_TO_SKIP[@]}" | grep -c "^$BRANCH_NAME$")
BRANCH_IN_COMMIT=$(grep -c "\[$BRANCH_NAME\]" $1)
if [ -n "$BRANCH_NAME" ] && ! [[ $BRANCH_EXCLUDED -eq 1 ]] && ! [[ $BRANCH_IN_COMMIT -ge 1 ]]; then
   sed -i.bak -e "1s/^/[$BRANCH_NAME] /" $1
fi
```

> NOTE: Reference code: https://gist.github.com/bartoszmajsak/1396344

```shell
#!/bin/bash

# For instance with feature/add_new_feature_HEYT-653
# $ git commit -m"Fixed bug"
# will result with commit "[HEYT-653] Fixed bug"


# Customize which branches should be skipped when prepending commit message.
if [ -z "$BRANCHES_TO_SKIP" ]; then
  BRANCHES_TO_SKIP=(master develop test)
fi

BRANCH_NAME=$(git symbolic-ref --short HEAD | grep -o '[A-Z]\+-[0-9]\+')
BRANCH_NAME="${BRANCH_NAME##*/}"

BRANCH_EXCLUDED=$(printf "%s\n" "${BRANCHES_TO_SKIP[@]}" | grep -c "^$BRANCH_NAME$")
BRANCH_IN_COMMIT=$(grep -c "\[$BRANCH_NAME\]" $1)

if [ -n "$BRANCH_NAME" ] && ! [[ $BRANCH_EXCLUDED -eq 1 ]] && ! [[ $BRANCH_IN_COMMIT -ge 1 ]]; then
  sed -i.bak -e "1s/^/[$BRANCH_NAME] /" $1
fi
```

> NOTE:
>
> ```
> BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD 2> /dev/null | grep -oE "[A-Z]+-[0-9]+")
> if [ -n "$BRANCH_NAME" ]; then
>     echo "[$BRANCH_NAME] $(cat $1)" > $1
> fi
> ```

```shell
#!/bin/bash

# This way you can customize which branches should be skipped when
# prepending commit message.
if [ -z "$BRANCHES_TO_SKIP" ]; then
  BRANCHES_TO_SKIP=(master develop test)
fi

BRANCH_NAME=$(git symbolic-ref --short HEAD)
BRANCH_NAME="${BRANCH_NAME##*/}"

BRANCH_EXCLUDED=$(printf "%s\n" "${BRANCHES_TO_SKIP[@]}" | grep -c "^$BRANCH_NAME$")
BRANCH_IN_COMMIT=$(grep -c "\[$BRANCH_NAME\]" $1)

if [ -n "$BRANCH_NAME" ] && ! [[ $BRANCH_EXCLUDED -eq 1 ]] && ! [[ $BRANCH_IN_COMMIT -ge 1 ]]; then
  sed -i.bak -e "1s/^/[$BRANCH_NAME] /" $1
fi
```

## Deployment

Reference: [How to setup deployment with Git](https://myifew.com/3932/how-to-set-up-deployment-with-git/)

https://engineerball.com/blog/2014/05/05/%e0%b9%83%e0%b8%8a%e0%b9%89-git-hook-%e0%b9%80%e0%b8%9e%e0%b8%b7%e0%b9%88%e0%b8%ad-deploy-code.html

https://www.imooh.com/git-hook-trigger-jenkins-build-job

## Bump-Version

The bump version is the script that auto update `CHANGELOG.md` file with all
commit messages after the latest bump version or first initial commit.

General digit of version naming, like `v1.2.3`, will mean
`v${Major}.${Minor}.${Patch}.${Support}`, reference from [semver](https://semver.org/)

Generate commit message:

```console
$ git log --pretty=format:"  - %s" "v$BASE_STRING"...HEAD
```

Auto generate version (Only increment last number):

```console
$ $(eval VERSION=$(`shell git describe --tags --abbrev=0 | awk -F. '{OFS="."; $NF+=1; print $0}'`))
$ git add .
$ git commit -m "$m"
$ git push origin master
$ git tag -a $(VERSION) -m "new release"
$ git push origin $(VERSION)
```

**Examples of Bump-version script**:

- [BUMP-VERSION-shell](https://gist.github.com/Nomane/df017387aaa2d24cbacb5da3a55256cf)
- [BUMP-VERSION-shell-v2](https://gist.github.com/jv-k/703e79306554c26a65a7cfdb9ca119c6)
