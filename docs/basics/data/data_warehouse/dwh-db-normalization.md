# Normalization

**Normalization** is a database design technique that reduces data redundancy and
eliminates undesirable characteristics like Insertion, Update and Deletion Anomalies.
Normalization rules divides larger tables into smaller tables and links them using
relationships. The purpose of Normalization in SQL is to eliminate redundant (repetitive)
data and ensure data is stored logically.

However, in most practical applications, normalization achieves its best in
**3rd Normal Form**.

Normalization using its primary keys and Foreign Keys to achieve the following:

- Reduce redundant groups and make redundancy few as possible.
- Make Data modification more efficient with no problems or errors (anomalies).

**Table of Contents**:

- [What is Anomalies?](#what-is-anomalies)
- [Dependency Rules](#dependency-rules)
- [Normalization Order](#normalization-order)
- [Why do we need to normalize our tables?](#why-do-we-need-to-normalize-our-tables)

## What is Anomalies?

Anomalies are the problems that occur in the update, delete and insert operations
in poorly designed or un-normalized data when all data stored in one table (Flat file).

Example of Anomalies:

| courseNo | Tutor | Lab | lab_size |
|----------|-------|-----|----------|
| 300      | Ahmed | C3  | 150      |
| 301      | John  | A1  | 210      |
| 302      | Kamal | C3  | 150      |

- **insert anomaly**: \
  What if we built a new lab(e.g. lab A4), but it’s not assigned to any courses or
  Tutors yet, so we won’t be able to insert it to our table because (lab) comes
  with (course) and (Tutor) because it doesn’t have separated table.

- **Delete anomaly**: \
  What if we need to delete (courseNo:300) that means we will delete the details
  of (lab:C3) also and that’s not what we want.

- **Update anomaly**: \
  What if we improved (Lab:C3) and now it (size:250), to update it we will have
  to update all other columns where (Lab:C3)

> **Note**: \
> In Simple words we can say anomaly is when you have one table which has multiple
> related information, and you cannot do any kind of operation on single information.

## Dependency Rules

Rule for call the attribute relationships

- **Functional Dependency**: \
  This is the primary key relationship for identified other attributes. When we say
  A is identified by B (B is a primary key), then A functionally dependent on B,
  can be represented graphically as (B -> A)

  For example,

  `(customerID) —> {name, salary}`

  - `name` and `salary` were identified by `customerID` and functionally dependent on it.
  - `customerID` determines `name` and `salary`.

- **Partial Dependency**: \
  When only one of the prime attributes determines another attribute with no exist
  of other prime attributes in this relation. OR when not all non-prime attributes
  depend on all prime attributes.

  For example,

  {A, B} are our prime attributes, C is non-prime attribute and A -> Z not {A, B} -> C,
  so it's partial dependency because C is functionally dependent on only one prime
  attribute not all prime attributes.

| Order | Product | P_Name | Qty |
|-------|---------|--------|-----|
| 1     | A       | AAA    | 100 |
| 1     | B       | BBB    | 200 |
| 1     | C       | CCC    | 300 |
| 2     | A       | AAA    | 300 |
| 2     | C       | CCC    | 400 |
| 3     | D       | DDD    | 100 |

   {`Order`, `Product`} -> `P_Name`, `Qty` is Functional Dependency, Full Functional Dependency (FFD)
   because of using for all key.

   `Product` -> `P_Name` is being Partial Dependency because use one key.

- **Transitive Dependency**: \
  There's non-prime attribute functionally dependent on another non-prime attribute
  OR It means that changing a value in one column leads to a change in another column
  -columns other than prime attributes.

  A transitive functional dependency is when changing a non-key column, might
  cause any of the other non-key columns to change

  > **Note**: \
  > In transitive dependency non-prime attribute determines another non-prime attribute,
  > In partial dependency when only one of the prime attributes determines another
  > attribute with no exist of other prime attributes
  > (because of that we called it partial dependency).

  For example,

  We say that A -> C is transitive dependency if it generated from A -> B & B -> C not A -> C directly.

| Member ID | Name   | Salutation |
|-----------|--------|------------|
| 1         | Sara   | Ms.        |
| 2         | Tome   | Mr.        |
| 3         | Robert | Mr.        |

  Changing the non-key column `Name` may change `Salutation`

- **Multivalued Dependency**: \
  It usually a relationship consisting of 3 attributes (A, B, C). single value
  from (A) gives more than one value in (B), single value of (A) gives more than
  one value in (C), and (B) , (C) are independent of each other.

  For example,

  (emp_no , proj_no, dependents)

  (employee) do have many (projects), (employee) do have many ( dependents ) like
  his children, and it’s obviously projects and his dependents are independent of each other,
  which means if we need to remove one of his projects we don't have to delete one
  of his dependent. so we have here multivalued dependency which violates 4NF.

- **Join Dependency**:

  การเชื่อมแอททริบิวต์ที่เหมือนกัน ระหว่างรีเรชั่นที่ต่างกัน

- **Candidate Key**:

  แอททริบิวต์ที่ มีความสามารถที่จะเป็น Primary key ได้

## Normalization Order

The normalization process takes our relational schema throw a series or pipeline
of tests to make sure that’s it satisfy a certain normal form, this process
proceeds in a top-down manner by evaluating our relational schema against the
criteria of normal forms.

### First Normal Form

**First Normal Form** (1NF) is the first step towards a full normalization of your data,
to apply 1NF you should not have the following in your data:

- Multi-valued attributes\
  Multi-valued attributes is when you have attribute that has a set of multiple
  values for a specific entity.
  For example, phone number, employee can have 2 or more phone numbers.

- Nested relations

- Composite attributes

| Employee | Location       |
|----------|----------------|
| 200      | New York,11782 |

| Employee | City     | Zip   |
|----------|----------|-------|
| 200      | New York | 11782 |

Finally, the attribute must include only atomic values (each cell is single-valued;
there are not repeating groups or arrays), let’s now check each type of attributes
to understand how to handle it.

- Each table cell should contain a single value.
- Each record needs to be unique.

> **Primary Key**: A primary is a single column value used to identify a database
> record uniquely.

> **Composite Key**: A composite key is a primary key composed of multiple columns
> used to identify a record uniquely.

### Second Normal Form

**Second Normal Form** (2NF)

- It should be in 1NF.

- It should not have partial dependencies. Each non-prime attribute is full functionally
  dependent on the whole primary key (all prime attributes).

> **Prime attribute**: member of the primary key OR one of attributes that is
> considered as primary key of table and uniquely identify rows.
> if we have composite key, then we have more than one prime attribute.

- Single Column Primary Key that does not functionally dependent on any subset
  of candidate key relation

> **Foreign Key**: Foreign Key references the primary key of another Table! It helps connect your Tables,
>  - A foreign key can have a different name from its primary key
>  - It ensures rows in one table have corresponding rows in another
>  - Unlike the Primary key, they do not have to be unique. Most often they aren’t
>  - Foreign keys can be null even though primary keys can not

### Third Normal Form

**Third Normal Form** (3NF)

- It should be in 2NF.
- It should not have transitive functional dependencies.

### Boyce-Codd Normal Form

**Boyce-Codd Normal Form** (BCNF)
เป็นขั้นตอนที่ใช้กำจัด Candidate Key (Boyce-Codd normal form)

- It should be in 3NF.
- Any attribute in table depends only on super-Key.\
  A -> Z means (A) is super-key of (Z) (even (Z) is a prime attribute)

> **Warning**: \
> Prime attributes are super keys, the opposite isn’t true.

> **Note**:
> - If our table contains only one prime key, 3NF and BCNF are equivalent.
> - BCNF is a special case of 3NF, and it also called 3.5NF.

### Fourth Normal Form

**Fourth Normal Form** (4NF)

- It should be in BCNF.
- It should not have multivalued dependencies.

If no database table instance contains two or more, independent and multivalued
data describing the relevant entity, then it is in 4th Normal Form.

### Fifth Normal Form

**Fifth Normal Form** (5NF) \
จะเป็นการ Join Dependency แล้ว ได้ตารางที่เหมือนเดิม

- It cannot be decomposed into any number of smaller tables without loss of data.

### Sixth Normal Form

**Sixth Normal Form** (6NF) (Proposed)

- The row contains the Primary Key, and at most one other attribute

## Why do we need to normalize our tables?

- When (ACID compliant) is required \
  It improves integrity and consistency of your data.
  (ACID = Atomicity Consistency Isolation Durability)

- Fewer storage needed \
  Since we eliminated repeated groups, and divided our tables, we reduced the
  size of our tables and database.

- less logical I/O cost \
  When you need to retrieve data, you will retrieve smaller amount of data, and
  when you need to add or insert in tables, it will be easier, and more organized.

- Queries become easier \
  If we have un-normalized table that has (location) attribute {City, Zip} as
  composite attribute, and we need to count the unique zip codes in our table,
  so we will access first location, then we will try to get zip, after normalize
  this table we will be able to access zip directly because location will be
  divided to two attributes (city) and (zip).

- Write-intensive databases \
  Normalization increases the performance of write-intensive databases Significantly,
  because it reduces data modification anomalies, which make it easier to manipulate
  your database.

## Drawbacks of Normalization

When we need to work with **read-intensive** databases, you may need to **join** data
from multiple tables, and work with a huge amount of data.
In **normalized databases**, you will need many **join** operations to combine data from
multiple tables to satisfy user needs, which will **increase time-consuming**, and
make it difficult to work with **a huge amount of data**, so if you need to work with
the **read-intensive** database it's obviously normalization won't be your **optimal
solution**.

## References

- https://en.wikipedia.org/wiki/Third_normal_form/
- https://en.wikipedia.org/wiki/Database_normalization/
- [database normalization](https://en.wikipedia.org/wiki/Database_normalization)
- [table normalization](https://medium.com/@miwtoo/%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%97%E0%B8%B3-normalization-%E0%B9%80%E0%B8%9E%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%9B%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%9B%E0%B8%A3%E0%B8%B8%E0%B8%87-schema-d0324b6c9556)
- https://datavalley.technology/normalization-in-depth/
