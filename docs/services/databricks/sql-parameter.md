# SQL Parameterization

!!! warning

    Databricks SQL Warehouse supports robust parameterization, which you must
    know before starting with SQL scripting, which was introduced in DBR 16.3+.

## Variables

```sql
DECLARE OR REPLACE VARIABLE sal_range INT;
SET VAR sal_range = 20000;

SELECT * FROM employees
WHERE sal > sal_range;
```

## Parameter Markers

!!! note

    Widgets in SQL Editor on the notebook.

```sql
SELECT * FROM employees
WHERE sal > :sal_range;
```

## Dynamic Objects

```sql
DECLARE OR REPLACE VARIABLE table_name STRING = 'employees';

SELECT * FROM IDENTIFIER(table_name);
```

## Dynamic SQL with EXECUTE IMMEDIATE

```sql
DECLARE OR REPLACE sqlStr STRING = 'SELECT * FROM employees WHERE sal > ?';

EXECUTE IMMEDIATE sqlStr USING 2000;
```

## Parameterizing USE CATALOG (Databricks 16.1 Update)

```sql
DECLARE OR REPLACE VARIABLE catalog_name STRING = 'workspace';

USE CATALOG IDENTIFIER(catalog_name);
```

## Combining Variables and parameters

```sql
DECLARE OR REPLACE sql_query_top_1 STRING =
  'SELECT sal FROM employees WHERE name = ? ORDER BY sal DESC LIMIT 1';
DECLARE OR REPLACE user_salary INT;
DECLARE OR REPLACE user_name STRING = 'John';

EXECUTE IMMEDIATE sql_query_top_1 INTO user_salary USING user_name;

SELECT user_salary; -- we put result to variable
```

## :material-source-commit-end: Conclusion

- Variables allow storing temporary values within a session.
- Widgets (Parameter Markers) enable UI-driven dynamic queries.
- IDENTIFIER is helpful for dynamic object references but cannot be embedded
  (at least for now) inside a string for EXECUTE IMMEDIATE.
- EXECUTE IMMEDIATE is a key feature for future stored procedures and loops in
  Databricks SQL.

## :material-playlist-plus: References

- [SQL Parameterization in Databricks SQL](https://databrickster.medium.com/sql-parameterization-in-databricks-sql-de32a38865b9)
