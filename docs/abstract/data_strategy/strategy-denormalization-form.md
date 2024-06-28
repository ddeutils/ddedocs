# De-Normalization

De-normalization is an optimization technique to make our database respond faster
to queries by reducing the number of joins needed to satisfy user needs.

- In de-normalization, we mainly aim to reduce the number of tables that are needed
  by re-joining these tables together and add redundant data.

- De-normalization is commonly used with read-intensive, low number of updates and
  high number of read queries, systems such as Data Warehouse (DWH).

!!! quote

    De-normalization is a strategy used on a previously-normalized database to
    increase performance. In computing, denormalization is the process of trying
    to improve the read performance of a database, at the expense of losing some
    write performance, by adding redundant copies of data or by grouping data.
    It is often motivated by performance or scalability in relational database
    software needing to carry out very large numbers of read operations.
    Denormalization should not be confused with Unnormalized form. Databases/tables
    must first be normalized to efficiently denormalize them.

    [By Wiki Denormalization](https://en.wikipedia.org/wiki/Denormalization)

!!! note

    De-normalization doesn't mean that we won't normalize our tables, It's like we
    said before, an optimization technique that used after normalizing our table
    to make it faster in some cases.

## De-Normalization Techniques

To de-normalize our normalized table, We will follow some methods that will be
discussed below.

Before doing de-normalization you have to make sure of two things:

- The performance of the normalized system doesn't satisfy the user.
- De-normalization is the right solution for this performance issue.

So briefly, De-normalization is used for:

- Reduce the number and need for joins.
- Reduce the number of needed tables.
- Reduce foreign keys of your database.

### Adding Redundant columns

We can apply it by adding commonly used columns in joins to the joined table for
reducing or eliminating join operations.

For example,

If we have a customers table and orders table, the orders table does have customer_id
only (as a foreign key) that referenced to customers table, but It doesn't have customer_name.
When we need to retrieve a list of all orders with the customer name, we will
have to join these tables together.

```sql
SELECT
    C.CUSTOMER_NAME,
    O.ORDER_NAME
FROM CUSTOMERS  AS C
JOIN ORDERS     AS O
    ON C.CUSTOMER_ID = O.CUSTOMER_ID
;
```

To de-normalize this table, we will add a redundant customer_name column to Orders,
Which will increase performance, and we won't need to join this table again.

```sql
SELECT
    O.CUSTOMER_NAME,
    O.ORDER_NAME
FROM ORDERS O
;
```

**Drawbacks of this method**:

- Maintenance will be costly, and increase update overhead, because updates will
  be made for two tables: customers(name) and orders(customer_name).
- More storage will be needed because customer_name is duplicated now.
- Increase in Table Size.
- In case of an update in one value of a customer, you have to update all the
  records of that customer in the fact table which will be a very costly operation
  for big Fact tables.

### Coming tables

We can apply it by combine tables that are joined together frequently into one
table, which will eliminate join, and increase performance significantly.

For example,

If we frequently need to generate a report that shows all Employees their full addresses,
we will have to join these tables together.

```postgres-sql
SELECT E.* , A.CITY+", "+A.STATE+", "+A.DISTRICT+", "+A.ZIP AS "FULL ADDRESS"
FROM EMPLOYEES E
JOIN ADDRESSES A
ON A.LOCATION_ID = e.LOCATION_ID;
```

So to de-normalize this situation, We will combine employees' table and addresses
table into one table, And combine address table attributes into one attribute
(Full address) to make querying easier, This solution will increase performance
significantly, and eliminate costly joins.

```postgres-sql
SELECT *
FROM EMPLOYEES;
```

### Adding Derived column

Adding derived columns to our table can help us to eliminate joins, and improve
the performance of aggregating our data.

> A **derived column** is attribute whose value is derived from another attribute.
> For example: Using date_of_birth attribute to generate age attribute.

For example,

If we need to generate a report containing Students and their grades, We will join
students table and grades table, and start comparing marks with grades to know
the grade of each student.

```postgres-sql
SELECT S.NAME, S.MARKS, G.GRADE
FROM STUDENTS S
JOIN GRADES G
ON S.MARKS BETWEEN G.MIN_MARK AND G.MAX_MARK;
```

So to de-normalize this situation, We will use marks in students' table and compare
them to predefined values to generate grades with no need of joining grades with students.

```postgres-sql
SELECT NAME, MARKS,
CASE
  WHEN MARKS >= 85 AND MARKS <= 100 THEN "A"
  WHEN MARKS >= 75 AND MARKS  < 85  THEN "B"
  WHEN MARKS >= 65 AND MARKS  < 75  THEN "C"
  WHEN MARKS >= 50 AND MARKS  < 65  THEN "D"
  ELSE "F"
END AS "GRADE"
FROM STUDENTS;
```

### Partitioning Relation

In this approach, We won't combine tables together, We will go for decomposing
them into multiple smaller manageable tables, It will decrease the size that we
have to read, which will impact the performance of operations in some meaningful way.

#### Horizontal partitioning

**Horizontal partitioning** or **Row Splitting**. Split our main table rows into
smaller partitions (tables) that will have the same columns.

This approach aims to make where clause more efficient by making it search in a
smaller amount of data, Filter specify only a subset of the table that related to
the query, not the whole table, and reduced I/O overhead.

#### Vertical partitioning

**Vertical partitioning** or **Column Splitting**. In Vertical partitioning, We
distribute table attributes across multiple partitions with primary key duplicated
for each partition to make reconstructing of original table easier. We partition
our table based on frequently used attributes and rarely used attributes.

We need to use this approach When some columns are frequently accessed more than
other columns, To reduce table header size, And retrieve only the required attributes.

!!! warning

    In case you have multiple requirements that needs the data combined you will
    have to join the tables again which will cause performance problems.

### Materialized Views

**Materialized Views** can improve performance and decrease time-consuming significantly,
by using it to precomputing and store the result of costly queries like join and
aggregation as **view** in your storage disk for future usage.

Materialized View is all about run one time, and read many times.

When you need to use a query frequently, you can store it as materialized view,
So in the future, you can retrieve the result of your query directly from the view
stored in your disk, So you don't need to recompute query again.

But you should to know that,

- Data will be updated once, And to refresh you have to re-run the query again.
- The unavailable source will block maintenance of view.
- Data are replicated, And it needs more storage.

## Drawbacks of De-Normalization

- De-normalization can slow updates, with many update overheads.
- De-normalization can increase your table and database size.
- De-normalization in some cases can make querying more complex instead of making it easier.
- More storage will be needed for duplicated data.

## De-Normalization and Data Warehouses

De-normalization is stable and commonly used with data warehouses, Data warehouse
is a Specially created data repository for decision-making, It involves a large
historical data repository related to the organization, The typical data warehouse
is a subject-oriented corporate database that involves multiple data models
implemented on multiple platforms and architectures.

There are some aspects to consider when building data warehouses:

- Extraction of data from several sources that may be homogeneous or heterogeneous.

- Initialize data for compatibility in the data warehouse.

- Cleaning the data with validity, and is done through the database from which the data were taken.

- Monitor and control the data warehouse while it is uploading data.

- Update data every period of time.

De-normalization can increase the speed of retrieval and optimize query performance
for data warehouses, with some drawbacks of update anomalies, but it won't be a big
problem because data warehouse is not typically used for update, It's commonly used
for reading operations, which are used for analysis and decision-making as we said,
hence, a data warehouse is a great source for applying de-normalization, because
it attributes rarely updated.

### Use Case: Star Schema

**Dimensional Model**: It is a special model that is an alternative to an
entity-relationship (ER) model consisting of the ER information and itself, but
combines the data in an abbreviated form that makes the model more understandable
to perform the queries efficiently, and has the flexibility to change (Dimensional
model is the modeling approach of data warehouses).

**Star schema** is the simplest and easiest dimensional model for data warehouses,
because of that it's the most suitable schema for query processing, and it's highly
de-normalized, but its drawback is its need for a large space to store data.

Star schema consists of a fact table with a single table for each dimension.

- A fact table in a pure star schema consists of multiple foreign keys, each paired
  with a primary key in a dimension, together with the facts containing the measurements.
  - Typically, **normalized**.
- Dimension tables not joined for each other.
  - It joined using a fact table that does have a foreign key for each dimension.
  - Typically, heavily **de-normalized**.

## Summary

De-normalization aims to add redundancy to your database for better performance,
It also a great optimization technique that will help you to decrease query processing time.
with drawbacks of reducing the integrity of your system, slowing data manipulation operations,
and need more space for storing redundant data.

## References

- [DataValley: De-normalization When, Why, and How](https://datavalley.technology/denormalization-when-why-and-how/)
