# Dynamic JSON

JSON is a lightweight data-interchange format that’s easy to read and write for
humans, and easy to parse and generate for machines. In the realm of big data,
JSON has emerged as the de facto standard for semi-structured data.
However, this flexibility also introduces challenges, especially when dealing
with data of varying structures.
This blog dives into how you can leverage PySpark to dynamically parse and process
JSON data, ensuring your Big Data pipelines remain both flexible and scalable.

## Code Walkthrough: Dynamic JSON Schema Handling

### Step 1: Create a DataFrame from JSON Strings

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType

# Initialize SparkSession
spark = SparkSession.builder.master("local[*]").appName("DynamicJSONParsing").getOrCreate()

# Sample data showcasing varying JSON structures
data = [
    ("1", '{"name": "John Doe", "age": 30}'),
    ("2", '{"city": "New York", "country": "USA", "zipcode": "10001"}'),
    ("3", '{"product": "Laptop", "brand": "Dell", "specs": {"RAM": "16GB", "Storage": "512GB SSD"}}')
]

# Creating the DataFrame
df = spark.createDataFrame(data, ["id", "json_string"])
```

### Step 2: Define a Dynamic Schema

```python
dynamic_schema = spark.read.json(df.rdd.map(lambda row: row.json_string)).schema
```

### Step 3: Convert JSON Strings to Structured Data

```python
df = df.withColumn("json_struct", from_json(col("json_string"), dynamic_schema))
```

### Step 4: Accessing All JSON Keys

```python
def get_json_keys(schema, prefix):
    """
    Recursively fetches all the keys from a complex JSON schema.

    :param schema: The schema of the DataFrame or a part of it.
    :param prefix: The current struct column name.
    :return: A list of strings representing the path to each key in the JSON object.
    """
    keys = []
    for field in schema.fields:
        # If the current field is a StructType, recurse
        if isinstance(field.dataType, StructType):
            if prefix:
                new_prefix = f"{prefix}.{field.name}"
            else:
                new_prefix = field.name
            keys += get_json_keys(field.dataType, new_prefix)
        elif isinstance(field.dataType, ArrayType) and isinstance(field.dataType.elementType, StructType):
            # Handle arrays of StructTypes
            if prefix:
                new_prefix = f"{prefix}.{field.name}"
            else:
                new_prefix = field.name
            keys += get_json_keys(field.dataType.elementType, new_prefix)
        else:
            # Base case: add the field name to the keys list
            if prefix:
                keys.append(f"{prefix}.{field.name}")
            else:
                keys.append(field.name)
    return keys

cols = get_json_keys(dynamic_schema, "json_struct")
```

### Step 5: Accessing Specific Fields

```python
df.select("id", *cols).show(truncate=False)
df.show(truncate=False)
```

```text
+---+----+-----+--------+-------+--------+-------+------+---------------+----+---------+-------+
| id| age|brand|    city|country|    name|product|memory|          model| RAM|  Storage|zipcode|
+---+----+-----+--------+-------+--------+-------+------+---------------+----+---------+-------+
|  1|  50| null|    null|   null|John Doe|   null|  null|           null|null|     null|   null|
|  2|null| null|New York|    USA|    null|   null|  null|           null|null|     null|  10001|
|  3|null| Dell|    null|   null|    null| Laptop|   4GB|NVIDIA GTX 1650|16GB|512GB SSD|   null|
+---+----+-----+--------+-------+--------+-------+------+---------------+----+---------+-------+
```

### Step 6: Give Hierarchy to the Columns

```python
df = df.select([col(c).alias(n) for c, n in zip(df.columns, ['id'] + cols)])
df.show()
```

```text
+---+---------------+-----------------+----------------+-------------------+----------------+-------------------+---------------------+-------------------------+-------------------+
| id|json_struct.age|json_struct.brand|json_struct.city|json_struct.country|json_struct.name|json_struct.product|json_struct.specs.RAM|json_struct.specs.Storage|json_struct.zipcode|
+---+---------------+-----------------+----------------+-------------------+----------------+-------------------+---------------------+-------------------------+-------------------+
|  1|             30|             null|            null|               null|        John Doe|               null|                 null|                     null|               null|
|  2|           null|             null|        New York|                USA|            null|               null|                 null|                     null|              10001|
|  3|           null|             Dell|            null|               null|            null|             Laptop|                 16GB|                512GB SSD|               null|
+---+---------------+-----------------+----------------+-------------------+----------------+-------------------+---------------------+-------------------------+-------------------+
```

## Conclusion

Mastering dynamic JSON parsing in PySpark is essential for processing semi-structured
data efficiently.
By leveraging PySpark’s flexible schema handling capabilities, you can build
robust data pipelines that adapt to changing JSON structures.
Whether you’re working with IoT data, e-commerce platforms, log files, NoSQL
databases, or data integration tasks, PySpark’s dynamic JSON parsing features
empower you to extract valuable insights from diverse data sources.
With the right tools and techniques, you can unlock the full potential of your
Big Data pipelines and drive data-driven decision-making across your organization.


## :material-playlist-plus: Read Mores

- [:simple-medium: Dynamic JSON Parsing in PySpark: A Guide to Flexible Schema Handling](https://halismanaz.medium.com/dynamic-json-parsing-in-pyspark-a-guide-to-flexible-schema-handling-ce31dc475fe0)
