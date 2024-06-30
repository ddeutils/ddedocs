# Date & Timezone

## :material-arrow-down-right: Getting Started

### Convert Timezone

```sql
SELECT
    CAST(
        CAST(
            [DateColumn] AS DATETIMEOFFSET
        ) AT TIME ZONE 'SE Asia Standard Time' AS DATETIME2
    ),
    ...
FROM ...
```

## :material-playlist-plus: Read Mores

- [:material-microsoft: Microsoft: Data Types - Datetimeoffset](https://learn.microsoft.com/en-us/sql/t-sql/data-types/datetimeoffset-transact-sql?view=sql-server-ver16)
