# Connect to Azure Services

## :material-account-check-outline: Authentication

### Using System-Assigned Managed Identity

#### Enable System-Assigned Managed Identity

- Go to **Azure Function App** :octicons-arrow-right-24: Select **Identity**
  :octicons-arrow-right-24: Click nav **System Assigned**
- On **Status** :octicons-arrow-right-24: Enable to **On** :octicons-arrow-right-24:
  Click **Save**

## :material-microsoft-azure: Services

### Key Vault

#### Prerequisite

Add The **Azure Function** MSI User to the **Azure Key Vault**.

- Go to **Azure Key Vault** :octicons-arrow-right-24: Select `Access policies`
  :octicons-arrow-right-24: Click nav `Create`
- On `Configure from a template` :octicons-arrow-right-24: Select `Secret Management`
  :octicons-arrow-right-24: Click `Next`
- On `Principle` :octicons-arrow-right-24: Search the Azure Function name
  :octicons-arrow-right-24: Click `Create`

Add **Secret** to **Azure Function**:

- Go **to Azure Key Vault** :octicons-arrow-right-24: Select **Secrets**
  :octicons-arrow-right-24: Click nav `Generate/Import`
- Create your Secrets :octicons-arrow-right-24: Copy the `Secret Identifier`
  uri
- Go to **Azure Function App** :octicons-arrow-right-24: Select `Configuration`
  :octicons-arrow-right-24: Click `New application setting`
- Pass the name to environment variable with this value:
  `@Microsoft.KeyVault(SecretUri=<secret-identifier-uri>)`

#### Connection Code

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

!!! note "References"

    - [Accessing Azure Key Vault from Python](https://servian.dev/accessing-azure-key-vault-from-python-functions-44d548b49b37)

### Service Bus

#### Connection Code

```python
import os
import asyncio
from aiohttp import ClientSession
from azure.servicebus.aio import ServiceBusClient

conn_str = os.environ['SERVICE_BUS_CONNECTION_STR']
topic_name = os.environ['SERVICE_BUS_TOPIC_NAME']
subscription_name = os.environ['SERVICE_BUS_SUBSCRIPTION_NAME']

async def watch(
    topic_name,
    subscription_name,
):
    async with ServiceBusClient.from_connection_string(conn_str=conn_str) as service_bus_client:
        subscription_receiver = service_bus_client.get_subscription_receiver(
            topic_name=topic_name,
            subscription_name=subscription_name,
        )
    async with subscription_receiver:
         message = await subscription_receiver.receive_messages(max_wait_time=1)

    if message.body is not None:
        async with ClientSession() as session:
            await session.post('ip:port/endpoint',
                               headers={'Content-type': 'application/x-www-form-urlencoded'},
                               data={'data': message.body.decode()})

async def do():
    while True:
        for topic in ['topic1', 'topic2', 'topic3']:
            await watch(topic, 'watcher')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do())
```

!!! note "References"

    - https://stackoverflow.com/questions/63149310/azure-servicebus-using-async-await-in-python-seems-not-to-work
    - https://iqan.medium.com/how-to-use-managed-identity-in-azure-functions-for-service-bus-trigger-fc61fb828b90

### Synapse

#### Prerequisite

Enable AAD integration for **Azure Synapse** workspace.

- Go to **Azure Synapse Workspace** :octicons-arrow-right-24: Select **Azure Active Directory**
- Click nav **Set admin** :octicons-arrow-right-24: Select your user :octicons-arrow-right-24:
  Click **Save**

Add The Azure Function MSI User to the Azure Synapse SQL Pool.

- Connect to **Azure Synapse SQL Pool** on target database.
- Create MSI user that use the Azure Function name

    ```sql
    CREATE USER <azure-function-name> FROM EXTERNAL PROVIDER
    GO
    ```

#### Connection Code

=== "ActiveDirectoryMsi"

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

=== "SQL User"

    ```python
    import logging
    import pyodbc

    server = 'tcp:<server-name>.database.windows.net'
    database = '<database-name>'
    driver = '{ODBC Driver 17 for SQL Server}'

    username = "<username>"
    password = "<password>"

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

!!! note

    If the Python runtime has version more than `3.11`, it will upgrade ODBC driver to version 18.
