# Azure Synapse Analytic: _Authentication_

## Users & Roles

### Getting Users

=== "External Users"

    ```sql
    SELECT
        [name]
        , [type_desc]
        , [type]
    FROM [sys].[database_principals]
    WHERE [type_desc] like 'external%'
    ORDER BY [name]
    ;
    ```

### Getting Relations

=== ":octicons-code-review-16: List relate roles and users"

    ```sql
    SELECT
        r.[name]                                    AS [Role]
        , m.[name]                                  AS [Member]
        , m.Create_date                             AS [Created Date]
        , m.modify_Date                             AS [Modified Date]
    FROM
        [sys].[database_role_members]               AS rm
    JOIN [sys].[database_principals]                AS r
        ON rm.[role_principal_id] = r.[principal_id]
    JOIN [sys].[database_principals]                AS m
        ON rm.[member_principal_id] = m.[principal_id]
    WHERE
        r.[type_desc] = 'DATABASE_ROLE'
    ORDER BY
        r.[name], m.[name];
    ;
    ```

=== ":octicons-code-review-16: List all roles"

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
        r.[name], ISNULL(m.[name], 'No members')
    ;
    ```

**Example Results**:

=== ":material-table-eye: List relate roles and users"

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

=== ":material-table-eye: List all roles"

    ```text
    Role         |Member          |Created Date           |Modified Date          |
    -------------+----------------+-----------------------+-----------------------+
    DATA ENGINEER|No members      |NULL                   |NULL                   |
    db_owner     |dbo             |2003-04-08 00:00:00.000|2021-09-21 00:00:00.000|
    db_owner     |admin@mail.com  |2021-05-12 00:00:00.000|2021-05-12 00:00:00.000|
    db_ddladmin  |DATA ENGINEER   |2022-11-15 00:00:00.000|2022-11-15 00:00:00.000|
    db_datareader|DATA ENGINEER   |2022-11-15 00:00:00.000|2022-11-15 00:00:00.000|
    db_datawriter|DATA ENGINEER   |2022-11-15 00:00:00.000|2022-11-15 00:00:00.000|
    ```

### Users

**Create Examples**:

=== ":octicons-code-review-16: AD User"

    ```sql
    USE [<database-name>];
    CREATE USER [username@mail.com] FROM EXTERNAL PROVIDER
    GO
    ```

=== ":octicons-code-review-16: AD User from AD Group"

    ```sql
    USE [<database-name>];
    CREATE USER [usernane@mail.com] FROM LOGIN [group-name];
    GO
    ```

=== ":octicons-code-review-16: AD Group"

    ```sql
    USE [<database-name>];
    CREATE USER [group-name] FROM LOGIN [group-name];
    GO
    ```

=== ":octicons-code-review-16: SQL User"

    ```sql
    USE [master];
    CREATE LOGIN <username> WITH PASSWORD = 'P@ssW0rd'
    GO
    ```

    ```sql
    USE [<database-name>];
    CREATE USER <username> FOR LOGIN <username>;
    GO
    ```

=== ":octicons-code-review-16: SQL User without Login"

    ```sql
    USE [<database-name>];
    CREATE USER <username> WITHOUT LOGIN;
    GRANT IMPERSONATE ON USER::<username> TO [<another-username>];
    GO
    ```

    ```sql
    EXECUTE AS USER = '<username>';
    GO
    ...
    REVERT;
    GO
    ```

**Getting User Example**:

=== ":octicons-code-review-16: AD User"

    ```sql
    SELECT
        [name]
    FROM [sys].[database_principals]
    WHERE
        [type] = 'E'
        AND [name] = 'username@mail.com'
    ;
    ```

=== ":octicons-code-review-16: AD User from AD Group"

    ```sql
    SELECT
        [name]
    FROM [sys].[database_principals]
    WHERE
        [type] = 'E'
        AND [name] = 'username@mail.com'
    ;
    ```

=== ":octicons-code-review-16: AD Group"

    ```sql
    SELECT
        [name]
    FROM [sys].[database_principals]
    WHERE
        [type] = 'X'
        AND [name] = 'username@mail.com'
    ;
    ```

=== ":octicons-code-review-16: SQL User"

    ```sql
    SELECT
        [name]
    FROM [sys].[database_principals]
    WHERE
        [type] = 'S'
        AND [name] = 'username@mail.com'
    ;
    ```

=== ":octicons-code-review-16: SQL User without Login"

    ```sql
    SELECT
        [name]
    FROM [sys].[database_principals]
    WHERE
        [type] = 'S'
        AND [name] = 'username@mail.com'
    ;
    ```

!!! note

    If you want to drop user, you would use:

    ```sql
    DROP USER [username@mail.com]
    GO
    ```

    If this user have login, you would use:

    ```sql
    DROP LOGIN [username@mail.com]
    GO
    ```

    Generate drop statement with multi-users:

    ```sql
    SELECT CONCAT('DROP USER [', [name], '];')  AS remove_user
    FROM
        [sys].[database_principals]
    WHERE
        [type] = 'E'
        AND LOWER([name]) IN ('username@mail.com', ...)
    ;
    ```

### Roles

=== ":material-database-settings-outline: Dedicate SQL Pool"

    ```sql
    CREATE ROLE <role-name>
    GO
    EXEC sp_addrolemember '<role-name>', [username@mail.com]
    GO
    ```

=== ":material-database-off-outline: Serverless SQL Pool"

    ```sql
    CREATE ROLE <role-name>
    GO
    ALTER ROLE [role-name] ADD MEMBER [username@mail.com]
    GO
    ```

!!! note

    If you want to remove user from this role,

    === ":material-database-settings-outline: Dedicate SQL Pool"

        ```sql
        EXEC sp_droprolemember '<role-name>', 'username@mail.com';
        ```

    === ":material-database-off-outline: Serverless SQL Pool"

        ```sql
        ALTER ROLE [role-name] DROP MEMBER [username@mail.com];
        ```

    Generate systax,

    === ":material-database-settings-outline: Dedicate SQL Pool"

        ```sql
        SELECT
          CONCAT(
                'EXEC sp_droprolemember ''', r.name, ''', ''', m.name, ''';'
          ) AS remove_member_command
        FROM
            sys.database_role_members  AS rm
        RIGHT OUTER JOIN sys.database_principals AS r
            ON rm.role_principal_id = r.principal_id
        LEFT OUTER JOIN sys.database_principals AS m
            ON rm.member_principal_id = m.principal_id
        WHERE
            r.type = 'R'
            AND LOWER(m.name) IN (
                'userbane@mail.com',
                ...
            )
        ORDER BY
            r.name, ISNULL(m.name, 'No members')
        ;
        ```

## Permissions

### Getting Relations

=== ":octicons-code-review-16: List relate permissions"

    ```sql
    SELECT DISTINCT
         pr.principal_id				AS [ID],
         pr.[name] 						AS [User],
         pr.[type_desc] 				AS [Type],
         pr.authentication_type_desc 	AS [Auth_Type]
         pe.state_desc					AS [State]
         pe.permission_name				AS [Permission]
         pe.class_desc					AS [Class]
         coalesce(o.[name], sch.name) 	AS [Object]
    FROM
        sys.database_principals 		AS pr
    JOIN sys.database_permissions 		AS pe
        ON pe.grantee_principal_id = pr.principal_id
    LEFT JOIN sys.objects 				AS o
        ON o.object_id = pe.major_id
    LEFT JOIN sys.schemas 				AS sch
        ON sch.schema_id = pe.major_id
        AND class_desc = 'SCHEMA'
    ;
    ```

=== ":octicons-code-review-16: List relate permissions with grantor"

    ```sql
    SELECT DISTINCT
    	DB_NAME() 							AS [DB],
       	p.[name] 							AS [User],
       	p.[type_desc] 						AS [Type],
       	p2.[name] 							AS [Grantor],
        pe.[state_desc]						AS [State],
        pe.[permission_name]				AS [Permission],
       	o.[Name] 							AS [Object],
       	o.[type_desc] 						AS [Object Type]
    FROM [sys].[database_permissions] 		AS pe
    LEFT JOIN [sys].[objects] 				AS o
    	ON pe.[major_id] = o.[object_id]
    LEFT JOIN [sys].[database_principals]	AS p
    	ON pe.[grantee_principal_id] = p.[principal_id]
    LEFT JOIN [sys].[database_principals] 	AS p2
    	ON pe.[grantor_principal_id] = p2.[principal_id]
    ;
    ```

**Example Results**:

=== ":material-table-eye: List relate permissions"

    ```text
    ID|User              |Type          |Auth Type|State|Permission             |Class             |Object         |
    --+------------------+--------------+---------+-----+-----------------------+------------------+---------------+
    25|username@mail.com |EXTERNAL_USER |EXTERNAL |GRANT|CONNECT                |DATABASE          |               |
    26|de_external       |DATABASE_ROLE |NONE     |GRANT|ALTER                  |SCHEMA            |DATAEXTERNAL   |
    26|de_external       |DATABASE_ROLE |NONE     |GRANT|ALTER                  |SCHEMA            |MART           |
    26|de_external       |DATABASE_ROLE |NONE     |GRANT|ALTER                  |SCHEMA            |CURATED        |
    26|de_external       |DATABASE_ROLE |NONE     |GRANT|ALTER ANY DATA SOURCE  |DATABASE          |               |
    26|de_external       |DATABASE_ROLE |NONE     |GRANT|ALTER ANY FILE FORMAT  |DATABASE          |               |
    26|de_external       |DATABASE_ROLE |NONE     |GRANT|EXECUTE                |OBJECT_OR_COLUMN  |FUNC_CHK_ID    |
    26|de_external       |DATABASE_ROLE |NONE     |GRANT|EXECUTE                |OBJECT_OR_COLUMN  |FUNC_CHK_TITLE |
    ```

=== ":material-table-eye: List relate permissions with grantor"

    ```text
    DB      |User       |Type          |Grantor               |State|Permission                    |Object          |Object Type         |
    --------+-----------+--------------+----------------------+-----+------------------------------+----------------+--------------------+
    syndpdev|adfuser    |SQL_USER      |dbo                   |GRANT|ALTER                         |                |                    |
    syndpdev|adfuser    |SQL_USER      |dbo                   |GRANT|ALTER ANY EXTERNAL DATA SOURCE|                |                    |
    syndpdev|adfuser    |SQL_USER      |dbo                   |GRANT|ALTER ANY EXTERNAL FILE FORMAT|                |                    |
    syndpdev|adfuser    |SQL_USER      |dbo                   |GRANT|CONNECT                       |                |                    |
    syndpdev|de_vendor  |DATABASE_ROLE |dbo                   |GRANT|ALTER ANY EXTERNAL FILE FORMAT|                |                    |
    syndpdev|de_vendor  |DATABASE_ROLE |dbo                   |GRANT|EXECUTE                       |                |                    |
    syndpdev|de_vendor  |DATABASE_ROLE |user@email.com        |GRANT|EXECUTE                       |FUNC_CHK_ID     |SQL_SCALAR_FUNCTION |
    syndpdev|de_vendor  |DATABASE_ROLE |user@email.com        |GRANT|EXECUTE                       |FUNC_CHK_TITLE  |SQL_SCALAR_FUNCTION |
    ```

### Grant

=== "data execution"

    ```sql
    GRANT CREATE VIEW TO [role-name];
    GRANT CREATE PROCEDURE TO [role-name];
    GRANT ALTER TO [role-name];
    ```

    ```sql
    GRANT EXECUTE ON SCHEMA::<schema-name> TO [role-name];
    GRANT UPDATE ON SCHEMA::<schema-name> TO [role-name];
    GRANT INSERT ON SCHEMA::<schema-name> TO [role-name];
    GRANT DELETE ON SCHEMA::<schema-name> TO [role-name];
    GRANT ALTER ON SCHEMA::<schema-name> TO [role-name];
    ```

```sql
GRANT IMPERSONATE ON USER::<user-name> TO <user-name>;
```

[More Example for Grant Permissions](https://learn.microsoft.com/en-us/sql/t-sql/statements/grant-transact-sql?view=azure-sqldw-latest#examples)

## Workload

```sql
CREATE WORKLOAD GROUP <group-name>
WITH (
    MIN_PERCENTAGE_RESOURCE = 100,
    CAP_PERCENTAGE_RESOURCE = 100,
    REQUEST_MIN_RESOURCE_GRANT_PERCENT = 100
);

--classifies load_user with the workload group LoadData
CREATE WORKLOAD CLASSIFIER [<classifier-name>]
WITH (
    WORKLOAD_GROUP = '<group-name>',
    MEMBERNAME = '<username>'
);
```

## References

- [Microsoft Azure Synapse Analytics SQL Authentication](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/sql-authentication?tabs=serverless)
- [Microsoft SQL T-SQL Create User Transaction](https://learn.microsoft.com/en-us/sql/t-sql/statements/create-user-transact-sql?view=azure-sqldw-latest)
