# Azure Key Vaults

## Getting Started

## Connection Code

The Python connection code that use to interact with the Azure Key Vaults service.

```shell
pip install azure-keyvault-secrets==4.8.0
```

=== "Default"

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient, KeyVaultSecret

    def get_kv_secret(name: str) -> str:
        credential = DefaultAzureCredential()
        secret_client = SecretClient(
            vault_url=f"https://{os.environ['keyvault']}.vault.azure.net",
            credential=credential,
            logging_enable=False,
        )
        secret: KeyVaultSecret = secret_client.get_secret(secret_name)
        return secret.value
    ```

=== "MSI"

    ```python
    from azure.identity import ManagedIdentityCredential
    from azure.keyvault.secrets import SecretClient, KeyVaultSecret

    def get_kv_secret(name: str) -> str:
        credential = ManagedIdentityCredential()
        secret_client = SecretClient(
            vault_url=f"https://{os.environ['keyvault']}.vault.azure.net",
            credential=credential,
            logging_enable=False,
        )
        secret: KeyVaultSecret = secret_client.get_secret(secret_name)
        return secret.value
    ```

## :material-playlist-plus: Read Mores
