# Start Task

## :material-arrow-down-right: Getting Started

### Command Line

Below CMD will remove newline charactor that come from **Windows** first and then
it will execute the start task file with `bash`.

```shell
/bin/bash -c "sed -i 's/\r$//' start_task.sh && bash ./start_task.sh"
```

### Start Task File

=== "Python 3.8"

    ```shell title="start_task.sh"
    #!/bin/bash

    echo 'Update Ubuntu'
    sudo apt update
    echo 'Import Python 3.8 PPA on Ubuntu'
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update
    sudo apt -y install python3.8
    sudo update-alternatives --set python3 /usr/bin/python3.8
    python3 --version
    ```

=== "Python 3.11"

    ```shell title="start_task.sh"
    sudo export DEBIAN_FRONTEND=noninteractive
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update -y
    sudo apt -y install python3.11 python3-pip
    sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
    python --version
    echo $(date -u) '########## INSTALL python3.11-full DONE ##########'
    sudo systemctl restart walinuxagent.service
    sudo systemctl restart networkd-dispatcher.service
    sudo systemctl restart unattended-upgrades.service
    echo "########## INSTALL python3-pip DONE ##########"
    sudo python -m pip install --upgrade pip
    ```

---

## :material-test-tube: Examples

=== "ETL Python 3.8"

    ```shell title="start_task.sh"
    #!/bin/bash

    echo 'Set Python 3.10' &&
    sudo update-alternatives --set python3 /usr/bin/python3.10 || echo 'Skipped: Set Python 3.10' &&
    echo '########## Add PPA Repository ##########' &&
    sudo apt update &&
    sudo add-apt-repository ppa:deadsnakes/ppa || echo 'Skipped: Add Repository' &&
    echo '########## Install Python V3.8 ##########' &&
    sudo apt -y install python3.8 || echo 'Skipped: Install Python 3.8' &&
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2 &&
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 &&
    sudo update-alternatives --set python3 /usr/bin/python3.8 &&
    python3 --version &&
    sudo apt -y install python3-pip &&
    sudo apt -y install python3.8-distutils &&
    python3 -m pip install --upgrade pip &&
    echo '########## Start Install Python Library ##########' &&
    pip3 install backports.zoneinfo &&
    pip3 install azure-storage-file-datalake==12.4.0 &&
    pip3 install azure-keyvault-secrets==4.3.0 &&
    pip3 install azure-identity==1.6.1 &&
    pip3 install cffi==1.16.0 &&
    pip install google-cloud-bigquery==3.13.0 &&
    pip install pandas_gbq==0.17.0 &&
    pip install pandas==2.0.3 &&
    pip install pyarrow==14.0.1 &&
    pip install -U pytz
    ```

=== "ETL Python 3.8 with UV"

    ```shell title="start_task.sh"
    #!/bin/bash

    echo 'Set Python 3.10' &&
    sudo update-alternatives --set python3 /usr/bin/python3.10 || echo 'Skipped: Set Python 3.10' &&
    echo '########## Add PPA Repository ##########' &&
    sudo apt update &&
    sudo add-apt-repository ppa:deadsnakes/ppa || echo 'Skipped: Add Repository' &&
    echo '########## Install Python V3.8 ##########' &&
    sudo apt -y install python3.8 || echo 'Skipped: Install Python 3.8' &&
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2 &&
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 &&
    sudo update-alternatives --set python3 /usr/bin/python3.8 &&
    python3 --version &&
    sudo apt -y install python3-pip &&
    sudo apt -y install python3.8-distutils &&
    python3 -m pip install --upgrade pip &&
    echo '########## Start Install Python Library ##########' &&
    echo $(date -u) &&
    sudo pip install --upgrade pip &&
    sudo pip install uv &&
    sudo uv pip install --system backports.zoneinfo &&
    sudo uv pip install --system azure-storage-file-datalake==12.4.0 &&
    sudo uv pip install --system azure-keyvault-secrets==4.3.0 &&
    sudo uv pip install --system azure-identity==1.6.1 &&
    sudo uv pip install --system cffi==1.16.0 &&
    sudo uv pip install --system google-cloud-bigquery==3.13.0 &&
    sudo uv pip install --system pandas_gbq==0.17.0 &&
    sudo uv pip install --system pandas==2.0.3 &&
    sudo uv pip install --system pyarrow==14.0.1 &&
    sudo uv pip install --system -U pytz
    echo $(date -u) "End of Python Library installation"
    ```

=== "ODBC SQL Server"

    ```shell title="start_task.sh"
    #!/bin/bash

    echo '########## Installing Python 3.11 on Ubuntu 22.04 by using the PPA repository ##########' &&
    sudo apt install python3-apt --fix-missing &&
    sudo apt update &&
    sudo add-apt-repository ppa:deadsnakes/ppa || echo 'Skipped: Add Repository' &&
    sudo apt -y install python3.11 &&
    sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 2 &&
    sudo update-alternatives --config python3 &&
    sudo apt install python-is-python3 &&
    python --version &&
    echo '########## Install Extras for Python 3.11 ##########' &&
    sudo apt-get install python3.11-full -y &&
    sudo apt-get install python3-pip -y &&
    sudo python3 -m pip install --upgrade pip &&
    echo '########## Setting ODBC Libs ##########' &&
    sudo curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - &&
    sudo curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list &&
    sudo apt-get update &&
    sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17 &&
    echo '--- Done: msodbcsql17' &&
    sudo ACCEPT_EULA=Y apt-get install -y mssql-tools &&
    echo '--- Done: mssql-tools' &&
    echo 'export PATH=\"$PATH:/opt/mssql-tools/bin\"' >> ~/.bashrc &&
    source ~/.bashrc
    ```

    ??? note

        ```shell title="install_msodbcsql17.sh"
        if ! [[ "16.04 18.04 20.04 22.04" == *"$(lsb_release -rs)"* ]];
        then
            echo "Ubuntu $(lsb_release -rs) is not currently supported.";
            exit;
        fi
        curl https://packages.microsoft.com/keys/microsoft.asc | sudo tee /etc/apt/trusted.gpg.d/microsoft.asc
        curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
        sudo apt-get update
        sudo ACCEPT_EULA=Y apt-get install -y msodbcsql17
        # Optional: for bcp and sqlcmd
        sudo ACCEPT_EULA=Y apt-get install -y mssql-tools
        echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
        source ~/.bashrc
        # Optional: for unixODBC development headers
        sudo apt-get install -y unixodbc-dev
        ```

        Reference from [How to Install Microsoft ODBC Driver for SQL Server on Ubuntu](https://medium.com/@hoon33710/how-to-install-microsoft-odbc-driver-for-sql-server-on-ubuntu-6e6e2ec2f561)

=== "Docker"

    ```shell
    sudo apt-get update
    sudo apt -y install curl apt-transport-https ca-certificates software-properties-common
    sudo mkdir -p /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod 755 /etc/apt/keyrings
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg ] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
        | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    sudo usermod -aG docker $USER
    sudo chmod 666 /var/run/docker.sock
    docker ps
    ```

=== "GCloud"

    ```shell
    sudo mkdir -p /etc/apt/keyrings
    sudo curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
    sudo chmod 755 /etc/apt/keyrings
    sudo chmod a+r /etc/apt/keyrings/cloud.google.gpg
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
        | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    sudo apt-get update
    sudo apt-get -y install google-cloud-cli
    ```

## Advance

### Wrapped Start Task

```shell
/bin/bash -c "sed -i 's/\r$//' start_task.sh && bash ./start_task.sh"
```

```shell
#!/bin/bash

cnt_startup=$( cat /root/cnt_startup.txt ) || echo "0" > /root/cnt_startup.txt
cnt_startup=$( cat /root/cnt_startup.txt )
((cnt_startup++))
echo "########## Start up count = [$cnt_startup] ##########"
echo "$cnt_startup" > /root/cnt_startup.txt

echo '########## Install Azure CLI for calling Azure function ##########'
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

az login --identity
FUNC_APP=$( az keyvault secret show --name "FUNCAPP" --vault-name "$KEYVAULT_NM" --query "value" )
# NOTE: Convert secret to percent encoding
FUNC_APP=$( python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$FUNCAPP" )

/bin/bash -c "sed -i 's/\r$//' start_task.sh && bash ./start_task.sh"
if [ $? -eq 0 ]
then
    echo "########## Successfully start up task. ##########"
else
    echo "########## Startup task fail, calling Azure function. ########## "
    # NOTE: Creating Azure function to check API Azure batch
    curl --location "$FUNC_URL?code=$FUNC_APP" \
        --header 'Content-Type: application/json' \
        --data "{\"pool_id\": \"$AZ_BATCH_POOL_ID\", \"node_id\": \"$AZ_BATCH_NODE_ID\", \"reboot_cnt\": $cnt_startup}"
    exit 1
fi
```
