# Partition View

!!! warning

    The `OPENROWSET` syntax can use **Azure Synapse Serverless SQL Pool** only

## :material-arrow-down-right: Getting Started

### Manage Permission

1.  Remove bulk operations on master

    ```sql
    USE [master];
    DENY ADMINISTER BULK OPERATIONS TO [username];
    DENY ADMINISTER BULK OPERATIONS TO [public];
    GO
    ```

2.  Grant bulk operations on the database level

    ```sql
    USE [database];
    GRANT ADMINISTER DATABASE BULK OPERATIONS TO [username];
    GRANT ADMINISTER DATABASE BULK OPERATIONS TO [public];
    GRANT REFERENCES ON DATABASE SCOPED CREDENTIAL::[<credential-name>] TO [<user-name>];
    GO
    ```

---

### Partition Pruning

=== ":simple-apacheparquet: Parquet"

    ```sql
    CREATE VIEW [<schema-name>].[<view-name>]
    AS
    SELECT
        *,
    	CAST(temp.filepath(1) AS INT) AS [year],
    	CAST(temp.filepath(2) AS TINYINT) AS [month],
    	CAST(temp.filepath(3) AS TINYINT) AS [day]
    FROM
        OPENROWSET(
            BULK 'data/table/year=*/month=*/day=*/**',
            DATA_SOURCE = '<external-storage-name>',
            FORMAT = 'PARQUET'
        )
    WITH (
        [timestamp]       [datetime],
        [edge_id]         [varchar](max),
        [temperature]     [float],
        [humidity]        [float],
        [lqi]             [float],
        [pm1.0]           [float],
        [pm2.5]           [float],
        [pm10.0]          [float],
        [date]            [date]
    ) AS temp
    GO
    ```

=== ":material-delta: Delta"

    ```sql
    CREATE VIEW [<schema-name>].[<view-name>]
    AS
    SELECT
        *
    FROM
        OPENROWSET(
            BULK 'data/delta_table/',
            DATA_SOURCE = '<external-storage-name>',
            FORMAT = 'DELTA'
        )
    WITH (
        [timestamp]       [datetime],
        [edge_id]         [varchar](max),
        [temperature]     [float],
        [humidity]        [float],
        [lqi]             [float],
        [pm1.0]           [float],
        [pm2.5]           [float],
        [pm10.0]          [float],
        [date]            [date]
    ) AS temp
    GO
    ```

=== ":material-file-chart: CSV"

    ```sql
    CREATE VIEW [<schema-name>].[<view-name>]
    AS
    SELECT
        *
    FROM
        OPENROWSET(
            BULK 'data/delta_table/',
            DATA_SOURCE = '<external-storage-name>',
            FORMAT = 'CSV',
            PARSER_VERSION ='2.0',
            FIELDTERMINATOR =',',
            ROWTERMINATOR = '\n',
            HEADER_ROW = TRUE,
            FIRSTROW = 1,
            FIELDQUOTE = '"',
            ESCAPECHAR = '\\',
            ROWSET_OPTIONS = '{"READ_OPTIONS":["ALLOW_INCONSISTENT_READS"]}'
        )
    WITH (
        [timestamp]       [datetime],
        [edge_id]         [varchar](max),
        [temperature]     [float],
        [humidity]        [float],
        [lqi]             [float],
        [pm1.0]           [float],
        [pm2.5]           [float],
        [pm10.0]          [float],
        [date]            [date]
    ) AS temp
    GO
    ```

=== ":material-file-code: Json"

    ```sql
    CREATE VIEW [<schema-name>].[<view-name>]
    AS
    SELECT
        *
    FROM
        ...
    ```

---

## :material-playlist-plus: Read Mores

- [:material-newspaper: User Permission in Serverless SQL Pools](https://www.serverlesssql.com/user-permissions-in-serverless-sql-pools-external-tables-vs-views/)
- [:material-newspaper: Serverless SQL: Partition Pruning Delta Tables in Azure Synapse Analytics](https://www.serverlesssql.com/partition-pruning-delta-tables-in-azure-synapse-analytics/#Database_Types)
