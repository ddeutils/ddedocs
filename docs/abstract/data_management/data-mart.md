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

A data mart (as noted above) is a focused version of a data warehouse that contains
a smaller subset of data important to and needed by a single team or a select
group of users within an organization.
A data mart is built from an existing data warehouse (or other data sources)
through a complex procedure that involves multiple technologies and tools to
design and construct a physical database, populate it with data, and set up
intricate access and management protocols.

## Types

There are three types of data marts that differ based on their relationship to
the data warehouse and the respective data sources of each system.

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

## :material-playlist-plus: Read Mores

- [:simple-ibm: IBM: Data Mart](https://www.ibm.com/topics/data-mart)
