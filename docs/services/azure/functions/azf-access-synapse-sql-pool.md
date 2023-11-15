# Azure Function: _To Synapse SQL Pool_

## Managed Service Identity

### 1) Enable MSI

Enable Managed Service Identity (MSI) on Azure Function App Protol.

* Go to Azure Function App :octicons-arrow-right-24: Select `Identity`
  :octicons-arrow-right-24: Click nav `System Assigned`
* On Status :octicons-arrow-right-24: Enable to `On` :octicons-arrow-right-24:
  Click `Save`

### 2) Enable AAD integration

Enable AAD integration for Azure Synapse Workspace.

* Go to Azure Synapse Workspace :octicons-arrow-right-24: Select `Azure Active Directory`
* Click nav `Set admin` :octicons-arrow-right-24: Select your user :octicons-arrow-right-24: Click `Save`

### 3) Add user to Azure Synapse

Add The Azure Function MSI User to the Azure Synapse SQL Pool.

* Connect to **Azure Synapse SQL Pool** on target database.
* Create MSI user that use the Azure Function name

  ```sql
  CREATE USER <azure-function-name> FROM EXTERNAL PROVIDER
  GO
  ```

### 4) Connection Code

Use `Authentication=ActiveDirectoryMsi` in the Python code.

```python
import logging
import pyodbc

server = 'tcp:<server-name>.database.windows.net'
database = '<database-name>'
driver = '{ODBC Driver 17 for SQL Server}'

with pyodbc.connect(
    (
        f"Driver={driver};Server={server};PORT=1433;Database={database};"
        f"Authentication=ActiveDirectoryMsi;"
    )
) as conn:
    logging.info("Successful connection to database")
    with conn.cursor() as cursor:
        cursor.execute("SELECT <column-name> FROM <table-name>;")
        row = cursor.fetchone()
        while row:
            logging.info(str(row[0]).strip())
            row = cursor.fetchone()
```

## SQL Authentication

### 1) Connection Code

```python
import logging
import pyodbc

server = 'tcp:<server-name>.database.windows.net'
database = '<database-name>'
driver = '{ODBC Driver 17 for SQL Server}'

username = "<username>"
password = "P@ssW0rd"

with pyodbc.connect(
    (
        f"Driver={driver};Server={server};PORT=1433;Database={database};"
        f"UID={username};PWD={password}"
    )
) as conn:
    logging.info("Successful connection to database")
    with conn.cursor() as cursor:
        cursor.execute("SELECT <column-name> FROM <table-name>;")
        row = cursor.fetchone()
        while row:
            logging.info(str(row[0]).strip())
            row = cursor.fetchone()
```

## Reference

- [Azure Function MSI Python](https://github.com/crgarcia12/azure-function-msi-python)
