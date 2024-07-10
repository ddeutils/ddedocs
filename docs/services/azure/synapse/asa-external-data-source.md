# External Data Source

## :material-arrow-right-bottom: Database Scope Credential

A **Database Credential** is not mapped to a server login or database user. The
credential is used by the database to access to the external location anytime the
database is performing an operation that requires access.

### List Credentials

```sql
SELECT * FROM [sys].[database_scoped_credentials];
```

### Create Master Key

Create a new Master Key, `ENCRYPTION` to encrypt the credentials for the external
data source.

```sql
-- Optional: Create MASTER KEY if not exists in database:
CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'P@ssW0rd'
GO
```

If the master key already exists on the database, you can use:

```sql
OPEN MASTER KEY DECRYPTION BY PASSWORD = 'P@ssW0rd';
...
CLOSE MASTER KEY;
```

### Create Credential

=== "Managed Identity"

    ```sql
    CREATE DATABASE SCOPED CREDENTIAL <credential-name>
    WITH IDENTITY = 'Managed Identity'
    GO

    CREATE EXTERNAL DATA SOURCE <external-data-source>
    WITH (
        LOCATION   = 'https://<storage_account>.dfs.core.windows.net/<container>/<path>',
        CREDENTIAL = <credential-name>
    )
    ```

=== "Service Principle"

    ```sql
    -- authority-url: `https://login.microsoftonline.com/<tenant-id>/oauth2/token`
    CREATE DATABASE SCOPED CREDENTIAL <credential-name>
    WITH IDENTITY = '<client-id>@<authority-url>',
        SECRET = '<client-secret>'
    GO

    CREATE EXTERNAL DATA SOURCE <external-data-source>
    WITH (
        LOCATION   = 'https://<storage_account>.dfs.core.windows.net/<container>/<path>',
        CREDENTIAL = <credential-name>
    )
    ```

=== "Shared Access Signature"

    ```sql
    -- The secret value must remove the leading '?'
    CREATE DATABASE SCOPED CREDENTIAL <credential-name>
    WITH IDENTITY = 'SHARED ACCESS SIGNATURE',
        SECRET = 'sv=2018-03-28&ss=bfqt&...&sig=lQHczN...'
    GO

    CREATE EXTERNAL DATA SOURCE <external-data-source>
    WITH (
        LOCATION   = 'https://<storage_account>.dfs.core.windows.net/<container>/<path>',
        CREDENTIAL = <credential-name>
    )
    ```

And the permission of **User**, **Managed Identity**, or **Service Principle** that want to
access data on target external data source should be any role in
`Storage Blob Data Owner/Contributor/Reader` roles in order for the application
to access the data via RBAC in **Azure Portal**.

!!! example

    ```sql
    USE [master];
    CREATE LOGIN [username] WITH PASSWORD = 'P@ssW0rd';
    GO

    USE [database];
    CREATE USER [username] FROM LOGIN [username];
    GRANT REFERENCES ON DATABASE SCOPED CREDENTIAL::[credential-name] TO [username];
    GO
    ```

    ```sql
    IF NOT EXISTS (
        SELECT *
        FROM [sys].[external_data_sources]
        WHERE [name] = '<external-data-source-name>'
    )
        CREATE EXTERNAL DATA SOURCE <external-data-source-name>
        WITH (
            CREDENTIAL = <credential-name>,
            LOCATION = 'abfss://<container>@<storage-account>.dfs.core.windows.net'
        )
    GO
    ```

    ```sql
    CREATE OR ALTER VIEW [CURATED].[<view-name>]
    AS
        SELECT *
        FROM OPENROWSET(
            BULK '/delta_silver/<delta-table-name>',
            DATA_SOURCE = '<external-data-source-name>',
            FORMAT = 'DELTA'
    ) AS [r]
    GO

    GRANT SELECT ON OBJECT::[CURATED].[<view-name>] TO <user-name>
    GO
    ```

---

## :material-arrow-right-bottom: External Data Source

### List Data Source

```sql
SELECT * FROM [sys].[external_data_sources];
```

### Create Data Source

=== ":material-database-settings-outline: Dedicate SQL Pool"

    ```sql
    CREATE EXTERNAL DATA SOURCE [<external-data-source>]
    WITH(
        LOCATION = 'abfss://<container>@<storage-account>.dfs.core.windows.net',
        CREDENTIAL = <credential-name>,
        PUSHDOWN = ON,
        TYPE = HADOOP
    );
    ```

    !!! note

        **PolyBase** data virtualization is used when the `EXTERNAL DATA SOURCE`
        is created with `TYPE=HADOOP`.

        `PUSHDOWN = ON | OFF` is set to `ON` by default, meaning the ODBC Driver
        can leverage server-side processing for complex queries.

=== ":material-database-off-outline: Serverless SQL Pool"

    ```sql
    CREATE EXTERNAL DATA SOURCE [<external-data-source>]
    WITH(
        LOCATION = 'abfss://<container>@<storage-account>.dfs.core.windows.net',
        CREDENTIAL = <credential-name>
    );
    ```

For the `LOCATION`, it provide the connectivity protocol and path to the external
data source. See [More Supported Protocol](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=azure-sqldw-latest&preserve-view=true&tabs=serverless#location--prefixpath)

!!! note

    If you want to use **Azure AD** for access an external data source you can use:

    ```sql
    -- The Permission from this solution will up to user that want to access
    -- target external data source.
    CREATE EXTERNAL DATA SOURCE [<external-data-source>]
    WITH (
        LOCATION  = 'https://<storage_account>.dfs.core.windows.net/<container>/<path>'
    )
    ```

---

## :material-arrow-right-bottom: External File Format

### List File Format

```sql
SELECT * FROM [sys].[external_file_formats]
```

### Create File Format

```sql
CREATE EXTERNAL FILE FORMAT <parquet_snappy>
WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);
```

=== "CSV"

    ```sql
    CREATE EXTERNAL FILE FORMAT <skip_header_csv>
    WITH (
        FORMAT_TYPE = DELIMITEDTEXT,
        FORMAT_OPTIONS(
            FIELD_TERMINATOR    = ',',
            STRING_DELIMITER    = '"',
            FIRST_ROW           = 2,
            USE_TYPE_DEFAULT    = True
        )
    );
    ```

=== "JSON"

    ```sql
    CREATE EXTERNAL FILE FORMAT <json-format>
    WITH (
        FORMAT_TYPE = JSON,
        DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
    );
    ```

=== "DELTA"

    ```sql
    CREATE EXTERNAL FILE FORMAT <delta-format>
    WITH (
        FORMAT_TYPE = DELTA
    );
    ```

---

## :material-arrow-right-bottom: External Table

=== "Serverless SQL Pool"

    ```sql
    CREATE EXTERNAL TABLE [CURATED].[<external-table-name>]
    (
        [PurposeId] [varchar](max),
        [RetireOnDate] [datetime],
        [CreatedDate] [datetime]
    )
    WITH (
        DATA_SOURCE = [<data-source-name>],
        FILE_FORMAT = [<external-file-format>],
        LOCATION = N'/path/of/data/date=20240708'
    )
    GO
    ```

## :material-playlist-plus: Read Mores

- [Microsoft: Develop Storage Files Access Control](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/develop-storage-files-storage-access-control?tabs=user-identity)
- [Microsoft: TSQL - Create External Data Source](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=azure-sqldw-latest&preserve-view=true&tabs=dedicated)
- [Microsoft: TSQL - Create External File Format](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-file-format-transact-sql)
- [Medium: Query Azure Data Lake via Synapse Serverless Security](https://medium.com/@diangermishuizen/query-azure-data-lake-via-synapse-serverless-security-credentials-setup-eedb5175d5da)
