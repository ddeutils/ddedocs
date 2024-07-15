# IO

## :material-arrow-down-right: Getting Started

### Why _SUCCESS file

https://towardsdev.com/why-does-spark-write-output-a-success-file-83662e43b515

## Data

### Json

```python
data = [
    ['EMP001', '{"dept" : "account", "fname": "Ramesh", "lname": "Singh", "skills": ["excel", "tally", "word"]}'],
    ['EMP002', '{"dept" : "sales", "fname": "Siv", "lname": "Kumar", "skills": ["biking", "sales"]}'],
    ['EMP003', '{"dept" : "hr", "fname": "MS Raghvan", "skills": ["communication", "soft-skills"]}']
]

df_raw = spark.createDataFrame(data=data, schema=['emp_no', 'raw_data'])
```

```python
# Determine the schema of the JSON payload from the column
json_schema_df = spark.read.json(df_raw.rdd.map(lambda row: row.raw_data))
json_schema = json_schema_df.schema
```

```python
# Apply the schema to payload to read the data
from pyspark.sql.functions import from_json

df_details = (
    df_raw
        .withColumn("parsed_data", from_json(df_raw["raw_data"], json_schema))
        .drop("raw_data")
)
df_details.printSchema()
```

```python
# Lets verify the data
df_details.select("emp_no", "parsed_data.*").show(10, False)
```

```python
# We can explode the data further from list
from pyspark.sql.functions import explode

df_details.select("emp_no", "parsed_data.dept", "parsed_data.fname", "parsed_data.lname", "parsed_data") \
    .withColumn("skills", explode("parsed_data.skills")) \
    .drop("parsed_data") \
    .show(100, False)
```

https://subhamkharwal.medium.com/pyspark-read-parse-json-column-from-another-data-frame-e2e98d80e9b6
