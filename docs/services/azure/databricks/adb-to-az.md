# Connect to Azure Services

## :material-account-check-outline: Authentication

### Using Service Principal

### 1) Create Service Principal

To register your application and create your service principal:

- Go to `Azure Active Directory` :octicons-arrow-right-24: `App registrations`
  :octicons-arrow-right-24: `New registration`
- Add the information of this app like `name` is `cnct-adb-dev` (The name of app
  should be formatted like `{app}-{resource-shortname}-{environment}`)
- Click register for create

You will then be required to generate a secret:

- Go to `App registrations` :octicons-arrow-right-24: `Certificates&secrets`
  :octicons-arrow-right-24: `New Client Secret`
- Save this value to `Azure Key Vaults`

!!! note

     We write both the `Client ID` and `Secret` to Key Vault for a number of reasons:

     * The `Secret` is sensitive and like a `Storage Key` or `Password`, we don't want
       this to be hardcoded or exposed anywhere in our application.
     * Normally we would have an instance of `Databricks` and `Key Vault` per environment
       and when we come to referencing the secrets, we want the secrets names to remain
       the same, so the code in our Databricks notebooks referencing the `Secrets` doesn't
       need to be modified when we deploy to different environments.

!!! abstract

    The **App Registration** is the template used to create the security principal
    (like a User) which can be authenticated and authorized.

## :material-microsoft-azure: Azure Services

### Azure SQL

#### 1) Create User in Azure SQL

The app registration still needs permission to log into `Azure SQL` and access the
objects within it. You’ll need to Create that user (**App & Service Principal**)
in the database and then grant it permissions on the underlying objects.

```sql
CREATE USER [cnct-adb-dev] FROM EXTERNAL PROVIDER;
```

**Permission**:

=== "Read Only"

    ```sql
    GRANT SELECT ON SCHEMA::dbo TO [cnct-adb-dev];
    ```

=== "Overwrite"

    ```sql
    GRANT SELECT ON SCHEMA::dbo TO [cnct-adb-dev];
    GRANT INSERT ON SCHEMA::dbo TO [cnct-adb-dev];
    GRANT ALTER ON SCHEMA::dbo TO [cnct-adb-dev];
    GRANT CREATE TABLE TO [cnct-adb-dev];
    ```

#### 2) Connection Code

##### Method 01: Spark Connector

To connect to `Azure SQL`, you will need to install the [SQL Spark Connector](https://github.com/microsoft/sql-spark-connector)
and the [Microsoft Azure Active Directory Authentication Library](https://pypi.org/project/adal/)
(ADAL) for Python code.

- Go to your cluster in Databricks and Install necessary packages:

  - **Maven**: `com.microsoft.azure:spark-mssql-connector_2.12_3.0:1.0.0-alpha`
  - **PYPI**: `adal`

- Also, if you haven’t already, [Create a Secret Scope](https://learn.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes)
  to your `Azure Key Vault` where your `Client ID`, `Secret`, and `Tenant ID` have
  been generated.

- Get `Access Token` from Service Principle authentication request

  ```python
  import adal

  context = adal.AuthenticationContext(
      f"https://login.windows.net/{dbutils.secrets.get(scope='defaultScope', key='TenantId')}"
  )
  token = context.acquire_token_with_client_credentials(
      "https://database.windows.net/",
      dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnId"),
      dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnSecret"),
  )
  access_token = token["accessToken"]
  ```

=== "Read Table"

    ```python
    df = (
        spark.read
            .format("com.microsoft.sqlserver.jdbc.spark")
            .option("url", "jdbc:sqlserver://<server-instance-name>.database.windows.net")
            .option("databaseName", "{dev}")
            .option("accessToken", access_token)
            .option("encrypt", "true")
            .option("hostNameInCertificate", "*.database.windows.net")
            .option("dbtable", "[dbo].[<table-name>]")
            .option("batchsize", 2500)
            .option("mssqlIsolationLevel", "READ_UNCOMMITTED")
            .load()
    )
    ```

    !!! note

        This connector by default uses `READ_COMMITTED` isolation level when performing
        the bulk insert into the database. If you wish to override the isolation
        level, use the `mssqlIsolationLevel` option as show above.

=== "Write Table"

    ```python
    (
        df.write
            .format("com.microsoft.sqlserver.jdbc.spark")
            .mode("append")
            .option("url", "jdbc:sqlserver://<server-instance-name>.database.windows.net")
            .option("dbtable", "[dbo].[<table-name>]")
            .option("accessToken", access_token)
            .option("schemaCheckEnabled", "false")
            .save()
    )
    ```

    !!! note

        When `schemaCheckEnabled` is `false`, we can write to the destination table
        which has less column than dataframe.

        [Read More](https://github.com/microsoft/sql-spark-connector/blob/master/samples/PySpark%20Connector%20with%20Big%20Data%20Clusters.ipynb)

!!! note

    Executing custom SQL through the connector. The previous Azure SQL Connector
    for Spark provided the ability to execute custom SQL code like **DML** or **DDL**
    statements through the connector. This functionality is out-of-scope of this
    connector since it is based on the DataSource APIs. This functionality is readily
    provided by libraries like `pyodbc`, or you can use the standard java sql interfaces
    as well.

##### Method 02: JDBC Connector

This method reads or writes the data **row by row**, resulting in performance issues.
**Not Recommended**.

In Databricks Runtime 11.3 LTS and above, you can use the sqlserver keyword to use
the included driver for connecting to SQL server.

=== "Format JDBC"

    === "Read"

        ```python
        df = (
            spark.read
                .format("jdbc")
                .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
                .option("url", "jdbc:sqlserver://<host>:1433;")
                .option("authentication", "ActiveDirectoryServicePrincipal")
                .option("user", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnId"))
                .option("password", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnSecret"))
                .option("database", "<database-name>")
                .option("dbtable", "<schema-name>.<table-name>")
                .option("encrypt", "true")
                .load()
        )
        ```

    === "Read (Legacy)"

        ```python
        df = (
            spark.read
                .jdbc(
                    url="jdbc:sqlserver://<host>:1433;database=<database>",
                    table="<schema-name>.<table-name>",
                    properties={
                        "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
                        "authentication": "ActiveDirectoryServicePrincipal",
                        "UserName": dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnId"),
                        "Password": dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnSecret"),
                    },
                )
        )
        ```

    === "Write Append"

        ```python
        (
            df.write
                .mode("append")
                .format("jdbc")
                .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
                .option("url", "jdbc:sqlserver://<host>:1433;")
                .option("authentication", "ActiveDirectoryServicePrincipal")
                .option("user", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnId"))
                .option("password", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnSecret"))
                .option("database", "<database-name>")
                .option("dbtable", "<schema-name>.<table-name>")
                .save()
        )
        ```

    === "Write Overwrite"

        ```python
        (
            df.write
                .mode("overwrite")
                .format("jdbc")
                .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
                .option("url", "jdbc:sqlserver://<host>:1433;")
                .option("authentication", "ActiveDirectoryServicePrincipal")
                .option("user", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnId"))
                .option("password", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnSecret"))
                .option("database", "<database-name>")
                .option("dbtable", "<schema-name>.<table-name>")
                .save()
        )
        ```

=== "Format SQLServer"

    === "Read"

        ```python
        df = (
            spark.read
                .format("sqlserver")
                .option("host", "<host-name>.database.windows.net")
                .option("port", "1433")
                .option("authentication", "ActiveDirectoryServicePrincipal")
                .option("user", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnId"))
                .option("password", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnSecret"))
                .option("database", "<database-name>")
                .option("dbtable", "<schema-name>.<table-name>")
                .option("encrypt", "true")
                .option("hostNameInCertificate", "*.database.windows.net")
                .load()
        )
        ```

    === "Write Append"

        ```python
        (
            df.write
                .mode("append")
                .format("sqlserver")
                .option("host", "<host:***.database.windows.net>")
                .option("port", "1433")
                .option("authentication", "ActiveDirectoryServicePrincipal")
                .option("user", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnId"))
                .option("password", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnSecret"))
                .option("database", "<database-name>")
                .option("dbtable", "<schema-name>.<table-name>")
                .save()
        )
        ```

    === "Write Overwrtie"

        ```python
        (
            df.write
                .mode("overwrite")
                .format("sqlserver")
                .option("host", "<host:***.database.windows.net>")
                .option("port", "1433")
                .option("authentication", "ActiveDirectoryServicePrincipal")
                .option("user", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnId"))
                .option("password", dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnSecret"))
                .option("database", "<database-name>")
                .option("dbtable", "<schema-name>.<table-name>")
                .option("truncate", true)
                save()
        )
        ```

        When using mode `overwrite` if you do not use the option truncate on recreation
        of the table, indexes will be lost. , a columnstore table would now be a heap.
        If you want to maintain existing indexing please also specify option truncate
        with value true. For example, `.option("truncate","true")`.

        [Microsoft: Spark - SQL Server Connector](https://learn.microsoft.com/en-us/sql/connect/spark/connector?view=sql-server-ver16#supported-features)

**References**:

- [Databricks: External Data - SQL Server](https://docs.databricks.com/en/external-data/sql-server.html)
- [Apache Spark: SQL Data Sources - JDBC](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html)

#### 2.1) Connection Code with SQL User
