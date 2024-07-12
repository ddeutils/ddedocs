---
icon: simple/delta
---

# Delta Lake

!!! quote

    **Delta Lake** is open source software that extends Parquet data files with a
    file-based transaction log for ACID transactions and scalable metadata handling.
    A Delta Lake table is a table created and managed using Delta Lake technology.

**Delta Lake** is the optimized storage layer that provides the foundation for storing
data and tables in the Databricks Lakehouse Platform. Delta Lake is fully compatible
with Apache Spark APIs, and was developed for tight integration with Structured Streaming,
allowing you to easily use a single copy of data for both batch and streaming operations
and providing incremental processing at scale.

---

## :material-arrow-down-right: Getting Started

### Basic Architecture

- **Delta Logs**: Utilizes JSON logs to record changes, ensuring accurate data
  lineage and versioning.
- **ACID Transactions**: Supports ACID transactions, providing reliable data management
  for concurrent operations.
- **Merge-on-Write**: Employs a merge-on-write strategy for updates, guaranteeing high
  performance and consistency.

### Use Cases

- **Real-Time Analytics**: Its time travel and versioning features make it perfect
  for real-time data processing and analytics.
- **Data Lakes in Cloud Environments**: With its high scalability and integration
  with cloud services, Delta Lake is well-suited for managing cloud-based data lakes.

---

## Read Mores

- [:material-microsoft: Microsoft - Azure Databricks: Delta](https://learn.microsoft.com/en-us/azure/databricks/delta/)
