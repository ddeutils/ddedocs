# Azure Function: _Access Azure Key Vault_

## Using System Assign Manage Identity

### 1) Enable MSI

Enable Managed Service Identity (MSI) on Azure Function App Protol:

* Go to **Azure Function App** :octicons-arrow-right-24: Select `Identity`
  :octicons-arrow-right-24: Click nav `System Assigned`

* On Status :octicons-arrow-right-24: Enable to `On` :octicons-arrow-right-24:
  Click `Save`

### 2) Add Policy to MSI

Add The Azure Function MSI User to the Azure Key Vault.

* Go to **Azure Key Vault** :octicons-arrow-right-24: Select `Access policies`
  :octicons-arrow-right-24: Click nav `Create`

* On `Configure from a template` :octicons-arrow-right-24: Select `Secret Management`
  :octicons-arrow-right-24: Click `Next`

* On `Principle` :octicons-arrow-right-24: Search the Azure Function name
  :octicons-arrow-right-24: Click `Create`

### 3) Add Secret to Azure Function

#### Setting Configuration

* Go **to Azure Key Vault** :octicons-arrow-right-24: Select `Secrets`
  :octicons-arrow-right-24: Click nav `Generate/Import`
* Create your Secrets :octicons-arrow-right-24: Copy the `Secret Identifier`
  uri
* Go to **Azure Function App** :octicons-arrow-right-24: Select `Configuration`
  :octicons-arrow-right-24: Click `New application setting`
* Pass the name to environment variable with this value:
  `@Microsoft.KeyVault(SecretUri=<secret-identifier-uri>)`

#### Develop Python Code

```python
from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

credentials = ManagedIdentityCredential()
secret_client = SecretClient(
    vault_url="https://<key-vault-name>.vault.azure.net",
    credential=credentials
)
secret = secret_client.get_secret("secret-name")
```

## References

* [Accessing Azure Key Vault from Python](https://servian.dev/accessing-azure-key-vault-from-python-functions-44d548b49b37)
