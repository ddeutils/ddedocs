# Azure Data Factory: _Link Services_

## Azure Services

=== "KeyVault"

    ```json
    {
        "name": "KeyVaultAll",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
            "description": "All of Key Vaults",
            "annotations": [],
            "type": "AzureKeyVault",
            "typeProperties": {
                "baseUrl": "https://kv-<platform>-dev.vault.azure.net/"
            }
        }
    }
    ```

=== "Function"

    ```json
    {
        "name": "DynamicAzureFunction",
        "properties": {
            "parameters": {
                "FuctionAppUrl": {
                    "type": "string"
                },
                "Secret": {
                    "type": "string"
                }
            },
            "annotations": [],
            "type": "AzureFunction",
            "typeProperties": {
                "functionAppUrl": "@{linkedService().FuctionAppUrl}",
                "functionKey": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": {
                        "value": "@linkedService().Secret",
                        "type": "Expression"
                    }
                },
                "authentication": "Anonymous"
            }
        }
    }
    ```

=== "Batch"

    ```json
    {
        "name": "DynamicAzureBatch",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
            "type": "AzureBatch",
            "annotations": [],
            "parameters": {
                "BatchURI": {
                    "type": "String"
                },
                "Pool": {
                    "type": "String"
                },
                "Account": {
                    "type": "String"
                }
            },
            "typeProperties": {
                "batchUri": "@linkedService().BatchURI",
                "poolName": "@linkedService().Pool",
                "accountName": "@linkedService().Account",
                "linkedServiceName": {
                    "referenceName": "<azure-blob-storage-link-service-name>",
                    "type": "LinkedServiceReference"
                }
            }
        }
    }
    ```

=== "Databricks"

    ```json
    {
        "name": "DynamicAzureDatabrick",
        "properties": {
            "description": "Databrick Connection used for common dynamic",
            "parameters": {
                "ClusterURL": {
                    "type": "String"
                },
                "ClusterID": {
                    "type": "String"
                },
                "Secret": {
                    "type": "string"
                }
            },
            "annotations": [],
            "type": "AzureDatabricks",
            "typeProperties": {
                "domain": "@concat('https://', linkedService().ClusterURL, '/')",
                "accessToken": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": "@linkedService().Secret"
                },
                "existingClusterId": "@linkedService().ClusterID"
            }
        }
    }
    ```

=== "DataLake"

    ```json
    {
        "name": "DynamicDataLake",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
            "description": "Azure Data Lake Gen 2",
            "annotations": [],
            "type": "AzureBlobFS",
            "typeProperties": {
                "url": "https://<storage-account-name>.dfs.core.windows.net"
            }
        }
    }
    ```

=== "Blob Storage"

    ```json
    {
        "name": "DynamicBlobStorage",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
            "annotations": [],
            "type": "AzureBlobStorage",
            "typeProperties": {
                "connectionString": "DefaultEndpointsProtocol=https;AccountName=<storage-account-name>;EndpointSuffix=core.windows.net;",
                "accountKey": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": "<secret-name>"
                }
            }
        }
    }
    ```

=== "SQLDatabase"

    ```json
    {
        "name": "AzureSqlAuto",
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

=== "Synapse"

    ```json
    {
        "name": "DynamicSynapse",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
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
            "type": "AzureSqlDW",
            "typeProperties": {
                "connectionString": "Integrated Security=False;Encrypt=True;Connection Timeout=30;Data Source=@{linkedService().Server};Initial Catalog=@{linkedService().Database};User ID=@{linkedService().Username}",
                "password": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": {
                        "value": "@{linkedService().Secret}",
                        "type": "Expression"
                    }
                }
            }
        }
    }
    ```

## Storage System

=== "MySQL"

    ```json
    {
        "name": "MySqlAuto",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
            "type": "MySql",
            "parameters": {
                "Server": {
                    "type": "String"
                },
                "Database": {
                    "type": "String"
                },
                "Username": {
                    "type": "String"
                },
                "Secret": {
                    "type": "String"
                }
            },
            "annotations": [],
            "typeProperties": {
                "connectionString": "Server=@{linkedService().Server};Port=3306;Database=@{linkedService().Database};User=@{linkedService().Username};SSLMode=1;UseSystemTrustStore=0",
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

=== "SQLServer"

    ```json
    {
        "name": "DynamicSqlServer",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
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
            "type": "SqlServer",
            "typeProperties": {
                "connectionString": "Data Source=@{linkedService().Server};Initial Catalog=@{linkedService().Database};Integrated Security=False;User ID=@{linkedService().Username}",
                "password": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": {
                        "value": "@{linkedService().Secret}",
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

=== "Postgres"

    ```json
    {
        "name": "DynamicPostgres",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
            "type": "PostgreSql",
            "annotations": [],
            "parameters": {
                "Server": {
                    "type": "String"
                },
                "Database": {
                    "type": "String"
                },
                "Username": {
                    "type": "String"
                },
                "Secret": {
                    "type": "String"
                }
            },
            "typeProperties": {
                "connectionString": "Server=@{linkedService().Server};Database=@{linkedService().Database};Port=5432;UID=@{linkedService().Username};",
                "password": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": "@{linkedService().Secret}"
                }
            },
            "connectVia": {
                "referenceName": "<integration-runtime-name>",
                "type": "IntegrationRuntimeReference"
            }
        }
    }
    ```

=== "MongoDB"

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

=== "BigQuery"

    ```json
    {
        "name": "DynamicBigQuery",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
            "type": "GoogleBigQuery",
            "annotations": [],
            "parameters": {
                "Project": {
                    "type": "String"
                },
                "ClientID": {
                    "type": "String"
                },
                "ClientSecret": {
                    "type": "String"
                },
                "RefreshToken": {
                    "type": "String"
                }
            },
            "typeProperties": {
                "project": "@replace(linkedService().Project, '''', '')",
                "requestGoogleDriveScope": false,
                "authenticationType": "UserAuthentication",
                "clientId": "@replace(linkedService().ClientID, '''', '')",
                "clientSecret": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "KVdataplat",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": "@replace(linkedService().ClientSecret, '''', '')"
                },
                "refreshToken": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": "@replace(linkedService().RefreshToken, '''', '')"
                }
            }
        }
    }
    ```

## File System

=== "File System"

    ```json
    {
        "name": "DynamicFileSystem",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
            "parameters": {
                "Server": {
                    "type": "string",
                    "defaultValue": "\\\\path\\sub-path\\folder"
                },
                "Username": {
                    "type": "string"
                },
                "Secret": {
                    "type": "string"
                }
            },
            "annotations": [],
            "type": "FileServer",
            "typeProperties": {
                "host": "@{linkedService().Server}",
                "userId": "@{linkedService().Username}",
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

=== "SFTP"

    ```json
    {
        "name": "DynamicSFTP",
        "properties": {
            "parameters": {
                "Server": {
                    "type": "string"
                },
                "Username": {
                    "type": "string"
                },
                "Secret": {
                    "type": "string"
                }
            },
            "annotations": [],
            "type": "Sftp",
            "typeProperties": {
                "host": "@{linkedService().Server}",
                "port": 22,
                "skipHostKeyValidation": true,
                "authenticationType": "Basic",
                "userName": "@{linkedService().Username}",
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

=== "GCS"

    ```json
    {
        "name": "DynamicGCS",
        "properties": {
            "type": "GoogleCloudStorage",
            "annotations": [],
            "parameters": {
                "ServiceURL": {
                    "type": "string"
                },
                "AccessKey": {
                    "type": "string"
                },
                "AccessSecret": {
                    "type": "string"
                }
            },
            "typeProperties": {
                "serviceUrl": "@linkedService().ServiceURL",
                "accessKeyId": "@linkedService().AccessKey",
                "secretAccessKey": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": "@linkedService().AccessSecret"
                }
            }
        }
    }
    ```

=== "S3"

    ```json
    {
        "name": "DynamicAmazonS3",
        "properties": {
            "type": "AmazonS3",
            "parameters": {
                "AccessSecret": {
                    "type": "string"
                },
                "AccessKey": {
                    "type": "string"
                },
                "S3URL": {
                    "type": "string"
                }
            },
            "annotations": [],
            "typeProperties": {
                "serviceUrl": "@{linkedService().S3URL}",
                "accessKeyId": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": {
                        "value": "@linkedService().AccessKey",
                        "type": "Expression"
                    }
                },
                "secretAccessKey": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "KVdataplat",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": {
                        "value": "@linkedService().AccessSecret",
                        "type": "Expression"
                    }
                },
                "authenticationType": "AccessKey"
            },
            "connectVia": {
                "referenceName": "<integration-runtime-name>",
                "type": "IntegrationRuntimeReference"
            }
        },
        "type": "Microsoft.DataFactory/factories/linkedservices"
    }
    ```

## HTTP

=== "Anonymous"

    ```json
    {
        "name": "DynamicHTTPAnonymous",
        "type": "Microsoft.DataFactory/factories/linkedservices",
        "properties": {
            "type": "HttpServer",
            "parameters": {
                "BaseURL": {
                    "type": "string",
                    "defaultValue": "https://dev.domain.com/api/"
                }
            },
            "annotations": [],
            "typeProperties": {
                "url": "@{linkedService().BaseURL}",
                "enableServerCertificateValidation": true,
                "authenticationType": "Anonymous"
            }
        }
    }
    ```

=== "Windows"

    ```json
    {
        "name": "DynamicHTTPWindows",
        "properties": {
            "type": "HttpServer",
            "parameters": {
                "BaseURL": {
                    "type": "string"
                },
                "Username": {
                    "type": "string"
                },
                "Secret": {
                    "type": "string"
                }
            },
            "annotations": [],
            "typeProperties": {
                "url": "@{linkedService().BaseURL}",
                "enableServerCertificateValidation": false,
                "authenticationType": "Windows",
                "userName": "@{linkedService().Username}",
                "password": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "<key-vault-link-service-name>",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": "@linkedService().Secret"
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

        The Windows username should has domain name before username:

        ```text
        domain\\username
        ```

!!! note

    If you want to use `AutoResolveIntegrationRuntime`, you can delete key `connectVia`
    from above json data.
