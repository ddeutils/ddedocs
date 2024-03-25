# On Kubernetes

As of **Apache Spark 3.1** release in March 2021, spark on kubernetes is generally
available. This is great in so many ways, including but not limited to:

- you have full control of your infra
- takes less than 10 seconds to start a spark cluster
- can store logs in a central location, to be viewed later via spark history server
- can use minio as local storage backend (better throughput compared to calling S3 via home/work internet)
- cheaper than all managed solutions, even serverless variants (more on this later)

## References

- [Spark on Kubernetes](https://karnwong.me/posts/2023/09/spark-on-kubernetes/?fbclid=IwAR1c9QzH5jSUpUw0cvPovkCWD7l1Tq7Kvmf7rBHToNRhW_IPKbGf3KjeEOQ)
