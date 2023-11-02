# Azure Batch: _Docker_

**Azure Batch** can be a great tool for instant batch processing as it creates and
manages a pool of compute nodes (virtual machines), installs the applications you
want to run, and schedules jobs to run on the nodes. Sometimes however a container
could be a more appropriate solution for simplicity and scaling than a virtual machine.

## Run with Python

- **Azure Container Registry** (ACR):

  - Go to `Container Registries` => Create container registry
  - Add the information of this registry like name is `btch-regis-dev`
  - Click create for registry creation
  - After registry creation, Go to `btch-regis-dev` registry => `Access Keys`
  - Click Enable on `Admin user` option
  - Save these values, `Login server`, `Username`, and `Password`

- **Docker Container**:

  - Go to your local terminal
  - Create your `Dockerfile` and test run your image on local

    ```dockerfile
    FROM python:3.9-slim

    WORKDIR /app

    COPY main.py ./

    RUN mkdir -p ./output

    CMD ["python","./main.py"]
    ```

    ```python
    # .\main.py
    print("This is a Docker test.")
    with open('/output/docker_test.txt', 'w') as f:
        f.write("This is a Docker test.")
    ```

    ```shell
    docker build -t "python-btch" . --no-cache
    ```

    ```shell
    docker run --name python-btch -v "${pwd}\output:/output" python-btch
    ```

  - Push your image to `Azure Container Registries`

    ```shell
    docker login dataplatdev.azurecr.io
    ```

    ```shell
    docker tag python-btch:latest dataplatdev.azurecr.io/btch/python-btch:0.0.1-test
    ```

    ```shell
    docker push dataplatdev.azurecr.io/btch/python-btch:0.0.1-test
    ```

- **Azure Batch Accounts**:

  - Go to your `Batch accounts` => `Pools` => Add new pool that [Supports Container](https://learn.microsoft.com/en-us/azure/batch/batch-docker-container-workloads#supported-virtual-machine-images)
  - Click Enable to `Custom` on `Container configuration` option
  - Go to `Container registries` => Add `btch-regis-dev` registry from ACR values
  - Create `Pool` with name is `btch-pool-cntn`
  - Go to `Jobs` => Create new job in `btch-pool-cntn` pool with name `btch-job-cntn`
  - Go to `Tasks` => Create new task in `btch-job-cntn` job
    - Go to `Image name` and add `dataplatdev.azurecr.io/btch/python-btch:0.0.1-test`
    - Go to `Container run options` and add
      ```text
      --rm --workdir /app
      ```

- **Automate Script**:

  Package image version from local to Azure Container Registries

  ```shell
  @echo off
  set "version=%~1"
  if defined version (
      echo Start package docker image version: %version% ...
      call docker build -t python-test:latest . --no-cache
      call docker tag python-test:latest dataplatdev.azurecr.io/poc/python-test:%version%
      call docker push dataplatdev.azurecr.io/poc/python-test:%version%
      ::call docker rmi dataplatdev.azurecr.io/poc/python-test:%version%
      for /f "tokens=1-3" %%c IN ('docker image ls ^| Findstr /r "^dataplatdev.azurecr.io* ^<none>"') do (
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

  ```shell
  {
    "id": "container-job-10",
    "commandLine": "",
    "containerSettings": {
        "containerRunOptions": "--rm --workdir /app",
        "imageName": "dataplatdev.azurecr.io/poc/python-test:0.0.8",
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

> **Note**: \
> `--mount type=bind,source=/datadisks/disk1,target=/data` \
> `-v {<volume_id>}:{<path>}`

> **Warning**: \
> Azure Data Factory does not support for run Azure Batch with docker container currently \
> refs: https://github.com/MicrosoftDocs/azure-docs/issues/16473

## Run with mount volume

- https://stackoverflow.com/questions/64763378/can-i-use-docker-volumes-in-container-based-azure-batch-pools

## References

- https://dev.to/kenakamu/use-container-for-azure-batch-service-2mnn
