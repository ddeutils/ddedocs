# Solving the Small File Problem

## Solutions

### 1. Reduce number of partitions after shuffle

```text
spark-submit --conf spark.sql.shuffle.partitions=200 your_app.jar
```

!!! warning

    trade-off: changing parallelism can be bad or worse and dependent on current
    situation of your application

### 2. Use write.distribution.mode

```sql
-- write.distribution.mode only works when your table has partition key
CREATE TABLE catalog.db.table_name ()
USING iceberg
PARTITIONED BY your_key
TBLPROPERTIES (
  'write.distribution.mode'='hash'
)

-- alter exists tables
ALTER TABLE catalog.db.table_name
  SET TBLPROPERTIES ('write.distribution.mode'='hash')
```

!!! warning

    trade-off: making more partitions writing to the same file will cause your
    INSERT process takes longer, but previous computation may remain the same

### 3. Increase default file size

```sql
-- by default, Iceberg target file size is 512MB or 536870912 bytes
CREATE TABLE catalog.db.table_name ()
USING iceberg
TBLPROPERTIES (
  'write.target-file-size-bytes' = '536870912'
)

-- or alter your existing table using this command
ALTER TABLE catalog.db.table_name
  SET TBLPROPERTIES ('write.target-file-size-bytes'='536870912')
```

!!! warning

    trade-off: same as parallelism, file size is hard to get one perfect recipe.
    But `512M` by default is the recommendation

### 4. Compaction

```sql
-- this command will compact new files generated between a window of time
CALL catalog.system.rewrite_data_files(
  table => 'streamingtable',
  strategy => 'binpack',
  where => 'created_at between "2023-01-26 09:00:00" and "2023-01-26 09:59:59" ',
  options => map(
    'rewrite-job-order','bytes-asc',
    'target-file-size-bytes','1073741824',
    'max-file-group-size-bytes','10737418240',
    'partial-progress-enabled', 'true'
  )
)
```

!!! warning

    trade-off: use other process to compact your file may get your system some
    time to breath, just choose an appropriate time to perform a compaction

## :material-playlist-plus: Read Mores

- https://medium.com/ancestry-product-and-technology/solving-the-small-file-problem-in-iceberg-tables-6c31a295f724
- [Some ways to solve small file problems in Apache Iceberg](https://medium.com/@huwng_learn_things/some-ways-to-solve-small-file-problems-in-apache-iceberg-0ee3014cd4bb)
