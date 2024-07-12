# Pyspark: _Unittest_

## Getting Started

### Create Fixtures

```python
@pytest.fixture(scope="session")
def spark():
    print("----Setup Spark Session---")
    spark = (
        SparkSession.builder.master("local[1]")
        .appName("Unit-Tests")
        .config("spark.executor.cores", "1")
        .config("spark.executor.instances", "1")
        .config("spark.port.maxRetries", "30")
        .config("spark.sql.shuffle.partitions", "1")
        .getOrCreate()
    )
    yield spark
    print("--- Tear down Spark Session---")
    spark.stop()
```

```python
@pytest.fixture(scope="session")
def input_data(spark):
    input_schema = StructType(
        [
            StructField("StoreID", IntegerType(), True),
            StructField("Location", StringType(), True),
            StructField("Date", StringType(), True),
            StructField("ItemCount", IntegerType(), True),
        ]
    )
    input_data = [
        (1, "Bangalore", "2021-12-01", 5),
        (2, "Bangalore", "2021-12-01", 3),
        (5, "Amsterdam", "2021-12-02", 10),
        (6, "Amsterdam", "2021-12-01", 1),
        (8, "Warsaw", "2021-12-02", 15),
        (7, "Warsaw", "2021-12-01", 99),
    ]
    input_df = spark.createDataFrame(data=input_data, schema=input_schema)
    return input_df
```

```python
@pytest.fixture(scope="session")
def expected_data(spark):
    # Define an expected data frame
    expected_schema = StructType(
        [
            StructField("Location", StringType(), True),
            StructField("TotalItemCount", IntegerType(), True),
        ]
    )
    expected_data = [("Bangalore", 8), ("Warsaw", 114), ("Amsterdam", 11)]
    expected_df = spark.createDataFrame(data=expected_data, schema=expected_schema)
    return expected_df
```

### Create Test Case

```python
def test_etl(spark, input_data, expected_data):
    # Apply transforamtion on the input data frame
    transformed_df = transform_data(input_data)

    # Compare schema of transformed_df and expected_df
    field_list = lambda fields: (fields.name, fields.dataType, fields.nullable)
    fields1 = [*map(field_list, transformed_df.schema.fields)]
    fields2 = [*map(field_list, expected_data.schema.fields)]
    res = set(fields1) == set(fields2)

    # assert
    # Compare data in transformed_df and expected_df
    assert sorted(expected_data.collect()) == sorted(transformed_df.collect())
```

## Auto CICD

```yaml title="azure-pipeline.yml"
name: Py Spark Unit Tests

pool:
  vmImage: ubuntu-latest

stages:
  - stage: Tests
    displayName: Unit Tests using Pytest

    jobs:
      - job:
        displayName: PySpark Unit Tests
        steps:
          - script: |
              sudo apt-get update
              sudo apt-get install default-jdk -y
              pip install -r $(System.DefaultWorkingDirectory)/src/tests/test-requirements.txt
              pip install --upgrade pytest pytest-azurepipelines
              cd src && pytest -v -rf --test-run-title='Unit Tests Report'
            displayName: Run Unit Tests
```

## References

- https://medium.com/@xavier211192/how-to-write-pyspark-unit-tests-ci-with-pytest-61ad517f2027
