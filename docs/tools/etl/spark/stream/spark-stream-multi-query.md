# Spark Stream: Multi Query

!!! note

    If you are looking for writing the same dataset to many different sinks, you
    should consider the foreachBatch sink.

```java
val filesWithNumbers = sparkSession.readStream.text(s"${basePath}/data").as[Int]

val multipliedBy2 = filesWithNumbers.map(nr => nr * 2)
val multipliedBy2Writer = multipliedBy2.writeStream.format("json")
    .option("path", s"${basePath}/output/sink-1")
    .option("checkpointLocation", s"${basePath}/checkpoint/sink-1")
    .start()

val multipliedBy3 = filesWithNumbers.map(nr => nr * 3)
val multipliedBy3Writer = multipliedBy3.writeStream.format("json")
    .option("path", s"${basePath}/output/sink-2")
    .option("checkpointLocation", s"${basePath}/checkpoint/sink-2")
    .start()

sparkSession.streams.awaitAnyTermination()
```

* https://www.waitingforcode.com/apache-spark-structured-streaming/multiple-queries-running-apache-spark-structured-streaming/read
* [Spark Structured Streaming: Multiple Sinks](https://blog.devgenius.io/spark-structured-streaming-multiple-sinks-writes-5dea139d4920)
