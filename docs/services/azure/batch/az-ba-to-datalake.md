# _To DataLake Storage_

On Bath Pool, it should install Python package:

```console
$ pip install -U azure-identity azure-storage-file-datalake cffi
```

## Using User-Assigned Managed Identity

### 1) Create Managed Identity

- In the `Azure Portal` :octicons-arrow-right-24: Go to `Managed Identities`
  :octicons-arrow-right-24: Click `Create`
- Add your managed identity information :octicons-arrow-right-24: Select `Review + create`

### 2) Enable Azure DataLake Storage

- Go to `Azure Storage Accounts` :octicons-arrow-right-24: Select your storage account name
- On `Access control (IAM)` :octicons-arrow-right-24: Click `Add` :octicons-arrow-right-24:
  Assign `Storage Blob Data Contributor` to your managed identity

### 3) Connection Code

```python
import io
import pathlib

import pyarrow.parquet as pq
import pandas as pd
from azure.core.exceptions import ResourceNotFoundError
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
