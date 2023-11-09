# DevOps: Multi Repository

```yaml
pool:
  vmImage: ubuntu-latest

trigger:
- none

resources:
  repositories:
  - repository: repo
    type: git
    name: {project-name}/{repo-name}
    trigger:
    - main

steps:
- checkout: self
- checkout: repo

- script: ls -al $(Build.SourcesDirectory)
  displayName: 'List on source dir'

- task: CopyFiles@2
  inputs:
    SourceFolder: '$(Build.SourcesDirectory)'
    Contents: '**'
    TargetFolder: '$(Build.ArtifactStagingDirectory)'

- task: DeleteFiles@1
  inputs:
    SourceFolder: '$(Build.ArtifactStagingDirectory)'
    Contents: |
      **/.git

- task: PublishBuildArtifacts@1
  inputs:
    PathtoPublish: '$(Build.ArtifactStagingDirectory)'
    ArtifactName: 'drop'
    publishLocation: 'Container'
  displayName: 'Publish Artifact: drop'
```
