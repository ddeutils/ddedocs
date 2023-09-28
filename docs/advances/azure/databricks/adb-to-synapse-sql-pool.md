# Databricks connect to Synapse Analytic SQL Pool

**Update**: `2023-04-27` |
**Tag**: `Azure` `Synapse Analytic` `Databricks`

When you want to read and write data on Azure Synapse Analytic SQL Pool via Azure Databricks,
that has 2 types of Azure Synapse SQL Pool: **Serverless**, and **Dedicate**.

**Table of Contents**:

- [Connect to Azure Synapse Serverless SQL Pool](#connect-to-azure-synapse-serverless-sql-pool)
- [Connect to Azure Synapse Dedicate SQL Pool](#connect-to-azure-synapse-dedicate-sql-pool)
- [Send DDL or DML to Azure Synapse SQL Pool](#send-ddl-or-dml-to-azure-synapse-sql-pool)
  - [JDBC Driver](#jdbc-driver)
  - [ODBC Driver](#odbc-driver)

## Connect to Azure Synapse Serverless SQL Pool

### Why do we need staging storage?

As mentioned above, staging folder is needed to store some temporary data whenever
we read/write data from/to `Azure Synapse`. Whenever we read/write data, we actually
leverage **PolyBase** to move the data, which staging storage is used to achieve
high performance.

### Create user in Azure Synapse Serverless

If you want to see the list of existing database scope credential, you can use this
command:

```sql
SELECT * FROM [sys].[database_scoped_credentials];
```

- Create individual database user for the JDBC connection

  ```sql
  CREATE MASTER KEY ENCRYPTION BY PASSWORD = 'sGrZ8Tes7qMC';
  SELECT * FROM [sys].[symmetric_keys];
  GO
  ```

- Create the database scope credential

  ```sql
  CREATE DATABASE SCOPED CREDENTIAL adb_cred
  WITH IDENTITY = 'Managed Identity';
  GO
  ```

  > **Note**: \
  > In an Azure Synapse Analytics serverless SQL pool, database-scoped credentials
  > can specify workspace `Managed Identity`, `service principal name`, or `shared access signature`
  > (SAS) token. \
  > Service Principal should be assigned Storage Blob Data Owner/Contributor/Reader
  > role in order for the application to access the data.
  >
  > ```sql
  > CREATE DATABASE SCOPED CREDENTIAL adb_cred
  > WITH IDENTITY = '<service-priciple-name>@https://login.microsoftonline.com/<directory-id>/oauth2/token',
  > SECRET = <service-priciple-secret>;
  > ```

  > **Warning**: \
  > Before creating a database scoped credential, the database must have a master
  > key to protect the credential.

- Create login user and grant permission reference above database scope credential

  ```sql
  CREATE LOGIN adbuser WITH PASSWORD = 'Gl2vimQkvpZp';
  GRANT REFERENCES ON DATABASE SCOPED CREDENTIAL::adb_cred TO adbuser;
  GO
  ```

- Create external datasource for connection from Synapse Serverless to ADLS

  ```sql
  IF NOT EXISTS (
          SELECT *
          FROM sys.external_data_sources
          WHERE NAME = 'dataplatdev_curated_adb'
      )
      CREATE EXTERNAL DATA SOURCE dataplatdev_curated_adb
      WITH (
          CREDENTIAL = adb_cred,
          LOCATION = 'abfss://{curated}@{dataplatdev}.dfs.core.windows.net'
      );
  SELECT * FROM sys.external_data_sources;
  GO
  ```

- Create temp view for read data from above external datasource

  ```sql
  CREATE OR ALTER VIEW [CURATED].[VW_DELTA_SALES]
  AS SELECT *
     FROM OPENROWSET(
         BULK '/{delta_silver}/{table_sales}',
         DATA_SOURCE = 'dataplatdev_curated_adb',
         FORMAT = 'DELTA'
     ) AS [R]
  ;
  GRANT SELECT ON OBJECT::[CURATED].[VW_DELTA_SALES] TO adbuser;
  ```

> Note:
> More Detail, [Control storage account access for serverless SQL pool in Azure Synapse Analytics](https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/develop-storage-files-storage-access-control?tabs=service-principal#supported-storage-authorization-types)

### Connection code in Databricks

- **Method 01**: Using JDBC Connector

  This method reads or writes the data row by row, resulting in performance issues.
  **Not Recommended**.

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

  > **Note**: \
  > For Azure Blob Storage will use `fs.azure.account.key.{dataplatdev}.blob.core.windows.net`

  ```python
  URL = (
      f"jdbc:sqlserver://{server}:1433;database={database};user={username};password={password};"
      f"encrypt=true;trustServerCertificate=true;hostNameInCertificate=*.sql.azuresynapse.net;loginTimeout=30;"
  )
  ```

  > **Note**: \
  > For Azure Blob Storage will use `wasbs://<container>@<your-storage-account-name>.blob.core.windows.net/<folder-for-temporary-data>`

  ```python
  (
    spark.read
      .format("jdbc")
      .option("url", URL)
      .option("tempDir", "abfss://{curated}@{dataplatdev}.dfs.core.windows.net/temp")
      .option("forwardSparkAzureStorageCredentials", "true")
      .option("query", "SELECT * FROM [CURATED].[VW_DELTA_SALES]")
      .load()
  )
  ```

  > **Reference:**
  > - [Microsoft Databricks JDBC](https://learn.microsoft.com/en-us/azure/databricks/external-data/jdbc)
  > - [Spark SQL Data Source JDBC](https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html)

- **Method 02**: Using Apache Spark Connector

  This method uses bulk insert to read/write data. There are a lot more options that
  can be further explored. First Install the Library using **Maven Coordinate** in
  the Data-bricks cluster, and then use the below code. **Recommended for Azure
  SQL DB or Sql Server Instance**

  - Install driver on cluster `com.microsoft.azure:spark-mssql-connector_2.12:1.2.0` with `Maven`

  ```python
  URL = f"jdbc:sqlserver://{server}:1433;database={database};"
  ```

  ```python
  (
    spark.read
      .format("com.microsoft.sqlserver.jdbc.spark")
      .option("url", URL)
      .option("user", username)
      .option("password", password)
      .option("mssqlIsolationLevel", "READ_UNCOMMITTED")
      .option("encrypt", "true")
      .option("query", "SELECT * FROM [sys].[external_data_sources]")
      .load()
  )
  ```

  ```python
  (
    spark.read \
      .format("com.microsoft.sqlserver.jdbc.spark")
      .option("url", URL)
      .option("user", username)
      .option("password", password)
      .option("mssqlIsolationLevel", "READ_UNCOMMITTED")
      .option("encrypt", "true")
      .option("dbTable", "[<schema>].[<table-or-view>]")
      .load()
  )
  ```

  > **Reference:**
  > - [Microsoft SQL Spark Connector](https://learn.microsoft.com/en-us/sql/connect/spark/connector?view=sql-server-ver15)
  > - [SQL Spark Connector](https://github.com/microsoft/sql-spark-connector)

## Connect to Azure Synapse Dedicate SQL Pool

When connect to Azure Synapse Dedicated SQL Pool, we will use special spark connector,
`com.databricks.spark.sqldw` method.
This method previously uses **Poly-base** to read and write data to and from
`Azure Synapse` using a staging server (mainly, blob storage or a Data Lake storage
directory), but now data are being read and write using **Copy**, as the Copy method
has improved performance. **Recommended for Azure Synapse**

> **Note**: \
> This connector is for use with **Synapse Dedicated Pool instances only**,
> and is not compatible with other Synapse components.

#### Using SQL Authentication

- Configuration

  ```python
  spark.conf.set("spark.databricks.sqldw.writeSemantics", "copy")

  URL = (
      f"jdbc:sqlserver://{server}:1433;database={database};user={username};password={password};"
      f"encrypt=true;trustServerCertificate=true;hostNameInCertificate=*.sql.azuresynapse.net;loginTimeout=30;"
  )
  ```

  ```python
  (
    spark.read
      .format("com.databricks.spark.sqldw")
      .option("url", f"jdbc:sqlserver://{server};database={database};")
      .option("user", username)
      .option("password", password)
      .option("forwardSparkAzureStorageCredentials", "true")
      .option("dbTable", "<your-table-name>")
      .option("tempDir", "abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<directory-name>")
      .load()
  )
  ```
> **Reference**:
> - https://bennyaustin.com/2020/02/05/pysparkupsert/

#### Using App Registration Authentication

- **Azure App Registration**:
  - Go to `App registrations` => `New registration`
  - Add the information of this app like `name` is `databricks_to_synapse`
  - Click register for create
  - Go to `App registrations` => `Certificates&secrets` => `New Client Secret`
  - Save this value to `Azure Key Vaults`

- **Azure Synapse**:
  - Give it some permissions (On the dedicated SQL pool, we can add a user and
    assign it to the proper role),

    ```sql
    CREATE USER [databricks_to_synapse] FROM EXTERNAL PROVIDER;
    sp_addrolemember 'db_owner','databricks_to_synapse';
    ```

  > **Warning**: \
  > The permission of the user should be owner of database because it is currently
  > required for Databricks to run `CREATE DATABASE SCOPED CREDENTIAL`.

  > **Note**: \
  > If you do not want to give owner permission to your SP, you can grant `CONTROL`;
  > ```sql
  > CREATE ROLE [databricks_reader];
  > EXEC sp_addrolemember 'databricks_reader', 'databricks_to_synapse';
  > GRANT CONTROL TO [databricks_to_synapse];
  > ```

- **Azure Storage temp account**:
  - Go to `Storage account` => `Access Control (IAM)` => `Add role assignment`
  - Select Role: `Storage Blob Data Contributor`
  - Select: `register application`
  - Click on save.

- **Azure Databricks**:
  - OAuth Configuration

    ```python
    spark.conf.set("fs.azure.account.auth.type", "OAuth")
    spark.conf.set("fs.azure.account.oauth.provider.type",  "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
    spark.conf.set("fs.azure.account.oauth2.client.id", "<service-principal-id>")
    spark.conf.set("fs.azure.account.oauth2.client.secret", "<service-principal-secret>")
    spark.conf.set("fs.azure.account.oauth2.client.endpoint", "https://login.microsoftonline.com/<directory-id>/oauth2/token")

    spark.conf.set("spark.databricks.sqldw.jdbc.service.principal.client.id", "<service-principal-id>")
    spark.conf.set("spark.databricks.sqldw.jdbc.service.principal.client.secret", "<service-principal-secret>")
    ```

    JDBC URL Pattern:

    ```text
    jdbc:sqlserver://<work-space-name>.sql.azuresynapse.net:1433;database=<database-name>;
    encrypt=true;trustServerCertificate=true;hostNameInCertificate=*.sql.azuresynapse.net;loginTimeout=30
    ```

    ```python
    (
      spark.read
        .format("com.databricks.spark.sqldw")
        .option("url", URL)
        .option("tempDir", "abfss://<container-name>@<storage-account-name>.dfs.core.windows.net/<directory-name>")
        .option("enableServicePrincipalAuth", "true")
        .option("dbTable", "[<schema>].[<table-name>]")
        .load()
    )
    ```

> **References**:
> - https://pl.seequality.net/load-synapse-analytics-sql-pool-with-azure-databricks/
> - https://learn.microsoft.com/en-us/answers/questions/327270/azure-databricks-to-azure-synapse-service-principa?orderby=newest

## Send DDL or DML to Azure Synapse SQL Pool

When execute DDL or DML statement to Azure Synapse SQL Pool, that has 2 solutions:
JDBC, and ODBC drivers.

### JDBC Driver

- Create JDBC Connection

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

- **Method 01**: Statement Execution

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

- **Method 02**: Batch Execution

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


- **Method 03**: Call Store Procedure

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

  > **Reference**:
  > - [How to Call MSSQL Stored Procedure](https://blog.devgenius.io/how-to-call-mssql-stored-procedure-pass-and-get-multiple-parameters-in-spark-using-aws-glue-f21b2f19657b)

#### ODBC Driver

- Create Connection

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

> **Reference**:
> - [Using PyODBC in Azure Databricks for Connecting with MSSQL](https://stackoverflow.com/questions/62005930/using-pyodbc-in-azure-databrick-for-connecting-with-sql-server)

## References

- https://docs.databricks.com/data/data-sources/azure/synapse-analytics.html
- https://joeho.xyz/blog-posts/how-to-connect-to-azure-synapse-in-azure-databricks/
- https://learn.microsoft.com/en-us/answers/questions/653154/databricks-packages-for-batch-loading-to-azure.html
- https://stackoverflow.com/questions/55708079/spark-optimise-writing-a-dataframe-to-sql-server/55717234 (***)
- https://docs.databricks.com/external-data/synapse-analytics.html
- https://learn.microsoft.com/en-us/azure/synapse-analytics/security/how-to-set-up-access-control
