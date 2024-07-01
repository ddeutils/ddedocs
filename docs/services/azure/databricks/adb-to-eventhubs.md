# To EventHubs

[Azure Event Hubs with Spark](https://github.com/Azure/azure-event-hubs-spark)

```text
groupId = com.microsoft.azure
artifactId = azure-eventhubs-spark_2.12
version = 2.3.22
```

!!! warning

    We should use 1 consumer group per query stream because it will raise `ReceiverDisconnectedException`.
    [Read More about multiple readers](https://github.com/Azure/azure-event-hubs-spark/blob/master/examples/multiple-readers-example.md).

## Using Shared Access Key

### Connection Code

=== "Eventhub"

    ```python
    from pyspark.sql import SparkSession

    spark = (
        SparkSession
            .builder
            .appName('App Connect Eventhub')
            .config("spark.jars.packages", "com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.22")
            .config("spark.locality.wait", "15s")  # Default: 3s
            .getOrCreate()
    )
    ```

    ```python
    connectionString: str = (
        f"Endpoint=sb://{eventhubs_namespace}.servicebus.windows.net/;"
        f"SharedAccessKeyName={sharekey_name};"
        f"SharedAccessKey={sharekey};"
        f"EntityPath={eventhubs_name}"
    )
    ehConf = {
      'eventhubs.connectionString' : spark._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connectionString),
      'eventhubs.consumerGroup' : "$Default",
    }
    ```

    ```python
    df = (
      spark
        .readStream
        .format("eventhubs")
        .options(**ehConf)
        .option("maxEventsPerTrigger", 1_000_000)  # Default: <partition> * 1_000
        .option("useExclusiveReceiver", False)  # Default: True
        .option("receiverTimeout", "PT000100")  # Default: 60 sec
        .option("operationTimeout", "PT000100")  # Default: 60 sec
        .load()
    )
    ```

=== "Kafka Protocol"

    !!! note

        This option require enable Kafka on the Azure Event Hubs.

    ```python
    connectionString: str = (
        f"Endpoint=sb://{eventhubs_namespace}.servicebus.windows.net/;"
        f"SharedAccessKeyName={sharekey_name};"
        f"SharedAccessKey={sharekey};"
        f"EntityPath={eventhubs_name}"
    )
    EH_SASL: str = (
        f'org.apache.kafka.common.security.plain.PlainLoginModule required '
        f'username="$ConnectionString" '
        f'password="{connectionString}";'
    )
    ```

    ```python
    df = (
        spark
            .readStream
            .format("kafka")
            .option("subscribe", f"{eventhubs_name}")
            .option("kafka.bootstrap.servers", f"{eventhubs_namespace}.servicebus.windows.net:9093")
            .option("kafka.sasl.mechanism", "PLAIN")
            .option("kafka.security.protocol", "SASL_SSL")
            .option("kafka.sasl.jaas.config", EH_SASL)
            .option("kafka.request.timeout.ms", "60000")
            .option("kafka.session.timeout.ms", "30000")
            .option("kafka.group.id", "$Default")
            .option("failOnDataLoss", "true")
            .option("spark.streaming.kafka.allowNonConsecutiveOffsets", "true")
            .load()
    )
    ```

## :material-playlist-plus: Read Mores

- https://github.com/Azure/azure-event-hubs-spark/blob/master/docs/PySpark/structured-streaming-pyspark.md#user-configuration
- https://medium.com/@kaviprakash.2007/structured-streaming-using-azure-databricks-and-event-hub-6b0bcbf029c4
- [Connect your Apache Spark application with Azure Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-kafka-spark-tutorial#read-from-event-hubs-for-kafka)
- [Using Apache Spark with Azure Event Hubs for Apache Kafka Ecosystems](https://github.com/Azure/azure-event-hubs-for-kafka/blob/master/tutorials/spark/README.md)
