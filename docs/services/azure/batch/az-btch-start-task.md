# Azure Batch: _Start Task_

## Command Line

```shell
/bin/bash -c "sed -i 's/\r$//' start_task.sh && bash ./start_task.sh"
```

## Start Task File

=== "Python 3.8"

    ```shell
    echo 'Update Ubuntu' &&
    sudo apt update &&
    echo 'Import Python 3.8 PPA on Ubuntu' &&
    sudo add-apt-repository ppa:deadsnakes/ppa -y &&
    sudo apt update &&
    sudo apt -y install python3.8 &&
    sudo update-alternatives --set python3 /usr/bin/python3.8 &&
    python3 --version
    ```

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
