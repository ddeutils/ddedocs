# SFTP Server

## Gen SSH

```shell
$ ssh-keygen
```

```shell
$ ls -l /home/user/.ssh
-rw------- 1 user user 2610 Feb  7 15:11 id_rsa
-rw-r--r-- 1 user user  573 Feb  7 15:11 id_rsa.pub
```

Take note of the permissions of the private key ( id_rsa ). SSH Private Key
files should **ALWAYS HAVE 600 PERMISSIONS!** If not, change its permission
to the said value using the chmod command:

```shell
$ chmod 600 /home/user/.ssh/id_rsa
```

```shell
$ ssh-copy-id USER@IP
```

If you do not have `ssh-copy-id` available, but you have password-based
SSH access to an account on your server, you can upload your keys using
a conventional SSH method.

```shell
$ cat ~/.ssh/id_rsa.pub | ssh username@remote_host "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

```shell
$ ssh USER@IP
```

## Connect with Python

...
