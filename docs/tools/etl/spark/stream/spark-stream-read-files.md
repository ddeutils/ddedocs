# Spark Stream: _Read from Files_

## Getting Started

### Create Spark Session

```python
# Create the Spark Session
from pyspark.sql import SparkSession

spark = (
    SparkSession
        .builder
        .appName("Streaming Process Files")
        .config("spark.streaming.stopGracefullyOnShutdown", True)
        .master("local[*]")
        .getOrCreate()
)
```

## References

* [Structured Streaming Read from Files](https://subhamkharwal.medium.com/pyspark-structured-streaming-read-from-files-c46fa0ce8888)
* [Structured Streaming for multi format scalable Data Ingestion Workloads](https://medium.com/@prithvijit.guha245/pyspark-structured-streaming-for-multi-format-scalable-data-ingestion-workloads-9cdac4b7c912)
