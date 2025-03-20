# BigQuery Iceberg Tables

BigQuery Iceberg tables enable the creation of open-format lakehouses on Google Cloud.
They combine the flexibility of customer-managed storage with BigQuery’s managed
analytics service, allowing you to work with data stored in your Cloud Storage
buckets using the open-source Apache Iceberg table format.

```sql
CREATE TABLE dataset_name.table_name (
    column1 STRING,
    column2 INT64
)
WITH CONNECTION connection_name
OPTIONS (
    file_format = 'PARQUET',
    table_format = 'ICEBERG',
    storage_uri = 'gs://your-bucket/path-to-data'
);
```

## References

- [:material-google-cloud: BigQuery tables for Apache Iceberg](https://cloud.google.com/bigquery/docs/iceberg-tables#architecture)
