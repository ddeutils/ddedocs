# Apache Spark: _Structured Stream_

## ETL

```python titles="Spark-streaming-medallion"
class Bronze():
    def __init__(self):
        self.base_data_dir = "/FileStore/spark_structured_streaming"

    def getSchema(self):
        return """InvoiceNumber string, CreatedTime bigint, StoreID string, PosID string, CashierID string,
                CustomerType string, CustomerCardNo string, TotalAmount double, NumberOfItems bigint,
                PaymentMethod string, TaxableAmount double, CGST double, SGST double, CESS double,
                DeliveryType string,
                DeliveryAddress struct<AddressLine string, City string, ContactNumber string, PinCode string,
                State string>,
                InvoiceLineItems array<struct<ItemCode string, ItemDescription string,
                    ItemPrice double, ItemQty bigint, TotalValue double>>
            """

    def readInvoices(self):
        return (
            spark.readStream
                .format("json")
                .schema(self.getSchema())
                #.option("cleanSource", "delete")
                .option("cleanSource", "archive")
                .option("sourceArchiveDir", f"{self.base_data_dir}/data/invoices_archive")
                .load(f"{self.base_data_dir}/data/invoices")
        )

    def process(self):
        print(f"\nStarting Bronze Stream...", end='')
        invoicesDF = self.readInvoices()
        sQuery =  ( invoicesDF.writeStream
                            .queryName("bronze-ingestion")
                            .option("checkpointLocation", f"{self.base_data_dir}/chekpoint/invoices_bz")
                            .outputMode("append")
                            .toTable("invoices_bz")
                    )
        print("Done")
        return sQuery


class Silver():
    def __init__(self):
        self.base_data_dir = "/FileStore/spark_structured_streaming"

    def readInvoices(self):
        return (
            spark.readStream
                .table("invoices_bz")
        )

    def explodeInvoices(self, invoiceDF):
        return ( invoiceDF.selectExpr("InvoiceNumber", "CreatedTime", "StoreID", "PosID",
                                      "CustomerType", "PaymentMethod", "DeliveryType", "DeliveryAddress.City",
                                      "DeliveryAddress.State","DeliveryAddress.PinCode",
                                      "explode(InvoiceLineItems) as LineItem")
                                    )

    def flattenInvoices(self, explodedDF):
        from pyspark.sql.functions import expr
        return( explodedDF.withColumn("ItemCode", expr("LineItem.ItemCode"))
                        .withColumn("ItemDescription", expr("LineItem.ItemDescription"))
                        .withColumn("ItemPrice", expr("LineItem.ItemPrice"))
                        .withColumn("ItemQty", expr("LineItem.ItemQty"))
                        .withColumn("TotalValue", expr("LineItem.TotalValue"))
                        .drop("LineItem")
                )

    def appendInvoices(self, flattenedDF):
        return (flattenedDF.writeStream
                    .queryName("silver-processing")
                    .format("delta")
                    .option("checkpointLocation", f"{self.base_data_dir}/chekpoint/invoice_line_items")
                    .outputMode("append")
                    .toTable("invoice_line_items")
        )

    def process(self):
           print(f"\nStarting Silver Stream...", end='')
           invoicesDF = self.readInvoices()
           explodedDF = self.explodeInvoices(invoicesDF)
           resultDF = self.flattenInvoices(explodedDF)
           sQuery = self.appendInvoices(resultDF)
           print("Done\n")
           return sQuery
```

```python titles="Spark_streaming_medallion_test_suite"
%run ../SparkStreaming/Spark-streaming-medallion

class medallionApproachTestSuite:
    def __init__(self):
        self.base_data_dir = "/FileStore/spark_structured_streaming"

    def cleanTests(self):
        print(f"Starting Cleanup...", end='')
        spark.sql("drop table if exists invoices_bz")
        spark.sql("drop table if exists invoice_line_items")
        dbutils.fs.rm("/user/hive/warehouse/invoices_bz", True)
        dbutils.fs.rm("/user/hive/warehouse/invoice_line_items", True)

        dbutils.fs.rm(f"{self.base_data_dir}/chekpoint/invoices_bz", True)
        dbutils.fs.rm(f"{self.base_data_dir}/chekpoint/invoice_line_items", True)

        dbutils.fs.rm(f"{self.base_data_dir}/data/invoices_archive", True)
        dbutils.fs.rm(f"{self.base_data_dir}/data/invoices", True)
        dbutils.fs.mkdirs(f"{self.base_data_dir}/data/invoices")
        print("Done")

    def ingestData(self, itr):
        print(f"\tStarting Ingestion...", end='')
        dbutils.fs.cp(f"{self.base_data_dir}/invoices/invoices_{itr}.json", f"{self.base_data_dir}/data/invoices/")
        print("Done")

    def assertResult(self, expected_count):
        print(f"\tStarting validation...", end='')
        actual_count = spark.sql("select count(*) from invoice_line_items").collect()[0][0]
        assert expected_count == actual_count, f"Test failed! actual count is {actual_count}"
        print("Done")

    def waitForMicroBatch(self, sleep=30):
        import time
        print(f"\tWaiting for {sleep} seconds...", end='')
        time.sleep(sleep)
        print("Done.")

    def runTests(self):
        self.cleanTests()
        bzStream = Bronze()
        bzQuery = bzStream.process()

        slStream = Silver()
        slQuery = slStream.process()

        print("\nTesting first iteration of invoice stream...")
        self.ingestData(1)
        self.waitForMicroBatch()
        self.assertResult(1253)
        print("Validation passed.\n")

        print("Testing second iteration of invoice stream...")
        self.ingestData(2)
        self.waitForMicroBatch()
        self.assertResult(2510)
        print("Validation passed.\n")

        print("Testing third iteration of invoice stream...")
        self.ingestData(3)
        self.waitForMicroBatch()
        self.assertResult(3990)
        print("Validation passed.\n")

        bzQuery.stop()
        slQuery.stop()

        print("Validating Archive...", end="")
        archives_expected = ["invoices_1.json", "invoices_2.json"]
        for f in dbutils.fs.ls(f"{self.base_data_dir}/data/invoices_archive/{self.base_data_dir}/data/invoices"):
            assert f.name in archives_expected, f"Archive Validation failed for {f.name}"
        print("Done")

# COMMAND ----------

maTS = medallionApproachTestSuite()
maTS.runTests()
```

## Optimization

[Optimizing Spark Structured Streaming](https://medium.com/towards-data-engineering/optimizing-spark-structured-streaming-84eccf50c607)
[5 Tips - Optimizing Spark Structured Streaming Apps](https://medium.com/@roeyshemtov1/5-tips-for-optimizing-spark-structured-streaming-applications-5ceb568a46e1)
