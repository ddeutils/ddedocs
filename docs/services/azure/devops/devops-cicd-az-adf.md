# Deploy Azure Data Factory

## Getting Started

### Development Flow Design

- In ADF Portal, create a feature branch(`feature_one`) from your collaboration branch(`main`).
- Develop and manually test your changes in the feature branch of ADF Portal.
- Create a PR from the feature branch to the collaboration branch in GitHub.
- Once PR is merged, the changes will be available in the collaboration branch(main).

### Project Initialize

```text
build/
    |- package.json
```

```json titiles="package.json"
{
    "scripts":{
        "build":"node node_modules/@microsoft/azure-data-factory-utilities/lib/index"
    },
    "dependencies":{
        "@microsoft/azure-data-factory-utilities":"^1.0.0"
    }
}
```

## Build Pipeline

1. you need to install the dependencies. Azure provides a tool **ADFUtilities**.
   This package is used to validate and create the deployment template.
   In order to install this package, we need to install Node.js and NPM
   package management.
2. Next, you need to **Validate all the Data Factory resource code** in the
   repository. This calls the `validate` function along with the path where the
   ADF code is stored in repo. The working directory is where the **ADFUtilities**
   is installed.
3. The next step is to **Generate ARM template** from Azure Data Factory source code.
   The `export` function is used to output the ARM template in the **ArmTemplate**
   folder inside the working Directory.
4. Finally, ARM template is generated and Published as a Pipeline artifact.
   This will create an artifact with the name **ArmTemplates** to be used as a
   source for a release pipeline

```yaml
variables:
    subscriptionId: '$(subscription_id)'    # Use your subscription ID
    resourceGroup: '$(resource_group)'      # Use the resource group for the development data factory
    dataFactory: '$(data_factory)'          # Use your development data factory name
    PackageFolder: '$(package_folder)'      # Use the GIT folder under which you have the package files
    adfRootFolder: ''                       # Use the GIT folder under which you have the ADF resources. If it's root leave as blank

stages:
    - stage: Build_And_Publish_ADF_Artifacts
      jobs:
          - job: Build_Adf_Arm_Templates
            displayName: 'Generate ADF Artifacts'
            steps:
                # Installs Node
                - task: NodeTool@0
                  inputs:
                    versionSpec: '14.x'
                  displayName: 'Install Node.js'
                # Installs the npm packages saved in your package.json file in the build
                - task: Npm@1
                  inputs:
                    command: 'install'
                    workingDir: '$(Build.Repository.LocalPath)/$(packageFolder)' #replace with the package.json folder
                    verbose: true
                  displayName: 'Install npm packages'
                 # Validates all the Data Factory resources in the repository. You'll get the same validation errors as when "Validate All" is selected.
                - task: Npm@1
                  inputs:
                    command: 'custom'
                    workingDir: '$(Build.Repository.LocalPath)/build' # replace with the package.json folder
                    customCommand: 'run build validate $(Build.Repository.LocalPath)/$(adfRootFolder) /subscriptions/$(subscriptionId)/resourceGroups/$(resourceGroup)/providers/Microsoft.DataFactory/factories/$(dataFactory)'
                  displayName: 'Validate Data Factory Resources'
                # Generate the ARM template into the destination folder, which is the same as selecting "Publish" from the UX.
                - task: Npm@1
                  inputs:
                    command: 'custom'
                    workingDir: '$(Build.Repository.LocalPath)/build' # replace with the package.json folder
                    customCommand: 'run build export $(Build.Repository.LocalPath)/$(adfRootFolder) /subscriptions/$(subscriptionId)/resourceGroups/$(resourceGroup)/providers/Microsoft.DataFactory/factories/$(dataFactory) "ArmTemplate"'
                  displayName: 'Generate ARM template'
                # Publish the artifact to be used as a source for a release pipeline.
                - task: PublishPipelineArtifact@1
                  inputs:
                    targetPath: '$(Build.Repository.LocalPath)/$(packageFolder)/ArmTemplate' #replace with the package.json folder
                    artifact: 'ArmTemplates'
                    publishLocation: 'pipeline'
                  displayName: 'Publish ARM tempate'
```

## Release Pipeline

## References

- [Automated CI/CD For Azure Data Factory With Azure DevOps](https://medium.com/@binayalenka/automated-ci-cd-for-azure-data-factory-with-azure-devops-fc8d02d12412)
