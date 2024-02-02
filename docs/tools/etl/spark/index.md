---
icon: simple/apachespark
---

# Apache Spark

https://medium.com/@think-data/this-level-of-detail-in-spark-is-tackled-only-by-experts-2-975cfb41af50
[Partitioning & Bucketing](https://blog.det.life/apache-spark-partitioning-and-bucketing-1790586e8917)
[How does Adaptive Query Execution fix your Spark performance issues](https://medium.com/@kerrache.massipssa/how-does-adaptive-query-execution-fix-your-spark-performance-issues-029166e772b7)

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

## Most Common Use Cases

https://towardsdatascience.com/fetch-failed-exception-in-apache-spark-decrypting-the-most-common-causes-b8dff21075c
https://medium.com/art-of-data-engineering/distinct-and-dropduplicates-in-spark-real-project-example-9007954b49af
https://medium.com/@vishalbarvaliya/coalesce-vs-repartition-58b12a0f0a3d
https://medium.com/@vishalbarvaliya/apache-sparks-reducebykey-and-reduce-transformations-42b3bd80e32e

## Interview Questions

https://blog.devgenius.io/spark-interview-questions-ii-120e1621be9a
https://blog.devgenius.io/spark-interview-questions-x-843a24cb703a
https://gsanjeewa1111.medium.com/pyspark-facts-b83366842ddf


## Optimization

https://medium.com/plumbersofdatascience/7-key-strategies-to-optimize-your-spark-applications-948e7df607b
* [PySpark Tips](https://towardsdev.com/pyspark-tip-d4614b013d6f)
* [4 Examples to Take Your PySpark Skills to Next Level](https://towardsdatascience.com/4-examples-to-take-your-pyspark-skills-to-next-level-2a04cbe6e630)
