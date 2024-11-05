# To Excel

!!! note

    There is no `read_excel()` function. If you want to do this, you have to use
    DuckDB’s Spatial extension. The spatial extension enables advanced spatial
    data processing and analysis capabilities within the database.

## Getting Started

```python
import duckdb as db

db.sql("INSTALL spatial;LOAD spatial;")
results = db.sql("SELECT * FROM st_read('xl_duck.xlsx');")
```

```python
db.sql("""
    SELECT *
    FROM st_read(
        'xl_duck.xlsx',
        layer = 'Sheet2',
        open_options = ['HEADERS=FORCE', 'FIELD_TYPES=STRING']
    );
"""
```

## Options

### Layer

```sql
SELECT * FROM st_read('xl_duck.xlsx', layer='sheet2')
```

### Header

```sql
SELECT * FROM st_read(
    'xl_duck.xlsx',
    open_options = ['HEADERS=FORCE']
);
```

- `FORCE`: treat the first row as a header
- `DISABLE`: treat the first row as a row of data
- `AUTO`: attempt auto-detection (default)

### Field type

```sql
SELECT *
FROM st_read(
    'xl_duck.xlsx',
    open_options = ['FIELD_TYPES=STRING']
);
```

- `STRING`: all fields should be loaded as strings (`VARCHAR` type)
- `AUTO`: field types should be auto-detected (default)

## Writing

```python
db.sql("COPY new_tbl TO 'output.xlsx' WITH (FORMAT GDAL, DRIVER 'xlsx');")
db.sql("COPY (SELECT * FROM results where order_id = 100) TO 'output.xlsx' WITH (FORMAT GDAL, DRIVER 'xlsx');")
```

## Read Mores

- [Where’s the read_excel() function in DuckDB?](https://ai.gopubby.com/wheres-the-read-excel-function-in-duckdb-d76bab1e2b85)
