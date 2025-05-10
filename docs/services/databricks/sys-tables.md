# System tables

## What Are Databricks System Tables?

Located within the system catalog, Databricks system tables are a collection of
metadata repositories that serve as the backbone for analyzing various aspects
of your Databricks environment.
They help monitor performance, track resource consumption, and analyze activity logs.

Importantly, these tables offer users the ability to:

- Track the utilization of Databricks services like SQL Warehouses, Unity Catalog, Notebooks, Jobs, and Delta Live Tables.
- Gain detailed insights into resource consumption and billing to optimize costs effectively.
- Establish traceability for data transformations at both the table and column levels.
- Review operations initiated by Databricks, such as maintenance tasks.

## Real-World Use Cases and Practical Examples

### Auditing User Activities

To maintain a secure environment, tracking user actions is essential.
The `system.access.audit` table provides a detailed log of user events,
such as SQL executions and data access.

=== "Example Query: Identifying Resource-Intensive Queries"

    ```sql
    SELECT user_email, query_text, execution_time, rows_read
    FROM system.access.audit
    WHERE event_type = 'query' AND rows_read > 1000000
    ORDER BY execution_time DESC
    LIMIT 10;
    ```

### Tracing Data Lineage

Understanding data flow is crucial for compliance and integrity.
The `system.access.table_lineage` and `system.access.column_lineage` tables track
transformations and relationships between datasets.

=== "Example Query: Tracking Table Dependencies"

    ```sql
    SELECT source_table_name, target_table_name, operation
    FROM system.access.table_lineage
    WHERE target_table_name = 'customer_analytics';
    ```

### Managing Costs Effectively

The `system.billing.usage` table simplifies cost analysis, helping organizations
allocate budgets wisely and identify inefficiencies.

=== "Example Query: Monthly Cost Analysis"

    ```sql
    WITH usage_costs AS (
      SELECT
        u.workspace_id,
        u.sku_name,
        u.usage_date,
        DATE_FORMAT(u.usage_date, 'yyyy-MM') AS YearMonth,
        u.usage_quantity,
        lp.pricing.default AS list_price,
        lp.pricing.default * u.usage_quantity AS list_cost,
        COALESCE(u.usage_metadata.job_id, u.usage_metadata.dlt_pipeline_id, u.usage_metadata.warehouse_id, u.usage_metadata.notebook_id) AS resource_id
      FROM
        system.billing.usage u
        INNER JOIN system.billing.list_prices lp
          ON u.cloud = lp.cloud
          AND u.sku_name = lp.sku_name
          AND u.usage_start_time >= lp.price_start_time
          AND (u.usage_end_time <= lp.price_end_time OR lp.price_end_time IS NULL)
      WHERE u.usage_start_time >= '2024-02-01'
    )
    SELECT usage_type, resource_id, SUM(usage_quantity) AS quantity, SUM(list_cost) AS cost
    FROM usage_costs
    GROUP BY usage_type, resource_id
    ORDER BY cost DESC
    LIMIT 20;
    ```

### Monitoring Compute Resources

The `system.compute.clusters` table provides insights into cluster activity,
enabling better resource management.

=== "Example Query: Recently Terminated Clusters"

    ```sql
    SELECT cluster_name, terminated_time, termination_reason
    FROM system.compute.clusters
    WHERE terminated_time IS NOT NULL
    ORDER BY terminated_time DESC
    LIMIT 5;
    ```

## Conclusion

Databricks system tables offer unparalleled opportunities for monitoring and
optimization.
By combining metadata analysis with actionable insights, these tables help users
maintain efficiency, control costs, and ensure compliance.
Leverage the sample queries and schemas provided to unlock the full potential
of your Databricks environment.

## References

- [Databricks System Tables for Monitoring and Optimization](https://medium.com/towards-data-engineering/databricks-system-tables-for-monitoring-and-optimization-37267e723ede)
