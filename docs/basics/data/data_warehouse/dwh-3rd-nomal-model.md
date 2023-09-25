# Third Normal From Model

In the perspective of Bill Inmon, the first step should be to create a consolidated
enterprise-wide data warehouse. This can be made by connecting numerous databases
to the analytical needs of departments, which are later referred to as data marts.
As a result, this method is known as the top-down approach.

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
