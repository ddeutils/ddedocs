# Databricks: _To Azure SQL_

## Azure Service Principal

### 1) Create Service Principal

To register your application and create your service principal

* Go to `Azure Active Directory` :octicons-arrow-right-24: `App registrations`
  :octicons-arrow-right-24: `New registration`
* Add the information of this app like `name` is `cnct-adb-dev`
* Click register for create

!!! note

    The name of app should be format, `{app}-{resource-shortname}-{environment}`

You will then have to generate a secret

* Go to `App registrations` :octicons-arrow-right-24: `Certificates&secrets`
  :octicons-arrow-right-24: `New Client Secret`
* Save this value to `Azure Key Vaults`

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

### 2) Create User in Azure SQL

The app registration still needs permission to log into `Azure SQL` and access the
objects within it. You’ll need to Create that user (**App & Service Principal**) in the
database and then grant it permissions on the underlying objects.

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
    GRANT CREATE TABLE TO [cnct-adb-dev];
    GRANT ALTER ON SCHEMA::dbo TO [cnct-adb-dev];
    ```

### 3) Connection Code

#### Method 01: Spark Connector

To connect to `Azure SQL`, you will need to install the [SQL Spark Connector](https://github.com/microsoft/sql-spark-connector)
and the [Microsoft Azure Active Directory Authentication Library](https://pypi.org/project/adal/)
(ADAL) for Python code.

* Go to your cluster in Databricks and Install necessary packages
  * `com.microsoft.azure:spark-mssql-connector_2.12_3.0:1.0.0-alpha` from `Maven`
  * `adal` from `PYPI`

* Also, if you haven’t already, [Create a Secret Scope](https://learn.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes)
  to your `Azure Key Vault` where your `Client ID`, `Secret`, and `Tenant ID` have
  been generated.

* Get `Access Token` from Service Principle authentication request

  ```python
  import adal

  sp_id = dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnId")
  sp_secret = dbutils.secrets.get(scope="defaultScope", key="DatabricksSpnSecret")
  tenant_id = dbutils.secrets.get(scope="defaultScope", key="TenantId")

  context = adal.AuthenticationContext(f"https://login.windows.net/{tenant_id}")
  token = context.acquire_token_with_client_credentials(
      "https://database.windows.net/",
      sp_id,
      sp_secret,
  )
  access_token = token["accessToken"]
  ```

- Read a table from Azure SQL

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
          .load()
  )
  ```

!!! note

    Executing custom SQL through the connector. The previous Azure SQL Connector
    for Spark provided the ability to execute custom SQL code like DML or DDL statements
    through the connector. This functionality is out-of-scope of this connector since
    it is based on the DataSource APIs. This functionality is readily provided by
    libraries like `pyodbc`, or you can use the standard java sql interfaces as well.

#### Method 02: JDBC Connector

More detail about [Microsoft JDBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/jdbc/microsoft-jdbc-driver-for-sql-server?view=sql-server-ver16).

```python
jdbcHostname = "******.database.windows.net"
jdbcPort = 1433
jdbcDatabase = "******"
jdbcTable = "******"
dbr_PrincipalId = "******"
dbr_PrincipalSecret = "******"

jdbcUrl = f"jdbc:sqlserver://{jdbcHostname}:{jdbcPort};database={jdbcDatabase}"

connectionProperties = {
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
    "authentication": "ActiveDirectoryServicePrincipal",
    "UserName": dbr_PrincipalId ,
    "Password": dbr_PrincipalSecret
}

df = spark.read.jdbc(
    url=jdbcUrl,
    table=jdbcTable,
    properties=connectionProperties,
)
```

## SQL Authentication

### 1) Create SQL User & Password

```sql
USE [master];
CREATE LOGIN [cnct-adb-dev] WITH PASSWORD = 'P@ssW0rd'
GO

USE [<database-name>];
CREATE USER [cnct-adb-dev] FOR LOGIN [cnct-adb-dev];
GO
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
    GRANT CREATE TABLE TO [cnct-adb-dev];
    GRANT ALTER ON SCHEMA::dbo TO [cnct-adb-dev];
    ```

### 2) Connection Code

#### Method 01: Use PyODBC

```text
%sh
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get -q -y install msodbcsql17
```

```python
import pyodbc
server = '<Your_server_name>'
database = '<database_name>'
username = '[cnct-adb-dev]'
password = '<password>'

conn = pyodbc.connect(
  f'DRIVER={{ODBC Driver 17 for SQL Server}};'
  f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
)
```

- https://stackoverflow.com/questions/62005930/using-pyodbc-in-azure-databrick-for-connecting-with-sql-server

#### Method 02: Use JDBC on Databricks

```python
remote_table = (
    spark.read
        .format("sqlserver")
        .option("host", "hostName")
        .option("port", "1433")
        .option("user", "[cnct-adb-dev]")
        .option("password", "password")
        .option("database", "databaseName")
        .option("dbtable", "schemaName.tableName") # (if schemaName not provided, default to "dbo")
        .load()
)
```

#### Method 02: Use JDBC (Legacy)

```python
database_host = "<database-host-url>"
database_port = "1433"
database_name = "<database-name>"
url = f"jdbc:sqlserver://{database_host}:{database_port};database={database_name}"

remote_table = (
    spark.read
        .format("jdbc")
        .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver")
        .option("url", url)
        .option("dbtable", "tableName")
        .option("user", "[cnct-adb-dev]")
        .option("password", "password")
        .load()
)
```

## References

* [TheDataSwamp: Databricks](https://www.thedataswamp.com/blog/databricks-connect-to-azure-sql-with-service-principal)
* [Databricks: External Data - SQL Server](https://docs.databricks.com/en/external-data/sql-server.html)
* https://learn.microsoft.com/en-us/sql/connect/spark/connector?view=sql-server-ver16
