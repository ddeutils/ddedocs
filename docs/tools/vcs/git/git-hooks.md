# Git: _Hooks_

`git hooks` ชุดของคำสั่งที่ Git จะเรียก ก่อนหรือหลังคำสั่งหลักใดๆ เช่น commit, push

Git hooks เป็นสิ่งที่ติดตัวมากับ Git อยู่แล้วไม่ต้องไปดาวโหลดอะไรมาลงเพิ่มและ Git hooks นั้นเป็นฟีเจอร์ที่จำทำงานแบบ local หรือเฉพาะเครื่องของคนๆนั้นเท่านั้น

> NOTE:
>
> ```shell
> $ git config --global core.hooksPath /path/to/my/centralized/hooks
> $ git config --local core.hooksPath /path/to/my/centralized/hooks
> ```

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

#### Scenario 03:

```shell
#!/bin/sh
git checkout -f
touch restart.txt
```
