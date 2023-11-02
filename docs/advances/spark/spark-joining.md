# Spark: _Joining_

## SortMerge Joins

 It consists of hashing each row on both table and shuffle the rows with the same
 hash into the same partition. There the keys are sorted on both side and the `sortMerge`
 algorithm is applied.

To drastically speed up your sortMerges, write your large datasets as a Hive table
with pre-bucketing and pre-sorting option (same number of partitions) instead of
flat parquet dataset.

```python
(
    large_df
        .repartition(2200, "col_A", "col_B")
        .write
        .bucketBy(2200, "col_A", "col_B")
        .sortBy("col_A", "col_B")
        .mode("overwrite")
        .format("parquet")
        .saveAsTable("schema.large_tbl")
)
```

The overhead cost of writing pre-bucketed/pre-sorted table is modest compared to
the benefits.

The underlying dataset will still be parquet by default, but the Hive metastore
(can be Glue metastore on AWS) will contain precious information about how the
table is structured. Because all possible "joinable" rows are colocated, Spark
won't shuffle the tables that are pre-bucketd (big savings!) and won't sort the
rows within the partition of table that are pre-sorted.

> **Warning**: \
> Spark bucketing is incompatible with hive bucketing

- https://towardsdatascience.com/best-practices-for-bucketing-in-spark-sql-ea9f23f7dd53

## References

- https://towardsdatascience.com/the-art-of-joining-in-spark-dcbd33d693c
- https://towardsdatascience.com/strategies-of-spark-join-c0e7b4572bcf
