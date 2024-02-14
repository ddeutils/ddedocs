# CI/CD: _Azure Databricks_

## Solution 01

### Setup Databricks Repository

1.  Go to **Azure DevOps** :octicons-arrow-right-24: Click your Project
    :octicons-arrow-right-24: Click bottom `Project setting`.

2.  On `Repositories` :octicons-arrow-right-24: Click `Create` and create new
    repository for Azure Databricks.

3.  Go to **Azure Databricks** :octicons-arrow-right-24: On `Workspace`
    :octicons-arrow-right-24: Click `Repos`

4.  Click `Add repo` :octicons-arrow-right-24: Pass Git repository URL and
    Select `Azure DevOps Services`

### Deploy to other Databricks Workspace

#### Pipline

```yaml
jobs:
  - job: Job_1
    displayName: Agent job 1
    pool:
      name: Azure Pipelines
    steps:
      # Check out the notebooks from Repo
      - checkout: self

      - task: PublishBuildArtifacts@1
        displayName: "Publish Artifact: notebooks"
        inputs:
          PathtoPublish: notebooks
          FileCopyOptions: ""
```

#### Release

```yaml
jobs:
  - job: Job_1
    displayName: Agent job 1
    pool:
      name: Azure Pipelines

    variables:
      sp_client_id: "{service-principle-client-id}"
      sp_tenant_id: "{service-principle-tenant-id}"
      resource_group: "{resource-group-name}"
      subscription_id: "{workspace-subscription-id}"
      workspace: "{workspace-name}"
      region: "{workspace-region-id}"
      notebook_root_path: "/DEV/"

    steps:
      - task: DataThirstLtd.databricksDeployScriptsTasks.databricksDeployScriptsTask.databricksDeployScripts@0
        displayName: "Databricks Notebooks deployment"
        inputs:
          authMethod: servicePrincipal
          applicationId: "$(sp_client_id)"
          spSecret: "$(sp_secret)"
          resourceGroup: "$(resource_group)"
          workspace: "$(workspace)"
          subscriptionId: "$(subscription_id)"
          tenantId: "$(sp_tenant_id)"
          region: "$(region)"
          localPath: "$(System.DefaultWorkingDirectory)/_DATA360-databricks-CI/drop"
          databricksPath: "$(notebook_root_path)"
```

## Solution 02

### Reference

- https://medium.com/@yatin.kumar/ci-cd-on-databricks-using-azure-devops-3f8a4aabebaa
