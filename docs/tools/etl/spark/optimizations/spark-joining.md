# Spark: _Joining_

[](https://medium.com/@kerrache.massipssa/apache-spark-join-strategies-in-depth-171bf7fef4b0)

## Broadcast Hash Join

Utilizes the broadcasting of a smaller DataFrame to all worker nodes, thus avoiding
the need to shuffle the larger DataFrame. This strategy significantly improves
performance, especially for joins between a large and a small DataFrame.

**Use Case**: Best used when joining a small reference or lookup table with a larger fact table.

**Example**: Joining a small product catalog DataFrame with a large sales transactions
DataFrame, where broadcasting the product catalog allows for efficient joins at
each node.

## SortMerge Joins

It consists of hashing each row on both table and shuffle the rows with the same
hash into the same partition. There the keys are sorted on both side and the `sortMerge`
algorithm is applied.

To drastically speed up your sortMerges, write your large datasets as a Hive table
with pre-bucketing and pre-sorting option (same number of partitions) instead of
flat parquet dataset.

**Use Case**: Ideal for large datasets with relatively uniform distribution and
when broadcasting is not feasible.

**Example**: Merging two large datasets, such as customer data and transaction data,
where both are sorted by customer ID for efficient merging.

```python
(
    df.repartition(2200, "colA", "colB")
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

!!! warning

    Spark bucketing is incompatible with hive bucketing

- https://towardsdatascience.com/best-practices-for-bucketing-in-spark-sql-ea9f23f7dd53
- https://subhamkharwal.medium.com/pyspark-optimize-joins-in-spark-804fb098d4ee

## Shuffle Hash Join

Involves partitioning and shuffling data based on the join key, then building a hash table for the smaller partition to join with the larger one. It’s a compromise between broadcast and sort-merge joins.

Use Case: Suitable for datasets where one is significantly smaller than the other, but still too large to broadcast.
Example: Joining customer demographic data with a larger dataset of customer transactions, where the demographic data forms the smaller partition.

## Skewed Join

Tackles the issue of data skewness, where certain keys are overly represented. Spark implements techniques to split and replicate these skewed keys, balancing the data distribution across nodes.

Use Case: Useful when dealing with large datasets that have uneven key distribution, which can lead to performance bottlenecks.
Example: In a join operation between a customer orders table and a products table, if a few products account for most of the orders, a skewed join can distribute the load more evenly.

## Conditional Join

This approach is used for joins based on complex conditions beyond simple key equality, incorporating multiple conditions or sophisticated business logic.

Use Case: Appropriate for scenarios where the relationship between tables is defined by more than just key matching.
Example: Joining a sales table with a customer table where the join condition includes multiple factors like customer demographics, purchase history, and recent activity.

## Broadcast Nested Loop Join

Applied when both DataFrames are small and involve a nested loop join, where each row of one DataFrame is compared with all rows of the other DataFrame.

Use Case: Suitable for small datasets or when other join strategies are not applicable.
Example: Joining two small datasets where one contains discount information and the other contains product categories, and the relationship does not depend on a specific key.

## Cartesian Product (Cross Join)

Produces a Cartesian product of the datasets; every row of the first DataFrame is paired with every row of the second DataFrame. It is a resource-intensive operation.

Use Case: Used when every combination of rows from the datasets needs to be considered, though generally avoided due to its high computational cost.
Example: Generating all possible combinations of two small datasets, such as colors and sizes for a clothing line.

## Bucketed Joins

Bucketing involves organizing data into fixed-size buckets based on a hash function of the join key. When two DataFrames are bucketed on the same columns, Spark can efficiently join them by matching bucket IDs, reducing shuffles.

Use Case: Effective for frequent joins on the same key columns, especially in iterative ETL processes.
Example: If both customer and transaction DataFrames are bucketed by customer ID, joins between these DataFrames can be more efficient, as Spark can bypass the shuffle phase.

## Z-Order Join (Space-filling Curve Optimization)

This technique involves organizing data using a Z-order curve to colocate related information. By doing so, range queries and certain types of joins are optimized, reducing the amount of data scanned.

Use Case: Beneficial for multidimensional data, particularly when range queries are common.
Example: In a geospatial analysis scenario, joining geographic data organized by Z-order can significantly reduce the data scanned, making queries for a specific region more efficient.

## References

- https://towardsdatascience.com/the-art-of-joining-in-spark-dcbd33d693c
- https://towardsdatascience.com/strategies-of-spark-join-c0e7b4572bcf
- [:simple-medium: Spark Joining Strategy Part I](https://medium.com/@patrickwork0001/spark-joining-strategy-part-1-1f9ca35dc87f)
