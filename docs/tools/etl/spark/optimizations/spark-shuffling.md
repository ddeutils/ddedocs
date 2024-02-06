# Spark: _Shuffling_

**Shuffling** is the process of redistributing data across different partitions
and nodes. It occurs during operations like `.join`, `.groupBy`, and `.reduceBy`.
Shuffling is one of the most resource-intensive operations in Spark.

**Consequences of Excessive Shuffling**:

* Network Overhead: Shuffling involves moving large amounts of data over the network, which can be time-consuming and lead to bottlenecks.
* Disk I/O: Excessive shuffling can result in significant disk I/O when data is spilled to disk, slowing down the processing.

## Handling Shuffling

* Minimize Shuffling Operations: Restructuring Spark jobs to reduce the need for shuffling, such as using map-side joins.
* Tuning Partition Sizes: Adjusting the number of partitions to balance load and reduce unnecessary data movement.
* Custom Partitioners: Using custom partitioners to control the distribution of data and minimize shuffling.

* [:simple-medium:](https://medium.com/@tomhcorbin/boosting-efficiency-in-pyspark-a-guide-to-partition-shuffling-9a5af77703ea)

## References

* [:simple-medium: ](https://medium.com/@tomhcorbin/boosting-efficiency-in-pyspark-a-guide-to-partition-shuffling-9a5af77703ea)
