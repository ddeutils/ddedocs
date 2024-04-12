---
icon: material/chat-question-outline
---

# Pandera

[Pandera](https://github.com/unionai-oss/pandera) is a Python library that provides
flexible and expressive data validation for pandas data structures.
It’s designed to bring more rigor and reliability to the data processing steps,
ensuring that your data conforms to specified formats, types, and other constraints
before you proceed with analysis or modeling.

**Why Pandera?**

In the intricate tapestry of data science, where data is the fundamental thread,
ensuring its quality and consistency is paramount.
**Pandera** promotes the integrity and quality of data through rigorous validation.
It’s not just about checking data types or formats;
**Pandera** extends its vigilance to more sophisticated statistical validations,
making it an indispensable ally in your data science endeavours.
Specifically, Pandera stands out by offering:

- Schema enforcement: Guarantees that your DataFrame adheres to a predefined schema.
- Customisable validation: Enables creation of complex, custom validation rules.
- Integration with Pandas: Seamlessly works with existing pandas workflows.

## :material-arrow-down-right: Getting Started

```shell
pip install pandera
```

### With Pandas

```python
import pandas as pd
from pandas import Timestamp
import pandera as pa
from pandera import Column, DataFrameSchema, Check, Index

schema = DataFrameSchema({
    "name": Column(str),
    "age": Column(int, checks=pa.Check.ge(0)),  # age should be non-negative
    "email": Column(str, checks=pa.Check.str_matches(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'))  # email format
})

# Sample DataFrame
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, -5, 30],
    "email": ["alice@example.com", "bob@example", "charlie@example.com"]
})

# Validate
validated_df = schema(df)
```

```console
SchemaError: <Schema Column(name=age, type=DataType(int64))> failed element-wise validator 0:
<Check greater_than_or_equal_to: greater_than_or_equal_to(0)>
failure cases:
   index  failure_case
0      1            -5
```

```python
@pa.check_input(schema)
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    # Some code to process the DataFrame
    return df

processed_df = process_data(df)
```

The `@pa.check_input` decorator ensures that the input DataFrame adheres to the
schema before the function processes it.

## Advanced data validation

### Custom Check

```python
# Define the enhanced schema
enhanced_schema = DataFrameSchema(
    columns={
        "name": Column(str),
        "age": Column(int, checks=[Check.ge(0), Check.lt(100)]),
        "email": Column(str, checks=[Check.str_matches(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')]),
        "salary": Column(float, checks=Check.in_range(30000, 150000)),
        "department": Column(str, checks=Check.isin(["HR", "Tech", "Marketing", "Sales"])),
        "start_date": Column(pd.Timestamp, checks=Check(lambda x: x < pd.Timestamp("today"))),
        "performance_score": Column(float, nullable=True)
    },
    index=Index(int, name="employee_id")
)

# Custom check function
def salary_age_relation_check(df: pd.DataFrame) -> pd.DataFrame:
    if not all(df["salary"] / df["age"] < 3000):
        raise ValueError("Salary to age ratio check failed")
    return df

# Function to process and validate data
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    # Apply custom check
    df = salary_age_relation_check(df)

    # Validate DataFrame with Pandera schema
    return enhanced_schema.validate(df)
```

```python
df_example = pd.DataFrame({
    "employee_id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 35, 45],
    "email": ["alice@example.com", "bob@example.com", "charlie@example.com"],
    "salary": [50000, 80000, 120000],
    "department": ["HR", "Tech", "Sales"],
    "start_date": [Timestamp("2022-01-01"), Timestamp("2021-06-15"), Timestamp("2020-12-20")],
    "performance_score": [4.5, 3.8, 4.2]
})

# Make sure the employee_id column is the index
df_example.set_index("employee_id", inplace=True)

# Process and validate data
processed_df = process_data(df_example)
```

```console
SchemaError: expected series 'salary' to have type float64, got int64
```

### Statistical Hypothesis

```python
from scipy.stats import ttest_1samp

# Define the custom check for the salary column
def mean_salary_check(series: pd.Series, expected_mean: float = 75000, alpha: float = 0.05) -> bool:
    stat, p_value = ttest_1samp(series.dropna(), expected_mean)
    return p_value > alpha

salary_check = Check(mean_salary_check, element_wise=False, error="Mean salary check failed")

# Correctly update the checks for the salary column by specifying the column name
enhanced_schema.columns["salary"] = Column(float, checks=[Check.in_range(30000, 150000), salary_check], name="salary")
```

```python
# Change the salaries to exceede the expected mean of £75,000
df_example["salary"] = df_example["salary"] = [100000.0, 105000.0, 110000.0]
validated_df = enhanced_schema(df_example)
```

```console
SchemaError: <Schema Column(name=salary, type=DataType(float64))> failed series or dataframe validator 1:
<Check mean_salary_check: Mean salary check failed>
```

## :material-vector-link: References

- [Cultivating Data Integrity in Data Science with Pandera](https://towardsdatascience.com/cultivating-data-integrity-in-data-science-with-pandera-2289608626cc)
