---
icon: simple/apachespark
---

# Apache Spark

https://medium.com/@think-data/this-level-of-detail-in-spark-is-tackled-only-by-experts-2-975cfb41af50

## Memory

https://medium.com/@think-data/understanding-the-memory-components-of-spark-e3070f315d17

## Spark Context vs Spark Session

**Create Spark Session**:

```python
from pyspark.sql import SparkSession

spark = (
    SparkSession
        .builder
        .appName("YourAppName")
        .config("spark.some.config.option", "some-value")
        .getOrCreate()
)
```

https://towardsdev.com/spark-context-vs-spark-session-97d87bd5ef9e

## Execution

https://blog.stackademic.com/apache-spark-101-understanding-spark-code-execution-cbff49cb85ac

## Most Common Usecases

https://towardsdatascience.com/fetch-failed-exception-in-apache-spark-decrypting-the-most-common-causes-b8dff21075c

## Interview Questions

https://blog.devgenius.io/spark-interview-questions-ii-120e1621be9a
https://blog.devgenius.io/spark-interview-questions-x-843a24cb703a
