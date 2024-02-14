# Azure Database: _Authentication_

## Users & Roles

### Getting Users

=== "All"

    ```sql
    SELECT
        [name]
        , [type_desc]
        , [type]
    FROM [sys].[database_principals]
    ```

=== "External Users"

    ```sql
    SELECT
        [name]
        , [type_desc]
        , [type]
    FROM [sys].[database_principals]
    WHERE [type] like 'E'
    ```

=== "External Group Users"

    ```sql
    SELECT
        [name]
        , [type_desc]
        , [type]
    FROM [sys].[database_principals]
    WHERE [type] = 'X'
    ```

=== "SQL User"

    ```sql
    SELECT
        [name]
        , [type_desc]
        , [type]
    FROM [sys].[database_principals]
    WHERE [type] = 'S'
    ```

=== "SQL User without login"

    ```sql
    SELECT
        [name]
        , [type_desc]
        , [type]
    FROM [sys].[database_principals]
    WHERE [type] = 'S'
    ```

!!! note

    If you want to list of users on server, you can change information table to

    ```sql
    ...
    FROM [sys].[database_principals]
    ...
    ```

### Create User

=== "External User"

    ```sql
    USE [master];
    CREATE LOGIN [username@email.com] FROM EXTERNAL PROVIDER;
    GO
    USE [database];
    CREATE USER [username@email.com] FROM LOGIN [username@email.com];
    GO
    ```

=== "External Group"

    ```sql
    USE [master];
    CREATE LOGIN [groupname@email.com] FROM EXTERNAL PROVIDER;
    GO
    USE [database];
    CREATE USER [groupname@email.com] FROM LOGIN [groupname@email.com];
    GO
    ```

=== "SQL User"

    ```sql
    USE [master];
    CREATE LOGIN [username@email.com] WITH PASSWORD = 'P@ssW0rd';
    GO
    USE [database];
    CREATE USER [username@email.com] FROM LOGIN [username@email.com];
    GO
    ```

=== "SQL User without login"

    ```sql
    USE [database];
    CREATE USER [username@email.com] WITHOUT LOGIN;
    GRANT IMPERSONATE ON USER::[username@email.com] TO [anothername@email.com];
    GO
    ```

!!! note

    If you want to delete user,

    ```sql
    USE [database];
    DROP USER [username@email.com];
    GO
    USE [master];
    DROP LOGIN [username@email.com];
    GO
    ```

### Relationship of Users and Roles

```sql
SELECT
    r.[name]                                    AS [Role]
    , ISNULL(m.[name], 'No members')            AS [Member]
    , m.create_date                             AS [Created Date]
    , m.modify_Date                             AS [Modified Date]
FROM
    [sys].[database_role_members]               AS rm
RIGHT OUTER JOIN [sys].[database_principals]    AS r
    ON rm.[role_principal_id] = r.[principal_id]
LEFT OUTER JOIN [sys].[database_principals]     AS m
    ON rm.[member_principal_id] = m.[principal_id]
WHERE
    r.[type] = 'R'
ORDER BY
    r.[name]
    , ISNULL(m.[name], 'No members')
;
```

```text
Role         |Member          |Created Date           |Modified Date          |
-------------+----------------+-----------------------+-----------------------+
DATA ENGINEER|demo@mail.com   |2022-11-15 00:00:00.000|2022-11-15 00:00:00.000|
db_owner     |dbo             |2003-04-08 00:00:00.000|2021-09-21 00:00:00.000|
db_owner     |admin@mail.com  |2021-05-12 00:00:00.000|2021-05-12 00:00:00.000|
db_ddladmin  |DATA ENGINEER   |2022-11-15 00:00:00.000|2022-11-15 00:00:00.000|
db_datareader|DATA ENGINEER   |2022-11-15 00:00:00.000|2022-11-15 00:00:00.000|
db_datawriter|DATA ENGINEER   |2022-11-15 00:00:00.000|2022-11-15 00:00:00.000|
```

### Create Role

```sql
CREATE ROLE [role-name];
ALTER ROLE [role-name] ADD MEMBER [username@email.com];
GO
```

!!! note

    If you want to remove user from role, you should use

    ```sql
    ALTER ROLE [role-name] DROP MEMBER [username@email.com];
    ```

## Permissions

### Grant

=== "All"

    ```sql
    GRANT ALL PRIVILEGES ON DATABASE [database] TO [username@email.com];
    ```

=== "Operation"

    ```sql
    USE [master];

    -- Monitor the Appliance
    GRANT VIEW SERVER STATE TO [username@email.com];

    -- Terminate Connections
    GRANT ALTER ANY CONNECTION TO [username@email.com];

    GO
    ```

=== "Manage Database"

    ```sql
    USE [database];

    -- Manage Databases
    GRANT CONTROL ON DATABASE::[database] TO [username@email.com];

    GO
    ```

=== "Manage Login"

    ```sql
    USE [master]

    -- Manage and add logins
    GRANT ALTER ANY LOGIN TO [username@email.com];

    -- Grant permissions to view sessions and queries
    GRANT VIEW SERVER STATE TO [username@email.com];

    -- Grant permission to end sessions
    GRANT ALTER ANY CONNECTION TO [username@email.com];
    GO

    USE [database];

    -- Grant permissions to create and drop users
    GRANT ALTER ANY USER TO [username@email.com];

    -- Grant permissions to create and drop roles
    GRANT ALTER ANY ROLE TO [username@email.com];

    GO
    ```

=== "Load Data"

    ```sql
    USE [master];

    -- Grant BULK Load permissions
    GRANT ADMINISTER BULK OPERATIONS TO [username@email.com];

    GO

    USE [database];

    GRANT CREATE TABLE ON DATABASE::[database] TO [username@email.com];

    -- On Schema Usage
    GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA [schemaname] TO [username@email.com];
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA [schemaname] TO [username@email.com];

    GO
    ```

=== "Schema"

    ```sql
    USE [database];

    ALTER AUTHORIZATION ON SCHEMA::[schemaname] to [username@email.com];
    GRANT USAGE ON SCHEMA::[schemaname] TO [username@email.com];
    GRANT ALTER ON SCHEMA::[schemaname] TO [username@email.com];

    GO
    ```

=== "Creator"

    ```sql
    USE [database];

    GRANT CREATE TABLE, CREATE VIEW, CREATE PROCEDURE TO [username@email.com];

    GO
    ```

!!! note

    If you want to revoke granted permission, you can use:

    ```sql
    REVOKE ...;
    ```

    The **REVOKE** statement can be used to remove granted permissions, and the **DENY**
    statement can be used to prevent a principal from gaining a specific permission
    through a **GRANT**

!!! example

    ```sql
    USE Adventureworks
    DROP TABLE IF EXISTS dbo.mytable, dbo.mytable2, Sales.mytable, Sales.mytable2
    DROP USER IF EXISTS TestRole

    CREATE USER TestRole WITHOUT LOGIN
    GRANT CREATE TABLE to TestRole

    GRANT ALTER ON SCHEMA :: dbo To TestRole;
    EXECUTE AS USER = 'TestRole'
    --OK
    CREATE TABLE dbo.mytable(c1 int)
    GO
    --Fails
    CREATE TABLE Sales.mytable(c1 int)
    GO
    REVERT
    REVOKE ALTER ON SCHEMA :: dbo To TestRole;

    GRANT ALTER To TestRole;
    EXECUTE AS USER = 'TestRole'
    --OK
    CREATE TABLE dbo.mytable2(c1 int)
    GO
    --OK
    CREATE TABLE Sales.mytable2(c1 int)
    GO
    REVERT
    ```

### Impersonate

```sql
GRANT IMPERSONATE ON USER::[username@mail.com] TO [targetname@mail.com];
GO
EXECUTE AS USER = 'username@mail.com';
...
REVERT;
GO
```

!!! note

    If you want to revoke impersonate, you can use:

    ```sql
    REVOKE IMPERSONATE ON USER::[<user@mail.com>] TO [<target@mail.com>];
    ```

### Relationship of Permissions and Objects

```sql
SELECT
	dp.[name]									AS [Principle]
    , dp.[type_desc]							AS [Principal Type]
    , o.[name]									AS [Object Name]
	, p.[permission_name]						AS [Permission]
    , p.[state_desc]							AS [Permission State]
FROM [sys].[database_permissions]				AS p
LEFT OUTER JOIN [sys].[all_objects]				AS o
	ON p.[major_id] = o.[OBJECT_ID]
INNER JOIN [sys].[database_principals]			AS dp
	ON p.[grantee_principal_id] = dp.[principal_id]
```

```text
Principle        |Principal Type|Object Name              |Permission|Permission State|
-----------------+--------------+-------------------------+----------+----------------+
dbo              |SQL_USER      |                         |CONNECT   |GRANT           |
DWHCTRLADMIN     |SQL_USER      |                         |CONNECT   |GRANT           |
username@scg.com |EXTERNAL_USER |                         |CONNECT   |GRANT           |
public           |DATABASE_ROLE |query_store_query_variant|SELECT    |GRANT           |
```

=== "On Schema"

    ```sql
    SELECT
        state_desc
        ,permission_name
        ,'ON'
        ,class_desc
        ,SCHEMA_NAME(major_id)
        ,'TO'
        ,USER_NAME(grantee_principal_id)
    FROM [sys].[database_permissions]       AS PERM
    JOIN [sys].[database_principals]        AS Prin
        ON PERM.[major_ID] = Prin.[principal_id]
        AND class_desc = 'SCHEMA'
    WHERE
        user_name(grantee_principal_id) = 'username@email.com'
    ```

    ```text
    state_desc|permission_name|  |class_desc|             |  |                  |
    ----------+---------------+--+----------+-------------+--+------------------+
    GRANT     |EXECUTE        |ON|SCHEMA    |             |TO|public            |
    GRANT     |SELECT         |ON|SCHEMA    |             |TO|public            |
    GRANT     |ALTER          |ON|SCHEMA    |DWHCURATED   |TO|username@email.com|
    GRANT     |EXECUTE        |ON|SCHEMA    |DWHMDL       |TO|username@email.com|
    GRANT     |EXECUTE        |ON|SCHEMA    |DWHMDL       |TO|de_vendor         |
    ```

!!! note

    For more detail, you can follew store procedure statement,
    [sp_dbpermissions](https://sqlstudies.com/free-scripts/sp_dbpermissions/)

## References

- [SQL Server Create User and Grant Permission](https://copyprogramming.com/howto/sql-sql-server-create-user-and-grant-permission)
