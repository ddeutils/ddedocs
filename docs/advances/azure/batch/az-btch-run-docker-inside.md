# Azure Batch Account run Docker Container inside VM

**Update**: `2023-04-26` |
**Tag**: `Azure` `Batch Account` `Docker`

Azure Batch is a very useful service that you can manage VMs and run tasks among
the VMs. It fits into my need naturally. To avoid the dependencies of running some
Python training code, I notice docker container is another natural tool to help
– build all the dependencies and external service connections into the container
and let Azure Batch to run container task in the VM. In this way, the VM managed
by Azure Batch does not need to worry about the version of OS, dependencies etc.
All we need to ensure is the docker container can be run correctly on the VM,
which is a very simple step for Ubuntu or other Linux system. The same training
container could accept different parameters and run as much as we want.

## Create Pool

Create Ubuntu pool and set start task command line:

```text
/bin/bash -c
"sudo apt-get update &&
sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common &&
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - &&
sudo apt-key fingerprint 0EBFCD88 &&
sudo add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" &&
sudo apt-get update &&
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin &&
sudo usermod -aG docker $USER &&
sudo systemctl restart docker &&
sudo apt-get install dos2unix
"
```

> **Note**: \
> We add `$USER` to docker group because we want to execute `docker` command without
> `sudo`.

## Create Dockerfile

```dockerfile
FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y cmake build-essential gcc g++ git wget libgl1-mesa-glx

RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
RUN apt-get install -y --no-install-recommends msttcorefonts

# python-package
# miniconda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    /bin/bash Miniconda3-latest-Linux-x86_64.sh -f -b -p /opt/conda && \
    export PATH="/opt/conda/bin:$PATH"

ENV PATH /opt/conda/bin:$PATH

RUN conda install -y numpy scipy scikit-learn pandas matplotlib

# azure storage
RUN pip install azure azure-storage

# clean
RUN apt-get autoremove -y && apt-get clean && \
    conda clean -i -l -t -y && \
    rm -rf /usr/local/src/*

# copy resource files
COPY . .

ENV AZURE_BLOB_KEY="[AZURE_BLOB_KEY]"

ENTRYPOINT [ "python", "train.py" ]
```

## Create runner script file

```shell
#!/bin/bash

echo "Script Name: $0 with process id: $$";
echo "Start run docker with image: $1";
echo "Receive environment file name: $2";

echo ${AZ_BATCH_CERTIFICATES_DIR};
mkdir certs/;
cp ${AZ_BATCH_CERTIFICATES_DIR}/* certs/;
ls certs/;

ACR_PWD=$(python3 runner.py 2>&1 >/dev/null);

# Build Docker Container
docker --version;
docker build -t $1:latest . --no-cache;
docker login dataplatdev.azurecr.io -u dataplatdev -p $ACR_PWD;
docker pull dataplatdev.azurecr.io/poc/python-test:0.0.8 >/dev/null 2>&1;
docker images;
echo
echo "Delete Old images ...";
docker rmi -f $(docker image ls -f "dangling=true" -q);
docker images;
echo
# Run Docker Container
OLD=$(docker ps --all --quiet --filter=name="$1");
if [[ -n "$OLD" ]]; then docker stop $OLD && docker rm $OLD; fi;
# docker run --name $1 --env-file "./$2" -v "$(pwd)\output:/output" $1:latest;
docker run --name $1 -v "$(pwd)\output:/output" $1:latest;
docker ps -a;
CONTAINER_RC=$(docker inspect --format '{{.State.ExitCode}}' $1);
exit $CONTAINER_RC;
```

## References

- https://jilongliao.com/2018/05/28/container-ml-azure-batch/
