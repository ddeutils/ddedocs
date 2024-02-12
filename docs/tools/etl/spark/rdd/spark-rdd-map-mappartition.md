# Spark RDD: _Map & MapPartitions_

`map()` and `mapPartitions()` are two transformation operations in PySpark that
are used to process and transform data in a distributed manner.

## Map

`map()` is a transformation operation that applies a function to each element of
an RDD independently and returns a new RDD. The function applied to each element
should be a pure function, which means it should not have any side effects and
should return a new value based on the input value.

=== "Map"

    ```python
    rdd = sc.parallelize([1, 2, 3, 4])
    squared_rdd = rdd.map(lambda x: x**2)
    squared_rdd.collect()

    # output
    [1, 4, 9, 16]
    ```

=== "Filter"

    ```python
    rdd = sc.parallelize(["This is a sentence.", "Another sentence.", "Yet another sentence."])
    filtered_rdd = rdd.filter(lambda x: "sentence" in x)
    filtered_rdd.collect()

    # output
    ['This is a sentence.', 'Another sentence.', 'Yet another sentence.']
    ```

## Map Partitions

`mapPartitions()` is also a transformation operation that applies a function to
each partition of an RDD. Unlike `map()`, the function applied to each partition
is executed once for each partition, not once for each element. This can be useful
when the processing of each partition requires some initialization or setup that
can be done once for each partition, instead of for each element.

=== "MapPartition"

    ```python
    rdd = sc.parallelize([1, 2, 3, 4], 2)
    def sum_partition(iterator):
        yield sum(iterator)

    sum_rdd = rdd.mapPartitions(sum_partition)
    sum_rdd.collect()

    # output
    [3, 7]
    ```

=== "MapPartition with Func"

    ```python
    rdd = sc.parallelize([(1, 2), (3, 4), (5, 6), (7, 8)], 2)
    def average_partition(iterator):
         x_sum = 0
         y_sum = 0
         count = 0
         for (x, y) in iterator:
             x_sum += x
             y_sum += y
             count += 1
         yield (x_sum/count, y_sum/count)

    avg_rdd = rdd.mapPartitions(average_partition)
    avg_rdd.collect()

    # output
    [(2.0, 3.0), (6.0, 7.0)]
    ```

## Difference between map() and mapPartitions()

The main difference between `map()` and `mapPartitions()` is that `map()` applies
a function to each element of an RDD independently, while `mapPartitions()` applies
a function to each partition of an RDD. Therefore, `map()` is more suitable when
the processing of each element is independent, while `mapPartitions()` is more
suitable when the processing of each partition requires some initialization or
setup that can be done once for each partition.

The choice between the two depends on the nature of the data and the processing
required for each element or partition.

## References

* [Understanding PySpark Transformations: Map and MapPartitions Explained](https://medium.com/@uzzaman.ahmed/understanding-pyspark-transformations-map-and-mappartitions-explained-db04931a93ef)
