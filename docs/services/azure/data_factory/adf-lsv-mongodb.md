# Azure Data Factory: _Link MongoDB_

## Create Link Service

Create dynamic parameters MongoDB link service.

```json
{
    "name": "MongoDBAuto",
    "type": "Microsoft.DataFactory/factories/linkedservices",
    "properties": {
        "type": "MongoDbV2",
        "annotations": [],
        "parameters": {
            "Database": {
                "type": "String"
            },
            "Secret": {
                "type": "String"
            }
        },
        "typeProperties": {
            "connectionString": {
                "type": "AzureKeyVaultSecret",
                "store": {
                    "referenceName": "<key-vault-link-service-name>",
                    "type": "LinkedServiceReference"
                },
                "secretName": "@linkedService().Secret"
            },
            "database": "@linkedService().Database"
        },
        "connectVia": {
            "referenceName": "<integration-runtime-name>",
            "type": "IntegrationRuntimeReference"
        }
    }
}
```

The Connection String that keep in Azure Key Vaults:

```text
mongodb://<username>:<password>@<host>:27017
```
