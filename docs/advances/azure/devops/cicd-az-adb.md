# CI/CD to Azure Databricks

**Update**: `2023-05-29` |
**Tag**: `Cloud` `Azure` `Azure DevOps` `CICD` `Azure Databricks`

**Table of Contents**:

- [Get Started](#get-started)
  - [Setup Databricks Repository](#setup-databricks-repository)
  - [Deploy to other Databricks Workspace](#deploy-to-other-databricks-workspace)

We want to deploy Databricks notebooks to any workspace.

## Get Started

### Setup Databricks Repository

We should setup our Databricks repository to **Azure DevOps**

### Deploy to other Databricks Workspace

For **CI pipeline**, it only pack the code to artifact server.

```yaml
jobs:
- job: Job_1
  displayName: Agent job 1
  pool:
    name: Azure Pipelines
  steps:
  - checkout: self
  - task: PublishBuildArtifacts@1
    displayName: 'Publish Artifact: drop'
    inputs:
      PathtoPublish: notebooks
```

For **CD pipeline**, we use Databricks deploy scripts from Azure DevOps marketplace.

```yaml
jobs:
- job: Job_1
  displayName: Agent job 1
  pool:
    name: Azure Pipelines
  variables:
    sp_client_id: '{service-principle-client-id}'
    sp_tenant_id: '{service-principle-tenant-id}'
    resource_group: '{resource-group-name}'
    subscription_id: '{workspace-subscription-id}'
    workspace: '{workspace-name}'
    region: '{workspace-region-id}'
    notebook_root_path: '/DEV/'
  steps:
  - task: DataThirstLtd.databricksDeployScriptsTasks.databricksDeployScriptsTask.databricksDeployScripts@0
    displayName: 'Databricks Notebooks deployment'
    inputs:
      authMethod: servicePrincipal
      applicationId: '$(sp_client_id)'
      spSecret: '$(sp_secret)'
      resourceGroup: '$(resource_group)'
      workspace: '$(workspace)'
      subscriptionId: '$(subscription_id)'
      tenantId: '$(sp_tenant_id)'
      region: '$(region)'
      localPath: '$(System.DefaultWorkingDirectory)/_DATA360-databricks-CI/drop'
      databricksPath: '$(notebook_root_path)'
```
