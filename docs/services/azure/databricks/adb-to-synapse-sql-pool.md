# Databricks: _To Synapse SQL Pool_

When you want to read and write data on **Azure Synapse Analytic SQL Pool** via
**Azure Databricks**, that has 2 types of Azure Synapse SQL Pool:

* [Serverless SQL Pool](#access-serverless-sql-pool)
* [Dedicate SQL Pool](#access-dedicate-sql-pool)

!!! note

    Why do we need staging storage?

    Staging folder is needed to store some temporary data whenever we read/write
    data from/to `Azure Synapse`. Whenever we read/write data, we actually
    leverage **PolyBase** to move the data, which staging storage is used to achieve
    high performance.

## Access Serverless SQL Pool

### 1) Create Database Scope

If you want to see the list of existing database scope credential, you can use
this command:

```sql
SELECT * FROM [sys].[database_scoped_credentials];
```

### 2) Create External Data Source

Create external datasource for connection from Synapse Serverless to Azure Data
Lake Storage.

```sql
IF NOT EXISTS (
    SELECT *
    FROM [sys].[external_data_sources]
    WHERE NAME = 'dataplatdev_curated_adb'
)
    CREATE EXTERNAL DATA SOURCE [dataplatdev_curated_adb]
    WITH (
        CREDENTIAL = [adb_cred],
        LOCATION = 'abfss://{curated}@{dataplatdev}.dfs.core.windows.net'
    );
GO
```

!!! abstract

    ```sql
    SELECT * FROM [sys].[external_data_sources];
    ```

### 3) Create User in Serverless SQL Pool

Create login user and grant permission reference above database scope credential

```sql
CREATE LOGIN [adbuser] WITH PASSWORD = 'Gl2vimQkvpZp'
;
GRANT REFERENCES ON DATABASE SCOPED CREDENTIAL::[adb_cred] TO [adbuser];
GO
```

Create temp view for read data from above external datasource

```sql
CREATE OR ALTER VIEW [CURATED].[VW_DELTA_SALES]
AS SELECT *
   FROM OPENROWSET(
       BULK '/{delta_silver}/{table_sales}',
       DATA_SOURCE = 'dataplatdev_curated_adb',
       FORMAT = 'DELTA'
   ) AS [R]
;

GRANT SELECT ON OBJECT::[CURATED].[VW_DELTA_SALES] TO [adbuser]
;
```

More Detail, [Control storage account access for serverless SQL pool in Azure Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/develop-storage-files-storage-access-control?tabs=service-principal#supported-storage-authorization-types)

### 4) Connection Code

#### Method 01: JDBC Connector

This method reads or writes the data row by row, resulting in performance issues.
**Not Recommended**.

Set Spark Config:

=== "Azure Data Lake Gen 2"

    ```python
    spark.conf.set(
        "fs.azure.account.key.{dataplatdev}.dfs.core.windows.net",
        "<storage-account-access-key>"
    )
    sc._jsc.hadoopConfiguration().set(
        "fs.azure.account.key.{dataplatdev}.dfs.core.windows.net",
        "<storage-account-access-key>"
    )
    ```

=== "Azure Blob Storage"

    ```python
    spark.conf.set(
        "fs.azure.account.key.{dataplatdev}.blob.core.windows.net",
        "<storage-account-access-key>"
    )
    sc._jsc.hadoopConfiguration().set(
        "fs.azure.account.key.{dataplatdev}.blob.core.windows.net",
        "<storage-account-access-key>"
    )
    ```

**Make JDBC URL**:

```python
URL = (
    f"jdbc:sqlserver://{server}:1433;database={database};user={username};password={password};"
    f"encrypt=true;trustServerCertificate=true;hostNameInCertificate=*.sql.azuresynapse.net;loginTimeout=30;"
)
```

=== "Azure Data Lake Gen 2"

    ```python
    df = (
      spark.read
          .format("jdbc")
          .option("url", URL)
          .option("tempDir", "abfss://{curated}@{storage-account}.dfs.core.windows.net/<folder-for-temporary-data>")
          .option("forwardSparkAzureStorageCredentials", "true")
          .option("query", "SELECT * FROM [CURATED].[VW_DELTA_SALES]")
          .load()
      )
    ```

=== "Azure Blob Storage"

    ```python
    df = (
      spark.read
          .format("jdbc")
          .option("url", URL)
          .option("tempDir", "wasbs://{curated}@{storage-account}.blob.core.windows.net/<folder-for-temporary-data>")
          .option("forwardSparkAzureStorageCredentials", "true")
          .option("query", "SELECT * FROM [CURATED].[VW_DELTA_SALES]")
          .load()
      )
    ```

**Reference**:

* [Microsoft Databricks JDBC](https://learn.microsoft.com/en-us/azure/databricks/external-data/jdbc)
* [Spark SQL Data Source JDBC](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html)

#### Method 02: Spark Connector

This method uses bulk insert to read/write data. There are a lot more options that
can be further explored. First Install the Library using **Maven Coordinate** in
the Data-bricks cluster, and then use the below code. **Recommended for Azure
SQL DB or Sql Server Instance**

Install Driver on cluster:

* **Maven**: `com.microsoft.azure:spark-mssql-connector_2.12:1.2.0`

    | SPARK VERSION | MAVEN DEPENDENCY                                                                                 |
    |---------------|--------------------------------------------------------------------------------------------------|
    | Spark 2.4.x   | groupeId : com.microsoft.azure <br> artifactId : spark-mssql-connector <br> version : 1.0.2      |
    | Spark 3.0.x   | groupeId : com.microsoft.azure <br> artifactId : spark-mssql-connector_2.12 <br> version : 1.1.0 |
    | Spark 3.1.x   | groupeId : com.microsoft.azure <br> spark-mssql-connector_2.12 <br> version : 1.2.0              |

    Read More [Supported Version](https://search.maven.org/search?q=spark-mssql-connector)

=== "Table"

    ```python
    df = (
      spark.read
        .format("com.microsoft.sqlserver.jdbc.spark")
        .option("url", "jdbc:sqlserver://<server-name>:1433;database=<database-name>;")
        .option("user", username)
        .option("password", password)
        .option("mssqlIsolationLevel", "READ_UNCOMMITTED")
        .option("encrypt", "true")
        .option("dbTable", "[<schema>].[<table-or-view>]")
        .load()
    )
    ```

=== "Custom Query"

    ```python
    df = (
      spark.read
        .format("com.microsoft.sqlserver.jdbc.spark")
        .option("url", "jdbc:sqlserver://<server-name>:1433;database=<database-name>;")
        .option("user", username)
        .option("password", password)
        .option("mssqlIsolationLevel", "READ_UNCOMMITTED")
        .option("encrypt", "true")
        .option("query", "SELECT * FROM [sys].[external_data_sources]")
        .load()
    )
    ```

**Reference**:

* [Microsoft SQL Spark Connector](https://learn.microsoft.com/en-us/sql/connect/spark/connector?view=sql-server-ver15)
* [SQL Spark Connector](https://github.com/microsoft/sql-spark-connector)

## Access Dedicate SQL Pool

When connect to Azure Synapse Dedicated SQL Pool, we will use special spark connector,
`com.databricks.spark.sqldw` method.
This method previously uses **Poly-base** to read and write data to and from
`Azure Synapse` using a staging server (mainly, blob storage or a Data Lake storage
directory), but now data are being read and write using **Copy**, as the Copy method
has improved performance. **Recommended for Azure Synapse**

!!! note

    This connector is for use with **Synapse Dedicated Pool instances only**,
    and is not compatible with other Synapse components.

### SQL Authentication

#### 1) Connection Code

```python
spark.conf.set("spark.databricks.sqldw.writeSemantics", "copy")
```

```python
df = (
    spark.read
        .format("com.databricks.spark.sqldw")
        .option("url", f"jdbc:sqlserver://<work-space-name>;database=<database-name>;")
        .option("user", "<username>")
        .option("password", "<password>")
        .option("forwardSparkAzureStorageCredentials", "true")
        .option("dbTable", "<your-table-name>")
        .option("tempDir", "abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<directory-name>")
        .option("hostNameInCertificate", "*.sql.azuresynapse.net")
        .option("loginTimeout", "30")
        .option("encrypt", "true")
        .option("trustServerCertificate", "true")
        .load()
)
```

**Reference**:

* https://bennyaustin.com/2020/02/05/pysparkupsert/

### Azure Service Principle

#### 1) Create Service Principal

* Go to `Azure Active Directory` :octicons-arrow-right-24: `App registrations`
  :octicons-arrow-right-24: `New registration`
* Add the information of this app like `name` is `adb_to_synapse`
* Click register for create
* Go to `App registrations` :octicons-arrow-right-24: `Certificates&secrets`
  :octicons-arrow-right-24: `New Client Secret`
* Save this value to `Azure Key Vaults`

#### 2) Create User in Azure Synapse

* Give it some permissions (On the Dedicated SQL pool, we can add a user and
  assign it to the proper role),

  ```sql
  CREATE USER [adb_to_synapse] FROM EXTERNAL PROVIDER;
  sp_addrolemember 'db_owner','adb_to_synapse';
  GO
  ```

!!! warning

    The permission of the user should be owner of database because it is currently
    required for Databricks to run `CREATE DATABASE SCOPED CREDENTIAL`.

!!! note

    If you do not want to give owner permission to your Service Principle,
    you can grant `CONTROL`.

    ```sql
    CREATE ROLE [databricks_reader];
    EXEC sp_addrolemember 'databricks_reader', 'adb_to_synapse';
    GRANT CONTROL TO [adb_to_synapse];
    ```

#### 3) Azure Storage Temp Account

* Go to `Storage account` :octicons-arrow-right-24: `Access Control (IAM)`
  :octicons-arrow-right-24: `Add role assignment`
* Select Role: `Storage Blob Data Contributor`
* Select: `register application`
* Click on save.

#### 4) Connection Code

**OAuth Configuration**:

```python
spark.conf.set("fs.azure.account.auth.type", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type",  "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id", "<service-principal-id>")
spark.conf.set("fs.azure.account.oauth2.client.secret", "<service-principal-secret>")
spark.conf.set("fs.azure.account.oauth2.client.endpoint", "https://login.microsoftonline.com/<directory-id>/oauth2/token")

spark.conf.set("spark.databricks.sqldw.jdbc.service.principal.client.id", "<service-principal-id>")
spark.conf.set("spark.databricks.sqldw.jdbc.service.principal.client.secret", "<service-principal-secret>")
```

**JDBC URL Pattern**:

```python
URL: str = (
    "jdbc:sqlserver://<work-space-name>.sql.azuresynapse.net:1433;"
    "database=<database-name>;"
    "encrypt=true;trustServerCertificate=true;"
    "hostNameInCertificate=*.sql.azuresynapse.net;"
    "loginTimeout=30"
)
```

```python
df = (
  spark.read
    .format("com.databricks.spark.sqldw")
    .option("url", "jdbc:sqlserver://<work-space-name>.sql.azuresynapse.net:1433;")
    .option("tempDir", "abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<directory-name>")
    .option("enableServicePrincipalAuth", "true")
    .option("dbTable", "[<schema>].[<table-name>]")
    .load()
)
```

**References**:

* https://pl.seequality.net/load-synapse-analytics-sql-pool-with-azure-databricks/
* https://learn.microsoft.com/en-us/answers/questions/327270/azure-databricks-to-azure-synapse-service-principa?orderby=newest

## Send DDL or DML to Azure Synapse SQL Pool

When execute DDL or DML statement to Azure Synapse SQL Pool, that has 2 solutions:
JDBC, and ODBC drivers.

### JDBC Driver

#### 1) Create JDBC Connection

```python
URL = f"jdbc:sqlserver://{server}:1433;database={database};"

props = spark._sc._gateway.jvm.java.util.Properties()
props.putAll({
    'username': username,
    'password': password,
    'Driver': "com.microsoft.sqlserver.jdbc.SQLServerDriver",
})

Connection = spark._sc._gateway.jvm.java.sql.Connection

driver_manager = spark._sc._gateway.jvm.java.sql.DriverManager
connection: Connection = driver_manager.getConnection(URL, props)
```

#### 2) Connection Code

=== "Statement Execution"

    ```python
    ResultSet = spark._sc._gateway.jvm.java.sql.ResultSet
    ResultSetMetaData = spark._sc._gateway.jvm.java.sql.ResultSetMetaData
    Connection = spark._sc._gateway.jvm.java.sql.Connection
    Statement = spark._sc._gateway.jvm.java.sql.Statement

    stmt: Statement = connection.createStatement()  # Statement
    ```

    ```python
    query: str = f"""
      SELECT * FROM [<schema>].[<table-name>]
    """

    rs: ResultSet = stmt.executeQuery(query)  # ResultSet
    metadata: ResultSetMetaData = rs.getMetaData()  # ResultSetMetaData
    col_numbers = metadata.getColumnCount()

    col_names: list = []
    for i in range(1, col_numbers + 1):
        if column:
          col_names.append(metadata.getColumnName(i))
        else:
          col_names.append(f"col_{i}")

    results: list = []
    while rs.next():
      result: dict = {}
      for i in range(col_numbers):
        name: str = col_names[i]
        result[name] = rs.getString(name)
      results.append(result)
    ```

    ```python
    stmt.close()
    connection.close()
    ```

=== "Batch Execution"

    ```python
    PreparedStatement = spark._sc._gateway.jvm.java.sql.PreparedStatement

    preps: PreparedStatement = connection.prepareStatement(
      "INSERT INTO [dev].[people]"
      "VALUES (?, ?, ?);"
    )
    rows = [
      ["Gandhi", "politics", 12],
      ["Turing", "computers", 31],
    ]
    for row in rows:
      for idx, data in enumerate(row, start=1):
        if isinstance(data, int):
          preps.setInt(idx, data)
        else:
          preps.setString(idx, data)
      preps.addBatch()

    connection.setAutoCommit(False)
    result_number: int = preps.executeBatch()
    preps.clearBatch()
    connection.setAutoCommit(True)
    ```

    > **Note**:
    > Add parameter `rewriteBatchedStatements=true` to JDBC URL for improve execute
    > performance from before add this parameter,
    > ```sql
    > INSERT INTO jdbc (`name`) VALUES ('Line 1: Lorem ipsum ...')
    > INSERT INTO jdbc (`name`) VALUES ('Line 2: Lorem ipsum ...')
    > ```
    > Then, after add this parameter to JDBC URL,
    > ```sql
    > INSERT INTO jdbc (`name`) VALUES ('Line 1: Lorem ipsum ...'), ('Line 2: Lorem ipsum ...')
    > ```


=== "Call Store Procedure"

    ```python
    exec_statement = connection.prepareCall(
        f"""{{CALL {schema}.usp_stored_procedure(
          {master_id}, {parent_id}, {child_id}, '{table}', ?,
          ?, ?, ?, ?
        )}}"""
    )
    exec_statement.setString(5, 'data')

    exec_statement.registerOutParameter(1, spark._sc._gateway.jvm.java.sql.Types.INTEGER)
    exec_statement.registerOutParameter(2, spark._sc._gateway.jvm.java.sql.Types.VARCHAR)
    exec_statement.registerOutParameter(3, spark._sc._gateway.jvm.java.sql.Types.VARCHAR)
    exec_statement.registerOutParameter(4, spark._sc._gateway.jvm.java.sql.Types.VARCHAR)

    exec_statement.executeUpdate()

    res1 = exec_statement.getInt(1)
    res2 = exec_statement.getString(2)
    res3 = exec_statement.getString(3)
    res4 = exec_statement.getString(4)

    exec_statement.close()
    connection.close()
    ```

    **Reference**:

    * [How to Call MSSQL Stored Procedure](https://blog.devgenius.io/how-to-call-mssql-stored-procedure-pass-and-get-multiple-parameters-in-spark-using-aws-glue-f21b2f19657b)

### ODBC Driver

#### 1) Create ODBC Connection

```text
%sh
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get -q -y install msodbcsql17
```

```python
import pyodbc
server = '<server-name>'
database = '<database-name>'
username = '<username>'
password = '<password>'

conn = pyodbc.connect(
  f'DRIVER={{ODBC Driver 17 for SQL Server}};'
  f'SERVER={server};DATABASE={database};UID={username};PWD={password}'
)
```

**Reference**:

* [Using PyODBC in Azure Databricks for Connecting with MSSQL](https://stackoverflow.com/questions/62005930/using-pyodbc-in-azure-databrick-for-connecting-with-sql-server)

## References

* (https://docs.databricks.com/data/data-sources/azure/synapse-analytics.html)
* (https://joeho.xyz/blog-posts/how-to-connect-to-azure-synapse-in-azure-databricks/)
* (https://learn.microsoft.com/en-us/answers/questions/653154/databricks-packages-for-batch-loading-to-azure.html)
* (https://stackoverflow.com/questions/55708079/spark-optimise-writing-a-dataframe-to-sql-server/55717234) (***)
* (https://docs.databricks.com/external-data/synapse-analytics.html)
* (https://learn.microsoft.com/en-us/azure/synapse-analytics/security/how-to-set-up-access-control)
