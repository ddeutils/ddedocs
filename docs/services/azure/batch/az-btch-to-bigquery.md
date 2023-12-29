# Azure Batch: _To BigQuery_

On Bath Pool, it should install Python package:

```console
$ pip install google-cloud-bigquery pandas_gbq
```

## Using Service Account

### 1) Keep Credential to Key Vault

* In the `IAM & Admin` :octicons-arrow-right-24: Go to `Service Accounts`
  :octicons-arrow-right-24: Click `CREATE SERVICE ACCOUNT`
* On `Permission` :octicons-arrow-right-24: Assign `BigQuery Job User` and `BigQuery Data Editor`
  to this service account
* When a service account was created, it will generate Json credential file that
  has detail like:

    ```json
    {
      "type": "service_account",
      "project_id": "<project-id>",
      "private_key_id": "<private-key-id>",
      "private_key": "-----BEGIN PRIVATE KEY-----\n???\n-----END PRIVATE KEY-----\n",
      "client_email": "<service-name>@<project-id>.iam.gserviceaccount.com",
      "client_id": "<client-id>",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/<service-name>%40<project-id>.iam.gserviceaccount.com",
      "universe_domain": "googleapis.com"
    }
    ```

### 2) Connection Code

```python
import json
import pandas as pd
import pandas_gbq as pg
from google.oauth2.service_account import Credentials

df: pd.DataFrame = pd.read_parquet("/dummy-file.parquet")

json_info = json.loads(secret_client.get_secret("GOOGLE-JSON-STR").value)
pg.to_gbq(
    df,
    destination_table="<dataset>.<table-name>",
    if_exists='replace',
    project_id="<project-id>",
    credentials=Credentials.from_service_account_info(json_info),
)
```
