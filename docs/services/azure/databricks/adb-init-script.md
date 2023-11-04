# Azure Databricks: _Init Script_

An init script (initialization script) is a shell script that runs during
startup of each cluster node before the Apache Spark driver or executor
JVM starts.

!!! danger

    **Legacy global** and **legacy cluster-named** init scripts run before other
    init scripts. These init scripts might be present in workspaces created
    before **February 21, 2023**.

## Cluster-scoped init scripts

We want to initialize some program before a cluster started like:

```shell
#!/bin/bash

echo "Start running init script: adb-default"
echo "Running on the driver? $DB_IS_DRIVER"
echo "Driver IP: $DB_DRIVER_IP"

timedatectl set-timezone Asia/Bangkok
```

To use the UI to configure a cluster to run an init script, complete the following steps:

- On the cluster configuration page, click the Advanced Options toggle.
- At the bottom of the page, click the Init Scripts tab.
- In the Destination drop-down, select the Workspace destination type.
- Specify a path to the init script.
- Click Add.

!!! note

    Each user has a Home directory configured under the `/Users` directory in
    the workspace. If a user with the name `user1@databricks.com` stored an
    init script called `my-init.sh` in their home directory, the configured
    path would be `/Users/user1@databricks.com/my-init.sh`.

## Global init scripts

- Go to the admin settings and click the `Global Init Scripts` tab.
- Click + `Add`.
- Name the script and enter it by typing, pasting, or dragging a text file
  into the Script field.

## References

- https://docs.databricks.com/clusters/init-scripts.html
- https://www.youtube.com/watch?v=p9IPgYM4AyI
