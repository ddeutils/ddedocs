# Azure Synapse Analytics: _Partition View_

## Manage Permission

**Remove bulk operations on master**:

```sql
USE master;
DENY ADMINISTER BULK OPERATIONS to {user-name};
DENY ADMINISTER BULK OPERATIONS TO [public];
```

**Grant bulk operations on the database level**:

```sql
USE serverless;
GRANT ADMINISTER DATABASE BULK OPERATIONS to {user-name};
GRANT ADMINISTER DATABASE BULK OPERATIONS TO [public];
GRANT REFERENCES ON DATABASE SCOPED CREDENTIAL::[{credential-name}] TO [{user-name}];
```

## Partition Pruning

=== "Parquet"

    ```sql
    ```

=== "Delta"

    ```sql
    ```

## References

- [User Permission in Serverless SQL Pools](https://www.serverlesssql.com/user-permissions-in-serverless-sql-pools-external-tables-vs-views/)
