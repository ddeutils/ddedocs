# SCD2

**Slowly Changing Dimensions (SCD)** are a concept used in data warehousing to maintain
historical data over time, while tracking changes in data. SCDs are important for
analysis and reporting purposes, and there are different types of SCDs to choose
from depending on the specific requirements of the data warehouse.

## Advantages of Using Delta Lake for SCD2 Implementation

- **ACID Transactions**: \
  Delta Lake on Databricks provides full support for ACID transactions,
  which means that data changes are atomic, consistent, isolated, and durable.
  This guarantees that SCD2 updates are executed in a way that preserves the integrity
  and consistency of the data.

- **Optimized Performance**: \
  Delta Lake on Databricks is optimized for performance, allowing for fast read
  and write operations. This means that even as the size of your data grows over
  time, your SCD2 updates can be executed quickly and efficiently.

- **Schema Enforcement**: \
  Delta Lake on Databricks provides built-in schema enforcement,
  which ensures that SCD2 updates adhere to the schema defined for the data. This
  helps to prevent errors and inconsistencies that can arise from data type mismatches
  or missing fields.

- **Time Travel**: \
  Delta Lake on Databricks provides time travel capabilities, allowing
  you to access the full history of changes to your SCD2 data. This means that you
  can easily view and audit changes over time, or even revert to a previous version
  of the data if necessary. Time travel also enables the creation of data-driven
  reports and dashboards that can provide insights into trends and patterns over
  time.

## Setup Data table

We define customer table that has initialized data name `initial_df` and incoming
data name `source_df`.

```python
from pyspark.sql import Row
from datetime import date

initial_df = spark.createDataFrame(
  [
    Row(cust_id=1001, first_name="John", city="A", address="A001", update_date=date(2023, 4, 1)),
    Row(cust_id=1002, first_name="Sara", city="B", address="B001 IT", update_date=date(2023, 4, 1)),
    Row(cust_id=1003, first_name="Tommy", city="C", address="C001 BKK", update_date=date(2023, 4, 1)),
  ]
)

source_df = spark.createDataFrame(
  [
    Row(cust_id=1001, first_name="John", city="A", address="A001 NEW", update_date=date(2023, 4, 2)),
    Row(cust_id=1004, first_name="Smile", city="D", address="D012", update_date=date(2023, 4, 2)),
  ]
)
```

Let create delta table in the Databricks `hiveme_tastore` schema.

```python
from delta.tables import DeltaTable

spark.sql("""
    CREATE OR REPLACE TABLE customer_history (
      cust_id INTEGER,
      first_name STRING,
      city STRING,
      address STRING,
      eff_start_date TIMESTAMP,
      eff_end_date TIMESTAMP,
      is_active STRING
    )
    USING DELTA
    LOCATION '/mnt/delta_silver/customer_history'
""")

# Read the target data (Delta Lake table)
target_delta_table = DeltaTable.forPath(
  spark, "/mnt/delta_silver/customer_history"
)
```

```python
high_date: str = "9999-12-31"
is_active: str = "Y"
current_date = lambda: f"{date.today():%Y-%m-%d}"
```

In the given code, `high_date` and `is_active` are variables used to define the
end date and active status for records in the customer table.

`high_date` is used to represent the maximum possible date in the future and is used
to indicate the end date for records that are currently active. For records that
are closed, the `eff_end_date` column in the Delta Lake table will be set to the
date when the record was closed.

`is_active` is used to indicate whether a record is currently active or not.

## Method 01: Insert, Update, and Overwrite

```python
import pyspark.sql.functions as f

joined_data = (
  source_df.alias("src")
    .join(
      other=target_delta_table.toDF().alias("tgt"),
      on=f.col("src.cust_id") == f.col("tgt.cust_id"),
      how="full_outer"
    )
    .select(
      "src.*",
      *[
        f.col("tgt." + c).alias("tgt_" + c)
        for c in target_delta_table.toDF().columns
      ]
    )
)
```

A full outer join is here to ensure that all rows from both the source and target
data are included in the resulting joined data set. This is important because we
need to identify rows in the target table that need to be updated or deleted, as
well as rows in the source table that need to be inserted. A full outer join ensures
that we do not miss any rows that may exist in one table but not the other.

Additionally, since the SCD2 implementation requires comparing values from both
the source and target data, a full outer join helps us compare all the rows and
determine which ones have changed.

```python
insert_data = (
  joined_data.filter(f.col("tgt_cust_id").isNull())
    .withColumn("eff_start_date", f.lit(current_date()))
    .withColumn("eff_end_date", f.lit(high_date))
    .withColumn("is_active", f.lit("Y"))
)
if insert_data.count() > 0:
    (
      target_delta_table.alias("tgt")
        .merge(
          source=insert_data.alias("src"),
          condition="tgt.cust_id = src.cust_id"
        )
        .whenNotMatchedInsertAll()
        .execute()
    )
```

`insert_data` is a DataFrame variable created by filtering the `joined_data` DataFrame
to select only the rows that have a `null` value for the `tgt_cust_id` column. These
are the rows that are in the source data but not in the target data. The `insert_data`
DataFrame is then used to insert new records into the target Delta Lake table.

Additionally, `eff_start_date`, `eff_end_date`, and `is_active` columns are added to
`insert_data` using the withColumn method before merging it with the target Delta
Lake table.

```python
update_data = (
  joined_data.filter(
    f.col("src.cust_id").isNotNull() &
    f.col("tgt_cust_id").isNotNull() &
    (
        (f.col("src.first_name") != f.col("tgt_first_name")) |
        (f.col("src.city") != f.col("tgt_city")) |
        (f.col("src.address") != f.col("tgt_address"))
    )
  )
)

if update_data.count() > 0:
    (
      target_delta_table.alias("tgt")
        .merge(
          update_data.alias("src"),
          "tgt.cust_id = src.cust_id"
        )
        .whenMatchedUpdate(
            condition="tgt.is_active = 'Y'",
            set={
                "eff_end_date": f.lit(current_date()),
                "tgt.is_active": f.lit("N")
            }
        )
        .execute()
    )
```

The `update_data` variable in the given code represents the records from the joined
data where the `cust_id` is present in both the source and target tables, and where
there is at least one attribute that has changed. This is determined by checking
if any of the following attributes in the source data are different from their
corresponding attributes in the target data: `first_name`, `city`, and `address`.

The purpose of this variable is to identify the records that need to be updated
in the Delta Lake table. The subsequent operations performed on this data, such
as closing old records and inserting new records with updated values, ensure that
the table is updated with the latest information.

```python
new_records = update_data.select(
    f.col("src.cust_id"),
    f.col("src.first_name"),
    f.col("src.city"),
    f.col("src.address"),
    f.lit(current_date()).alias("eff_start_date"),
    f.lit(high_date).alias("eff_end_date"),
    f.lit(is_active).alias("is_active")
)

(
  target_delta_table.toDF()
    .union(new_records)
    .write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .save("/mnt/delta_silver/customer_history")
)
```

The `new_records` DataFrame is union with the existing Delta Lake table data and
written to the Delta Lake table location using the `write()` method of the
DataFrameWriter object. The `mode()` method is set to "overwrite" to replace the
existing data, and the `option()` method is set to "overwriteSchema" to overwrite
the schema of the table if it already exists.

> **Note**: \
> This method will use for large data source because we check the record of `insert_data`
> and `update_data` before merge to target delta table.

## Method 02: Union after Merge

```python
new_records = (
  source_df.alias("src")
    .join(
        other=target_delta_table.toDF().alias("tgt"),
        on="cust_id"
    )
    .where(
      (f.col("tgt.is_active") == 'Y') &
      (
        (f.col("src.first_name") != f.col("tgt.first_name")) |
        (f.col("src.city") != f.col("tgt.city")) |
        (f.col("src.address") != f.col("tgt.address"))
      )
    )
    .select("src.*")
)
```

An inner join is here to ensure that new rows from the source data are included in
the resulting joined data set. This is important because we need to identify rows
in the source data that need to be inserted, as well as rows in the target table
that need to be updated.

```python
staged_updates = (
  new_records
    .selectExpr("NULL as mergeKey", "src.*")
    .union(source_df.selectExpr("cust_id as mergeKey", "*"))
)
```

`staged_updates` is the update DataFrame by unioning two sets of rows; Rows that
will be inserted in the `whenNotMatched` clause, and rows that will either update
the current addresses of existing customers or insert the new addresses of new
customers.

```python
(
  target_delta_table.alias("tgt")
    .merge(
      source=staged_updates.alias("src"),
      condition="tgt.cust_id = src.mergeKey"
    )
    .whenMatchedUpdate(
      condition=(
        "(tgt.is_active = 'Y') AND ("
          "src.first_name <> tgt.first_name OR "
          "src.city <> tgt.city OR "
          "src.address <> tgt.address"
        ")"
      ),
      set = {
        "is_active": f.lit("N"),
        "eff_end_date": f.lit(current_date())
      }
    )
    .whenNotMatchedInsert(
      values = {
        "cust_id": "src.cust_id",
        "first_name": "src.first_name",
        "city": "src.city",
        "address": "src.address",
        "is_active": f.lit("Y"),
        "eff_start_date": f.lit(current_date()),
        "eff_end_date": f.lit(high_date)
      }
    )
    .execute()
)
```

> **Note**: \
> This method will use for small data source because we union the record of `new_records`
> to `source_df` before merge to target delta table.

## Method 03: Merge and Append

> **Warning**: \
> This method need to use `whenNotMatchedBySource` method that support for DBR 12.1 or higher.
> [(More Detail about DBR)](https://learn.microsoft.com/en-us/azure/databricks/release-notes/runtime/12.1#support-for-when-not-matched-by-source-for-merge-into)

```python
new_records = (
  source_df.alias("src")
    .join(target_delta_table.toDF().alias("tgt"), "cust_id")
    .where(
      (f.col("tgt.is_active") == 'Y') &
      (
        (f.col("src.first_name") != f.col("tgt.first_name")) |
        (f.col("src.city") != f.col("tgt.city")) |
        (f.col("src.address") != f.col("tgt.address"))
      )
    )
    .select("src.*")
    .withColumn("eff_start_date", f.lit(current_date()).cast('timestamp'))
    .withColumn("eff_end_date", f.lit(high_date).cast('timestamp'))
    .withColumn("is_active", f.lit("Y"))
    .withColumn('cust_id', f.col('cust_id').cast('integer'))
    .drop('update_date')
)
```

```python
(
  target_delta_table
    .alias("tgt")
    .merge(
      source=source_df.alias("src"),
      condition="tgt.cust_id = src.cust_id"
    )
    .whenMatchedUpdate(
      condition="tgt.is_active = 'Y'",
      set={
        "eff_end_date": f.lit(current_date()),
        "is_active": f.lit("N")
      }
    )
    .whenNotMatchedInsert(
      values={
        "cust_id": "src.cust_id",
        "first_name": "src.first_name",
        "city": "src.city",
        "address": "src.address",
        "eff_start_date": f.lit(current_date()),
        "eff_end_date": f.lit(high_date),
        "is_active": f.lit("Y"),
      }
    )
    .whenNotMatchedBySourceUpdate(
      condition="tgt.is_active = 'Y'",
      set={
        "eff_end_date": f.lit(current_date()),
        "is_active": f.lit("D"),
      }
    )
    .execute()
)
```

The method `whenNotMatchedBySource` help you to handle delete records when it does
not match by source, but you can still insert record that not match by target data.

```python
(
  target_delta_table.toDF()
    .write.format("delta")
    .mode("append")
    .option("overwriteSchema", "true")
    .save("/mnt/delta_silver/customer_history")
)
```

## References

- https://medium.com/@manishshrivastava26/mastering-dimensional-data-with-delta-lake-implementing-scd2-on-databricks-4d56a6f636b5
- https://docs.delta.io/latest/delta-update.html#slowly-changing-data-scd-type-2-operation-into-delta-tables
