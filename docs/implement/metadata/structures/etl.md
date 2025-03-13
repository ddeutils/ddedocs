# ETL

The table that use the ETL process that ingest data to it should has process tracking
field for tracking this record ingest from which process.

| Field Name              |     Alias      | Data Type |  PK  | Description |
|:------------------------|:--------------:|:----------|:----:|:------------|
| **process_name**        |     ps_nm      | STRING    |      |             |
| **process_date**        |    ps_date     | DATETIME  |      |             |
| **update_process_name** |  update_ps_nm  | STRING    |      |             |
| **update_process_date** | update_ps_date | DATETIME  |      |             |

## Delete before

```sql
DELECT FROM {target-schema}.{target-table-name}
WHERE
        process_name =  '{process-name}'
    AND process_date >= '{current-date}'
```
