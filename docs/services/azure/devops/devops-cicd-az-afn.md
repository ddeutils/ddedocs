# CI/CD to Azure Function App

## Get Started

### Setup Application

### Deploy to Function App

For **CI pipeline**, we install the Python dependencies and package to the artifact server.

```yaml
parameters:
  - name: azfList
    type: object
    default: ["framework", "ingestion"]

stages:
  - stage: Build
    displayName: Build Stage
    jobs:
      - ${{ each azf in parameters.azfList }}:
          - job: Build_${{azf}}
            displayName: Build ${{azf}}
            pool:
              vmImage: "ubuntu-latest"
            steps:
              - bash: |
                  if [ -f extensions.csproj ]
                  then
                      dotnet build extensions.csproj --runtime ubuntu.16.04-x64 --output ./bin
                  fi
                workingDirectory: $(System.DefaultWorkingDirectory)
                displayName: "Build extensions"
              - task: UsePythonVersion@0
                displayName: "Use Python 3.8"
                inputs:
                  versionSpec: 3.8
              - bash: |
                  pip install --target="./.python_packages/lib/site-packages" -r ./requirements.txt
                workingDirectory: $(System.DefaultWorkingDirectory)/${{azf}}
                displayName: "Install application dependencies"
              - task: ArchiveFiles@2
                displayName: "Archive Files ${{azf}}"
                inputs:
                  rootFolderOrFile: $(System.DefaultWorkingDirectory)/${{azf}}
                  includeRootFolder: false
                  archiveType: zip
                  archiveFile: $(Build.ArtifactStagingDirectory)/${{azf}}/${{azf}}-$(Build.BuildId).zip
                  replaceExistingArchive: true
              - task: CopyFiles@2
                displayName: "Copy IP Address File From Repo to Artifact"
                inputs:
                  sourceFolder: $(System.DefaultWorkingDirectory)/deployment
                  contents: "*"
                  targetFolder: $(Build.ArtifactStagingDirectory)/${{azf}}/deployment
              - task: PublishBuildArtifacts@1
                displayName: "Publish Artifact ${{azf}}"
                inputs:
                  PathtoPublish: "$(Build.ArtifactStagingDirectory)/${{azf}}"
                  ArtifactName: drop
```

For **CD pipeline**, we deploy with Azure CLI after replace variable from setting file.

```yaml
jobs:
  - job: Job_1
    displayName: Agent job 1
    pool:
      name: Hosted Windows 2019 with VS2019
    steps:
      - task: AzureFunctionApp@1
        displayName: "Azure Function App Deploy: Framework"
        inputs:
          azureSubscription: "{subscription-name} ({subscription-id})"
          appType: functionAppLinux
          appName: "azf-data360-common-$(ENV)"
          package: "$(System.DefaultWorkingDirectory)/_DATA360-common-function/drop/framework-*.zip"
          runtimeStack: "PYTHON|3.8"
      - task: AzurePowerShell@5
        displayName: "Azure PowerShell script: Framework"
        inputs:
          azureSubscription: "{subscription-name} ({subscription-id})"
          ScriptPath: "$(System.DefaultWorkingDirectory)/_DATA360-common-function/drop/deployment/ReadIPAddress.ps1"
          ScriptArguments: |
            -IPAddressSourceFileName $(System.DefaultWorkingDirectory)/_DATA360-common-function/drop/deployment/$(ENV)_IPAddress.txt -ResourceGroupName data360-$(ENV)-rg -WebAppName azf-data360-common-$(ENV)
          azurePowerShellVersion: LatestVersion
          pwsh: true
      - task: AzureFunctionApp@1
        displayName: "Azure Function App Deploy: Ingestion"
        inputs:
          azureSubscription: "{subscription-name} ({subscription-id})"
          appType: functionAppLinux
          appName: "azf-data360-ingestion-$(ENV)"
          package: "$(System.DefaultWorkingDirectory)/_DATA360-common-function/drop/ingestion-*.zip"
          runtimeStack: "PYTHON|3.8"
      - task: AzurePowerShell@5
        displayName: "Azure PowerShell script: Ingestion"
        inputs:
          azureSubscription: "{subscription-name} ({subscription-id})"
          ScriptPath: "$(System.DefaultWorkingDirectory)/_DATA360-common-function/drop/deployment/ReadIPAddress.ps1"
          ScriptArguments: |
            -IPAddressSourceFileName $(System.DefaultWorkingDirectory)/_DATA360-common-function/drop/deployment/$(ENV)_IPAddress.txt -ResourceGroupName data360-$(ENV)-rg -WebAppName azf-data360-ingestion-$(ENV)
          azurePowerShellVersion: LatestVersion
          pwsh: true
      - task: qetza.replacetokens.replacetokens-task.replacetokens@5
        displayName: "Replace var in appsettings.json"
        inputs:
          rootDirectory: "$(System.DefaultWorkingDirectory)/_DATA360-common-function/drop/deployment"
          targetFiles: "appsettings*.json"
          encoding: "utf-8"
          writeBOM: false
          escapeType: json
          actionOnMissing: fail
          actionOnNoFiles: fail
      - task: AzureCLI@2
        displayName: "Azure CLI: App Setting"
        inputs:
          azureSubscription: "{subscription-name} ({subscription-id})"
          scriptType: bash
          scriptLocation: inlineScript
          inlineScript: |
            echo "##### Deploy Framework Appsettings #####"
            az webapp config appsettings set --resource-group $(ResourceGroupName) --name azf-data360-common-$(ENV) --settings "@$(System.DefaultWorkingDirectory)/_DATA360-common-function/drop/deployment/appsettings_framework.json" --output none
            echo "##### Deploy Ingestion Appsettings #####"
            az webapp config appsettings set --resource-group $(ResourceGroupName) --name azf-data360-ingestion-$(ENV) --settings "@$(System.DefaultWorkingDirectory)/_DATA360-common-function/drop/deployment/appsettings_ingestion.json" --output none
```
