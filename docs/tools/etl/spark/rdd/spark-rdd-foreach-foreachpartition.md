# Spark RDD: _Map & MapPartitions_

# Foreach

foreach is a PySpark RDD (Resilient Distributed Datasets) action that applies a
function to each element of an RDD. It is used to perform some side-effecting
operations, such as writing output to a file, sending data to a database, or printing
data to the console. The function passed to foreach should have a void return type,
meaning it does not return anything.

```python
rdd = sc.parallelize([1, 2, 3, 4, 5])
def print_num(num):
    print(num)
rdd.foreach(print_num)

# OUTPUT
1
2
3
4
5
```

# Foreach Partition

foreachPartition is similar to foreach, but it applies the function to each partition
of the RDD, rather than each element. This can be useful when you want to perform
some operation on a partition as a whole, rather than on each element individually.
The function passed to foreachPartition should have a void return type.

```python
rdd = sc.parallelize([1, 2, 3, 4, 5], 2)
def print_partition(iter):
    for num in iter:
        print(num)
rdd.foreachPartition(print_partition)

# OUTPUT
1
2
3
4
5
```

## Use Cases

- **Writing data to external systems**: foreach and foreachPartition are often used
  to write the output of a PySpark job to an external system such as a file, database,
  or message queue. For example, you could use foreach to write each element of
  an RDD to a file, or use foreachPartition to write each partition to a separate
  file.
- Sending data to an external service: Similarly, foreach and foreachPartition can be used to send data to an external service for further analysis. For example, you could use foreach to send each element of an RDD to a web service, or use foreachPartition to send each partition to a separate service.
- Performing custom processing: foreachPartition can be useful when you want to perform some custom processing on each partition of an RDD. For example, you might want to calculate some summary statistics for each partition or perform some machine learning model training on each partition separately.
- Debugging and logging: foreach and foreachPartition can be used for debugging and logging purposes. For example, you could use foreach to print the output of each element to the console for debugging purposes, or use foreachPartition to log each partition to a separate file for debugging and monitoring purposes.
- Performing complex side-effecting operations: Finally, foreach and foreachPartition can be used to perform complex side-effecting operations that cannot be expressed using built-in PySpark transformations. For example, you could use foreach to perform some custom analysis on each element of an RDD, or use foreachPartition to perform some complex transformation on each partition.

It’s worth noting that foreach and foreachPartition are actions, meaning they
trigger the execution of the computation on the RDD. Therefore, they should be used
sparingly, as they can result in significant overhead and slow down the computation.
It's usually better to use transformations like map, filter, and reduceByKey to
perform operations on RDDs, and only use foreach and foreachPartition when necessary.

## References

- [](https://medium.com/@uzzaman.ahmed/exploring-the-power-of-pyspark-a-guide-to-using-foreach-and-foreachpartition-actions-ce63c28feade)
