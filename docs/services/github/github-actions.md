# GitHub Actions: _Common_

GitHub provide the action marketplace.

```text
Events ---( trigger )---> Workflows ---( use )---> Actions
```

## GitHub Action Components

### Events

GitHub triggered events: push, pull-request, public. If you use by scheduled
events, you can use `schedule`.

#### Events

=== "All Branches"

    ```yaml
    ...
    name: Event Job
    on: [push]
    ...
    ```

=== "Custom Branches"

    ```yaml
    ...
    name: Event Job
    on:
        push:
            branches:
                - '*'
            tags:
                - 'v[0-9]+.[0-9]+.[0-9]+'
        pull_request:
            branches: [ main ]

        # Allows you to run this workflow manually from the Actions tab
        workflow_dispatch:
    ...
    ```

#### Schedules

```yaml
---
name: Weekly Job
on:
  schedule:
    - cron: 0 12 * * 1
```

!!! note

    The manually triggered: `workflow_dispatch` (external systems)

### Workflows

```yaml
name: Something CI

on: [push]

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  build:
    # - Actions run in VMs (Linux, Win, Max), or Docker on Linux Vm
    # - Logs Steaming & Artifacts
    # - Secret store with each repo or orgs
    run-on: ${{ matrix.os }}
    env:
      IMG_NAME: ${{ github.repository }}

    strategy:
      matrix:
        node-version: [8.x, 10.x, 12.x]
        os: [macos-latest, windows-latest, ubuntu-18.04]

    steps:
      # Check out the code
      - uses: actions/checkout@1

      # Run pre-existing actions
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v1
        with:
          node-version: ${{ matrix.node-version }}

      - name: npm install, build, and test
        run: |
          npm ci
          npm run build --if-present
          npm test
        env:
          CI: true

  test:
    needs: [build]
```

!!! note

    We can set condition for filter jobs like,

    ```yaml
    deploy-dev:
        name: Deploy to Dev
        if: github.event_name == 'pull_request'
        needs: [ build ]
    ```

    Or another conditions can be:

    ```text
    github.event.ref == 'refs/heads/main
    ```

### Actions

Reusable units of code.

```yaml
---
jobs:
  build_and_release:
    name: Build and Release
    run-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v1.0.0

      - name: Build and Test
        uses: actions/build-and-test@v1.0.0

      - name: Create Draft Release
        id: create_draft_release
        uses: actions/create-draft-release@v1.0.0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          draft: true
          prerelease: false

      - name: Generate Release notes
        id: generate_release_notes
        uses: actions/generate-release-notes@v1.0.0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Edit Release to add notes
        uses: actions/add-release-notes@v1.0.0
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          release_notes: ${{ steps.generate_release_notes.outputs.release_notes }}
          release_id: ${{ steps.create_draft_release.outputs.release_id }}
```

## Environments

- Go to your Repository > Click on `Settings`
- Go to `Environments` > Click `New environment`

```yaml
deploy-dev:
  name: Deploy to Dev
  needs: [build]
  environment:
    # Same the name that setting on repo
    name: Development
    url: "http://dev.myapp.com"
```

## Self-hosted Runners

Steps:

- Download and extract the setup scripts
- Configure and authenticate the runner with the token
- Start listening for jobs

!!! note

    GitHub recommends AGAINST self-hosted runners for public repositories

## Runner Groups

- Configure on enterprise and/or organization level
- Scope to specific organizations and/or repositories
- Move runners between groups
- A runner can only be in one group at a time

## Secrets

!!! warning

    Secrets are limited to **64K** so, use `gpg` to encrypt larger secrets on the repository.

## Trigger Workflow

```yaml
name: Target for call from another workflow
on:
  repository_dispatch:
    type: [MyCustomEventName]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Print client payload
        run: |
          echo 'ParamA' is ${{ github.event.client_payload.paramA }}
          echo 'boolean' is ${{ github.event.client_payload.boolean }}
```

```yaml
on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Repository Dispatch
        uses: peter-evans/repository-dispatch@v1.1.2
        with:
          # A repo scoped GitHub Personal Access Token (PAT)
          token: ${{ secrets.REPO_PAT }}
          event-type: MyCustomEventName
          client-payload: '{ "paramA": 123, "boolean": false }'
```

## GitHub Action Examples

### CI/CD Workflow

!!! abstract

    * **CI** - Merge Code In
    * **CD** - Release Code Out

=== "AWS Serverless"

    ```yaml
    name: Node CI
    on: [ push, pull_request ]
    jobs:
        build:
            runs-on: ubuntu-latest
            strategy:
                matrix:
                    node-version: [ 10.x ]
            steps:
                # Checkout is separate
                - uses: actions/checkout@v2

                # Run Linter against code base
                - name: Lint Code Base
                  uses: docker://github/super-linter:v3
                  env:
                      VALIDATE_ALL_CODEBASE: false
                      DEFAULT_BRANCH: master

                - name: Use Node.js ${{ matrix.node-version }}
                  uses: actions/setup-node@v1
                  with:
                      node-version: ${{ matrix.node-version }}

                # Run the npm by shell
                - name: npm install, and test
                  run: |
                      npm ci
                      npm run build --if-present
                      npm test -- -u
                  env:
                      CI: true

                # Artifact uploaded separately
                - uses: actions/upload-artifact@master
                  with:
                      name: webpack artifacts
                      path: public/

        deploy:
            runs-on: ubuntu-latest
            needs: build
            name: Deploy Node.js app to AWS

            steps:
                - uses: actions/checkout@v2

                - name: Download build artifact
                  uses: actions/download-artifact@master
                  with:
                      name: webpack artifacts
                      path: public

                - name: Deploy to AWS
                  uses: github/deploy-nodejs@master
                  env:
                      AWS_ACCESS_KEY: ${{ secrets.AWS_ACCESS_KEY }}
                      AWS_SECRET_KEY: ${{ secrets.AWS_SECRET_KEY }}
                      AWS_REGION: us-west-2
    ```

=== "Azure"

    ```yaml
    jobs:
        build-docker-image:
            runs-on: ubuntu-latest
            steps:
                - name: create image and store in Packages
                  uses: mattdavis0351/actions/docker-gpr@1.3.0
                  with:
                      repo-token: ${{ secrets.GITHUB_TOKEN }}
                      image-name: ${{ env.DOCKER_IMAGE_NAME }}

        deploy-to-azure:
            runs-on: ubuntu-latest
            needs: build-docker-image
            name: Deploy app container to Azure
            steps:
                - name: "Login via Azure CLI"
                  uses: azure/login@v1
                  with:
                      creds: ${{ secrets.AZURE_CREDENTIALS }}

                - uses: azure/docker-login@v1
                  with:
                      login-server: ${{ env.IMAGE_REGISTRY_URL }}
                      username: ${{ github.actor }}
                      password: ${{ secrets.GITHUB_TOKEN }}

                - name: Deploy web app container
                  uses: azure/webapps-container-deploy@v1
                  with:
                      - app-name: ${{ env.AZURE_WEBAPP_NAME }}
                      - images: ${{ env.IMAGE_REGISTRY_URL }}/${{ github.repository }}/${{ env.DOCKER_IMAGE_NAME }}
    ```

=== "AWS ECS"

    ```yaml
    jobs:
        build-docker-image:
            runs-on: ubuntu-latest
            steps:
                - name: create image and store in Packages
                  uses: mattdavis0351/actions/docker-gpr@1.3.0
                  with:
                      repo-token: ${{ secrets.GITHUB_TOKEN }}
                      image-name: ${{ env.DOCKER_IMAGE_NAME }}

        deploy-to-azure:
            runs-on: ubuntu-latest
            needs: build-docker-image
            name: Deploy app container to Azure
            steps:
                - uses: actions/checkout@v1

                - name: Download build artifact
                  uses: actions/download-artifact@master
                  with:
                      name: webpack artifacts
                      path: public

                - name: Render Amazon ECS task definition
                  id: render-web-container
                  uses: aws-actions/amazon-ecs-render-task-definition@1
                  with:
                      task-definition: task-definition.json
                      container-name: tic-tac-toe
                      image: ${{ env.IMAGE_REGISTRY_URL }}/${{ github.repository }}/${{ env.DOCKER_IMAGE_NAME }}

                - name: Configure AWS Credentials
                  uses: aws-actions/configure-aws-credentials@v1
                  with:
                      aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY }}
                      aws-secret-access-key: ${{ secrets.AWS_SECRET_KEY }}
                      aws-region: us-west-2

                - name: Deploy to Amazon ECS service
                  uses: aws-actions/amazon-ecs-deploy-task-definition@v1
                  with:
                      task-definition: ${{ steps.render-web-container.outputs.task-definition }}
                      cluster: dev-cluster
    ```

=== "Kubernetes"

    ```yaml
    jobs:
        build-docker-image:
            runs-on: ubuntu-latest
            steps:
                - name: create image and store in Packages
                  uses: mattdavis0351/actions/docker-gpr@1.3.0
                  with:
                      repo-token: ${{ secrets.GITHUB_TOKEN }}
                      image-name: ${{ env.DOCKER_IMAGE_NAME }}
        deploy-to-k8s:
            runs-on: ubuntu-latest
            name: Deploy to Kubernetes
            needs: build-docker-image
            steps:
                - uses: azure/aks-set-context@v1
                  id: login
                  with:
                      creds: '${{ secrets.AZURE_CREDENTIALS }}'
                      resource-group: ${{ env.AZURE_RESOURCE_GROUP }}
                      cluster-name: ${{ env.AZURE_AKS_CLUSTER }}

                - name: Set imagePullSecret
                  id: create-secret
                  uses: azure/k8s-create-secret@v1
                  with:
                      namespace: ${{ env.AZURE_AKS_NAMESPACE }}
                      container-registry-url: ${{ env.IMAGE_REGISTRY_URL }}
                      container-registry-username: ${{ github.actor }}
                      container-registry-password: ${{ secrets.GITHUB_TOKEN }}
                      secret-name: 'image-pull-secret'

                - uses: azure/k8s-deploy@v1
                  with:
                      namespace: ${{ env.AZURE_AKS_NAMESPACE }}
                      manifests: |
                                deployment.yaml
                      images: ${{ env.IMAGE_REGISTRY_URL }}/${{ github.repository }}/${{ env.DOCKER_IMAGE_NAME }}
                      imagepullsecrets: |
                                image-pull-secret

    ```

=== "Docker"

    ```yaml
    name: Docker image
    on:
        push:
            branches:
                - '*'
            tags:
                - 'v[0-9]+.[0-9]+.[0-9]+'
        pull_request:
            branches:
                - '*'
    jobs:
        build:
            name: Build & push docker image
            runs-on: ubuntu-latest
            env:
                IMG_NAME: ${{ github.repository }}
            steps:
                - name: Checkout
                  uses: actions/checkout@v3

                - name: Info
                  run: echo "Parameters. ${{ github.event.base_ref }}, ${{ github.ref_type }}, ${{ github.ref }}"

                - name: Docker metadata
                  id: metadata
                  uses: docker/metadata-action@v4
                  with:
                    images: ${{ env.IMG_NAME }}
                    tags: |
                      type=semver,pattern={{version}}
                      type=semver,pattern={{major}}.{{minor}}
                      type=raw,value={{sha}},enable=${{ github.ref_type != 'tag' }}
                - name: Log in to Docker Hub
                  uses: docker/login-action@v2
                  with:
                    username: ${{ secrets.DOCKER_USERNAME }}
                    password: ${{ secrets.DOCKER_PASSWORD }}

                - name: Build and push Docker image
                  uses: docker/build-push-action@v3
                  with:
                    context: .
                    push: ${{ github.event.base_ref =='refs/heads/main' && github.ref_type == 'tag' && !startsWith(github.ref, 'refs/tags/v0.')}}
                    tags: ${{ steps.metadata.outputs.tags }}
                    labels: ${{ steps.metadata.outputs.labels }}
    ```

## References

- [Jose Phrodriguezg: Build and Publish Docker Image with GitHub Actions](https://josephrodriguezg.medium.com/build-and-publish-docker-images-with-github-actions-78be3b3fbb9b)
