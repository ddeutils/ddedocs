# Databricks connect to Azure SQL


**Table of Contents**:

- [Connect to Azure SQL with Service Principal](#connect-to-azure-sql-with-service-principal)
  - [Create Service Principal](#create-service-principal)
  - [Create user in Azure SQL](#create-user-in-azure-sql)
  - [Connection code in Databricks](#connection-code-in-databricks)
- [Connect to Azure SQL with SQL Authentication]

## Connect to Azure SQL with Service Principal

When using the **Apache Spark Connector** for Azure Server in Databricks, I’ve
seen a lot of people using SQL authentication instead of authenticating with
**Azure Active Directory** (AAD). The server admin login and password, which are
generated on the creation of the server are retrieved from `Key Vault` to Create
objects, run queries, and load data. This is all very well, but the admin account
has admin rights, which isn’t ideal if you want to restrict what can be run in
**Azure Server**.

### Create Service Principal

To register your application and create your service principal

- Go to `Azure Active Directory` => `App registrations` => `New registration`
- Add the information of this app like `name` is `cnct-adb-dev`
- Click register for create

> **Note**: \
> The name of app should be format, `{app}-{resource-shortname}-{environment}`

You will then have to generate a secret

- Go to `App registrations` => `Certificates&secrets` => `New Client Secret`
- Save this value to `Azure Key Vaults`

> **Note**: \
> We write both the `Client ID` and `Secret` to Key Vault for a number of reasons:
> - The `Secret` is sensitive and like a `Storage Key` or `Password`, we don't want
>   this to be hardcoded or exposed anywhere in our application.
> - Normally we would have an instance of `Databricks` and `Key Vault` per environment
>   and when we come to referencing the secrets, we want the secrets names to remain
>   the same, so the code in our Databricks notebooks referencing the `Secrets` doesn't
>   need to be modified when we deploy to different environments.

> **Warning**: \
> The App registration is the template used to create the security principal (like a User)
> which can be authenticated and authorized.

### Create user in Azure SQL

The app registration still needs permission to log into `Azure SQL` and access the
objects within it. You’ll need to Create that user (**App & Service Principal**) in the
database and then grant it permissions on the underlying objects.

```sql
CREATE USER [cnct-adb-dev] FROM EXTERNAL PROVIDER;
GRANT SELECT ON SCHEMA::dbo TO [cnct-adb-dev];
```

### Connection code in Databricks

To connect to `Azure SQL`, you will need to install the [SQL Spark Connector](https://github.com/microsoft/sql-spark-connector)
and the [Microsoft Azure Active Directory Authentication Library](https://pypi.org/project/adal/)
(ADAL) for Python code.

- Go to your cluster in Databricks and Install necessary packages
  - `com.microsoft.azure:spark-mssql-connector_2.12_3.0:1.0.0-alpha` from `Maven`
  - `adal` from `PYPI`

  > **Note**: \
  > More detail about [Microsoft JDBC Driver for SQL Server](https://learn.microsoft.com/en-us/sql/connect/jdbc/microsoft-jdbc-driver-for-sql-server?view=sql-server-ver16)

- Also, if you haven’t already, [Create a Secret Scope](https://learn.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes)
  to your `Azure Key Vault` where your `Client ID`, `Secret`, and `Tenant ID` have
  been generated.

- Get `Access Token` from Service Principle authentication request

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

> Note: \
> Executing custom SQL through the connector. The previous Azure SQL Connector
> for Spark provided the ability to execute custom SQL code like DML or DDL statements
> through the connector. This functionality is out-of-scope of this connector since
> it is based on the DataSource APIs. This functionality is readily provided by
> libraries like `pyodbc`, or you can use the standard java sql interfaces as well.

## Connect to Azure SQL with SQL Authentication

### Method 01: Use PyODBC

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
username = '<username>'
password = '<password>'

conn = pyodbc.connect(
  f'DRIVER={{ODBC Driver 17 for SQL Server}};'
  f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
)
```

- https://stackoverflow.com/questions/62005930/using-pyodbc-in-azure-databrick-for-connecting-with-sql-server

## References

- https://www.thedataswamp.com/blog/databricks-connect-to-azure-sql-with-service-principal
