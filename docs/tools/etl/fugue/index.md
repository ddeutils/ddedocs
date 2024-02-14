---
icon: material/chat-question-outline
---

# Fugue

[Fugue](https://github.com/fugue-project/fugue)

## Getting Started

```console
pip install fugue
```

## Examples

```python
import pandas as pd
from typing import Dict

input_df = pd.DataFrame({"id":[0,1,2], "value": (["A", "B", "C"])})
map_dict = {"A": "Apple", "B": "Banana", "C": "Carrot"}

def map_letter_to_food(df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
    df["value"] = df["value"].map(mapping)
    return df
```

```python
from pyspark.sql import SparkSession
from fugue import transform

spark = SparkSession.builder.getOrCreate()
sdf = spark.createDataFrame(input_df)

out = transform(
    sdf,
    map_letter_to_food,
    schema="*",
    params=dict(mapping=map_dict),
)
# out is a Spark DataFrame
out.show()
```

```text
+---+------+
| id| value|
+---+------+
|  0| Apple|
|  1|Banana|
|  2|Carrot|
+---+------+
```

## References

- https://towardsdatascience.com/introducing-fugue-reducing-pyspark-developer-friction-a702230455de
