# Data Warehouse: _Bill Inmon Approach_

The Bill Inmon design approach uses the normalized form for building entity structure,
avoiding data redundancy as much as possible. This results in clearly identifying
business requirements and preventing any data update irregularities.
Moreover, the advantage of this top-down approach in database design is that it
is robust to business changes and contains a dimensional perspective of data across data mart.

The Inmon methodology, also known as normalized modeling, is a top-down approach that focuses on designing the data warehouse around the data.

It uses a 3NF (third normal form) schema to model the data and focuses on creating a single integrated data model that supports all of the organization’s reporting and analysis needs.

The Inmon methodology is known for its data integrity, consistency, and accuracy.

* Inmon’s model follows a top-down approach. The Data Warehouse (DWH) is sourced
  from OLTP systems and is the central repository of data.

* The Data Warehouse in Inmon’s model is in Third Normal Form (3NF).

* The Data marts (DM) are provisioned out of the Data Warehouse as and when required.
  Data marts in Inmon’s model are in 3NF from which the OLAP cubes are built.

!!! quote

    Single version of the truth

## Advantages of the Inmon

The following are the main advantages of the Inmon method:

- Because it is the only source for data marts and all data in the data warehouse is integrated, the data warehouse genuinely acts as the enterprise's single source of truth.

- Due to the limited redundancy, data update abnormalities are avoided. This simplifies the ETL(Extraction, transformation, and loading) procedure and reduces the risk of failure.

- Because the logical model represents the distinct business entities, We may easily understand the business processes.

- Very versatile — As business requirements change or source data changes, updating the data warehouse is simple because everything is in one location.

- Can handle a variety of reporting requirements within the organisation.

## Disadvantages of the Inmon

The following are some drawbacks of the Inmon method:

- As more tables and joins are added, the model and implementation can grow increasingly complicated.

- We'll need people knowledgeable in data modelling and the business in general. These resources might be difficult to come by and can be rather costly.

- Management should be aware that the initial setup and delivery will take longer.

- More ETL work is required as the data marts are developed from the data warehouse.

- A vast team of professionals is required to manage the data environment efficiently.

## Reference

- https://www.codingninjas.com/codestudio/library/inmon-approach-in-data-warehouse-designing
