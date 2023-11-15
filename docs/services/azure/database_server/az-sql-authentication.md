# Azure Server: Authentication

## Users & Roles

### Getting Users

=== "Azure Server"

    === "External Users"

        ```sql
        SELECT
            [name]
            , type_desc
            , type
            , is_disabled
        FROM [sys].[server_principals]
        WHERE [type_desc] like 'external%'
        ```

        ```sql
        CREATE USER [username@email.com] FROM EXTERNAL PROVIDER
        GO
        ```

=== "Azure Database"

    === "External Users"

        ```sql
        SELECT
            [name]
            , type_desc
            , type
        FROM [sys].[database_principals]
        WHERE [type_desc] like 'external%'
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
WHERE
    DP1.type = 'R'
ORDER BY
    DP1.name,
    ISNULL(DP2.name, 'No members')
;
```

### Role

Create Role and add new member to this role:

```sql
CREATE ROLE de_trainer;
ALTER ROLE [de_trainer] ADD MEMBER [username@email.com];
ALTER ROLE [db_datareader] ADD MEMBER [de_trainer];
```

!!! note

    If you want to remove user from role, you would use
    `ALTER ROLE [db_datareader] DROP MEMBER [de_trainer]`

## Permission

```sql
create user do_data with encrypted password 'w*35LSjwoB6GdeUU';
grant all privileges on database [database-name] to do_data;
GRANT USAGE ON SCHEMA public TO do_data;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO do_data;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO do_data;
```

```sql
EXECUTE AS USER = 'CPAC';
SELECT ...
REVERT;
```

## Impersonate

For use `EXECUTE AS [<user@mail.com>]`

```sql
GRANT IMPERSONATE ON USER::[<user@mail.com>] TO [<target@mail.com>];
```

```sql
REVOKE IMPERSONATE ON USER::[<user@mail.com>] TO [<target@mail.com>];
```
