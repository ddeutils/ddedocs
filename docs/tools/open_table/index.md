# File Formats

In the realm of big data, choosing the right file format is crucial for efficient
data storage, retrieval, and processing. Four prominent file formats that have
gained traction in recent years are **Apache Iceberg**, **Apache Hudi**, **Parquet**,
and **Delta Lake**. Each format offers unique features and benefits tailored to
different use cases. In this article, we’ll delve into these file formats,
exploring their characteristics, advantages, and code examples to illustrate
their usage.

## Apache Iceberg

**Apache Iceberg** is a table format designed for massive-scale data platforms.
It offers features like schema evolution, data versioning, and time travel
capabilities. Iceberg organizes data into tables and provides ACID transactions
for data modifications.

**Features and Benefits**:

**Schema Evolution**

:   Iceberg allows schema changes without interrupting concurrent reads and writes.

**Data Versioning**

:   It maintains a history of data changes, facilitating easy rollback or time-travel queries.

**ACID Transactions**

:   Iceberg ensures data consistency with atomicity, consistency, isolation, and durability.

```python
from pyiceberg import HadoopTables

# Assuming `hadoopConf`, `schema`, and `tableIdentifier` are defined elsewhere
iceberg_table = HadoopTables(hadoopConf).create(schema, tableIdentifier)
```

## Apache Hudi

**Apache Hudi** (Hadoop Upserts Deletes and Incrementals) is a data lake storage
format that supports record-level insert, update, and delete operations.
It provides efficient ingestion and query performance with features like columnar
storage and indexing.

**Features and Benefits**:

**Upserts and Deletes**

:   Hudi enables efficient upserts and deletes, making it suitable for use cases requiring real-time data updates.

**Incremental Processing**

:   It supports incremental data processing, reducing the computational overhead for large datasets.

**Query Performance**

:   Hudi optimizes query performance through columnar storage and indexing mechanisms.

```python
# Python example to write data using Hudi
(
    hudi_df
        .write
        .format("org.apache.hudi")
        .option("hoodie.datasource.write.operation", "upsert")
        .save("/path/to/hudi_table")
)
```

## Parquet

**Apache Parquet** is a columnar storage format optimized for big data processing
frameworks like Apache Hadoop and Apache Spark. It offers efficient compression
and encoding techniques, making it suitable for analytical workloads.

**Features and Benefits**:

**Columnar Storage**

:   Parquet organizes data by column, enabling efficient query execution by reading
    only the necessary columns.

**Compression**

:   It provides built-in compression algorithms like Snappy and Gzip, reducing
    storage costs and improving query performance.

**Predicate Pushdown**

:   Parquet supports predicate pushdown, filtering data at the storage level
    before retrieval, further enhancing query performance.

```scala
// Scala example to read Parquet file using Apache Spark
val parquetDF = spark.read.parquet("/path/to/parquet_file")
```

## Delta Lake

**Delta Lake** is an open-source storage layer that brings ACID transactions to
Apache Spark and big data lakes. It provides features like data versioning,
schema enforcement, and time travel capabilities.

**Features and Benefits**:

**ACID Transactions**

:   Delta Lake ensures atomicity, consistency, isolation, and durability for
    data modifications, enhancing data integrity.

**Schema Enforcement**

:   It enforces schema evolution and validation, preventing data inconsistencies.

**Time Travel**

:   Delta Lake enables querying data at different versions or timestamps,
    facilitating historical analysis and debugging.

```python
query = (
    myDF.writeStream
        .format("delta")
        .partitionBy("dt")
        .outputMode("append")
        .trigger(processingTime='60 seconds')
        .option("checkpointLocation", checkpointLocation)
        .option("path",refine_loc)
        .option("overwriteSchema", "true")
        .option("mergeSchema", "true")
        .start()
)
```

## References

- [A Comprehensive Guide to Modern File Formats in Data Engineering 2024!](https://medium.com/@shenoy.shashwath/a-comprehensive-guide-to-modern-file-formats-in-data-engineering-2024-9e4bfb6f2d2a)
