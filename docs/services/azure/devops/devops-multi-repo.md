# Multi-Repositories

```yaml
pool:
  vmImage: ubuntu-latest

trigger:
  - none

parameters:
  - name: repo_branch
    type: string
    default: "main"

resources:
  repositories:
  - repository: self
    ref: $(branch)
  - repository: repo
    type: git
    name: {project-name}/{repo-name}
    ref: ${{ parameters.repo_branch }}

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
