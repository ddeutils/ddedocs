# Data Warehouse: _Ralph Kimball Approach_

https://towardsdatascience.com/data-modeling-for-mere-mortals-part-2-dimensional-modeling-fundamentals-ae2f53622321

The Kimball methodology, also known as dimensional modeling, is a bottom-up approach
that focuses on designing the data warehouse around the business process or subject
area.

It uses a star schema or snowflake schema to model the data and focuses on creating
dimension and fact tables to support analysis. The Kimball methodology is known for
its simplicity, flexibility, and ease of use.

In contrast, dimensional models or Kimball dimensional data models, data models
based on the technique developed by _Ralph Kimball_, are denormalized structures designed
to retrieve data from a data warehouse. They are optimized to perform the Select
operation and are used in the basic design framework to build highly optimized
and functional data warehouses.

- Kimball’s model follows a bottom-up approach. The Data Warehouse (DW) is provisioned
  from Datamarts (DM) as and when they are available or required.

- The Datamarts are sourced from OLTP systems are usually relational databases in
  Third normal form (3NF).

- The Data Warehouse which is central to the model is a de-normalized star schema.
  The OLAP cubes are built on this DWH.

I will say that this is the latest model that serve to Data Science or Data Analytic
for using to cube analysis process.

In contrast, dimensional models or Kimball dimensional data models, data models
based on the technique developed by _Ralph Kimball_, are denormalized structures designed
to retrieve data from a data warehouse. They are optimized to perform the Select
operation and are used in the basic design framework to build highly optimized
and functional data warehouses.

The Kimball approach is called bottom-up because we start with user-specific data marts,
which are the core building blocks of our conceptual data warehouse. It's critical
to know which model best meets your needs from the start; so that it can be
incorporated into the data warehouse structure.

- Begin by identifying and documenting the most significant business operations,
  demands, and queries that are being asked.
- All data sources available across the organisation should be documented.
- Create ETL pipelines that gather, modify, and load data into a de-normalised
  data model from data sources. The dimensional model is constructed in the form
  of either a star schema or a snowflake schema.
- The dimensional model has frequently constructed around and within dimensional
  data marts for specific departments.

## What is Data Dimensional Modelling?

**Data Dimension Model** (DDM) : is a technique that uses Dimensions and Facts to
store the data in a Data Warehouse efficiently. The purpose is to optimize the database
for faster retrieval of the data. Dimensional Models have a specific structure and organise
the data to generate reports that improve performance.

A dimensional model in data warehouse is designed to read, summarize, analyze numeric information
like values, balances, counts, weights, etc. in a data warehouse. In contrast,
relation models are optimized for addition, updating and deletion of data in
a real-time Online Transaction System.

The concept of Dimensional Modelling was developed by _Ralph Kimball_ and consists
of "fact" and "dimension" tables.

This article will introduce the concepts and features of Dimensional Data Modelling,
the components that make up a Dimensional Data Model, the types & steps of Dimensional Data Modelling
and also the benefits and limitations of Dimensional Data Modelling.

**Key Features of Dimensional Data Modelling**:

Data Dimensional Modelling has gained popularity because of its unique way of analysing
data present in different Data Warehouses. The 3 main features of DDM are as follows:

- **Easy to Understand**: \
  DDM helps developers create and design databases and Schemas easily interpreted
  by business users. The relationship between Dimensions and Facts are pretty simple
  to read and understand.

- **Promote Data Quality**: \
  DDM schemas enforce data quality before loading into Facts and Dimensions.
  Dimension and Fact are tied up by foreign keys that act as a constraint for
  referential integrity check to prevent fraudulent data from being loaded onto Schemas.

- **Optimise Performance**: \
  DDM breaks the data into Dimensions and Facts and links them with foreign keys,
  thereby reducing the data redundancy. The data is stored in the optimised form
  and hence occupies less storage and can be retrieved faster.

Hence, Dimensional models are used in [data warehouse](https://www.guru99.com/data-warehousing.html)
systems and not a good fit for relational systems.

## Components of Dimensional Data Modelling

There are 5 main components of any DDM.

1. **Dimension** \
   Dimensions are the assortment of information that contain data around one or
   more business measurements. It may be topographical information, item data,
   contacts, and so on. In simple terms, they give who, what, where, and the context
   to the fact creation. \
   In other words, a dimension is a window to view information in the facts.

2. **Facts/Measures** \
   Facts are the collection of measurements, metrics, transactions, etc.,
   from different business processes and are almost always numeric.
   It typically contains business transactions and measure values.
   A single fact table row has a one-to-one relationship to a
   measurement event as described by the fact table’s grain. Thus, a fact table
   corresponds to a physical observable event, and not to the demands of a particular report.

   Within a fact table, only facts consistent with the declared grain are allowed.
   For example, in a retail sales transaction, the quantity of a product sold and
   its extended price are good facts, whereas the store manager’s salary is disallowed.

3. **Attributes** \
   Attributes are the elements of the Dimension Table. For example, in an account Dimension,
   the attributes can be:

   - First Name
   - Last Name
   - Phone, etc.

   Attributes are used to search, filter, or classify facts.
   Dimension Tables contain Attributes

4. **Fact Tables** \
   Fact tables are utilized to store measures or transactions in the business.
   The Fact Tables are related to Dimension Tables with the keys known as foreign keys. \
   For example, in Internet business, a Fact can store the requested amount of items.
   Fact Tables, as a rule, have huge rows and fewer columns.

   > **Note**: \
   > All fact tables have foreign keys that refers to the dimension tables primary keys
   > to easily connect them to produce specific measure.

5. **Dimension Tables** \
   Dimension Tables store the Dimensions from the business and establish the context
   for the Facts (They are joined to fact table via a foreign key).
   They contain descriptive data that is linked to the Fact Table.
   Dimension Tables are usually optimized tables and hence contain large columns
   and fewer rows.

   For example:

   - Contact information can be viewed by name, address and phone dimension.
   - Product information can be viewed by product-code, brand, color, etc.
   - City, state, etc. can view store information.

   > **Note**: \
   > No set limit set for given for number of dimensions \
   > The dimension can also contain one or more hierarchical relationships

## Types of Dimensions in Dimensional Data Modelling

There are 9 types of Dimensions/metrics when dealing with Dimensional Data Modelling.

1. **Conformed Dimension** \
   A Conformed Dimension is a type of Dimension that has the same meaning to all
   the Facts it relates to. This type of Dimension allows both Dimensions and
   Facts to be categorised across the Data Warehouse.

2. **Outrigger Dimension** \
   An Outrigger Dimension is a type of Dimension that represents a connection between
   different Dimension Tables.

3. **Shrunken Dimension** \
   A Shrunken Dimension is a perfect subset of a more general data entity.
   In this Dimension, the attributes that are common to both the subset and the
   general set are represented in the same manner.

4. **Role-Playing Dimension** \
   A Role-Playing Dimension is a type of table that has multiple valid relationships
   between itself and various other tables. Common examples of Role-Playing Dimensions
   are time and customers. They can be utilised in areas where certain Facts do not
   share the same concepts.

5. **Dimension to Dimension Table** \
   This type of table is a table in the Star Schema of a Data Warehouse. In a Star Schema,
   one Fact Table is surrounded by multiple Dimension Tables. Each Dimension corresponds
   to a single Dimension Table.

6. **Junk Dimension** \
   A Junk Dimension is a type of Dimension that is used to combine 2 or more related
   low cardinality Facts into one Dimension. They are also used to reduce
   the Dimensions of Dimension Tables and the columns from Fact Tables.

7. **Degenerate Dimension** \
   A Degenerate Dimension is also known as a Fact Dimension. They are standard
   Dimensions that are built from the attribute columns of Fact Tables.
   Sometimes data are stored in Fact Tables to avoid duplication.

8. **Swappable Dimension** \
   A Swappable Dimension is a type of Dimension that has multiple similar versions
   of itself which can get swapped at query time. The structure of this Dimension
   is also different, and it has fewer data when compared to the original Dimension.
   The input and output are also different for this Dimension.

9. **Step Dimension** \
   This is a type of Dimension that explains where a particular step fits into the process.
   Each step is assigned a step number and how many steps are required by that
   step to complete the process.

To explore about the types of Dimensions in detail, click this
[**link**](https://www.javatpoint.com/types-of-dimensions).

## Types of Dimension Tables

## Steps to Carry Out Dimensional Data Modelling

Dimensional Data Modelling requires certain analysis on the data to understand
data behaviour and domain. The main goal a Dimensional Data Model tries to address
is that it tries to describe the Why, How, When, What, Who, Where of the business
process in detail.

```text
Select the business process (WHY)
|
|---> Declare the Grain (HOW MUCH)
      |
      |---> Identify the Dimension (3WS)
            |
            |---> Identity (WHAT)
                  |
                  |---> Build the Schema
```

The major steps to start Dimensional Data Modelling are:

1. **Identify the Business Process** \
   A Business Process is a very important aspect when dealing with Dimensional Data Modelling.
   The business process helps to identify what sort of Dimension and Facts are needed
   and maintain the quality of data.

   To describe business processes, you can use
   **Business Process Modelling Notation** (BPMN) or
   **[Unified Modelling Language](https://www.guru99.com/uml-tutorial.html)** (UML).

2. **Identify Grain** \
   Identification of Grain is the process of identifying how much normalisation
   (the lowest level of information) can be achieved within the data for any
   table in your data warehouse.

   It is the stage to decide the incoming frequency of data (i.e.daily, weekly, monthly, yearly),
   how much data we want to store in the database (one day, one month, one year, ten years),
   and how much the storage will cost.

   During this stage, you answer questions like

   - Do we need to store all the available products or just a few types of products? \
     This decision is based on the business processes selected for Data Warehouse

   - Do we store the product sale information on a yearly, monthly, weekly, daily or hourly basis? \
     This decision depends on the nature of reports requested by executives

   - How do the above two choices affect the database size?

   > **Note**: \
   > **Grain** is the level of detail or the depth of the information that’s
   > stored in the data warehouse and answer this type of questions:
   >
   > - Do we store all products or specific categories?
   > - We will use data from week or month or year?
   > - We will hold sales per day or per product or per store?
   >
   > Only facts consistent with the declared grain are allowed.

3. **Identify the Dimensions** \
   Dimensions are the key components in the Dimensional Data Modelling process.
   It contains detailed information about the objects like date, store, name,
   address, contacts, etc. For example, in an E-Commerce use case,
   a Dimension can be:

   - Product
   - Order Details
   - Order Items
   - Departments
   - Customers (etc).

   The Dimensional Model for a customer conducting an E-Commerce transaction is shown below:

   ```text
   Customer Dimension  -----> table name
   ---
   Customer ID         -----> primary key
   Customer Name
   Gender
   Age
   Address
   City                --|
   State                 |--> hierarchy level for location
   Country             --|
   Annual income
   Phone number
   Purchased day       --|
   Purchased month       |--> hierarchy level for date
   Purchased quarter     |
   Purchased year      --|
   ```

4. **Identify the Facts** \
   Once the Dimensions are created, the measures/transactions are supposed to be linked
   with the associated Dimensions. The Fact Tables hold measures and are linked to Dimensions
   via foreign keys. Usually, Facts contain fewer columns and huge rows.

   For example, in an E-Commerce use case, one of the Fact Tables can be of orders,
   which holds the products’ daily ordered quantity. Facts may contain more than
   one foreign key to build relationships with different Dimensions.

   This step is co-associated with the business users of the system because this
   is where they get access to data stored in the data warehouse.
   Most of the fact table rows are numerical values like price or cost per unit, etc.

5. **Build the Schema** \
   The next step is to tie Dimensions and Facts into the Schema. Schemas are the table structure,
   and they align the tables within the database.

   There are 2 popular types of Schemas:

   - **Star Schema**: \
      The Star Schema is the Schema with the simplest structure and easy to design.
     In a Star Schema, the Fact Table surrounds a series of Dimensions Tables.
     Each Dimension represents one Dimension Table. These Dimension Tables are not
     fully normalised (The fact tables in a star schema which is third normal form
     whereas dimensional tables are de-normalized).

     In this Schema, the Dimension Tables will contain a set of
     attributes that describes the Dimension. They also contain foreign keys that
     are joined with the Fact Table to obtain results.

     ```mermaid
     erDiagram
        DIM_DATE ||--o{ FCT_SALES : is
        DIM_DATE {
           string timestamp_id PK
           string date
           string month
           string year
        }
        DIM_CUSTOMER ||--o{ FCT_SALES : is
        DIM_CUSTOMER {
           string customer_id PK
           string firstname
           string lastname
           int age
        }
        FCT_SALES {
           string sales_key PK
           string date_key FK
           string customer_key FK
           string store_key FK
           numeric sales_amount
        }
        DIM_STORE ||--o{ FCT_SALES : is
        DIM_STORE {
           string customer_id PK
           string firstname
           string lastname
           int age
        }
        DIM_MOVIE ||--o{ FCT_SALES : is
        DIM_MOVIE {
           string customer_id PK
           string firstname
           string lastname
           int age
        }
     ```

   - **Snowflake Schema**: \
      A Snowflake Schema is the extension of a Star Schema, and includes more Dimensions.
     Unlike a Star Schema, the Dimensions are fully normalised and are split down
     into further tables.
     This Schema uses less disk space because they are already normalised.
     It is easy to add Dimensions to this Schema and the data redundancy
     is also less because of the intricate Schema design.

     ```mermaid
     erDiagram
        DIM_DATE ||--o{ FCT_SALES : is
        DIM_DATE {
           string timestamp_id PK
           string date
           string month
           string year
        }
        DIM_CUSTOMER ||--o{ FCT_SALES : is
        DIM_CUSTOMER {
           string customer_id PK
           string firstname
           string lastname
           int age
        }
        FCT_SALES {
           string sales_key PK
           string date_key FK
           string customer_key FK
           string store_key FK
           numeric sales_amount
        }
        DIM_STORE ||--o{ FCT_SALES : is
        DIM_STORE {
           string customer_id PK
           string firstname
           string lastname
           int age
        }
        DIM_MOVIE ||--o{ FCT_SALES : is
        DIM_MOVIE {
           string customer_id PK
           string firstname
           string lastname
           int age
        }
        DIM_COUNTRY ||--o{ DIM_STORE : in
     ```

| Star Schema                                                                                                            | Snowflake Schema                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Hierarchies for the dimensions are stored in the dimensional table.                                                    | Hierarchies are divided into separate tables.                                                                    |
| It contains a fact table surrounded by dimension tables.                                                               | One fact table surrounded by dimension table which are in turn surrounded by dimension table                     |
| In a star schema, only single join creates the relationship between the fact table and any dimension tables.           | A snowflake schema requires many joins to fetch the data.                                                        |
| Simple DB Design.                                                                                                      | Very Complex DB Design.                                                                                          |
| Denormalized Data structure and query also run faster.                                                                 | Normalized Data Structure.                                                                                       |
| High level of Data redundancy                                                                                          | Very low-level data redundancy                                                                                   |
| Single Dimension table contains aggregated data.                                                                       | Data Split into different Dimension Tables.                                                                      |
| Cube processing is faster.                                                                                             | Cube processing might be slow because of the complex join.                                                       |
| Offers higher performing queries using Star Join Query Optimization. Tables may be connected with multiple dimensions. | The Snowflake schema is represented by centralized fact table which unlikely connected with multiple dimensions. |

More Detail: [Star and Snowflake Schema in Data Warehouse with Model Examples](https://www.guru99.com/star-snowflake-data-warehousing.html)

## Types of Fact Tables

There are three main types of fact tables:

1. **Transaction** \
   The transaction fact table is the most basic and the simplest type, In the Transaction
   fact table, every row corresponding to a measurement event at a point in space
   and time which means a grain set at a single transaction. The row is added only
   if there’s a transaction is happened by a customer or for a product.

   > **Note**:
   > Row in Transaction fact table represents transaction, and it dimensions.

   For example, \
   If we have a retail store, on Sunday we sold 40 items, and on Monday we sold 15 items,
   So on Sunday there are 40 transaction rows had been added to our fact table and on Monday
   there are 15 transaction rows had been added to our table, There are no aggregate values,
   we are storing the transaction's data.

   Because of low granularity, we can monitor detailed business processes.
   But because we have rows for each transaction that happened, It causes performance
   issues due to the large size of data.

2. **Periodic Snapshot** \
   In the periodic table, We have lower granularity which means that the row in
   the periodic table is a summarization of data over a period of time (day, week, month, etc).
   Our grain here is periodic data summarization, not single transactions.
   It helps to review the aggregate performance of the business process at intervals
   of time.

   Then those unavailable measurements can be kept empty (Null) or can be filled
   up with the last available measurements.

   For example, \
   If we want to know the quantity that been sold from specific product through
   the last week. Our grain is a week.

   Because of summarized data, our performance now is better than the transaction
   fact table. But now we have higher grain, So we lost the detailed business
   processes that we had in the transaction fact table.

   > **Note**:
   > Rows in Periodic table represent performance of an activity at the end of specific period.

3. **Accumulated Snapshot** \
   In Accumulating snapshot fact table, Row represents an Entire process,
   which means that our row corresponding to measurements that occurred at defined
   steps between the beginning and end of the process. we use it when users need
   to perform pipeline and workflow analysis like Order fulfillment.

   **Order fulfillment** covers the complete process from when a sale process takes
   place all the way through delivery to the customer. So here we have multiple
   activities in the process, First when we receive an order from a customer,
   then send the order to the inventory to organize it, then move the order to
   the shipment activity, and finally, the customer receives his order.

   > **Note**:
   >
   > - Row in Accumulating snapshot represents an Entire process
   > - There is a date foreign key in the fact table for each critical activity in the process.

   Accumulating Snapshot fact table helps us in complex analysis, workflow, and
   pipeline process, on another hand It needs high ETL process complexity.

|             | Transaction                                | Periodic                                   | Accumulating                               |
| ----------- | ------------------------------------------ | ------------------------------------------ | ------------------------------------------ |
| Row         | Transaction and It dimensions.             | summarized data over a period of time.     | Entire process activities.                 |
| Granularity | Lowest granularity 1 row / Transaction     | Higher than transaction.1 row / period     | Highest granularity 1 Row / Entire process |
| Table Size  | Largest                                    | Smaller than Transaction                   | Smallest                                   |
| Example     | Sales amount of products on a daily basis. | Total sales amount of product through May. | Order fulfillment                          |

> **Fact-less Fact Table**: \
> Fact-less facts are fact tables that haven’t any measures, It only has a foreign key
> for each dimension. We can say that Fact-less fact is only an intersection of
> Dimensions Or A bridge between dimension keys.

## Rules for Dimensional Modelling

Following are the rules and principles of Dimensional Modeling:

- Load atomic data into dimensional structures.

- Build dimensional models around business processes.

- Need to ensure that every fact table has an associated date dimension table.

- Ensure that all facts in a single fact table are at the same grain or level of detail.

- It’s essential to store report labels and filter domain values in dimension tables

- Need to ensure that dimension tables use a _surrogate key_

- Continuously balance requirements and realities to deliver business solution to
  support their decision-making

## Benefits of Dimensional Data Modelling

As now, you understand the process of Dimensional Data Modelling, you can imagine
why it is so important and how many benefits DDM provides for the company.
Some of those benefits are given below:

- The Dimension Table stores the history information and a standard Dimension Table
  holds good quality data and allows easy access across the business.

- You can introduce new Dimensions without affecting other Dimensions and Facts in the Schema.

- Dimension and Fact Tables are easier to read and understand as compared to a normal table.

- Dimensional Models are built based on business terms, and hence it is quite
  understandable by the business.

- Dimensional Data Modelling in a Data Warehouse creates a Schema which is optimised
  for high performance. It means fewer joins between tables, and it also helps with
  minimised data redundancy.

- The Dimensional Data Model also helps to boost query performance. It is more denormalized;
  therefore, it is optimized for querying.

- Dimensional Data Models can comfortably accommodate the change. Dimension Tables
  can have more columns added to them without affecting existing Business Intelligence
  applications using these tables.

## Limitations of Dimensional Data Modelling

Although Dimensional Data Modelling is very crucial to any organisation,
it has a few limitations that companies need to take care of when incorporating
the concept into their applications. Some of those limitations are given below:

- Designing and creating Schemas require domain knowledge about the data.

- To maintain the integrity of Facts and Dimensions, loading the Data Warehouses
  with a record from various operational systems is complicated.

- It is severe to modify the Data Warehouse operations if the organisation adopts
  the Dimensional technique and changes the method in which they do business.

Despite these limitations, the DDM technique has proved to be one of the simplest
and most efficient techniques to handle data in Data Warehouses to date.

## Advantages

Kimball's architecture has several advantages.

- Simplicity and speed: Kimball's architecture is significantly easier and faster to construct and establish.
- Understandable: Non-technical and technical staff both may understand the dimensional data model.
- Relevancy: Kimball's bottom-up methodology, unlike Inmon's, makes all data linkages relevant to the business needs.
- Engineering team needs: In comparison to Inmon's technique, Kimball requires fewer engineers with less specific technical abilities to set up and operate the data warehouse.

Good fit for:

- Medium-to-large number of data sources
- Centralized data teams
- End-use case for data is primarily around business intelligence and providing insights
- Teams that want to create an easily navigable and predictable data warehouse design

## Disadvantages

Kimball's architecture has some drawbacks.

- Data redundancy: There is more data redundancy and hence a higher likelihood of errors since data is fed into a dimensional model.
- No single source of truth: Data marts are used to design and organise data in the data warehouse. When combined with data redundancy, Kimball's architecture prevents the company from having a single source of truth.
- Less adaptable: Kimball's architecture is less flexible and adaptable to modifications when data demands change, business requirements vary, and incoming data sources alter their payloads.
- Incomplete: The strategy taken begins (and concludes) with important business processes. As a result, it does not provide a complete 360-degree picture of business data. Instead, it helps report on particular subject areas in the corporate world.

## What is Multi-Dimensional Data Model in Data Warehouse?

Multidimensional data model in data warehouse is a model which represents data in
the form of data cubes. It allows to model and view the data in multiple dimensions,
and it is defined by dimensions and facts.

Multidimensional data model is generally categorized around a central theme and
represented by a fact table.

## Conclusion

This article gave an in-depth knowledge about Dimensional Data Modelling, its types,
features, components and also the steps required for any company to set up a DDM approach.
It also gave a brief understanding of the benefits and limitations of the DDM approach.
Overall, adopting any new approach can be a tedious task for any company, but,
by having systematic techniques put in place the company can monitor those parameters carefully
and also optimise the performance.

- A dimensional model is a data structure technique optimized for
  [Data warehousing tools](https://www.guru99.com/top-20-etl-database-warehousing-tools.html).

- A fact table is a primary table in a dimensional model. \
   There are 4 types of facts/measures:

  1. **Additive**: \
     Business measures that can be aggregated across all dimensions

  2. **Non-additive**: \
     Business measures that can be aggregated across some dimensions and not across
     others (usually date and time dimensions).\
     For example, `Items Inventory` (can be summed through product, But it can’t be summed through date)

  3. **Semi-additive**: \
     Business measures that cannot be aggregated across any dimension.\
     For example, `Sales Tax`, or `Unit Price`

  4. **Fact-less**

The most common form of dimensional modeling is the star schema. A star schema is
a multidimensional data model used to organize data so that it is easy to understand
and analyze, and very easy and intuitive to run reports on. Kimball-style star schemas
or dimensional models are pretty much the gold standard for the presentation layer
in data warehouses and data marts, and even semantic and reporting layers.
The star schema design is optimized for querying large data sets.

## Reference

- https://hevodata.com/learn/dimensional-data-modelling
- https://www.guru99.com/dimensional-model-data-warehouse.html
- https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/
- https://datavalley.technology/dimensional-modeling-part-1-introduction-and-fact-types/
- https://dwgeek.com/types-of-dimension-tables-data-warehouse.html/
