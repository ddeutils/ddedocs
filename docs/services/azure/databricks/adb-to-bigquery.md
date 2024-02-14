# Databricks: _To BigQuery_

## Using JSON Encoding

```python
credentials_json_str: str = dbutils.secrets.get(scope="<scope-name>", key="<secret-key-name>")

df = (
    spark.read
        .format("bigquery")
        .option("credentials", base64.b64encode(credentials_json_str.encode()).decode('utf-8'))
        .option("parentProject", "<project-id>")
        .option("table", "<dataset>.<table-name>")
        .load()
)
df.show()
```

!!! bug

    [GitHub: Error getting access token from metadata server](https://github.com/GoogleCloudDataproc/spark-bigquery-connector/issues?q=is%3Aissue+Error+getting+access+token+from+metadata+server+at%3A+http%3A%2F%2F169.254.169.254%2FcomputeMetadata%2Fv1%2Finstance%2Fservice-accounts%2Fdefault%2Ftoken)

## Using GOOGLE_APPLICATION_CREDENTIALS

```python
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "</path/to/key/file>"
```

## Using Filepath

```python
df = (
    spark.read
        .format("bigquery")
        .option("credentialsFile", "</path/to/key/file>")
        .option("table", "<dataset>.<table-name>")
        .load()
)
```

## Access Token

```python
# Globally
spark.conf.set("gcpAccessToken", "<access-token>")

# Per read/Write
df = (
    spark.read
        .format("bigquery")
        .option("gcpAccessToken", "<acccess-token>")
)
```

## References

- (https://docs.databricks.com/en/external-data/bigquery.html#step-2-set-up-databricks)
- https://github.com/GoogleCloudDataproc/spark-bigquery-connector
