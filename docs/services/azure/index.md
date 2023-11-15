---
icon: material/microsoft-azure
---

# Azure

## Azure CLI

### Installation

#### On Local

Install:

```console
$ curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
$ az upgrade
```

!!! note

    If you want to remove all azure data from the CLI, you can use `rm -rf ~/.azure`.

#### On Docker

```shell
$ docker pull mcr.microsoft.com/azure-cli
$ docker run -it mcr.microsoft.com/azure-cli
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
