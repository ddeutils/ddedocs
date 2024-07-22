# Connect to AWS Services

## :material-account-check-outline: Authentication

### Using AWS Access Token

- Go to **IAM**

## :material-arrow-right-bottom: Kinesis

!!! warning

    In **Databricks Runtime 11.3 LTS and Above**, the `Trigger.Once` setting is
    deprecated.
    Databricks recommends you use `Trigger.AvailableNow` for all incremental batch
    processing workloads.[^1]

### 1) IAM Policy

By default, the Kinesis connector resorts to [:material-aws: Amazon’s default credential provider chain](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/credentials.html#credentials-default)

=== "Read"

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "kinesis:Get*",
                    "kinesis:DescribeStreamSummary"
                ],
                "Resource": [
                    "arn:aws:kinesis:us-east-1:111122223333:stream/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "kinesis:ListStreams"
                ],
                "Resource": [
                    "*"
                ]
            }
        ]
    }
    ```

=== "Put"

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "kinesis:PutRecord"
                ],
                "Resource": [
                    "arn:aws:kinesis:us-east-1:111122223333:stream/*"
                ]
            }
        ]
    }
    ```

### 2) Connection Code

=== "ReadStream"

    ```python
    df = (
        spark.readStream
            .format("kinesis")
            .option("streamName", "<aws-kinesis-stream-name>")
            .option("initialPosition", "latest")
            .option("format", "json")
            .option("awsAccessKey", "<aws-access-key>")
            .option("awsSecretKey", "<aws-access-secret-key")
            .option("region", "<aws-region>")
            .option("inferSchema", "true")
            .load()
    )
    ```

    !!! note

        **initialPosition**:

        - `latest`: Read from the latest position that data ingest.
        - `trim_horizon` or `earliest`:  Read all data that keep in shard.
        - `at_timestamp`: Specify time value such as
          `{"at_timestamp": "06/25/2020 10:23:45 PDT", "format": "MM/dd/yyyy HH:mm:ss ZZZ"}`

        [Read more about `StartingPosition`](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_StartingPosition.html)

=== "WriteStream"

    ```python
    (
        df
            .writeStream
            .format("kinesis")
            .outputMode("update")
            .option("streamName", "<aws-kinesis-stream-name>")
            .option("region", "<aws-region>")
            .option("awsAccessKeyId", "<aws-access-key>")
            .option("awsSecretKey", "aws-access-secret-key")
            .option("checkpointLocation", "/path/to/checkpoint")
            .start()
            .awaitTermination()
    )
    ```

!!! note

    Kinesis returns records with the following schema:

    ```python
    from pyspark.sql.types import TimestampType, StringType, StructType, StructField, BinaryType

    schema: StructType = StructType(
        [
            StructField("partitionKey", StringType(), True),
            StructField("data", BinaryType(), False),
            StructField("stream", StringType(), False),
            StructField("shardId", StringType(), False),
            StructField("sequenceNumber", StringType(), False),
            StructField("approximateArrivalTimestamp", TimestampType(), False),
        ],
    )
    ```

**References**:

- [:simple-databricks: Apache Spark’s Structured Streaming with Amazon Kinesis on Databricks](https://www.databricks.com/blog/2017/08/09/apache-sparks-structured-streaming-with-amazon-kinesis-on-databricks.html)
- [:simple-databricks: Connect to Amazon Kinesis](https://docs.databricks.com/en/connect/streaming/kinesis.html)
- [:material-github: Amazon Kinesis Data Streams Connector for Spark Structured Streaming](https://github.com/awslabs/spark-sql-kinesis-connector)

[^1]: [:simple-databricks: Configure Structured Streaming trigger intervals](https://docs.databricks.com/en/structured-streaming/triggers.html#available-now)
