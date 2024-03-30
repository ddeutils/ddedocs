---
icon: simple/apachehadoop
---

# Hadoop

**Hadoop** is an open-source framework that allows for the distributed processing
of large data sets across clusters of computers. It is a fundamental tool in
big data analytics.

:material-page-last: One of the key features of Hadoop is its ability to handle
massive amounts of data.
Traditional databases often struggle with processing and analyzing large datasets,
but Hadoop's _distributed architecture allows it to scale horizontally_
by adding more machines to the cluster.
This enables organizations to store and process petabytes of data efficiently.

!!! note "Key Concept"

    The key concept is that we split the data up and store it across the collection
    of machines known as a cluster. Then when we want to process the data,
    we process it where it’s actually stored. Rather than retrieving the data
    from a central server, the data’s already on the cluster,
    so we can process it in place.

## :material-arrow-down-right: Getting Started

:material-page-last: Thus, Hadoop consists of two main components:
the Hadoop Distributed File System (HDFS) and the MapReduce programming model.

- **HDFS** is a distributed file system that provides high-throughput access to
  data across multiple machines. It breaks down large files into smaller blocks
  and distributes them across the cluster, ensuring data redundancy
  and fault tolerance.

- The **MapReduce** programming model is the heart of Hadoop.
  It allows users to write parallelizable algorithms that can process large
  datasets in a distributed manner.

### HDFS

Imagine we’re going to store a file called mydata.txt. In HDFS. This file is 150 megabytes. When a file is loaded into HDFS, it’s split into chunks which we call blocks. Each block is pretty big. The default is 64 megabytes. Each block is given a unique name, which is BLK, an underscore, and a large number.

### MapReduce

...

## Ecosystems

Hadoop also provides a range of tools and libraries that enhance its functionality.
For example,

- Apache Hive allows users to query and analyze data using a SQL-like language called HiveQL.

- Apache Pig provides a high-level scripting language called Pig Latin, which simplifies the development of data processing tasks.

Additionally, Hadoop supports machine learning libraries like Apache Mahout,
enabling the implementation of advanced analytics and predictive modeling.

## :material-vector-link: References

- [Big Data: Hadoop](https://ogre51.medium.com/big-data-hadoop-0baee8241354)
