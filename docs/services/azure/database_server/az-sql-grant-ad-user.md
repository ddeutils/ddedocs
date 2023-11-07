# Azure Server: Authentication

## Users & Roles

### Select External Users

=== "Azure Server"

    ```sql
    SELECT name, type_desc, type, is_disabled
    FROM sys.server_principals
    WHERE type_desc like 'external%'
    ```

=== "Azure Database"

    ```sql
    SELECT name, type_desc, type
    FROM sys.database_principals
    WHERE type_desc like 'external%'
    ```

    ```sql
    CREATE USER [username@email.com] FROM EXTERNAL PROVIDER
    GO
    ```

### Select Relationship of Users and Roles

```sql
SELECT
    DP1.name AS DatabaseRoleName
    ,ISNULL(DP2.name, 'No members') AS DatabaseUserName
    ,DP2.principal_id
    ,DP2.create_date
FROM sys.database_role_members AS DRM
RIGHT OUTER JOIN sys.database_principals AS DP1
ON DRM.role_principal_id = DP1.principal_id
LEFT OUTER JOIN sys.database_principals AS DP2
ON DRM.member_principal_id = DP2.principal_id
WHERE DP1.type = 'R'
ORDER BY DP1.name, ISNULL(DP2.name, 'No members');
GO
```

- Create Role and add new member to this role

  ```sql
  CREATE ROLE de_trainer;
  ALTER ROLE [de_trainer] ADD MEMBER [username@email.com];
  ALTER ROLE [db_datareader] ADD MEMBER [de_trainer];
  ```

  !!! note

      If you want to remove user from role, you would use
      `ALTER ROLE [db_datareader] DROP MEMBER [de_trainer]`
