# SSH

## Certificate

There are 4 different ways to present certificates and their components:

**PEM**

:   Governed by RFCs, used preferentially by open-source software because it is
    text-based and therefore less prone to translation/transmission errors. It
    can have a variety of extensions (`.pem`, `.key`, `.cer`, `.cert`, more)

**PKCS7**

:   An open standard used by Java and supported by Windows. Does not contain
    private key material.

**PKCS12**

:   A Microsoft private standard that was later defined in an RFC that provides
    enhanced security versus the plain-text PEM format. This can contain private
    key and certificate chain material. Its used preferentially by Windows systems,
    and can be freely converted to PEM format through use of openssl.

**DER**

:   The parent format of PEM. It's useful to think of it as a binary version of
    the base64-encoded PEM file. Not routinely used very much outside of
    Windows.


## Authenticate with Password and Public Key

First, we set the **SSHD configuration file** for allow support public key and
password authentication methods together.

```text title="~/etc/ssh/sshd_config"
AuthenticationMethods "publickey,password"
```

Add a command to get the public key matching process after the default step for
easy maintenance in the future.

```text title="~/etc/ssh/sshd_config"
AuthorizedKeysCommand /etc/ssh/authorized.sh %u
AuthorizedKeysCommandUser root
```

!!! note

    **AuthorizedKeysCommand** will run after SSH daemon read public key from
    `authorized_keys` and does not found any matching key.

Create bash script with root user,

```bash title="/etc/ssh/authorized.sh"
#!/bin/bash
for file in /home/$1/.ssh/*.pub; do
   cat $file;
done
```

Should grant permission with `sudo chmod 755 /etc/ssh/authorized.sh` for execute
by SSH daemon.

Add your client public key to `~/.ssh/` path, for example, I will add my public
key with `username.pub`.

```text
~/.ssh/
    .
    ..
    authorized_keys
    username.pub
```

Finally, refresh ssh service

=== "Ubuntu/Debian"

    ```shell
    sudo service ssh reload
    ```

Testing,

=== "Default"

    ```shell
    ssh username@hostname
    ```

=== "Fix Private Key Path"

    ```shell
    ssh -i /path/of/private-key/username username@hostname
    ```

## Multiple Public Keys

Generate multi pair of private and public key,

```shell
ssh-keygen -t rsa -f ~/.ssh/id_rsa.home
ssh-keygen -t rsa -f ~/.ssh/id_rsa.work
```

```text title="~/.ssh/config"
Host home
    Hostname home.example.com
    IdentityFile ~/.ssh/id_rsa.home
    User <your home acct>

Host work
    Hostname work.example.com
    IdentityFile ~/.ssh/id_rsa.work
    User <your work acct>
```

## References

- [:material-frequently-asked-questions: Key based SSH login that requires both key AND password](https://askubuntu.com/questions/1019999/key-based-ssh-login-that-requires-both-key-and-password)
