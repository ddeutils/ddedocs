# Connection BigQuery

## :material-account-check-outline: Authentication

### Using Service Account

#### 1) Create Service Account

- In the **IAM & Admin** :octicons-arrow-right-24: Go to **Service Accounts**
  :octicons-arrow-right-24: Click **CREATE SERVICE ACCOUNT**
- On **Permission** :octicons-arrow-right-24: Assign **BigQuery Job User** and
  **BigQuery Data Editor** to this service account

#### 2) Keep Credential to Key Vault

-   When a service account was created, it will generate Json credential file that
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

#### 3) Connection Code

On Bath Pool, it should install Python package:

```console
$ pip install google-auth
```

```python
import json
from google.oauth2.service_account import Credentials

json_info = json.loads(secret_client.get_secret("GOOGLE-JSON-STR").value)
credentials = Credentials.from_service_account_info(json_info),
```

### Using OAuth Token

User credentials are typically obtained via **OAuth2.0**

```python
from google.oauth2.credentials import Credentials

credentials = Credentials(
    '<access-token>',
    # NOTE: If you obtain a refresh token
    refresh_token='<refresh_token>',
    token_uri='<token_uri>',
    client_id='<client_id>',
    client_secret='<client_secret>',
)
```

---

### :material-arrow-right-bottom: BigQuery

On Bath Pool, it should install Python package:

```console
$ pip install google-cloud-bigquery pandas_gbq
```

!!! note

    I recommend `padas_gbq` because it does not implement complex code.

Before this connection code, you should implement connection for **Azure Key Vault**
first for getting above secret json.

```python
import json
import pandas as pd
import pandas_gbq as pg
from google.oauth2.service_account import Credentials

json_info = json.loads(secret_client.get_secret("GOOGLE-JSON-STR").value)
pg.to_gbq(
    pd.read_parquet("/dummy-file.parquet"),
    destination_table="<dataset>.<table-name>",
    if_exists='replace',
    project_id="<project-id>",
    credentials=Credentials.from_service_account_info(json_info),
)
```
