# Data Mart

**Data Mart** is a subset of the data warehouse. It specially designed for a particular
line of business, such as sales, finance, sales or finance.
In an independent data mart, data can collect directly from sources.

!!! note

    Data Mart is also a storage component used to store data of a specific function
    or part related to a company by an individual authority, so data marts are flexible
    and small.

---

## :material-arrow-down-right: Getting Started

A Data Mart is a subset of an EDW that is designed to serve a specific business
unit or department. It is optimized for querying and reporting on a specific subject
area, such as sales or marketing, and it is typically easier and faster to implement
than an EDW.

!!! quote

    In truth, the Kimball model was for data marts, not a data warehouse.
    A data mart and a data warehouse are fundamentally different things.
    — _Bill Inmon_

!!! quote

    A data mart is a curated subset of data often generated for analytics and
    business intelligence users. Data marts are often created as a repository
    of pertinent information for a subgroup of workers or a particular use case.
    — Snowflake

:material-page-last: A data mart (as noted above) is a focused version of a data
warehouse that contains a smaller subset of data important to and needed by a
single team or a select group of users within an organization.
A data mart is built from an existing data warehouse (or other data sources)
through a complex procedure that involves multiple technologies and tools to
design and construct a physical database, populate it with data, and set up
intricate access and management protocols.

### Who uses a data mart (and how)?

:material-page-last: Data marts guide important business decisions at a departmental
level.
For example, a marketing team may use data marts to analyze consumer behaviors,
while sales staff could use data marts to compile quarterly sales reports.
As these tasks happen within their respective departments, the teams don't need
access to all enterprise data.

Typically, a data mart is created and managed by the specific business department
that intends to use it. The process for designing a data mart usually comprises
the following steps:

1.  Document essential requirements to understand the business and technical needs
    of the data mart.

2.  Identify the data sources your data mart will rely on for information.

3.  Determine the data subset, whether it is all information on a topic or specific
    fields at a more granular level.

4.  Design the logical layout for the data mart by picking a schema that correlates
    with the larger data warehouse.

:material-page-last: With the groundwork done, you can get the most value from a
data mart by using specialist business intelligence tools, such as _Qlik_ or _SiSense_.
These solutions include a dashboard and visualizations that make it easy to discern
insights from the data, which ultimately leads to smarter decisions that benefit
the company.

---

## Types

:material-page-last: There are three types of data marts that differ based on their
relationship to the data warehouse and the respective data sources of each system.

-   **Dependent** data marts are partitioned segments within an enterprise data
    warehouse.
    This top-down approach begins with the storage of all business data in one
    central location. The newly created data marts extract a defined subset of
    the primary data whenever required for analysis.

-   **Independent** data marts act as a standalone system that doesn't rely on
    a data warehouse.
    Analysts can extract data on a particular subject or business process from
    internal or external data sources, process it, and then store it in a data
    mart repository until the team needs it.

-   **Hybrid** data marts combine data from existing data warehouses and other
    operational sources.
    This unified approach leverages the speed and user-friendly interface of a
    top-down approach and also offers the enterprise-level integration of the
    independent method.

---

## Structure

:material-page-last: A data mart is a subject-oriented relational database that
stores transactional data in rows and columns, which makes it easy to access,
organize, and understand.
As it contains historical data, this structure makes it easier for an analyst to
determine data trends.
Typical data fields include numerical order, time value, and references to one
or more objects.

Companies organize data marts in a multidimensional schema as a blueprint to address
the needs of the people using the databases for analytical tasks.
The three main types of schema are star, snowflake, and vault.

### Star

Star schema is a logical formation of tables in a multidimensional database that
resembles a star shape. In this blueprint, one fact table—a metric set that relates
to a specific business event or process—resides at the center of the star,
surrounded by several associated dimension tables.

There is no dependency between dimension tables, so a star schema requires fewer
joins when writing queries. This structure makes querying easier, so star schemas
are highly efficient for analysts who want to access and navigate large data sets.

### Snowflake

A snowflake schema is a logical extension of a star schema, building out the blueprint
with additional dimension tables. The dimension tables are normalized to protect
data integrity and minimize data redundancy.

While this method requires less space to store dimension tables, it is a complex
structure that can be difficult to maintain. The main benefit of using snowflake
schema is the low demand for disk space, but the caveat is a negative impact on
performance due to the additional tables.

### Vault

Data vault is a modern database modeling technique that enables IT professionals
to design agile enterprise data warehouses. This approach enforces a layered structure
and has been developed specifically to combat issues with agility, flexibility,
and scalability that arise when using the other schema models.

Data vault eliminates star schema's need for cleansing and streamlines the addition
of new data sources without any disruption to existing schema.

---

## :material-playlist-plus: Read Mores

- [IBM: Data Mart](https://www.ibm.com/topics/data-mart)
