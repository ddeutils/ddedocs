# Azure Function App: _Connect to Azure Synapse_

## Using ActiveDirectoryMSI

- Enable Azure Function Managed Service Identity (MSI)
- Enable AAD integration for Azure SQL Server
- Add The Azure Function MSI User to the DB

    ```sql
    CREATE USER "<MSI user display name>" FROM EXTERNAL PROVIDER;
    ```

- Use `Authentication=ActiveDirectoryMsi` in your `pyodbc.connect`


## Reference

- [Azure Function MSI Python](https://github.com/crgarcia12/azure-function-msi-python)
