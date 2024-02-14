# Data Warehouse: _Bill Inmon Approach_

The Bill Inmon design approach uses the normalized form (3NF) for building entity structure,
avoiding data redundancy as much as possible. This results in clearly identifying
business requirements and preventing any data update irregularities.

The Inmon approach, also known as normalized modeling, is known as the top-down
or data-driven strategy, in which we start with the data warehouse and break it
down into data marts. These data marts are then specialised to satisfy the demands
of other departments inside the firm, such as finance, accounting, and human
resources.

- Begin with the corporation's data model. Identify all of the data sources that
  the company has access to.
- Identify the essential entities (customer, product, order, etc.) and their respective
  linkages based on the data and understanding of business needs.
- Create a thorough, logical model using the entity structure. The logical model
  includes all the properties of each entity, as well as their respective interactions
  and co-dependencies, in great detail. According to data modelling terminology,
  the logical model creates logical schemas for entity relationships.
- Build the physical model from the logical one. Extract data from various sources,
  alter it and integrate it into a normalised data model using ETL operations.
  Each normalised data model stores data in the third normal form to avoid redundancy.
  The data warehouse's core is the normalised data model.
- Create data marts for different departments. For all reporting needs, data marts
  are used to access data, and the data warehouse serves as a single source of truth.

!!! quote

    Single version of the truth

## Advantages of the Inmon Approach

The following are the main advantages of the Inmon method:

- Because it is the only source for data marts and all data in the data warehouse is integrated, the data warehouse genuinely acts as the enterprise's single source of truth.

- Due to the limited redundancy, data update abnormalities are avoided. This simplifies the ETL(Extraction, transformation, and loading) procedure and reduces the risk of failure.

- Because the logical model represents the distinct business entities, We may easily understand the business processes.

- Very versatile — As business requirements change or source data changes, updating the data warehouse is simple because everything is in one location.

- Can handle a variety of reporting requirements within the organisation.

* Flexibility: Inmon's approach adapts faster to changing business needs and data source alterations. Inmon's architecture is more versatile due to the ETL process design that results in normalised data. The architects alter only a few normalised tables, communicating the modification downstream.
* Single source of truth: Because of the normalised data model, the data warehouse serves as a single source of truth for the entire organisation.
* Less prone to errors: Because normalisation minimises data redundancy, both engineering and analytical procedures are less susceptible to errors.
* Completeness: Inmon's approach incorporates all Enterprise data, ensuring that all reporting requirements are met.

Good fit for:

- Low complexity data that connects neatly together
- Simple, business-focused downstream use cases for the data
- Central data teams that have deep knowledge of the facets of their data

## Disadvantages of the Inmon Approach

The following are some drawbacks of the Inmon method:

- As more tables and joins are added, the model and implementation can grow increasingly complicated.

- We'll need people knowledgeable in data modelling and the business in general. These resources might be difficult to come by and can be rather costly.

- Management should be aware that the initial setup and delivery will take longer.

- More ETL work is required as the data marts are developed from the data warehouse.

- A vast team of professionals is required to manage the data environment efficiently.

* Cost of initial setup and regular maintenance: The time and cost required to set up and maintain Inmon's architecture are far greater than the time and investment needed for Kimball's architecture. Normalised schemas are more challenging to build and maintain than their denormalised counterparts.
* Skill requirement: Highly skilled engineers are required for Inmon's method, which is harder to come by and more expensive to maintain on the payroll.
* Extra ETL is required: Separating data marts from the data warehouse necessitates the employment of more ETL processes to generate the data marts, resulting in increased engineering overhead.

## Reference

- [Inmon Approach in DWH Designing](https://www.codingninjas.com/codestudio/library/inmon-approach-in-data-warehouse-designing)
