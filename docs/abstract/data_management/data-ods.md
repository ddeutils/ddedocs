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
