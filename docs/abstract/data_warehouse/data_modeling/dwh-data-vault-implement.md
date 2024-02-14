# Data Vault Implementation

## Hubs

```sql
CREATE PROCEDURE [RV].[LOAD_PRODUCT_HUB]
    @LOAD_PRCS      BIGINT
AS
    WITH NewProductBussKey AS
    (
        SELECT DISTINCT product_number
        FROM [STG].[PRODUCT_TABLE_2022]     AS SRC
        LEFT OUTER JOIN [RV].[HUB_PRODUCT]  AS TGT
            ON SRC.product_number = TGT.product_key
        WHERE TGT.product_key IS NULL
    )
    INSERT INTO [RV].[HUB_PRODUCT] WITH (TABLOCK) -- bulk load
    SELECT
        HASH(product_number)                AS product_hash_key,
        product_number                      AS product_key,
        GETDATE()                           AS LDTS,
        @LOAD_PRCS                          AS LDID, -- unique ID for load
        'PRODUCT_TABLE_2022'                AS Record_Source
    FROM [STG].[PRODUCT_TABLE_2022]
RETURN 0
```

## Links

```sql
CREATE PROCEDURE [RV].[LOAD_SALES_PRODUCT_LINK]
    @LOAD_PRCS      BIGINT
AS
    WITH NewDistinctBusinessKey AS
    (
        SELECT DISTINCT
            H_SALES.sales_key,
            H_PRODUCT.product_key
        FROM [STG].[SALES_ORDER_DETAIL_2022]        AS SRC
        LEFT OUTER JOIN [RV].[HUB_SALES]            AS H_SALES -- lookup sales key
            ON SRC.sales_order_id = H_SALES.sales_key
        LEFT OUTER JOIN [RV].[HUB_PRODUCT]          AS H_PRODUCT -- lookup product key
            ON SRC.product_number = H_PRODUCT.product_key
        LEFT OUTER JOIN [RV].[LINK_SALES_PRODUCT]     AS TGT
            ON TGT.product_key  = H_PRODUCT.product_key
            AND TGT.sales_key   = H_SALES.sales_key
        WHERE TGT.sales_key IS NULL
    )
    INSERT INTO [RV].[LINK_SALES_PRODUCT] WITH (TABLOCK) -- bulk load
    SELECT
        HASH(sales_order_id, product_number)        AS link_sales_product_hash_key,
        sales_order_id                              AS sales_key,
        product_number                              AS product_key,
        GETDATE()                                   AS LDTS,
        @LOAD_PRCS                                  AS LDID, -- unique ID for load
        'SALES_ORDER_DETAIL_2022'                   AS Record_Source
    FROM [STG].[SALES_ORDER_DETAIL_2022]
RETURN 0
```

## Satellites

```sql
CREATE PROCEDURE [RV].[Load_SAT_ProductDetails]
    @LOAD_PRCS BIGINT
As
    DECLARE @RecordSource        nvarchar(100)
    DECLARE @DefaultValidFrom    datetime2(0)     –use datetime2(0) to remove milliseconds
    Declare @DefaultValidTo      datetime2(0)
    DECLARE @LoadDateTime        datetime2(0)
    SET @RecordSource            = N’AdventureWorks2012.Product.Product‘
    SET @DefaultValidFrom        = ‚1900-01-01‘
    SET @DefaultValidTo          = ‚9999-12-31‘
    SET @LoadDateTime            = GETDATE()
BEGIN TRY
Begin Transaction
    INSERT INTO [RV].[SAT_ProductDetails_DV20]
    (
         Product_Hsk,
         LoadTimestamp,
         Name,
         ListPrice,
         LOAD_PRCS,
         RecordSource,
         ValidFrom,
         ValidTo,
         IsCurrent
    )
    SELECT
         Product_Hsk,                            –Hash Key
         @LoadDateTime,                          –LoadDatetimeStamp
         Name,
         ListPrice,
         @LOAD_PRCS as LOAD_PRCS,
         @RecordSource as RecordSource,
         @LoadDateTime,                          –Actual DateTimeStamp
         @DefaultValidTo,                        –Default Expiry DateTimestamp
         1                                       –IsCurrent Flag
    FROM
    (
        MERGE [RV].[SAT_ProductDetails_DV20]       AS Target     –Target: Satellite
        USING
        (
           — Query distinct set of attributes from source (stage)
           SELECT DISTINCT
               stage.Product_Hsk,
               stage.Name,
           stage.ListPrice
           FROM stage.Product_Product_AdventureWorks2012_DV20 as stage
        ) AS Source
            ON Target.Product_Hsk = Source.Product_Hsk         –Identify Columns by Hub/Link Hash Key
            AND Target.IsCurrent = 1                           –and only merge against current records in the target
        –when record already exists in satellite and an attribute value changed
        WHEN MATCHED AND
            (
                 Target.Name <> Source.Name
                 OR Target.ListPrice <> Source.ListPrice
            )
        — then outdate the existing record
        THEN UPDATE SET
            IsCurrent  = 0,
            ValidTo    = @LoadDateTime
        — when record not exists in satellite, insert the new record
        WHEN NOT MATCHED BY TARGET
        THEN INSERT
        (
            Product_Hsk,
            LoadTimestamp,
            Name,
            ListPrice,
            LOAD_PRCS,
            RecordSource,
            ValidFrom,
            ValidTo,
            IsCurrent
        )
        VALUES
        (
            Source.Product_Hsk,
            @LoadDateTime,
            Source.Name,
            Source.ListPrice,
            @LOAD_PRCS,
            @RecordSource,
            @DefaultValidFrom,     –Default Effective DateTimeStamp
            @DefaultValidTo,       –Default Expiry DateTimeStamp
            1                      –IsCurrent Flag
        )
        — Output changed records
        OUTPUT
            $action AS Action
            ,Source.*
    ) AS MergeOutput
    WHERE MergeOutput.Action = 'UPDATE' AND Product_Hsk IS NOT NULL;

    COMMIT

    SELECT
        'Success' as ExecutionResult
    RETURN;
END TRY
BEGIN CATCH
     IF @@TRANCOUNT > 0
     ROLLBACK
     SELECT
          'Failure' as ExecutionResult,
          ERROR_MESSAGE() AS ErrorMessage;
     RETURN;
END CATCH
GO
```

## Dimension

```sql
CREATE OR REPLACE VIEW v_curr_customer AS
SELECT hub.h_customer_key
     , hub.customer_no
     , s1.preferred_contact
     , s1.e_mail_address
     , s1.phone_number
     , s1.private_person
     , s1.reseller
     , s1.delivery_type
     , s2.last_name cust_last_name
     , s2.first_name cust_first_name
     , s2.street cust_street
     , s2.street_no cust_street_no
     , s2.zip_code cust_zip_code
     , s2.city cust_city
     , s3.last_name bill_last_name
     , s3.first_name bill_first_name
     , s3.street bill_street
     , s3.street_no bill_street_no
     , s3.zip_code bill_zip_code
     , s3.city bill_city
  FROM h_customer hub
  JOIN pit_customer pit
    ON (hub.h_customer_key = pit.h_customer_key)
  LEFT JOIN s_customer_info s1
    ON (s1.h_customer_key = pit.h_customer_key AND s1.load_date = pit.s1_load_date)
  LEFT JOIN s_customer_address s2
    ON (s2.h_customer_key = pit.h_customer_key AND s2.load_date = pit.s2_load_date)
  LEFT JOIN s_billing_address s3
    ON (s3.h_customer_key = pit.h_customer_key AND s3.load_date = pit.s3_load_date)
 WHERE pit.load_end_date IS NULL;
```

```sql
EXPLAIN PLAN FOR
SELECT h_customer_key
     , customer_no     — H_CUSTOMER
     , e_mail_address  — S_CUSTOMER_INFO
     , cust_first_name — S_CUSTOMER_ADDRESS
     , bill_first_name — S_BILLING_ADDRESS
  FROM v_curr_customer;

SELECT * FROM dbms_xplan.display();
——————————————————————–
| Id  | Operation                     | Name               | Rows  |
——————————————————————–
|   0 | SELECT STATEMENT              |                    | 20000 |
|*  1 |  HASH JOIN RIGHT OUTER        |                    | 20000 |
|   2 |   TABLE ACCESS STORAGE FULL   | S_CUSTOMER_INFO    | 27000 |
|*  3 |   HASH JOIN RIGHT OUTER       |                    | 20000 |
|   4 |    TABLE ACCESS STORAGE FULL  | S_BILLING_ADDRESS  |  4964 |
|*  5 |    HASH JOIN OUTER            |                    | 20000 |
|*  6 |     HASH JOIN                 |                    | 20000 |
|   7 |      TABLE ACCESS STORAGE FULL| H_CUSTOMER         | 20000 |
|*  8 |      TABLE ACCESS STORAGE FULL| PIT_CUSTOMER       | 20000 |
|   9 |     TABLE ACCESS STORAGE FULL | S_CUSTOMER_ADDRESS | 33406 |
——————————————————————–
```

```sql
EXPLAIN PLAN FOR
SELECT h_customer_key
   –, customer_no     — H_CUSTOMER
     , e_mail_address  — S_CUSTOMER_INFO
     , cust_first_name — S_CUSTOMER_ADDRESS
   –, bill_first_name — S_BILLING_ADDRESS
  FROM v_curr_customer;

SELECT * FROM dbms_xplan.display();
——————————————————————
| Id  | Operation                   | Name               | Rows  |
——————————————————————
|   0 | SELECT STATEMENT            |                    | 20000 |
|*  1 |  HASH JOIN RIGHT OUTER      |                    | 20000 |
|   2 |   TABLE ACCESS STORAGE FULL | S_CUSTOMER_INFO    | 27000 |
|*  3 |   HASH JOIN OUTER           |                    | 20000 |
|*  4 |    TABLE ACCESS STORAGE FULL| PIT_CUSTOMER       | 20000 |
|   5 |    TABLE ACCESS STORAGE FULL| S_CUSTOMER_ADDRESS | 33406 |
——————————————————————
```

## Loading Dimensions From Data Vault Model

https://danischnider.wordpress.com/2021/12/20/multi-version-load-in-data-vault/
https://danischnider.wordpress.com/2015/11/12/loading-dimensions-from-a-data-vault-model/

## Insert-only

https://www.scalefree.com/scalefree-newsletter/insert-only-in-data-vault/

## Tips to get the best performance out of a Data Vault Model in Databricks Lakehouse

- Use Delta Formatted tables for Raw Vault, Business Vault and Gold layer tables.

- Make sure to use OPTIMIZE and Z-order indexes on all join keys of Hubs, Links
  and Satellites.

- Do not over partition the tables -especially the smaller satellites tables.
  Use Bloom filter indexing on Date columns, current flag columns and predicate
  columns that are typically filtered on to ensure the best performance - especially
  if you need to create additional indices apart from Z-order.

- Delta Live Tables (Materialized Views) makes creating and managing PIT tables very easy.

- Reduce the `optimize.maxFileSize` to a lower number, such as 32-64MB vs. the
  default of 1 GB. By creating smaller files, you can benefit from file pruning
  and minimize the I/O retrieving the data you need to join.

- Data Vault model has comparatively more joins, so use the latest version of DBR
  which ensures that the Adaptive Query Execution is ON by default so that the best
  Join strategy is automatically used. Use Join hints only if necessary.
  (for advanced performance tuning).

## Implements

- [Data Vault on Snowflake](https://patrickcuba.medium.com/data-vault-on-snowflake-expanding-to-dimensional-models-5eb67cbdcf4b)

## References

- https://dbtvault.readthedocs.io/en/latest/
- https://www.oraylis.de/blog/2016/data-vault-satellite-loads-explained
- https://www.databricks.com/blog/2022/06/24/prescriptive-guidance-for-implementing-a-data-vault-model-on-the-databricks-lakehouse-platform.html
- https://datavaultalliance.com/news/building-a-real-time-data-vault-in-snowflake/ \*\*\*
- https://jerryrun.wordpress.com/2018/09/12/chapter-4-data-vault-20-modeling/
- https://github.com/dbsys21/databricks-lakehouse/blob/main/lakehouse-buildout/data-vault/TPC-DLT-Data-Vault-2.0.sql
- https://aws.amazon.com/blogs/big-data/design-and-build-a-data-vault-model-in-amazon-redshift-from-a-transactional-database/
