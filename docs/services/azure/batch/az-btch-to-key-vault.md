# Azure Batch: _To Key Vault_

On Bath Pool, it should install Python

```console
pip install azure-identity azure-keyvault-secrets
```

## Using Managed Identity

!!! warning

    The **system-assigned managed identity** created in a Batch account is only
    used for retrieving customer-managed keys from the Key Vault. This identity
    is not available on Batch pools.

### Create Managed Identity

* In the `Azure Portal` :octicons-arrow-right-24: Go to `Managed Identities`
  :octicons-arrow-right-24: Click `Create`
* Add your managed identity information :octicons-arrow-right-24: Select `Review + create`

### Enable Azure Key Vault

* Go to `Azure Key Vaults` :octicons-arrow-right-24: Select your key vault name
* On `Access control (IAM)` :octicons-arrow-right-24: Click `Add` :octicons-arrow-right-24:
  Assign `Key Vault Secrets User` to your managed identity

!!! tip

    Wait for at least 15 minutes for role to propagate and then try to access.

### Enable Azure Batch Account

* Go to `Azure Batch Accounts` :octicons-arrow-right-24: Go to `Pools`
  :octicons-arrow-right-24: Select your Batch Pool
* Go to `Identity` :octicons-arrow-right-24: Nav `User assigned` :octicons-arrow-right-24: Click `Add`
* Select your managed identity that was created from above :octicons-arrow-right-24: Click `Add`

### Connection Code

```python
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient


def secret_client(keyvault_name: str):
    """Return Secret Client from Managed Identity Authentication."""
    msi_credential = ManagedIdentityCredential()
    return SecretClient(
        vault_url=f"https://{keyvault_name}.vault.azure.net",
        credential=msi_credential
    )
```

## Using Certificate

The computational jobs running on Batch will need to use a certificate to prove
their identity to **Azure AD**, so they can assume the identity of the App you
registered.

!!! danger

    the Azure Batch Account [Certificates](#using-certificate) feature will be
    retired on **February 29, 2024**.

### Generate Certificate

Firstly we need to create a certificate which can be used for authentication.
To do that we're going to generate a **Certificate Signing Request** (CSR) using
`openssl`.

```shell
$ openssl req \
  -newkey rsa:4096 -nodes -keyout "service-principal.key" \
  -out "service-principal.csr"
```

We can now sign that **Certificate Signing Request** (CSR), in this example we're
going to self-sign this certificate using the Key we just generated; however it's
also possible to do this using a Certificate Authority. In order to do that
we're again going to use `openssl`

```shell
$ openssl x509 \
  -signkey "service-principal.key" \
  -in "service-principal.csr" \
  -req -days 365 \
  -out "service-principal.crt"
```

This `service-principal.crt` file you can upload to the App Registration and note the
resulting thumbprint. Then, we have an App Registration with a related certificate.
Finally, we can generate a `.pfx` file which can be used to authenticate with Azure:

```shell
$ openssl pkcs12 -export -out "service-principal.pfx" \
  -inkey "service-principal.key" \
  -in "service-principal.crt"
```

So we will use this `service-principal.pfx` file, providing the thumbprint we got
when we uploaded the certificate to the App Registration for Azure Batch Account.

!!! note

    We will actually need the thumbprint converted from its hexadecimal representation
    to base64. We can use sed to replace the colons and remove `SHA1 Fingerprint=`
    substring, `xxd` to convert to bytes, and `base64` to encode.

    ```shell
    $ echo $(openssl x509 -in "service-principal.csr" -fingerprint -noout) \
      | sed 's/SHA1 Fingerprint=//g' \
      | sed 's/://g' \
      | xxd -r -ps \
      | base64
    ```

    The `service-principal.csr` file contains the public key value of the self-signed
    certificate we generated. We will need to grab that value skipping the first
    and the last lines.

    ```shell
    $ tail -n+2 service-principal.csr | head -n-1
    ```

### Assign Certificate to Service Principle

Sometimes called a public key, a certificate is the recommended credential type
because they're considered more secure than client secrets.

- Go to Azure App registrations :octicons-arrow-right-24: Select `Certificates & secrets` :octicons-arrow-right-24: Click `Certificates`
- Upload the certificate that was created from above step. Select the file you
  want to upload. It must be one of the following file types: `.cer`, `.pem`, `.crt`
  :octicons-arrow-right-24: Select `Add`.

!!! warning

    This accepts the following file formats: `cer`, `pem` and `crt`.

### Assign Certificate to Batch Account

Assigning the certificate to the account lets Batch assign it to the pools and then
to the nodes.

- In the `Azure portal`, in `Batch accounts`, select your batch account.
- Select `Certificates`, select `Add`.
- Upload the `.pfx` file you generated and supply the password
- Pass the certificate thumbprint.
- Select `Create`

Now when you create a Batch pool, you can navigate to `Certificates` within the
pool and assign the certificate that you created in your Batch account to that
pool. When you do so, ensure you select `LocalMachine` for the store location.
The certificate is loaded on all Batch nodes in the pool.

In that setup, the certificates attached to the pool will be available in the folder
defined by an environmental variable `AZ_BATCH_CERTIFICATES_DIR`.

```text
${AZ_BATCH_CERTIFICATES_DIR}/sha1-${THUMBPRINT}.pfx
${AZ_BATCH_CERTIFICATES_DIR}/sha1-${THUMBPRINT}.pfx.pw
```

### Connection Code

If you are using the Azure SDK for python, unfortunately the pfx format is not compatible
with the SDK, so we need to convert it:

```dotenv
CERT_THUMBPRINT=<your-cert-thumbprint>;
CERT_IN="${AZ_BATCH_CERTIFICATES_DIR}/sha1-${CERT_THUMBPRINT}.pfx";
CERT_OUT="${AZ_BATCH_CERTIFICATES_DIR}/cert.pem";
CERT_PWD="${CERT_IN}.pw";
```

```shell
$ openssl pkcs12 -in ${CERT_IN} -out ${CERT_OUT} -nokeys -nodes -password file:${CERT_PWD};
$ openssl pkcs12 -in ${CERT_IN} -nocerts -nodes -password file:${CERT_PWD} \
  | openssl rsa -out ${AZ_BATCH_CERTIFICATES_DIR}/cert.key;
$ cat ${AZ_BATCH_CERTIFICATES_DIR}/cert.key >> CERT_OUT;
```

With these steps, we have converted the `.pfx` certificate file to a `.pem` style
certificate file, which is usable with Python:

```python
import os
from azure.identity import CertificateCredential

CERT_PATH: str = os.environ.get('AZ_BATCH_CERTIFICATES_DIR')

certificate_credential = CertificateCredential(
    tenant_id=os.environ["AZURE_TENANT_ID"],
    client_id=os.environ["CLIENT_ID"],
    certificate_path=f"{CERT_PATH}/cert.pem"
)
```

#### Full Python scripts

```python
import os

CERT_PATH: str = os.environ.get('AZ_BATCH_CERTIFICATES_DIR')

def gen_pem_cert(cert_thumbprint: str):
    # Start pem certificate generation
    os.system(
        (
            f"openssl pkcs12 -in {CERT_PATH}/sha1-{cert_thumbprint}.pfx "
            f"-out {CERT_PATH}/cert.pem -nokeys -nodes "
            f"-password file:{CERT_PATH}/sha1-{cert_thumbprint}.pfx.pw "
            f"2>/dev/null"
        )
    )
    # Start RSA Key generation
    os.system(
        (
            f"openssl pkcs12 -in {CERT_PATH}/sha1-{cert_thumbprint}.pfx "
            f"-nocerts -nodes "
            f"-password file:{CERT_PATH}/sha1-{cert_thumbprint}.pfx.pw "
            f"| openssl rsa -out {CERT_PATH}/cert.key "
            f"2>/dev/null"
        )
    )
    # Combine key with certificate
    os.system(
        f"cat {CERT_PATH}/cert.key >> {CERT_PATH}/cert.pem"
    )

def rm_pem_cert():
    # Start removing Certificate
    os.system(f"rm {CERT_PATH}/cert.key")
    os.system(f"rm {CERT_PATH}/cert.pem")
```

```python
import os
from azure.identity import CertificateCredential
from azure.keyvault.secrets import SecretClient

CERT_PATH: str = os.environ.get('AZ_BATCH_CERTIFICATES_DIR')

def gen_secret_client(
        keyvault_name: str,
        tenant_id: str,
        client_id: str
):
    keyvault_uri = f"https://{keyvault_name}.vault.azure.net"
    credential = CertificateCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        certificate_path=f"{CERT_PATH}/cert.pem"
    )
    return SecretClient(
        vault_url=keyvault_uri,
        credential=credential
    )
```

## References

- https://arsenvlad.medium.com/certificate-based-auth-with-azure-service-principals-from-linux-command-line-a440c4599cae
- https://msendpointmgr.com/2023/03/11/certificate-based-authentication-aad/
- https://learn.microsoft.com/en-us/azure/batch/managed-identity-pools
- https://medium.com/datamindedbe/how-to-access-key-vaults-from-azure-batch-jobs-34388b1adf46
- https://learn.microsoft.com/en-us/azure/batch/batch-customer-managed-key
