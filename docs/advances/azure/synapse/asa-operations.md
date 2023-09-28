# Azure Synapse Analytic: _Operation_

## Operation Status

```sql
-- This query returns the latest operations in the server
-- it needs to be executed in the master database
-- the information in this table is removed automatically after 2 or 3 hours
SELECT [session_activity_id]
      ,[resource_type]
      ,[resource_type_desc]
      ,[major_resource_id]
      ,[minor_resource_id]
      ,[operation]
      ,[state]
      ,[state_desc]
      ,[percent_complete]
      ,[error_code]
      ,[error_desc]
      ,[error_severity]
      ,[error_state]
      ,[start_time]
      ,[last_modify_time]
    FROM sys.dm_operation_status
```

## References

- https://davidalzamendi.com/azure-synapse-analytics-last-operations-in-server/
- https://github.com/ProdataSQL/SynapseTools/blob/main/SqlPools/
