# Azure SQL Database

```sql
create user do_data with encrypted password 'w*35LSjwoB6GdeUU';
grant all privileges on database scgtrinityprod to do_data;
GRANT USAGE ON SCHEMA public TO do_data;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO do_data;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO do_data;
```

```sql
EXECUTE AS USER = 'CPAC';
SELECT ...
REVERT;
```
