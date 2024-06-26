# Mount Azure Storage

**List of mounts**:

```python
display(dbutils.fs.mounts())
```

## Azure Blob Storage

```python
dbutils.fs.mount(
    source = "wasbs://<container-name>@<storage-account-name>.blob.core.windows.net",
    mount_point = "/mnt/<mount-path>",
    extra_configs = {
        "fs.azure.account.key.<storage-account-name>.blob.core.windows.net":
        dbutils.secrets.get(scope="<scope-name>", key="adls-account-key"),
    }
)
```

## DataLake

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
