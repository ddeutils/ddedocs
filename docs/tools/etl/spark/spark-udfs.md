# UDFs

Developers often create custom **User-Defined Functions (UDFs)** in their Spark code
to handle specific transformations. This allows users to develop personalized code
for their unique data processing requirements.

- https://tsaiprabhanj.medium.com/spark-user-defined-functions-udfs-043f1bdcd09b
- https://medium.com/geekculture/mastering-pyspark-udfs-advantages-disadvantages-and-best-practices-e70f15b5f75c

!!! warning

    [Why you should Avoid using UDFs](https://medium.com/@kerrache.massipssa/why-you-should-avoid-using-udf-in-pyspark-c57558af9d0a)

## Performance

(De)Serialization for Python UDF is carried out as a separate process which takes
additional time for its completion. Allow me to enhance the clarity of the performance
bottleneck by referring to a diagram from one of my previous posts which explains
the under the hood processes involved in converting Spark Dataframe to a Pandas
Dataframe.

![Issues in pickle format explained](img/spark-udfs-perf.png){ loading=lazy width="650" }

I hope the above diagram shows the additional process required in (de)serializing
the data using pickle format. Since all the records needs to be moved to driver
for serialization, most of the cases that involves huge data volume doesn't fit
the dataframe within driver memory and might fail. Though this can be fixed through
different options, it needs additional effort.

## Optimization

### With Apache Arrow

Unveiling a paradigm shift in Apache Spark 3.5 and Databricks Runtime 14.0, the
introduction of Arrow-optimized Python UDFs stands as a game-changer for performance
enhancement.

Anchored by Apache Arrow, a universally adopted cross-language columnar in-memory
data representation, this optimization dismantles traditional, slower data (de)serialization
methods. The result is an agile and efficient data interchange between JVM and
Python processes, elevating the overall efficiency of data processing. Enriched
by the versatility of Apache Arrow’s type system, these optimized UDFs establish
a new standard, offering a consistent and refined approach to handling type coercion.

```python
spark.conf.set("spark.sql.execution.pythonUDF.arrow.enabled", "true")
```

- [Fast-Track PySpark UDF execution with Apache Arrow](https://balachandar-paulraj.medium.com/fast-track-pyspark-udf-execution-with-apache-arrow-c4d872664e78)
- [Arrow-optimized Python UDFs in Apache Spark 3.5](https://www.databricks.com/blog/arrow-optimized-python-udfs-apache-sparktm-35)
