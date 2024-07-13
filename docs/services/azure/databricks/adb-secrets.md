# Secrets

**Azure Databricks** allow you to map **Azure Key Vault** with secrete module.

## :material-arrow-down-right: Getting Started

### Prerequisite

- Go to `https://<databricks-instance>.azuredatabricks.net#secrets/createScope`
- Create Scope with `All workspace users` manage principle

![Azure Databricks Secrets Scope](./img/adb-kv-scope.png)

### List of Secrets

**List of all secrets scopes**:

```python
display(dbutils.secrets.listScopes())
```

## Read Mores

- [:material-microsoft: Microsoft - Secret scopes](https://learn.microsoft.com/en-us/azure/databricks/security/secrets/secret-scopes)
