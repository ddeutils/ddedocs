# Monitoring

## :material-arrow-down-right: Getting Started

### Table Size

```sql
CREATE VIEW dbo.vTableSizes
AS
WITH base
AS
(
SELECT
 GETDATE()                                                             AS  [execution_time]
, DB_NAME()                                                            AS  [database_name]
, s.name                                                               AS  [schema_name]
, t.name                                                               AS  [table_name]
, QUOTENAME(s.name)+'.'+QUOTENAME(t.name)                              AS  [two_part_name]
, nt.[name]                                                            AS  [node_table_name]
, ROW_NUMBER() OVER(PARTITION BY nt.[name] ORDER BY (SELECT NULL))     AS  [node_table_name_seq]
, tp.[distribution_policy_desc]                                        AS  [distribution_policy_name]
, c.[name]                                                             AS  [distribution_column]
, nt.[distribution_id]                                                 AS  [distribution_id]
, i.[type]                                                             AS  [index_type]
, i.[type_desc]                                                        AS  [index_type_desc]
, nt.[pdw_node_id]                                                     AS  [pdw_node_id]
, pn.[type]                                                            AS  [pdw_node_type]
, pn.[name]                                                            AS  [pdw_node_name]
, di.name                                                              AS  [dist_name]
, di.position                                                          AS  [dist_position]
, nps.[partition_number]                                               AS  [partition_nmbr]
, nps.[reserved_page_count]                                            AS  [reserved_space_page_count]
, nps.[reserved_page_count] - nps.[used_page_count]                    AS  [unused_space_page_count]
, nps.[in_row_data_page_count]
    + nps.[row_overflow_used_page_count]
    + nps.[lob_used_page_count]                                        AS  [data_space_page_count]
, nps.[reserved_page_count]
 - (nps.[reserved_page_count] - nps.[used_page_count])
 - ([in_row_data_page_count]
         + [row_overflow_used_page_count]+[lob_used_page_count])       AS  [index_space_page_count]
, nps.[row_count]                                                      AS  [row_count]
from
    sys.schemas s
INNER JOIN sys.tables t
    ON s.[schema_id] = t.[schema_id]
INNER JOIN sys.indexes i
    ON  t.[object_id] = i.[object_id]
    AND i.[index_id] <= 1
INNER JOIN sys.pdw_table_distribution_properties tp
    ON t.[object_id] = tp.[object_id]
INNER JOIN sys.pdw_table_mappings tm
    ON t.[object_id] = tm.[object_id]
INNER JOIN sys.pdw_nodes_tables nt
    ON tm.[physical_name] = nt.[name]
INNER JOIN sys.dm_pdw_nodes pn
    ON  nt.[pdw_node_id] = pn.[pdw_node_id]
INNER JOIN sys.pdw_distributions di
    ON  nt.[distribution_id] = di.[distribution_id]
INNER JOIN sys.dm_pdw_nodes_db_partition_stats nps
    ON nt.[object_id] = nps.[object_id]
    AND nt.[pdw_node_id] = nps.[pdw_node_id]
    AND nt.[distribution_id] = nps.[distribution_id]
    AND i.[index_id] = nps.[index_id]
LEFT OUTER JOIN (select * from sys.pdw_column_distribution_properties where distribution_ordinal = 1) cdp
    ON t.[object_id] = cdp.[object_id]
LEFT OUTER JOIN sys.columns c
    ON cdp.[object_id] = c.[object_id]
    AND cdp.[column_id] = c.[column_id]
WHERE pn.[type] = 'COMPUTE'
)
, size
AS
(
SELECT
   [execution_time]
,  [database_name]
,  [schema_name]
,  [table_name]
,  [two_part_name]
,  [node_table_name]
,  [node_table_name_seq]
,  [distribution_policy_name]
,  [distribution_column]
,  [distribution_id]
,  [index_type]
,  [index_type_desc]
,  [pdw_node_id]
,  [pdw_node_type]
,  [pdw_node_name]
,  [dist_name]
,  [dist_position]
,  [partition_nmbr]
,  [reserved_space_page_count]
,  [unused_space_page_count]
,  [data_space_page_count]
,  [index_space_page_count]
,  [row_count]
,  ([reserved_space_page_count] * 8.0)                                 AS [reserved_space_KB]
,  ([reserved_space_page_count] * 8.0)/1000                            AS [reserved_space_MB]
,  ([reserved_space_page_count] * 8.0)/1000000                         AS [reserved_space_GB]
,  ([reserved_space_page_count] * 8.0)/1000000000                      AS [reserved_space_TB]
,  ([unused_space_page_count]   * 8.0)                                 AS [unused_space_KB]
,  ([unused_space_page_count]   * 8.0)/1000                            AS [unused_space_MB]
,  ([unused_space_page_count]   * 8.0)/1000000                         AS [unused_space_GB]
,  ([unused_space_page_count]   * 8.0)/1000000000                      AS [unused_space_TB]
,  ([data_space_page_count]     * 8.0)                                 AS [data_space_KB]
,  ([data_space_page_count]     * 8.0)/1000                            AS [data_space_MB]
,  ([data_space_page_count]     * 8.0)/1000000                         AS [data_space_GB]
,  ([data_space_page_count]     * 8.0)/1000000000                      AS [data_space_TB]
,  ([index_space_page_count]  * 8.0)                                   AS [index_space_KB]
,  ([index_space_page_count]  * 8.0)/1000                              AS [index_space_MB]
,  ([index_space_page_count]  * 8.0)/1000000                           AS [index_space_GB]
,  ([index_space_page_count]  * 8.0)/1000000000                        AS [index_space_TB]
FROM base
)
SELECT *
FROM size
;
```

[Design tables using dedicated SQL pool in Azure Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql-data-warehouse/sql-data-warehouse-tables-overview#table-size-queries)

### Operation Status

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

### Data Skew & Outdated State

```sql
-- data skew -> cmp_rows>1mil, skew >= 10%
-- missing stats -> cmp_rows>1mil, ctl_rows=1000
-- outdated stats -> cmp_rows>1mil, cmp_rows <> ctl_rows (for (cmp_rows-ctl_rows) > 20%)

DECLARE @minRows INT = 1000000;
DECLARE @minSkewPercent decimal=10.0;
DECLARE @missingStatCtlRowCount int=1000;
DECLARE @CtlCmpRowDifferencePercentageForOutdatedStats decimal=20.0;

WITH cmp_details AS
(
       select tm.object_id, ps.index_id, ps.distribution_id, count(ps.partition_number) [partitions], sum(ps.row_count) cmp_row_count
       from sys.dm_pdw_nodes_db_partition_stats ps
              join sys.pdw_nodes_tables nt on nt.object_id=ps.object_id and ps.distribution_id=nt.distribution_id
              join sys.pdw_table_mappings tm on tm.physical_name=nt.name
       where ps.index_id<2
       group by tm.object_id, ps.index_id, ps.distribution_id
)
, cmp_summary as
(
       select object_id, index_id, sum(cmp_row_count) cmp_row_count
              , (max(cmp_row_count)-min(cmp_row_count)) highest_skew_rows_difference
              , convert(decimal(10,2),((max(cmp_row_count) - min(cmp_row_count))*100.0 / nullif(sum(cmp_row_count),0))) skew_percent
       from cmp_details
       group by object_id, index_id
)
, ctl_summary as
(
       select t.object_id, i.index_id, s.name sch_name, t.name table_name, i.type_desc table_type, dp.distribution_policy_desc distribution_type, count(p.partition_number) [partitions], sum(p.rows) ctl_row_count
       from sys.schemas s
              join sys.tables t on t.schema_id=s.schema_id
              join sys.pdw_table_distribution_properties dp on dp.object_id=t.object_id
              join sys.indexes i on i.object_id=t.object_id and i.index_id<2
              join sys.partitions p on p.object_id=t.object_id and p.index_id=i.index_id
       group by t.object_id, i.index_id, s.name, t.name, i.type_desc, dp.distribution_policy_desc
)
, [all_results] as
(
       select ctl.object_id, ctl.index_id, ctl.sch_name, ctl.table_name, ctl.table_type, ctl.distribution_type, ctl.[partitions]
              , ctl.ctl_row_count, cmp.cmp_row_count, convert(decimal(10,2),(abs(ctl.ctl_row_count - cmp.cmp_row_count)*100.0 / nullif(cmp.cmp_row_count,0))) ctl_cmp_difference_percent
              , cmp.highest_skew_rows_difference, cmp.skew_percent
              , case
                     when (ctl.ctl_row_count = @missingStatCtlRowCount) then 'missing stats'
                     when ((ctl.ctl_row_count <> cmp.cmp_row_count) and ((abs(ctl.ctl_row_count - cmp.cmp_row_count)*100.0 / nullif(cmp.cmp_row_count,0)) > @CtlCmpRowDifferencePercentageForOutdatedStats)) then 'outdated stats'
                     else null
                end stat_info
              , case when (cmp.skew_percent >= @minSkewPercent) then 'data skew' else null end skew_info
       from ctl_summary ctl
              join cmp_summary cmp on ctl.object_id=cmp.object_id and ctl.index_id=cmp.index_id
)
select *
from [all_results]
where cmp_row_count>@minRows and (stat_info is not null or skew_info is not null)
order by sch_name, table_name
```

## :material-playlist-plus: Read Mores

- [:material-newspaper: Azure Synapse Last Operations in Server](https://davidalzamendi.com/azure-synapse-analytics-last-operations-in-server/)
- [:material-github: GitHub: ProdataSQL - SynapseTools](https://github.com/ProdataSQL/SynapseTools/blob/main/SqlPools/)
- [:material-github: GitHub: ProdataSQL - SynapseTools vTableStats](https://github.com/ProdataSQL/SynapseTools/blob/main/SqlPools/Maintenance/vTableStats.sql)
