# _To Synapse_

On Batch Pool, it should install Microsoft SQL Server ODBC Driver and Python
packages:

```console
$ pip install azure-identity arrow-odbc
```

=== note

    I recommend arrow-odbc for loadding performance.

## Using User-Assigned Managed Identity

### 1) Create User-Assigned Managed Identity

- In the `Azure Portal` :octicons-arrow-right-24: Go to `Managed Identities`
  :octicons-arrow-right-24: Click `Create`
- Add your managed identity information :octicons-arrow-right-24: Select `Review + create`

### 2) Grant Access to Synapse

- Go to `Azure Synapse SQL Pool` :octicons-arrow-right-24: Create user from external
  provider and grant permission of this user such as Read access,

    ```sql
    CREATE USER [<user-assigned-name>] FROM EXTERNAL PROVIDER;
    ```

### 3) Enable Azure Batch Account

- Go to `Azure Batch Accounts` :octicons-arrow-right-24: Go to `Pools`
  :octicons-arrow-right-24: Select your Batch Pool
- Go to `Identity` :octicons-arrow-right-24: Nav `User assigned` :octicons-arrow-right-24: Click `Add`
- Select your managed identity that was created from above :octicons-arrow-right-24: Click `Add`

### 4) Connection Code

```python
```
