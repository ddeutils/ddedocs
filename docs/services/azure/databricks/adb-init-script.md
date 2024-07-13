# Init Script

**Init Script** (Initialization Script) is a shell script that runs during
startup of each cluster node before the **Apache Spark** driver or executor
**JVM** starts.

!!! danger

    **Legacy Global** and **Legacy Cluster-Named** init scripts run before other
    init scripts. These init scripts might be present in workspaces created
    before **February 21, 2023**.

## :material-arrow-down-right: Getting Started

### Cluster-Scoped init scripts

We want to initialize some program before a cluster started like:

```shell title="init_script.sh"
#!/bin/bash

echo "Start running init script: adb-default"
echo "Running on the driver? $DB_IS_DRIVER"
echo "Driver IP: $DB_DRIVER_IP"

timedatectl set-timezone Asia/Bangkok
```

To use the UI to configure a cluster to run an init script, complete the following steps:

- On the Cluster **Configuration Page** :octicons-arrow-right-24: Click the **Advanced Options** toggle
- At the bottom of the page :octicons-arrow-right-24: click the **Init Scripts** tab
- In the **Destination** drop-down :octicons-arrow-right-24: Select the **Workspace** type
- Specify a path to the init script like `SYS/init_script.sh` :octicons-arrow-right-24:
  Click **Add**.

!!! note

    Each user has a Home directory configured under the `/Users` directory in
    the workspace. If a user with the name `user@databricks.com` stored an
    init script called `my-init.sh` in their home directory, the configured
    path would be `/Users/user@databricks.com/my-init.sh`.

---

### Cluster-Scoped with Shared Cluster

For shared access mode, you must add init scripts to the `allowlist`.
See [Allowlist libraries and init scripts on shared compute](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/allowlist).

---

### Global init scripts

- Go to the **Admin Settings** :octicons-arrow-right-24: Click `Global Init Scripts`
- Click **Add** :octicons-arrow-right-24: Name the script and enter it by typing,
  pasting, or dragging a text file into the Script field.

---

## :material-playlist-plus: Read Mores

- [:simple-databricks: Databricks - Init Scripts](https://docs.databricks.com/clusters/init-scripts.html)
- [:material-youtube: Global Init Script in Azure databricks](https://www.youtube.com/watch?v=p9IPgYM4AyI)
