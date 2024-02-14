# Azure Synapse: _Date & Timezone_

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

## References

- [Microsoft: Data Types - Datetimeoffset](https://learn.microsoft.com/en-us/sql/t-sql/data-types/datetimeoffset-transact-sql?view=sql-server-ver16)
