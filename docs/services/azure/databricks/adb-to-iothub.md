# To IoT Hub

[Azure Event Hubs with Spark](https://github.com/Azure/azure-event-hubs-spark)

```text
groupId = com.microsoft.azure
artifactId = azure-eventhubs-spark_2.12
version = 2.3.22
```

## Using Shared Access Key

### Connection Code

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession
        .builder
        .appName('App Connect IoT Hub')
        .config("spark.jars.packages", "com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.22")
        .config("spark.locality.wait", "15s")  # Default: 3s
        .getOrCreate()
)
```

```python

connectionString: str = (
    f"Endpoint=sb://{eventhubs_compatible_name}.servicebus.windows.net/;"
    f"SharedAccessKeyName={sharekey_name};"
    f"SharedAccessKey={sharekey};"
    f"EntityPath={endpoint_name}"
)
ehConf = {
    'eventhubs.connectionString' : spark._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connectionString),
    'eventhubs.consumerGroup' : "$Default",
    'eventhubs.partition.count': "1",
    'ehName': f"{IoTHubs-EventHub-Compatible-Name}",
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

## :material-playlist-plus: Read Mores

- https://github.com/Azure/azure-event-hubs-spark/blob/master/docs/PySpark/structured-streaming-pyspark.md#user-configuration
- https://medium.com/@kaviprakash.2007/structured-streaming-using-azure-databricks-and-event-hub-6b0bcbf029c4
