# Azure Synapse Analytic: _External Data_

A **Database Credential** is not mapped to a server login or database user. The
credential is used by the database to access to the external location
anytime the database is performing an operation that requires access.

## Database Scope Credential

=== "Azure AD"

    ```sql
    CREATE EXTERNAL DATA SOURCE <external-data-source>
    WITH (
        LOCATION  = 'https://<storage_account>.dfs.core.windows.net/<container>/<path>'
    )
    ```

=== "Managed Identity"

    ```sql
    -- Optional: Create MASTER KEY if not exists in database:
    CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'P@ssW0rd'
    GO

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
    -- Optional: Create MASTER KEY if not exists in database:
    CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'P@ssW0rd'
    GO

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

    !!! note

        **authority-url** like `https://login.microsoftonline.com/<tenant-id>/oauth2/token`

=== "Shared Access Signature"

    ```sql
    -- Optional: Create MASTER KEY if not exists in database:
    CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'P@ssW0rd'
    GO

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

If the master key already exists on the database, you can use:

```
OPEN MASTER KEY DECRYPTION BY PASSWORD = 'P@ssW0rd';
...
CLOSE MASTER KEY;
```

### List of all Credentials

```sql
SELECT * FROM [sys].[database_scoped_credentials]
;
```

!!! example

    ```sql
    CREATE LOGIN <username> WITH PASSWORD = 'P@ssW0rd'
    GO

    GRANT REFERENCES ON DATABASE SCOPED CREDENTIAL::<credential-name> TO <username>
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

    GRANT SELECT ON OBJECT::[DEVDWHCURATED].[VW_DELTA_DIS_T_SALEFPRCA_ADB] TO adbuser
    GO
    ```

## External Data Source

=== "Dedicate SQL Pool"

    ```sql
    CREATE EXTERNAL DATA SOURCE [<external-data-source-name>]
    WITH(
        LOCATION = 'abfss://<container>@<storage-account>.dfs.core.windows.net',
        CREDENTIAL = <credential-anme>,
        TYPE = HADOOP
    );
    ```

    !!! note

        PolyBase data virtualization is used when the `EXTERNAL DATA SOURCE`
        is created with `TYPE=HADOOP`.

=== "Serverless SQL Pool"

    ```sql
    CREATE EXTERNAL DATA SOURCE [<external-data-source-name>]
    WITH(
        LOCATION = 'abfss://<container>@<storage-account>.dfs.core.windows.net'
    );
    ```

## External File Format

```sql
CREATE EXTERNAL FILE FORMAT <parquet_snappy>
WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);
```

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

## Examples

### Copy data from Azure Blob to Table

- https://www.sqlservercentral.com/articles/loading-data-in-azure-synapse-using-copy

## References

- https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/develop-storage-files-storage-access-control?tabs=user-identity
- https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-data-source-transact-sql?view=azure-sqldw-latest&preserve-view=true&tabs=dedicated
- https://learn.microsoft.com/en-us/sql/t-sql/statements/create-external-file-format-transact-sql
