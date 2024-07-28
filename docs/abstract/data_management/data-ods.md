# Operational Data Store

:material-page-last: **Operational Data Store (ODS)** are nothing but data store
required when neither Data warehouse nor OLTP systems support organizations reporting
needs.
In ODS, Data warehouse is refreshed in real-time. Hence, it is widely preferred
for routine activities like storing records of the Employees.

!!! note

    Unlike traditional data warehouses typically used for long-term storage and
    historical data analysis, an ODS focuses on providing a current, integrated,
    and consistent view of operational data from multiple sources.

    It acts as an intermediary layer between the operational systems
    (such as transactional databases, CRM systems, or ERP systems)
    and the data warehouse or data mart.

    This is a type of data warehouse that stores operational data from various sources
    and provides near real-time reporting and analysis. It is designed to handle frequent
    updates and queries from operational systems. It also serves as a source of data
    for the EDW or data marts.

:material-page-last: An ODS is a type of data warehouse that stores real-time or
near-real-time data from transactional systems. It is designed to support operational
reporting and analysis, and it typically uses a bottom-up approach to design,
which means that the data model is based on specific business requirements.

---

## :material-arrow-down-right: Getting Started

An operational data store (ODS) is a central database that aggregates data from
multiple systems, providing a single destination for housing a variety of data.
With information constantly updated, an ODS enables a current snapshot of relevant
business metrics, allowing decision-makers to take advantage of time-sensitive
opportunities and make data-informed decisions while business operations are occurring.

Operational data stores integrate data from their source systems in their original
format.
Once loaded, data in the ODS can be scrubbed, resolved for redundancy, and checked
for compliance with relevant business rules. An ODS is especially useful for
light-duty analytical processing such as operational reporting.
And since data contained in the ODS is always the most recent data available,
this system is ideal for real-time data analysis on business processes as they
are happening.

Unlike extract, transform, load (ETL) systems, an operational data store ingests
raw data from production systems in its original format, storing it as is.
There’s no need to transform the data before it can be analyzed or used for making
operational decisions about the business.

## :material-playlist-plus: Read Mores

- [A Modern Approach To The Operational Data Store](https://www.snowflake.com/guides/modern-approach-operational-data-store/)
