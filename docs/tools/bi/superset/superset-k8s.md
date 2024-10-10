# On Kubernetes

## Getting Started

Use the following command to add the Superset Helm repository to your Helm client:

```shell
helm repo add superset https://apache.github.io/superset
helm search repo superset
```

Create a namespace

```shell
kubectl create namespace superset
```

Generate SECRET_KEY

```shell
openssl rand -base64 42
```

```yaml titles="superset_values.yaml"
# Define the namespace where Superset will be installed
namespace: superset

# Database configuration
postgresql:
  postgresqlUsername: supersetpostgres
  postgresqlPassword: SuperPGadmin@2024
  postgresqlDatabase: superset

configOverrides:
  secret: |
    SECRET_KEY = '<the-above-secret>'

bootstrapScript: |
  #!/bin/bash
  pip install psycopg2 \
    pip install pyhive && \
  if [ ! -f ~/bootstrap ]; then echo "Running Superset with uid {{ .Values.runAsUser }}" > ~/bootstrap; fi
```

## References

- [Reporting with Apache Superset on Kubernetes: Integrating SQL Server and Delta Lake](https://medium.com/@howdyservices9/reporting-with-apache-superset-on-kubernetes-integrating-sql-server-and-delta-lake-9d72da1597d5)
