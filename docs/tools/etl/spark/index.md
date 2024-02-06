---
icon: simple/apachespark
---

# Apache Spark

!!! quote

    **Apache Spark** is a unified computing engine and a set of libraries for parallel
    data processing on computer cluster

## Architecture

![Spark Cluster Overview](./images/spark-cluster-overview.png)

* https://medium.com/@think-data/this-level-of-detail-in-spark-is-tackled-only-by-experts-2-975cfb41af50
* [Partitioning & Bucketing](https://blog.det.life/apache-spark-partitioning-and-bucketing-1790586e8917)
* [How does Adaptive Query Execution fix your Spark performance issues](https://medium.com/@kerrache.massipssa/how-does-adaptive-query-execution-fix-your-spark-performance-issues-029166e772b7)

## Spark Context vs Spark Session

!!! quote

    **Spark Session** is a unified entry point of a spark application from Spark 2.0

=== "Spark Session"

    ```python
    from pyspark.sql import SparkSession

    spark = (
        SparkSession
            .builder
            .appName("YourAppName")
            .master("local")
            .config("park.executor.memory", "2g")
            .config("spark.executor.cores", 4)
            .enableHiveSupport()  # Default be True
            .getOrCreate()
    )
    ```

=== "Spark Context"

    ```python
    from pyspark.context import SparkContext
    from pyspark import SparkConf

    sc = (
        SparkContext(
            conf=(
                SparkConf()
                    .set("spark.executor.memory", "2g")
                    .set("spark.executor.cores", "4")
            )
        )
        .getOrCreate()
    )
    ```

* https://towardsdev.com/spark-context-vs-spark-session-97d87bd5ef9e

## Spark API

Spark has two API types

* Low-level API (unstructured)
* High-level API (Spark’s structured API)

### Low-level API

Resilient Distributed Datasets (RDDs) คือ collection ของ elements partitioned ที่กระจายไปตาม node ใน cluster ที่ทำงาน parallel กัน

RDDs นั้น support 2 operations

transformations — สร้าง dataset ใหม่
actions — return value ไปหา driver program หลัง compute dataset เสร็จ
ทุก transformations ใน spark จะ lazy คือมันจะไม่ compute ทันทีแต่จะจำไว้ว่า transformations นี้มันยุ่งกับ base dataset หรือไฟล์อะไร ถึงตอนที่มันจะ compute จริงๆ ถึงตอนนั้น action ค่อยเกิดขึ้นแล้ว return ค่าไปหา driver program ซึ่งเปรียบเทียบแล้ว transformations จึงเปรียบได้กับ map และ actions คือ reduce

หากมองในมุม End user เราจะไม่ได้ใช้ RDDs มากเท่าไร ยกเว้นในกรณีที่เราต้อง maintain old Spark code

### High-level API

Structured API เป็นเครื่องมือในการ manipulate all sorts of data ตั้งแต่ unstructured, semi-structured, structured data

Structured API สามารถใช้ได้ทั้งกับ batch และ streaming computation ซึ่งคือ ฝั่ง Spark SQL, Dataframes, Datasets API ส่วนในฝั่ง streaming จะเป็น Spark Structured Streaming ซึ่งเราจะขออธิบายแค่ฝั่งแรก

## Memory

* https://medium.com/@think-data/understanding-the-memory-components-of-spark-e3070f315d17

## Execution

https://blog.stackademic.com/apache-spark-101-understanding-spark-code-execution-cbff49cb85ac

## Most Common Use Cases

https://towardsdatascience.com/fetch-failed-exception-in-apache-spark-decrypting-the-most-common-causes-b8dff21075c
https://medium.com/art-of-data-engineering/distinct-and-dropduplicates-in-spark-real-project-example-9007954b49af
https://medium.com/@vishalbarvaliya/coalesce-vs-repartition-58b12a0f0a3d
https://medium.com/@vishalbarvaliya/apache-sparks-reducebykey-and-reduce-transformations-42b3bd80e32e

## Interview Questions

* https://blog.devgenius.io/spark-interview-questions-ii-120e1621be9a
* https://blog.devgenius.io/spark-interview-questions-x-843a24cb703a
* https://gsanjeewa1111.medium.com/pyspark-facts-b83366842ddf
* [Top 25 PySpark Interview Questions and Answers (2023)](https://blog.varunsingh.in/top-25-pyspark-interview-questions-and-answers-2023-2eb3c67cbaf5)

## Optimization

https://medium.com/plumbersofdatascience/7-key-strategies-to-optimize-your-spark-applications-948e7df607b
* [PySpark Tips](https://towardsdev.com/pyspark-tip-d4614b013d6f)
* [4 Examples to Take Your PySpark Skills to Next Level](https://towardsdatascience.com/4-examples-to-take-your-pyspark-skills-to-next-level-2a04cbe6e630)
