# To Delta

As of DuckDB 0.10.3 (2024–05–22) the extension [duckdb_delta](https://github.com/duckdb/duckdb_delta)
is now an experimental feature.
Now DuckDB natively supports reading the delta protocol.
The extension is automatically loaded upon using it.

## :material-arrow-down-right: Getting Started

### The Delta Log

```sql
WITH delta_log AS (
    SELECT
        add,
        remove,
        commitInfo,
        str_split(filename,'/')[-1] AS file_name
    FROM read_json_auto(
        './delta_table/_delta_log/*.json',
        filename=true
    )
)
SELECT * FROM delta_log;
```

### Commit Info

```sql
WITH commit_info AS (
    SELECT
        unnest(commitInfo),
        file_name
    FROM delta_log
    WHERE commitInfo IS NOT NULL
)
SELECT * FROM commit_info;
```

### Add Actions

```sql
WITH add_actions AS (
    SELECT
      unnest(add),
      delta_log.file_name,
      commit_info.timestamp
    FROM delta_log
    JOIN commit_info ON delta_log.file_name = commit_info.file_name
    WHERE add IS NOT NULL
)
SELECT * FROM add_actions;
```

### Filtering current files

```sql
current_files AS (
  SELECT
    path
  FROM add_actions
  WHERE NOT EXISTS (
    SELECT
      1
    FROM
    remove_actions
    WHERE add_transactions.path = remove_transactions.path
    AND add_transactions.timestamp < remove_transactions.timestamp
 )
SELECT * FROM current_files
```

---

## Reading Delta

```sql
SELECT
 *
FROM
  read_parquet(
    './delta_table/**/*.parquet',
    filename=true,
    hive_partitioning=true
  ) as deltatable
WHERE EXISTS (
  SELECT
    1
  FROM
  current_files
  WHERE ends_with(deltatable.filename, current_files.path)
);
```

---

## Macro

```sql
CREATE OR REPLACE MACRO read_delta(delta_table_path, version := -1) AS TABLE
WITH delta_log AS (
  SELECT
    add,
    remove,
    commitInfo,
    str_split(filename,'/')[-1] AS file_name
  FROM read_json_auto(
    concat(delta_table_path, '/_delta_log/*.json'),
    filename=true
    )
  WHERE str_split(file_name,'.')[1]::int <= version::int
  OR version::int = -1
), commit_info AS (
  SELECT
    unnest(commitInfo),
    file_name
  FROM delta_log
  WHERE commitInfo IS NOT NULL
), add_actions AS (
  SELECT
    unnest(add),
    delta_log.file_name,
    commit_info.timestamp
  FROM delta_log
  JOIN commit_info ON delta_log.file_name = commit_info.file_name
  WHERE add IS NOT NULL
), remove_actions AS (
  SELECT
    unnest(remove),
    delta_log.file_name,
    commit_info.timestamp
  FROM delta_log
  JOIN commit_info ON delta_log.file_name = commit_info.file_name
  WHERE remove IS NOT NULL
), current_files AS (
  SELECT
    path
  FROM add_actions
  WHERE NOT EXISTS (
    SELECT
      1
    FROM
    remove_actions
    WHERE add_actions.path = remove_actions.path
    AND add_actions.timestamp < remove_actions.timestamp
  )
)
SELECT
  *
FROM
  read_parquet(
    concat(delta_table_path, '/**/*.parquet'),
    filename=true,
    hive_partitioning=true
  ) as deltatable
WHERE EXISTS (
  SELECT
    1
  FROM current_files
  WHERE ends_with(deltatable.filename, current_files.path)
);
```

Query

```sql
SELECT * FROM read_delta('./delta_table')
```

```sql
SELECT * FROM read_delta('./delta_table', version := 5)
```

## :material-playlist-plus: Read Mores

- [:simple-duckdb: DuckDB - Delta extension](https://duckdb.org/2024/06/10/delta.html)
- [How to read Delta Lake tables in plain SQL with DuckDB](https://medium.com/@jimmy-jensen/how-to-read-delta-lake-tables-in-plain-sql-with-duckdb-3ff30b626a82)
