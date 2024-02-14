# Pyspark Delta lake: Star Schema

**Update**: `2023-04-27` |
**Tag**: `Python` `Spark` `Delta Lake` `Dimension Model` `Star Schema`

Most data warehouse developers are very familiar with the ever-present star schema.
Introduced by Ralph Kimball in the 1990s, a star schema is used to denormalize
business data into dimensions (like time and product) and facts (like transactions
in amounts and quantities). A star schema efficiently stores data, maintains history
and updates data by reducing the duplication of repetitive business definitions,
making it fast to aggregate and filter.

Just like in a traditional data warehouse, there are some simple rules of thumb
to follow on Delta Lake that will significantly improve your Delta star schema
joins.

**Table of Contents**:

- [Use Delta Tables to create your fact and dimension tables]()
- [Optimize your file size for fast file pruning]()
- []()

## Use Delta Tables to create your fact and dimension tables

**Delta Lake** is an open storage format layer that provides the ease of inserts,
updates, deletes, and adds ACID transactions on your data lake tables, simplifying
maintenance and revisions. Delta Lake also provides the ability to perform **dynamic
file pruning** to optimize for faster SQL queries.

The syntax is simple on Databricks Runtimes 8.x and newer where Delta Lake is the
default table format. You can create a Delta table using SQL with the following:

```sql
CREATE TABLE MY_TABLE (COLUMN_NAME STRING)
```

Before the 8.x runtime, Databricks required creating the table with the `USING DELTA`
syntax.

## Optimize your file size for fast file pruning

Two of the biggest time sinks in an Apache Spark query are the time spent reading
data from cloud storage and the need to read all underlying files. With **data skipping**
on Delta Lake, queries can selectively read only the Delta files containing relevant
data, saving significant time. Data skipping can help with static file pruning,
dynamic file pruning, static partition pruning and dynamic partition pruning.

One of the first things to consider when setting up data skipping is the ideal
data file size - too small, and you will have too many files (the well-known
"small-file problem"); too large and you won’t be able to skip enough data.

A good file size range is 32-128MB (1024 _ 1024 _ 32 = 33554432 for 32MB of course).
Again, the idea is that if the file size is too big, the dynamic file pruning
will skip to the right file or files, but they will be so large it will still
have a lot of work to do. By **creating smaller files**, you can benefit from file
pruning and minimize the I/O retrieving the data you need to join.

You can set the file size value for the entire notebook in Python:

```python
spark.conf.set("spark.databricks.delta.targetFileSize", 33554432)
```

Or you can set it only for a specific table using:

```sql
ALTER TABLE (database).(table)
SET TBLPROPERTIES (delta.targetFileSize=33554432)
```

If you happen to be reading this article after you have already created tables,
you can still set the table property for the file size and, when optimizing and
creating the `ZORDER`, the files will be proportioned to the new file size. If you
have already added a `ZORDER`, you can add and/or remove a column to force a re-write
before arriving at the final `ZORDER` configuration. Read more about `ZORDER` in step 3.

As Databricks continues to add features and capabilities, we can also Auto Tune
the file size based on the table size. For smaller databases, the above setting
will likely provide better performance but for larger tables and/or just to make
it simpler, you can follow the guidance
[here](https://docs.databricks.com/delta/index.html#autotune-based-on-table-size)
and implement the `delta.tuneFileSizesForRewrites` table property.

## Create a Z-Order on your fact tables

To improve query speed, Delta Lake supports the ability to optimize the layout of
data stored in cloud storage with **Z-Ordering**, also known as multidimensional
clustering. Z-Orders are used in similar situations as clustered indexes in the
database world, though they are not actually an auxiliary structure. A Z-Order
will cluster the data in the Z-Order definition, so that rows like column values
from the Z-order definition are collocated in as few files as possible.

Most database systems introduced indexing as a way to improve query performance.
Indexes are files, and thus as the data grows in size, they can become another
big data problem to solve. Instead, Delta Lake orders the data in the Parquet
files to make range selection on object storage more efficient. Combined with
the stats collection process and data skipping, Z-Order is similar to seek vs.
scan operations in databases, which indexes solved, without creating another
compute bottleneck to find the data a query is looking for.

For Z-Ordering, the best practice is to limit the number of columns in the Z-Order
to the best 1-4. We chose the foreign keys (foreign keys by use, not actually
enforced foreign keys) of the 3 largest dimensions which were too large to broadcast
to the workers.

```sql
OPTIMIZE MY_FACT_TABLE
  ZORDER BY (LARGEST_DIM_FK, NEXT_LARGEST_DIM_FK, ...)
```

Additionally, if you have tremendous scale and 100's of billions of rows or
Petabytes of data in your fact table, you should consider partitioning to further
improve file skipping. Partitions are effective when you are actively filtering
on a partitioned field.

## Create Z-Orders on your dimension key fields and most likely predicates

Although Databricks does not enforce primary keys on a Delta table, since you are
reading this blog, you likely have dimensions and a surrogate key exists - one
that is an integer or big integer and is validated and expected to be unique.

One of the dimensions we were working with had over 1 billion rows and benefited
from the file skipping and dynamic file pruning after adding our predicates into
the Z-Order. Our smaller dimensions also had Z-Orders on the dimension key field
and were broadcast in the join to the facts. Similar to the advice on fact tables,
limit the number of columns in the Z-Order to the 1-4 fields in the dimension that
are most likely to be included in a filter in addition to the key.

```sql
OPTIMIZE MY_BIG_DIM
  ZORDER BY (MY_BIG_DIM_PK, LIKELY_FIELD_1, LIKELY_FIELD_2)
```

## Analyze Table to gather statistics for Adaptive Query Execution Optimizer

One of the major advancements in Apache Spark 3.0 was the Adaptive Query Execution,
or AQE for short. As of Spark 3.0, there are three major features in AQE, including
coalescing post-shuffle partitions, converting sort-merge join to broadcast join,
and skew join optimization. Together, these features enable the accelerated performance
of dimensional models in Spark.

In order for AQE to know which plan to choose for you, we need to collect statistics
about the tables. You do this by issuing the ANALYZE TABLE command. Customers have
reported that collecting table statistics has significantly reduced query execution
for dimensional models, including complex joins.

```sql
ANALYZE TABLE MY_BIG_DIM COMPUTE STATISTICS FOR ALL COLUMNS
```

## Conclusion

By following the above guidelines, organizations can reduce query times - in our
example, from 90 seconds to 10 seconds on the same cluster. The optimizations greatly
reduced the I/O and ensured that we only processed the correct content. We also
benefited from the flexible structure of Delta Lake in that it would both scale
and handle the types of queries that will be sent ad hoc from the Business Intelligence
tools.

In addition to the file skipping optimizations mentioned in this blog, Databricks
is investing heavily in improving the performance of Spark SQL queries with Databricks
Photon. Learn more about `Photon` and the performance boost it will provide to all
of your Spark SQL queries with Databricks.

Customers can expect their ETL/ELT and SQL query performance to improve by enabling
Photon in the Databricks Runtime. Combining the best practices outlined here, with
the Photon-enabled Databricks Runtime, you can expect to achieve low latency query
performance that can outperform the best cloud data warehouses.

## References

- https://www.databricks.com/blog/2022/05/20/five-simple-steps-for-implementing-a-star-schema-in-databricks-with-delta-lake.html
