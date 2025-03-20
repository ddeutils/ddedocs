# ETL

The table that use the ETL process that ingest data to it should has process tracking
field for tracking this record ingest from which process.

| Field Name           |      Alias       | Data Type |  PK  | Description |
|:---------------------|:----------------:|:----------|:----:|:------------|
| **src_name**         |      src_nm      | STRING    |      |             |
| **load_date**        |    load_date     | DATETIME  |      |             |
| **update_src_name**  |  update_src_nm   | STRING    |      |             |
| **update_load_date** | update_load_date | DATETIME  |      |             |

## Delete before

```sql
DELECT FROM {target-schema}.{target-table-name}
WHERE
        src_name  =  '{src-name}'
    AND load_date >= '{current-date}'
```
