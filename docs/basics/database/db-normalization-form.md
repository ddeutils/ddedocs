# Database Normalization

**Normalization** is a database design technique that reduces data redundancy and
eliminates undesirable characteristics like Insertion, Update and Deletion Anomalies.
Normalization rules divides larger tables into smaller tables and links them using
relationships. The purpose of Normalization in SQL is to eliminate redundant
(repetitive) data and ensure data is stored logically.

However, in most practical applications, normalization achieves its best in
**3rd Normal Form** (3NF).

!!! quote

    Database normalization is the process of restructuring a relational database
    in accordance with a series of so-called normal forms in order to reduce data
    redundancy and improve data integrity. It was first proposed by Edgar F. Codd
    as an integral part of his relational model.

    Normalization entails organizing the columns (attributes) and tables (relations)
    of a database to ensure that their dependencies are properly enforced by database
    integrity constraints. It is accomplished by applying some formal rules either
    by a process of synthesis (creating a new database design) or decomposition
    (improving an existing database design).

    [By Wiki Database Normalization](https://en.wikipedia.org/wiki/Database_normalization)

!!! abstract

    **primary key**

    :   A single column that uniquely identifies the records of data in that
        table. It’s a unique identifier such as an employee ID, student ID,
        voter’s identification number (VIN), and so on.

    **foreign key**

    :   A field that relates to the primary key in another table. Unlike the primary
        key, they do not have to be unique. most often they are not. foreign keys
        can be null even though primary keys can not.

    **composite key**

    :   A **primary key** composed of multiple columns used to identify a record
        uniquely.

    **candidate key**

    :   A field that able to be primary key.

!!! abstract

    **prime attribute**

    :   Attributes can be used to uniquely identify a tuple in the table because
        they have unique values. they also known as **Key Attributes**.

    **non-prime attribute**

    :   Attributes of the relation which does not exist in any of the possible
        candidate keys of the relation. They also known as **Non-Key Attributes**.

    !!! example

        ```text
        R = (H, I, J, K, L, M, N, O)

        F = {
          L -> MNO
          HI -> JKLMNO
          J -> KL
          K -> H
        }
        ```

        This schema has three (candidate) keys:

        ```text
        HI
        IJ
        IK
        ```

        While it is immediate to discover tha HI is a candidate key since it determines
        all the other attributes, you can see that this is true also for IJ and IK by
        calculating the closure of those attributes:

        ```text
        IJ+ = IJ
        IJ+ = IJKL     (by adding the right part of J → KL)
        IJ+ = IJKLH    (by adding the rigth part of K → H)
        IJ+ = IJKLHMNO (by adding the right part of L → MNO)
        ```

        Note that it use the notation IJ+. This is called the closure, which means
        all the possible attributes that can be inferred from what we know in LHS.

        analogously for IK:

        ```text
        IK+ = IK
        IK+ = IKH      (by adding the rigth part of K → H)
        IK+ = IKHJLMNO (by adding the right part of HI → JKLMNO)
        ```

        For this reason, the prime attributes of the relation are:

        ```text
        HIJK
        ```

        while the non prime attributes are:

        ```text
        LMNO
        ```

        Note that there are no other candidate keys since M, N and O appear only
        on the right side of functional dependencies, so that they cannot “contribute”
        to any key. L appears both on a left part and on a right part of functional
        dependencies, but it is determined by HI, IJ and IK, and does not determine
        any of these attributes, so it cannot be part of a key. Finally, you cannot
        remove any attribute from HI, IJ and IK without losing the key property.

        [Read more this example](https://dba.stackexchange.com/questions/127298/what-are-the-prime-and-non-prime-attributes-in-this-relation)

## What is Anomalies?

Anomalies are the problems that occur in the update, delete and insert operations
in poorly designed or un-normalized data when all data stored in one table (Flat file).

In simple words we can say anomaly is when you have one table which has multiple
related information, and you cannot do any kind of operation on single information.

**Example of Anomalies**:

```text
R = (courseNo,  tutor,  lab, labSize){
    (300,       Ahmed,  C3,  150),
    (301,       John,   A1,  210),
    (302,       Kamal,  C3,  150)
}
```

### Insert anomaly

What if we built a new lab (e.g. `lab: A4`), but it’s not assigned to any courses
or tutors yet, so we won’t be able to insert it to our table because (`lab`) comes
with (`course`) and (`tutor`) because it does not have separated table.

### Delete anomaly

What if we need to delete (`courseNo: 300`) that means we will delete the details
of (`lab: C3`) also and that’s not what we want.

### Update anomaly

What if we improved (`lab: C3`) and now it (`labSize: 250`), to update it we will
have to update all other columns where (`lab: C3`).

## Dependency Rules

Rule for call the attribute relationships

### Functional Dependency

This is the primary key (single or composite) relationship for identified other
attributes. When we say A is identified by B (B is a primary key), then A
functionally dependent on B, can be represented graphically as (B -> A)

#### Complete/Fully Functional Dependency

!!! example

    ```text
    R = (customerID, name, salary){
        (1,          Tom,  18,000),
        (2,          June, 22,000),
        (3,          Rose, 15,000)
    }
    ```

    `customerID -> {name, salary}` is Fully Functional Dependency (FFD).

    - `name` and `salary` were identified by `customerID` and functionally dependent on it.
    - `customerID` determines `name` and `salary`.

#### Partial Dependency

When only one of the prime attributes determines another attribute with no exist
of other prime attributes in this relation. OR when not all non-prime attributes
depend on all prime attributes.

!!! example

    {A, B} are our prime attributes, C is non-prime attribute and A -> Z not {A, B} -> C,
    so it's partial dependency because C is functionally dependent on only one prime
    attribute not all prime attributes.

    ```text
    R = (order, product, productName, quantity){
        (1,     A,       table,       1),
        (1,     B,       chair,       4),
        (2,     A,       table,       2)
    }
    ```

    `{order, product} -> {productName, quantity}` is Fully Functional Dependency (FFD)
    because of using for all key.

    `product -> productName` is being Partial Dependency because use one key from
    prime attributes.

#### Transitive Dependency

There is non-prime attribute functionally dependent on another non-prime attribute
OR It means that changing a value in one column leads to a change in another
column-columns other than prime attributes.

A transitive functional dependency is when changing a non-key column, might
cause any of the other non-key columns to change

!!! note

    In transitive dependency non-prime attribute determines another non-prime attribute,
    In partial dependency when only one of the prime attributes determines another
    attribute with no exist of other prime attributes
    (because of that we called it partial dependency).

!!! example

    We say that A -> C is transitive dependency if it generated from A -> B & B -> C
    not A -> C directly.

#### Multivalued Dependency

It usually a relationship consisting of 3 attributes (A, B, C). single value
from (A) gives more than one value in (B), single value of (A) gives more than
one value in (C), and (B) , (C) are independent of each other.

* There are at least 3 attributes A, B, C in a relation and
* For each value of A there is a well-defined set of values
  for B, and a well-defined set of values for C,
* But the set of values for B is independent on the set of
  values for C

!!! example

    (emp_no , proj_no, dependents)

    (employee) do have many (projects), (employee) do have many ( dependents ) like
    his children, and it’s obviously projects and his dependents are independent of each other,
    which means if we need to remove one of his projects we don't have to delete one
    of his dependent. so we have here multivalued dependency which violates 4NF.

### Join Dependency

Whenever we can recreate a table by simply joining various tables where each of
these tables consists of a subset of the table’s attribute, then this table is
known as a **Join Dependency**.

## Normalization Order

The normalization process takes our relational schema throw a series or pipeline
of tests to make sure that’s it satisfy a certain normal form, this process
proceeds in a top-down manner by evaluating our relational schema against the
criteria of normal forms.

### 1NF: First Normal Form

**First Normal Form** (1NF) is the first step towards a full normalization of your
data, to apply 1NF it should have the following criteria:

* Each column or single cell contains atomic values

* Each entity has a **primary key**

* No duplicated rows or columns

In other words, each row in the table should have a unique identifier, and each
value in the table should be indivisible.

!!! example

    ```text
    R = (customerID, Address){
        (1,          Main street, First Town, BKK 10100),
        (2,          12 street, A Town, BKK 10120)
    }
    ```

    ```text
    R = (customerID, street,      town,       city, zipCode){
        (1,          Main street, First Town, BKK,  10100),
        (2,          12 street,   A Town,     BKK,  10120)
    }
    ```

### 2NF: Second Normal Form

**Second Normal Form** (2NF) do more than the 1NF because 1NF only eliminates
repeating groups, not redundancy.

* It should be in 1NF.

* It should not have **partial dependencies**. Each non-prime attribute is full
  functionally dependent on the whole primary key (all prime attributes).

!!! example

    ```text
    R = (studentID, studentName, subjectID, grade, prize){
        (1,         Tom,         S01,       A,     Voucher),
        (2,         Sara,        S01,       B+,    Nothing),
        (3,         John,        S02,       A,     Voucher)
    }
    ```

    ```text
    R = (studentID, subjectID, grade, prize){
        (1,         S01,       A,     Voucher),
        (2,         S01,       B+,    Nothing),
        (3,         S02,       A,     Voucher)
    }

    RS = (studentID, studentName){
         (1,         Tom),
         (2,         Sara),
         (3,         John)
    }
    ```

### 3NF: Third Normal Form

**Third Normal Form** (3NF)

* It should be in 2NF.

* It should not have **transitive dependencies**.

!!! example

    ```text
    R = (studentID, subjectID, grade, prize){
        (1,         S01,       A,     Voucher),
        (2,         S01,       B+,    Nothing),
        (3,         S02,       A,     Voucher)
    }
    ```

    ```text
    R = (studentID, subjectID, grade){
        (1,         S01,       A),
        (2,         S01,       B+),
        (3,         S02,       A)
    }

    RP = (grade, prize){
         (A,     Voucher),
         (B+,    Nothing),
    }
    ```

### BCNF: Boyce-Codd Normal Form

**Boyce-Codd Normal Form** (BCNF) will remove all candidate key.

* It should be in 3NF.

* Any attribute in table depends only on super-key.
  A -> Z means (A) is super-key of (Z) (even (Z) is a prime attribute)

!!! note

    * If our table contains only one prime key, 3NF and BCNF are equivalent.
    * BCNF is a special case of 3NF, and it also called 3.5NF.

!!! example

    ```text
    R = (student, subject, professor){
        (A,       Math,    P.Tom),
        (A,       Science, P.Sara),
        (B,       Math,    P.Kan),
    }
    ```

    * `{student, subject} -> professor`, so `student` and `subject` are super-key.
    * `professor -> subject`, but subject is prime attribute and professor is not
      super-key.

    ```text
    RS = (student, professorID){
         (A,       1),
         (A,       2),
         (B,       3),
    }

    RP = (professorID, professor, subject){
         (1,           P.Tom,     Math),
         (2,           P.Sara,    Science),
         (3,           P.Kan,     Math),
    }
    ```

### 4NF: Fourth Normal Form

**Fourth Normal Form** (4NF)

* It should be in BCNF.

* It should not have multivalued dependencies.

If no database table instance contains two or more, independent and multivalued
data describing the relevant entity, then it is in 4th Normal Form.

!!! example

    ```text
    R = (projectID, businessUnit, Location){
        (A01,       BU01,         North),
        (A01,       BU01,         South),
        (A01,       BU02,         North),
        (A01,       BU02,         South),
    }
    ```

    ```text
    R1 = (projectID, businessUnit){
         (A01,       BU01),
         (A01,       BU02)
    }

    R2 = (projectID, Location){
         (A01,       North),
         (A01,       South)
    }
    ```

### 5NF: Fifth Normal Form

**Fifth Normal Form** (5NF) is also known as Project-Join Normal Form (PJNF). It
is used to handle complex many-to-many relationships in a database.

- It should not have join dependency, it cannot be decomposed into any number of
  smaller tables without loss of data.

In a many-to-many relationship, where each table has a composite primary key, it
is possible for a non-trivial functional dependency to exist between the primary
key and a non-key attribute. 5NF deals with these situations by decomposing the
tables into smaller tables that preserve the relationships between the attributes.

!!! example

    ```text
    R = (year,   subjectID, buildingID){
        (1/2560, EE400,     A012),
        (1/2560, EE402,     B012),
        (2/2560, EE400,     B012),
        (1/2560, EE400,     B012)
    }
    ```

    ```text
    R1 = (year,   subjectID){
         (1/2560, EE400),
         (1/2560, EE402),
         (2/2560, EE400)
    }

    R2 = (subjectID, buildingID){
         (EE400,     A012),
         (EE400,     B012),
         (EE402,     B012),
    }

    R3 = (year,   buildingID){
         (1/2560, A012),
         (1/2560, B012),
         (2/2560, B012)
    }
    ```

    ```text
    R != R1 join R2 join R3
    ```

### 6NF: Sixth Normal Form

**Sixth Normal Form** (6NF) (Proposed)

- The row contains the primary key, and at most one other attribute

!!! warning

    The obvious drawback of 6NF is the proliferation of tables required to represent
    the information on a single entity. If a table in 5NF has one primary key column
    and N attributes, representing the same information in 6NF will require N tables;
    multi-field updates to a single conceptual record will require updates to multiple
    tables; and inserts and deletes will similarly require operations across multiple
    tables.

## Why do we need to normalize our tables?

* When (ACID compliant) is required

    It improves integrity and consistency of your data.
    (ACID = Atomicity Consistency Isolation Durability)

* Fewer storage needed

    Since we eliminated repeated groups, and divided our tables, we reduced the
    size of our tables and database.

* less logical I/O cost

  When you need to retrieve data, you will retrieve smaller amount of data, and
  when you need to add or insert in tables, it will be easier, and more organized.

* Queries become easier

  If we have un-normalized table that has (location) attribute {City, Zip} as
  composite attribute, and we need to count the unique zip codes in our table,
  so we will access first location, then we will try to get zip, after normalize
  this table we will be able to access zip directly because location will be
  divided to two attributes (city) and (zip).

* Write-intensive databases

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

The drawbacks of data redundancy include:

* Data maintenance becomes tedious – data deletion and data updates become problematic
* It creates data inconsistencies
* Insert, Update and Delete anomalies become frequent. An update anomaly, for example, means that the versions of the same record, duplicated in different places in the database, will all need to be updated to keep the record consistent
* Redundant data inflates the size of a database and takes up an inordinate amount of space on disk

## References

- https://en.wikipedia.org/wiki/Third_normal_form/
- https://en.wikipedia.org/wiki/Database_normalization/
- [database normalization](https://en.wikipedia.org/wiki/Database_normalization)
- [table normalization](https://medium.com/@miwtoo/%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B8%97%E0%B8%B3-normalization-%E0%B9%80%E0%B8%9E%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%9B%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%9B%E0%B8%A3%E0%B8%B8%E0%B8%87-schema-d0324b6c9556)
- https://datavalley.technology/normalization-in-depth/
- https://medium.com/swlh/a-complete-database-normalization-tutorial-732df3748d0e
