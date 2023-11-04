# Azure Databricks: _Mount Storage_

## Azure Blob Storage

```python
configs: Dict[str, str] = {
    "fs.azure.account.key.<storage-account-name>.blob.core.windows.net":
        dbutils.secrets.get(scope="<scope-name>", key="adls-account-key"),
}

dbutils.fs.mount(
  source = "wasbs://<container-name>@<storage-account-name>.blob.core.windows.net",
  mount_point = "/mnt/<mount-path>",
  extra_configs = configs
)
```


## Azure Data Lake Storage Gen 2

There are 3 different ways to access **Azure Data Lake Storage** (ADLS) Gen2
in your workspace:

- Using ADLS Gen2 storage account keys directly (highly not recommended for production workloads).
- Using Service Principal directly
- Mount an Azure Data Lake Storage Gen2 filesystem to DBFS using a service principal and OAuth 2.0.

But for now let’s concentrate on mounting ADLS Gen2 to your DBFS. Below are the
list of resources required for mounting:

- Storage Account with ADLS Gen2 hierarchical namespace feature enabled.
- Azure Key Vault Service
- Azure Active Directory
- Azure Databricks Workspace.

Mounting a storage system to your Databricks File System is a one time activity,
by this means, you will have to execute the code (code used for mounting) only
once in your workspace to mount your storage account, but not every time you
execute a particular notebook. Even though if you try it will through an error
like "Directory already mounted"

```python
adls_account = "<storage-account-name>"
adls_container = "<container-name>"
adls_dir = "<dir-path>"
mount_point = "/mnt/<mount-path>"

client_id = dbutils.secrets.get(scope="<scope-name>", key="adb-client-id")
client_secret_id = dbutils.secrets.get(scope="<scope-name>", key="adb-client-secrete-id")
tenant_id = dbutils.secrets.get(scope="<scope-name>", key="adb-tenant-id")

endpoint: str = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"

if adls_dir:
    source: str = f"abfss://{adls_container}@{adls_account}.dfs.core.windows.net/{adls_dir}"
else:
    source: str = f"abfss://{adls_container}@{adls_account}.dfs.core.windows.net"

# Connecting using Service Principal secrets and OAuth
configs: Dict[str, str] = {
    "fs.azure.account.auth.type": "OAuth",
    "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
    "fs.azure.account.oauth2.client.id": client_id,
    "fs.azure.account.oauth2.client.secret": client_secret_id,
    "fs.azure.account.oauth2.client.endpoint": endpoint
}

# Mount ADLS Storage to DBFS only if the directory is not already mounted
if not any(
        mount.mountPoint == mount_point
        for mount in dbutils.fs.mounts()
):
    dbutils.fs.mount(
        source = source,
        mount_point = mount_point,
        extra_configs = configs
    )
```

## Unmount command

```python
mount_point = "/mnt/<mount-path>"

if any(
        mount.mountPoint == mount_point
        for mount in dbutils.fs.mounts()
):
    dbutils.fs.unmount(mount_point)
```

## References

- https://vvin.medium.com/mount-adls-gen2-to-databricks-file-system-using-service-principal-oauth-2-0-47527e339178
- https://docs.databricks.com/en/storage/azure-storage.html
