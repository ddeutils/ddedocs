# To Database

##  Attaching to multiple databases at once

```python
import duckdb as db

db.sql("ATTACH 'dbname=your_db user=your_user password=your_password host=127.0.0.1' AS db_postgres (TYPE postgres)")
db.sql("ATTACH 'my_sqlite.db' AS sql_lite (TYPE sqlite)")
db.sql("create table sql_lite.small_table as SELECT * FROM db_postgres.large_table LIMIT 10")

sql_out = db.sql("SELECT * FROM sql_lite.small_table")

print(sql_out)
```

## Copying Data Between Databases

```python
import duckdb as db

db.sql("ATTACH 'dbname=your_db user=your_user password=your_passwrd host=127.0.0.1' AS db_postgres (TYPE postgres)")

# attach a DuckDB file
db.sql("ATTACH 'database.db' AS ddb")


# export all tables and views from the Postgres database to the DuckDB file
db.sql("COPY FROM DATABASE db_postgres TO ddb")
```

https://levelup.gitconnected.com/duckdb-database-connections-e041f8fcde9e
