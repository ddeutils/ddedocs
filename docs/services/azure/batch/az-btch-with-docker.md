# With Docker

**Azure Batch** can be a great tool for instant batch processing as it creates and
manages a pool of compute nodes (virtual machines), installs the applications you
want to run, and schedules jobs to run on the nodes.
Sometimes however a container could be a more appropriate solution for simplicity
and scaling than a virtual machine.

## :material-arrow-down-right: Getting Started

### Azure Container Registry

- Go to `Container Registries` :octicons-arrow-right-24: Create container registry with prefix name `cr`
- Add the information of this registry, for example with name: `cr-ba-python-dev`
  :octicons-arrow-right-24: Click create for registry creation
- After registry creation, Go to `cr-ba-python-dev` registry :octicons-arrow-right-24: On `Access Keys`
- Click Enable on `Admin user` option
- Save these values, `Login server`, `Username`, and `Password`
- Go to your local terminal for prepare docker file
- Create your `Dockerfile` and test run your image on local

    ```dockerfile title="Dockerfile"
    FROM python:3.9-slim

    WORKDIR /app

    COPY main.py ./

    RUN mkdir -p ./output

    CMD ["python","./main.py"]
    ```

    ```python title="./main.py"
    print("This is a Docker test.")
    with open('/output/docker_test.txt', 'w') as f:
        f.write("This is a Docker test.")
    ```

    ```shell
    docker build -t "python-ba" . --no-cache
    ```

    ```shell
    docker run --name python-btch -v "${pwd}\output:/output" python-btch
    ```

- Push your image to **Azure Container Registries**

    ```shell
    docker login cr-ba-python-dev.azurecr.io
    ```

    ```shell
    docker tag python-btch:latest cr-ba-python-dev.azurecr.io/btch/python-btch:0.0.1-test
    ```

    ```shell
    docker push cr-ba-python-dev.azurecr.io/btch/python-btch:0.0.1-test
    ```

### Azure Batch Accounts

- Go to your `Batch accounts` :octicons-arrow-right-24: `Pools` :octicons-arrow-right-24:
  Add new pool that [Supports Container](https://learn.microsoft.com/en-us/azure/batch/batch-docker-container-workloads#supported-virtual-machine-images)
- Click Enable to `Custom` on `Container configuration` option
- Go to `Container registries` :octicons-arrow-right-24: Add `cr-ba-python-dev` registry from ACR values
- Create `Pool` with name is `btch-pool-cntn`
- Go to `Jobs` :octicons-arrow-right-24: Create new job in `btch-pool-cntn` pool with name `btch-job-cntn`
- Go to `Tasks` :octicons-arrow-right-24: Create new task in `btch-job-cntn` job

    - Go to `Image name` and add `cr-ba-python-dev.azurecr.io/btch/python-btch:0.0.1-test`
    - Go to `Container run options` and add

        ```text
        --rm --workdir /app
        ```

- Create the **Automate Script** file

    Package image version from local to Azure Container Registries

    ```powershell
    @echo off
    set "version=%~1"
    if defined version (
        echo Start package docker image version: %version% ...
        call docker build -t python-test:latest . --no-cache
        call docker tag python-test:latest cr-ba-python-dev.azurecr.io/poc/python-test:%version%
        call docker push cr-ba-python-dev.azurecr.io/poc/python-test:%version%
        ::call docker rmi cr-ba-python-dev.azurecr.io/poc/python-test:%version%

        for /f "tokens=1-3" %%c IN ('docker image ls ^| Findstr /r "^cr-ba-python-dev.azurecr.io* ^<none>"') do (
            echo Start remove image: `%%c:%%d` with ID: %%e
            if "%%d" equ "<none>" (
                echo Delete image with id ...
                call docker rmi %%e > nul 2>&1
            ) else (
                echo Delete image with name:tag ...
                call docker rmi "%%c:%%d" > nul 2>&1
            )
        )
    )
    ```

    Run Task with JSON

    ```json
    {
      "id": "container-job-10",
      "commandLine": "",
      "containerSettings": {
          "containerRunOptions": "--rm --workdir /app",
          "imageName": "cr-ba-python-dev.azurecr.io/poc/python-test:0.0.8",
          "workingDirectory": "taskWorkingDirectory"
      },
      "userIdentity": {
          "autoUser": {
              "scope": "pool",
              "elevationLevel": "admin"
          }
      }
    }
    ```

https://raw.githubusercontent.com/Azure-Samples/compute-automation-configurations/master/prepare_vm_disks.sh

!!! note

    `--mount type=bind,source=/datadisks/disk1,target=/data`

    `-v {<volume_id>}:{<path>}`

!!! warning

    **Azure Data Factory** does not support for run Azure Batch with docker container currently,
    [read more information](https://github.com/MicrosoftDocs/azure-docs/issues/16473)

## Run with Mount Volume

- https://stackoverflow.com/questions/64763378/can-i-use-docker-volumes-in-container-based-azure-batch-pools

## References

- [Use Container for Azure Batch Service](https://dev.to/kenakamu/use-container-for-azure-batch-service-2mnn)
