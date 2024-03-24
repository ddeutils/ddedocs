---
icon: simple/apachehive
---

# Apache Hive

**Hive** tables can be partitioned based on specific columns. This allows efficient
data organization and retrieval based on partition values. For example, a web logs
table might be partitioned by year, month, and day. When querying this table,
you can specify the desired partition(s) to filter data efficiently.

However, as the number of partitions increases, managing them can become complex.
**Hive** needs to maintain metadata for each partition, impacting performance
and storage utilization.

## Setting Up Partition Projection

To enable partition projection for a Hive table, you can leverage table properties
during table creation or alteration. Here’s an example utilizing the
`TBLPROPERTIES` clause:

```hive
CREATE EXTERNAL TABLE web_logs (
  `user_id` string,
  `timestamp` timestamp,
  `page_view` string
)
PARTITIONED BY (
  `year` int,
  `month` int,
  `day` int
)
TBLPROPERTIES (
  'hive.partition-projection.enabled'='true',
  'projection.year.type'='integer',
  'projection.year.range'='2020-2024',
  'projection.month.type'='integer',
  'projection.month.range'='1-12',
  'projection.day.type'='integer',
  'projection.day.range'='1-31'
);
```

In this example, partition projection is enabled for the web_logs table. The schema
and ranges for each partitioned column (year, month, and day) are defined within
the table properties.

## References

- https://medium.com/@john_tringham/explained-apache-hive-5c801f543cb6
- [Simplifying Data Access with Partition Projection in Apache Hive](https://medium.com/@suhas_63074/simplifying-data-access-with-partition-projection-in-apache-hive-a788d1d068f1)
