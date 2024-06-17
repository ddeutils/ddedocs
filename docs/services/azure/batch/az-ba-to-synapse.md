# _To Synapse_

On Batch Pool, it should install Microsoft SQL Server ODBC Driver and Python
packages:

```console
$ pip install azure-identity arrow-odbc polars
```

!!! note

    I recommend `arrow-odbc` and `polars` for loadding performance.

## Using User-Assigned Managed Identity

### 1) Create User-Assigned Managed Identity

- In the `Azure Portal` :octicons-arrow-right-24: Go to `Managed Identities`
  :octicons-arrow-right-24: Click `Create`
- Add your managed identity information :octicons-arrow-right-24: Select `Review + create`

### 2) Grant Access to Synapse

- Go to `Azure Synapse SQL Pool` :octicons-arrow-right-24: Create user from external
  provider and grant permission of this user such as Read access,

    ```sql
    CREATE USER [<user-assigned-name>] FROM EXTERNAL PROVIDER;
    ```

### 3) Enable Azure Batch Account

- Go to `Azure Batch Accounts` :octicons-arrow-right-24: Go to `Pools`
  :octicons-arrow-right-24: Select your Batch Pool
- Go to `Identity` :octicons-arrow-right-24: Nav `User assigned` :octicons-arrow-right-24: Click `Add`
- Select your managed identity that was created from above :octicons-arrow-right-24: Click `Add`

### 4) Connection Code

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
    max_bytes_per_batch=536_870_912,  # Default: 2**29 (536_870_912)
    batch_size=1_000_000,  # Default: 65_535
)
reader.fetch_concurrently()
for batch in reader:
    df: pl.DataFrame = pl.from_arrow(batch)
```
