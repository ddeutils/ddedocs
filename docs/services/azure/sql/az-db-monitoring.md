# Monitoring

## :material-arrow-down-right: Getting Started

### Partition State

```sql
SELECT
    OBJECT_NAME(s.object_id)        AS [object]
	,i.[name]                       AS IndexName
	,SUM(s.[used_page_count]) * 8   AS IndexSizeKB
FROM [sys].[dm_db_partition_stats]  AS s
INNER JOIN [sys].[indexes]          AS i
	ON s.[object_id] = i.[object_id]
	AND s.[index_id] = i.[index_id]
GROUP BY
    s.[object_id], i.[name]
ORDER BY
    OBJECT_NAME(s.object_id), i.[name]
;
```
