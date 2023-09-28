---
icon: material/microsoft-azure
---

# Azure Cloud Service

## Azure CLI

### Run Azure CLI on Local

- Install

```shell
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

- Update & Test

```shell
az upgrade
```

> **Note**: \
> If you want to remove all azure data from the CLI, you can use `rm -rf ~/.azure`.

### Run Azure CLI on Docker Container

```shell
docker pull mcr.microsoft.com/azure-cli
```

```shell
docker run -it mcr.microsoft.com/azure-cli
```

> Note: \
> If you want to pick up the SSH keys from your user environment, use
> `docker run -it -v ${HOME}/.ssh:/root/.ssh mcr.microsoft.com/azure-cli`.

### Get Start with Azure CLI

```shell
# login
az login

# list subscriptions
az account list -o table

# set active subscription
az account set --subscription <SUBSCRIPTION_ID>

# create an Azure Resource Group
az group create -n rg-functions-with-go \
  -l germanywestcentral

# create an Azure Storage Account (required for Azure Functions App)
az storage account create -n safnwithgo2021 \
  -g rg-functions-with-go \
  -l germanywestcentral

# create an Azure Functions App
az functionapp create -n fn-with-go \
  -g rg-functions-with-go \
  --consumption-plan-location germanywestcentral \
  --os-type Linux \
  --runtime custom \
  --functions-version 3 \
  --storage-account safnwithgo2021
```

### Certificate-based auth with Azure Service Principals

- https://arsenvlad.medium.com/certificate-based-auth-with-azure-service-principals-from-linux-command-line-a440c4599cae

## Azure Services

| Type           | Services                                                                               |
|----------------|----------------------------------------------------------------------------------------|
| Database       | [`Azure Server`](database_server/READMD.md) `Azure Database`                           |
| Storage        | [`Azure Blob Storage`](storage_account/README.md)                                      |
| Data Warehouse | [Azure Synapse Analytic](https://learn.microsoft.com/en-us/azure/synapse-analytics/)   |

## References

-
