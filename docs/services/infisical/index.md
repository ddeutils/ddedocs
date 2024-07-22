---
icon: fontawesome/solid/infinity
---

# Infisical

**Infisical** is the open source secret management platform that developers use
to centralize their application configuration and secrets like API keys and
database credentials as well as manage their internal PKI. Additionally,
developers use Infisical to prevent secrets leaks to git and securely share
secrets amongst engineers.

## Getting Started

### Create with Python

#### Install Python Packages

```text
pip install flask infisical-python
```

#### Application Code

```python
from flask import Flask
from infisical_client import ClientSettings, InfisicalClient, GetSecretOptions, AuthenticationOptions, UniversalAuthMethod

app = Flask(__name__)

client = InfisicalClient(ClientSettings(
    auth=AuthenticationOptions(
      universal_auth=UniversalAuthMethod(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
      )
    )
))

@app.route("/")
def hello_world():
    name = client.getSecret(options=GetSecretOptions(
       environment="dev",
       project_id="PROJECT_ID",
       secret_name="NAME"
    ))

    return f"Hello! My name is: {name.secret_value}"
```

Read More [Guides - Python](https://infisical.com/docs/documentation/guides/python)
