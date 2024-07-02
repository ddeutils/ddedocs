# Memory Spill

**Memory Spill** in Apache Spark is the process of transferring data from RAM to
disk, and potentially back again.
This happens when the dataset exceeds the available memory capacity of an executor
during tasks that require more memory than is available.
In such cases, data is spilled to disk to free up RAM and prevent out-of-memory
errors. However, this process can slow down processing due to the slower speed
of disk I/O compared to memory access.

## Read Mores

- [:simple-medium: Understanding Memory Spills in Apache Spark](https://blog.stackademic.com/understanding-memory-spills-in-apache-spark-bb0eb5ed8e0d)
