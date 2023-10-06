# Azure Data Factory Link Service: _SQL Database_

**Table of Contents**:

- [Create Link Service for SQL Database](#create-link-service-for-sql-database)

## Create Link Service for SQL Database

Create dynamic parameters Azure SQL Database link service.

```json
{
    "name": "Dynamic_AzureSqlDatabase_Auto",
    "type": "Microsoft.DataFactory/factories/linkedservices",
    "properties": {
        "type": "AzureSqlDatabase",
        "parameters": {
            "Username": {
                "type": "String"
            },
            "Database": {
                "type": "String"
            },
            "Server": {
                "type": "String"
            },
            "Secret": {
                "type": "String"
            }
        },
        "annotations": [],
        "typeProperties": {
            "connectionString": "Integrated Security=False;Encrypt=True;Connection Timeout=30;Data Source=@{linkedService().Server};Initial Catalog=@{linkedService().Database};User ID=@{linkedService().Username}",
            "password": {
                "type": "AzureKeyVaultSecret",
                "store": {
                    "referenceName": "<key-vault-link-service-name>",
                    "type": "LinkedServiceReference"
                },
                "secretName": {
                    "value": "@linkedService().Secret",
                    "type": "Expression"
                }
            }
        },
        "connectVia": {
            "referenceName": "<integration-runtime-name>",
            "type": "IntegrationRuntimeReference"
        }
    }
}
```

!!! note

    If you want to use `AutoResolveIntegrationRuntime`, you can delete key `connectVia`
    from above json data.

## References

- https://www.tech-findings.com/2021/09/i-getting-started-with-adf-creating-and.html
