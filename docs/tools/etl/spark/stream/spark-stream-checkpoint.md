# Checkpoint

**Checkpoint** directories are of much help for Spark Streaming applications in order
to keep track of the metadata. In order to make sure that Spark Streaming Application
resumes from the same point where it stopped, we definitely need to define Checkpoint
directory in our application.

## Content of Checkpoint Directory

- **Metadata**: file keep tracks of the Query Id for the Streaming application.
- **Sources**: keeps track of the Micro batch data sources for the application.
- **Offsets**: keeps tracks of the Micro batch data that is being read and Processed.
- **Commits**: keeps track of the Micro batch that is processed successfully.


## References

- [Spark Streaming Checkpoint Directory](https://subhamkharwal.medium.com/pyspark-spark-streaming-checkpoint-directory-8754554bc838)
