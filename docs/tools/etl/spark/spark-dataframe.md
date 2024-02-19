# Spark: DataFrame

DataFrames are a higher-level abstraction in PySpark compared to RDDs, making it
easier to work with structured data. They offer a tabular structure, akin to a
spreadsheet or SQL table, with rows and columns.

## Create DataFrame

??? abstract "CSV data"

    id,name,age,salary,city,gender,marital_status,education_level,joining_date,performance_rating,attrition
    1,John Doe,28,60000,New York,Male,Married,Bachelor's,2022-01-01,90,No
    2,Jane Smith,35,75000,San Francisco,Female,Single,Master's,2021-12-15,75,Yes
    3,Bob Johnson,42,90000,Chicago,Male,Married,PhD,2022-02-10,88,No
    4,Alice Brown,31,65000,Los Angeles,Female,Single,Bachelor's,2021-11-20,77,Yes
    5,Charlie Wilson,45,80000,Houston,Male,Married,Master's,2021-10-05,92,No
    6,Eva Davis,29,70000,Miami,Female,Single,Bachelor's,2022-03-15,80,Yes
    7,Michael Lee,38,85000,Seattle,Male,Married,Master's,2021-09-30,85,No
    8,Sophia Chen,33,72000,Boston,Female,Single,Bachelor's,2022-04-20,79,Yes
    9,David White,40,95000,Atlanta,Male,Married,PhD,2021-08-12,93,No
    10,Olivia Miller,27,68000,Dallas,Female,Single,Master's,2022-05-25,76,Yes
    11,James Taylor,34,78000,Denver,Male,Married,Bachelor's,2021-07-10,82,No
    12,Emma Moore,32,72000,Austin,Female,Single,Master's,2022-06-18,88,Yes
    13,William Hall,39,92000,Phoenix,Male,Married,PhD,2021-06-05,90,No
    14,Grace Johnson,26,65000,Portland,Female,Single,Bachelor's,2022-07-30,78,Yes
    15,Liam Anderson,37,88000,San Diego,Male,Married,Master's,2021-05-15,87,No
    16,Ava Garcia,30,71000,Philadelphia,Female,Single,Bachelor's,2022-08-12,83,Yes
    17,Mason Lewis,41,97000,Minneapolis,Male,Married,PhD,2021-04-02,95,No
    18,Sofia Wright,28,69000,Charlotte,Female,Single,Master's,2022-09-25,79,Yes
    19,Ethan Davis,43,89000,Detroit,Male,Married,Bachelor's,2021-03-18,88,No
    20,Mia Martin,29,74000,San Antonio,Female,Single,Master's,2022-10-10,81,Yes
    21,Aiden Allen,36,82000,Orlando,Male,Married,PhD,2021-02-09,87,No
    22,Chloe Johnson,31,68000,Tampa,Female,Single,Bachelor's,2022-11-05,76,Yes
    23,Lucas Smith,44,92000,Raleigh,Male,Married,Master's,2021-01-22,90,No
    24,Zoe Brown,27,71000,Columbus,Female,Single,Bachelor's,2022-12-20,77,Yes
    25,Jackson Lee,38,85000,Indianapolis,Male,Married,PhD,2020-12-01,85,No
    26,Lily Wang,33,77000,San Jose,Female,Single,Master's,2023-01-15,79,Yes
    27,Logan Taylor,40,93000,Nashville,Male,Married,Bachelor's,2020-11-10,93,No
    28,Isabella Wilson,26,66000,Memphis,Female,Single,Master's,2023-02-28,68,Yes
    29,Christopher Miller,35,86000,New Orleans,Male,Married,PhD,2020-10-25,86,No
    30,Sophie Davis,32,70000,Louisville,Female,Single,Bachelor's,2023-03-20,78,Yes

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    FloatType,
    DateType,
)
from pyspark.sql.functions import round, col

spark = SparkSession.builder.appName("example").getOrCreate()

# Define a schema for the DataFrame
schema = StructType(
    [
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True),
        StructField("age", IntegerType(), True),
        StructField("salary", FloatType(), True),
        StructField("city", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("marital_status", StringType(), True),
        StructField("education_level", StringType(), True),
        StructField("joining_date", DateType(), True),
        StructField("performance_rating", IntegerType(), True),
        StructField("attrition", StringType(), True),
    ]
)

# Create a DataFrame from the CSV data
df = spark.read.csv(
    spark.sparkContext.parallelize(csv_data.split("\n")), header=True, schema=schema
)

# Display the DataFrame
df.show()
```

## Transformations and Actions

### Filtering

```python
df.filter(df.age > 30).show()
```

### Selecting Columns

```python
df.select("name", "salary").show()
```

### Aggregations and rounding decimals

```python
df.groupBy("gender").agg({"salary": "avg"}).withColumn(
    "avg(salary)", round(col("avg(salary)"), 2)
).show()
```

### Joining

```python
df.filter(df.age > 30).join(df.filter(df.salary > 80000), "id", "inner")
```

## References

- [Navigating PySpark DataFrames: An In-Depth Guide](https://blog.devgenius.io/navigating-pyspark-dataframes-an-in-depth-guide-646a15df4bc9)
