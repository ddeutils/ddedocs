# Databricks: _To EventHubs_

## Using Service Principal

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession
        .builder
        .appName('App Connect Eventhub')
        .config("spark.jars.packages", "com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.22")
        .config("spark.locality.wait", "1800s")
        .getOrCreate()
)
```

```python
connectionString = (
    f"Endpoint=sb://{eventhubs_namespace}.servicebus.windows.net/;"
    f"SharedAccessKeyName={sharekey_name};"
    f"SharedAccessKey={sharekey};"
    f"EntityPath={eventhubs_name}"
)
ehConf = {
  'eventhubs.connectionString' : spark._jvm.org.apache.spark.eventhubs.EventHubsUtils.encrypt(connectionString),
  'eventhubs.consumerGroup' : "$Default",
  'eventhubs.setUseExclusiveReceiver' : False
}
```

## References

* https://github.com/Azure/azure-event-hubs-spark/blob/master/docs/PySpark/structured-streaming-pyspark.md#user-configuration
