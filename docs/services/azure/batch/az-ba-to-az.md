# Connect to Azure Services

## :material-account-check-outline: Authentication

### Using User-Assigned Managed Identity

!!! warning

    The **system-assigned managed identity** created in a Batch account is only
    used for retrieving customer-managed keys from the Key Vault. This identity
    is not available on Batch pools.

#### 1) Create User-Assigned Managed Identity

- In the **Azure Portal** :octicons-arrow-right-24: Go to **Managed Identities**
  :octicons-arrow-right-24: Click **Create**
- Add the managed identity information :octicons-arrow-right-24: Select **Review + create**

#### 2) Enable Azure Batch Account

- Go to **Azure Batch Accounts** :octicons-arrow-right-24: Click **Pools**
  :octicons-arrow-right-24: Select your Batch Pool name
- Go to **Identity** :octicons-arrow-right-24: Nav **User assigned** :octicons-arrow-right-24: Click **Add**
- Select your managed identity that was created from above :octicons-arrow-right-24: Click **Add**

#### 3) Credential Code

Before getting managed identity, you should install the Azure client library;

```shell
pip install -U azure-identity
```

```python
from azure.identity import ManagedIdentityCredential

msi_credential = ManagedIdentityCredential()
```

### Using Certificate

The computational jobs running on Batch will need to use a certificate to prove
their identity to **Azure AD**, so they can assume the identity of the App you
registered.

!!! danger

    the Azure Batch Account [Certificates](#using-certificate) feature will be
    retired on **February 29, 2024**.

#### 1) Generate Certificate

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

#### 2) Assign Certificate to Service Principle

Sometimes called a public key, a certificate is the recommended credential type
because they're considered more secure than client secrets.

- Go to Azure App registrations :octicons-arrow-right-24: Select `Certificates & secrets`
  :octicons-arrow-right-24: Click `Certificates`
- Upload the certificate that was created from above step. Select the file you
  want to upload. It must be one of the following file types: `.cer`, `.pem`, `.crt`
  :octicons-arrow-right-24: Select `Add`.

!!! warning

    This accepts the following file formats: `cer`, `pem` and `crt`.

#### 3) Assign Certificate to Batch Account

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

#### 4) Credential Code

Before getting managed identity, you should install the Azure client library;

```shell
pip install -U azure-identity
```

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

**Full Python scripts**:

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

CERT_PATH: str = os.environ.get('AZ_BATCH_CERTIFICATES_DIR')

credential = CertificateCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    certificate_path=f"{CERT_PATH}/cert.pem"
)
```

---

## :material-microsoft-azure: Services

!!! tip

    Wait for at least 15 minutes for role to propagate and then try to access after
    assign **IAM Role** to target service.

### Key Vault

#### Prerequisite

- Go to **Azure Key Vaults** :octicons-arrow-right-24: Select your key vault name, `kv-demo`
- On **Access control (IAM)** :octicons-arrow-right-24: Click **Add** :octicons-arrow-right-24:
  Assign **Key Vault Secrets User** to your user-assigned managed identity

#### Connection Code

Before develop code, you should install Azure Key Vault client library;

```shell
pip install azure-keyvault-secrets
```

Implement connection code to the **Azure Batch Node** that use to get any secrets
from **Azure Key Vault**.

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

??? note "Reference Links"

    - https://arsenvlad.medium.com/certificate-based-auth-with-azure-service-principals-from-linux-command-line-a440c4599cae
    - https://msendpointmgr.com/2023/03/11/certificate-based-authentication-aad/
    - https://learn.microsoft.com/en-us/azure/batch/managed-identity-pools
    - https://medium.com/datamindedbe/how-to-access-key-vaults-from-azure-batch-jobs-34388b1adf46
    - https://learn.microsoft.com/en-us/azure/batch/batch-customer-managed-key

---

### Synapse

#### Prerequisite

-   Go to **Azure Synapse SQL Pool** :octicons-arrow-right-24: Create user from external
    provider and grant permission of this user such as **Read** access,

    ```sql
    CREATE USER [<user-assigned-name>] FROM EXTERNAL PROVIDER;
    ```

#### Connection Code

Before develop code, you should install DataFrame API library;

```shell
pip install arrow-odbc polars
```

!!! note

    I recommend `arrow-odbc` and `polars` for loadding performance.

```python
import os
import polars as pl
from arrow_odbc import read_arrow_batches_from_odbc

reader = read_arrow_batches_from_odbc(
    query="SELECT * FROM <schema-name>.<table-name>",
    connection_string=(
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server={os.getenv('MSSQL_HOST')};"
        f"Port=1433;"
        f"Database={os.getenv('MSSQL_DB')};"
        f"Uid={os.getenv('MSSQL_USER')};"
        f"Pwd={os.getenv('MSSQL_PASS')};"
    ),
    max_bytes_per_batch=536_870_912,  # Default: 2 ** 29 (536_870_912)
    batch_size=1_000_000,  # Default: 65_535
)
reader.fetch_concurrently()
for batch in reader:
    df: pl.DataFrame = pl.from_arrow(batch)
```

---

### DataLake

#### Prerequisite

- Go to **Azure Storage Accounts** :octicons-arrow-right-24: Select your storage account name
- On **Access control (IAM)** :octicons-arrow-right-24: Click **Add** :octicons-arrow-right-24:
  Assign **Storage Blob Data Contributor** to your user-assigned managed identity

#### Connection Code

Before develop code, you should install Azure Datalake Storage client library;

```shell
pip install azure-storage-file-datalake cffi
```

```python
from azure.identity import ManagedIdentityCredential
from azure.storage.filedatalake import DataLakeServiceClient


def lake_client(storage_account_name) -> DataLakeServiceClient:
    """Generate ADLS Client from input credential"""
    msi_credential = ManagedIdentityCredential()
    return DataLakeServiceClient(
        account_url=f"https://{storage_account_name}.dfs.core.windows.net",
        credential=msi_credential
    )
```

??? note "More Codes"

    ```python
    import io
    import pathlib

    import pyarrow.parquet as pq
    import pandas as pd
    from azure.core.exceptions import ResourceNotFoundError
    from azure.identity import ManagedIdentityCredential
    from azure.storage.filedatalake import (
        DataLakeServiceClient,
        DataLakeFileClient,
    )


    def lake_client(storage_account_name) -> DataLakeServiceClient:
        """Generate ADLS Client from input credential"""
        msi_credential = ManagedIdentityCredential()
        return DataLakeServiceClient(
            account_url=f"https://{storage_account_name}.dfs.core.windows.net",
            credential=msi_credential
        )


    def exists(
        client: DataLakeServiceClient,
        container: str,
        filepath: str,
    ) -> bool:
        """Return True if filepath on target container exists."""
        try:
            (
                client
                    .get_file_system_client(file_system=container)
                    .get_file_client(filepath)
                    .get_file_properties()
            )
            return True
        except ResourceNotFoundError:
            return False

    def download(
        client: DataLakeServiceClient,
        container: str,
        filepath: str,
    ) -> pathlib.Path:
        file_client: DataLakeFileClient = (
            client
                .get_file_system_client(file_system=container)
                .get_file_client(filepath)
        )
        output_file = pathlib.Path(filepath)
        output_file.parent.mkdir(exist_ok=True, parents=True)
        with output_file.open(mode='wb') as local_file:
            file_client.download_file().readinto(local_file)
        return output_file


    def upload(
        client: DataLakeServiceClient,
        container: str,
        dirpath: str,
        file: str,
        df: pd.DataFrame,
    ) -> DataLakeFileClient:
        dir_client: DataLakeFileClient = (
            client
                .get_file_system_client(file_system=container)
                .get_directory_client(directory=dirpath)
        )
        file_client = dir_client.create_file(file)

        # If Upload Parquet file
        io_file = df.to_parquet()

        # Or, file_client.append_data(data=df, offset=0, length=len(df))
        file_client.upload_data(data=io_file, overwrite=True)
        file_client.flush_data(len(io_file))
        return file_client


    def to_pyarrow(
        client: DataLakeServiceClient,
        container: str,
        filepath: str,
    ) -> pq.Table:
        file_client: DataLakeFileClient = (
            client
                .get_file_system_client(file_system=container)
                .get_file_client(filepath)
        )
        data = file_client.download_file(0)
        with io.BytesIO() as b:
            data.readinto(b)
            table = pq.read_table(b)
        return table
    ```
