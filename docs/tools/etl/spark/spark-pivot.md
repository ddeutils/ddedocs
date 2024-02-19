# Spark: Pivot

## Create DataFrame

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

data = [
    (1, "Ross", "Geller", "Fall94", "Mathematics", 93),
    (2, "Monica", "Geller", "Fall94", "Mathematics", 99),
    (3, "Rachel", "Green", "Fall94", "Mathematics", 87),
    (4, "Joey", "Tribbiani", "Fall94", "Mathematics", 73),
    (5, "Chandler", "Bing", "Fall94", "Mathematics", 82),
    (6, "Phoebe", "Buffay", "Fall94", "Mathematics", 87),
    (1, "Ross", "Geller", "Spring95", "CS101", 90),
    (2, "Monica", "Geller", "Spring95", "CS101", 89),
    (3, "Rachel", "Green", "Spring95", "CS101", 95),
    (4, "Joey", "Tribbiani", "Spring95", "CS101", 83),
    (5, "Chandler", "Bing", "Spring95", "CS101", 93),
    (6, "Phoebe", "Buffay", "Spring95", "CS101", 89),
    (1, "Ross", "Geller", "Fall95", "Science", 90),
    (2, "Monica", "Geller", "Fall95", "Science", 99),
    (3, "Rachel", "Green", "Fall95", "Science", 87),
    (4, "Joey", "Tribbiani", "Fall95", "Science", 78),
    (5, "Chandler", "Bing", "Fall95", "Science", 85),
    (6, "Phoebe", "Buffay", "Fall95", "Science", 89)
]

schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("fname", StringType(), True),
    StructField("lname", StringType(), True),
    StructField("semester", StringType(), True),
    StructField("course", StringType(), True),
    StructField("grade", IntegerType(), True)
])

# Create the DataFrame
df = spark.createDataFrame(data, schema=schema)
display(df)
```

## Pivot

```python
from pyspark.sql.functions import concat_ws, col, first

pivot_df = (
    df
    .withColumn("semester_course", concat_ws("_", col("semester"), col("course")))
    .withColumn("name", concat_ws(" ", col("fname"), col("lname")))
    .groupBy("id", "name")
    .pivot("semester_course")
    .agg(first("grade"))
    .orderBy("id")
)

display(pivot_df)
```
