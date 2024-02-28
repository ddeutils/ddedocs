# Kinesis Data Streams

**Kinesis Data Stream** is a set of shards. Each shard has a sequence of data
records. Each data record has a sequence number that is assigned by Kinesis Data
Streams.

![Kinesis Data Streams High-Level Architecture](img/kinesis-architecture.png){ loading=lazy }

**Shard**

:   A _shard_ is a uniquely identified sequence of data records in a stream.
    A stream is composed of one or more shards, each of which provides a fixed
    unit of capacity. Each shard can support **up to 5 transactions per second for
    reads**, up to a maximum total data read rate of 2 MB per second and **up to
    1,000 records per second for writes**, up to a maximum total data write rate of
    1 MB per second (including partition keys). The data capacity of your stream
    is a function of the number of shards that you specify for the stream. The
    total capacity of the stream is the sum of the capacities of its shards.

**Partition Key**

:   A _partition key_ is used to group data by shard within a stream. Kinesis Data
    Streams segregates the data records belonging to a stream into multiple shards.
    It uses the partition key that is associated with each data record to determine
    which shard a given data record belongs to. Partition keys are Unicode strings,
    with a maximum length limit of 256 characters for each key. An MD5 hash function
    is used to map partition keys to 128-bit integer values and to map associated
    data records to shards using the hash key ranges of the shards. When an application
    puts data into a stream, it must specify a partition key.

!!! note

    Sequence numbers cannot be used as indexes to sets of data within the same
    stream. To logically separate sets of data, use partition keys or create a
    separate stream for each dataset.

## References

- [:material-aws: What Is Amazon Kinesis Data Streams?](https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html)
- [:simple-medium: Streaming in Data Engineering](https://towardsdatascience.com/streaming-in-data-engineering-2bb2b9b3b603)
