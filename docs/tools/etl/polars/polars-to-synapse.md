# To Azure Synapse Dedicate SQL Pool

## Prerequisite

Install PyPI Packages:

```text
polars
```

## Getting Started

### Using Arrow ODBC

Install PyPI Package for `arrow-odbc`

```text
arrow-odbc
```

#### Read

=== "SQL User"

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

=== "MSI"

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
            f"Authentication=ActiveDirectoryMsi;"
        ),
        max_bytes_per_batch=536_870_912,  # Default: 2 ** 29 (536_870_912)
        batch_size=1_000_000,  # Default: 65_535
    )
    reader.fetch_concurrently()
    for batch in reader:
        df: pl.DataFrame = pl.from_arrow(batch)
    ```

---

#### Write

=== "SQL User"

    ```python
    import os
    import pyarrow as pa
    from arrow_odbc import insert_into_table

    table = df.to_arrow()
    reader = pa.RecordBatchReader.from_batches(
        table.schema, table.to_batches(1000)
    )
    insert_into_table(
        connection_string=(
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={os.getenv('MSSQL_HOST')};"
            f"Port=1433;"
            f"Database={os.getenv('MSSQL_DB')};"
            f"Uid={os.getenv('MSSQL_USER')};"
            f"Pwd={os.getenv('MSSQL_PASS')};"
        ),
        chunk_size=1000,
        table="<schema-name>.<table-name>",
        reader=reader,
    )
    ```

=== "MSI""

    ```python
    import os
    import pyarrow as pa
    from arrow_odbc import insert_into_table

    table = df.to_arrow()
    reader = pa.RecordBatchReader.from_batches(
        table.schema, table.to_batches(1000)
    )
    insert_into_table(
        connection_string=(
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={os.getenv('MSSQL_HOST')};"
            f"Port=1433;"
            f"Database={os.getenv('MSSQL_DB')};"
            f"Authentication=ActiveDirectoryMsi;"
        ),
        chunk_size=1000,
        table="<schema-name>.<table-name>",
        reader=reader,
    )
    ```

---

### Using Py ODBC

Install PyPI Package for `arrow-odbc`

```text
pyodbc sqlalchemy
```

#### Read

#### Write
