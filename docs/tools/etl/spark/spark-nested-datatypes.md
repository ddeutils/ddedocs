# Spark Nested Data Types

In the previous [article](https://towardsdatascience.com/higher-order-functions-with-spark-3-1-7c6cf591beaa)
on Higher-Order Functions, we described three complex data types: arrays, maps,
and structs and focused on arrays in particular. In this follow-up article, we
will take a look at structs and see two important functions for transforming nested
data that were released in Spark 3.1.1 version. For the code, we will use Python
API.

## Struct

The `StructType` is a very important data type that allows representing nested
hierarchical data. It can be used to group some fields together. Each element
of a `StructType` is called StructField and it has a name and also a type. The
elements are also usually referred to just as fields or subfields, and they are
accessed by the name. The `StructType` is also used to represent the schema of the
entire DataFrame. Let’s see a simple example

```python
from pyspark.sql.types import *
my_schema = StructType([
    StructField('id', LongType()),
    StructField('country', StructType([
        StructField('name', StringType()),
        StructField('capital', StringType())
    ])),
    StructField('currency', StringType())
])
l = [
        (1, {'name': 'Italy', 'capital': 'Rome'}, 'euro'),
        (2, {'name': 'France', 'capital': 'Paris'}, 'euro'),
        (3, {'name': 'Japan', 'capital': 'Tokyo'}, 'yen')
    ]
df = spark.createDataFrame(l, schema=my_schema)
df.printSchema()
root
 |-- id: long (nullable = true)
 |-- country: struct (nullable = true)
 |    |-- name: string (nullable = true)
 |    |-- capital: string (nullable = true)
 |-- currency: string (nullable = true)

df.show()
+---+---------------+--------+
| id|        country|currency|
+---+---------------+--------+
|  1|  {Italy, Rome}|    euro|
|  2|{France, Paris}|    euro|
|  3| {Japan, Tokyo}|     yen|
+---+---------------+--------+
```

The created DataFrame has one struct `country` that has two subfields:
`name` and `capital`.

## Creating a struct

There are at least four basic ways how to create a `StructType` in the DataFrame.
The first one we have already seen above — create DataFrame from a local collection.
The second and very common way is that it will come by reading data from a source
that supports complex data structures, such as JSON or Parquet. Next, there are
some functions that will create a struct as a result. One particular example of
such transformation is grouping by a _**window**_ that will produce a struct with two
subfields `start` and `end` as you can see here:

```python
l = [(1, 10, '2021-01-01'), (2, 20, '2021-01-02')]
dx = spark.createDataFrame(l, ['id', 'price', 'date'])
(
    dx
    .groupBy(window('date', '1 day'))
    .agg(sum('price').alias('daily_price'))
).printSchema()
root
 |-- window: struct (nullable = false)
 |    |-- start: timestamp (nullable = true)
 |    |-- end: timestamp (nullable = true)
 |-- daily_price: long (nullable = true)
```

The fourth way how to create a struct is by using the function `struct()`. The
function will create a `StructType` from other columns that are passed as arguments
and the `StructFields` will have the same names as the original columns unless we
rename them using `alias()`:

```python
df.withColumn('my_struct', struct('id', 'currency')).printSchema()
root
 |-- id: long (nullable = true)
 |-- country: struct (nullable = true)
 |    |-- name: string (nullable = true)
 |    |-- capital: string (nullable = true)
 |-- currency: string (nullable = true)
 |-- my_struct: struct (nullable = false)
 |    |-- id: long (nullable = true)
 |    |-- currency: string (nullable = true)
```

Here, we created a column `my_struct` that has two subfields that are derived from
two columns that were present in the DataFrame.

## Accessing the elements

As we mentioned above the subfields of a struct are accessed by the name, and it
is done with a dot notation:

```python
df.select('country.capital').show()
+-------+
|capital|
+-------+
|   Rome|
|  Paris|
|  Tokyo|
+-------+
```

What might be not obvious is that this works also for arrays of structs. Let’s
assume that we have an array `countries` and each element of the array is a struct.
If we want to access only the `capital` subfield of each struct we would do it exactly
in the same way and the resulting column would be an array containing all capitals:

```python
my_new_schema = StructType([
    StructField('id', LongType()),
    StructField('countries', ArrayType(StructType([
        StructField('name', StringType()),
        StructField('capital', StringType())
    ])))
])
l = [(1, [
        {'name': 'Italy', 'capital': 'Rome'},
        {'name': 'Spain', 'capital': 'Madrid'}
    ])
]

dz = spark.createDataFrame(l, schema=my_new_schema)
# we have array of structs:
dz.show(truncate=False)
+---+--------------------------------+
|id |countries                       |
+---+--------------------------------+
|1  |[{Italy, Rome}, {Spain, Madrid}]|
+---+--------------------------------+
# access all capitals:
dz.select('countries.capital').show(truncate=False)
+--------------+
|capital       |
+--------------+
|[Rome, Madrid]|
+--------------+
```

For another specific example of accessing elements in nested structs inside array
see [:fontawesome-brands-stack-overflow: This](https://stackoverflow.com/questions/57810876/how-to-check-if-a-spark-data-frame-struct-array-contains-a-specific-value/57812763#57812763)
Stack Overflow question.

## Adding new elements

Adding a new subfield to an existing struct is supported since Spark 3.1 using
the function `withField()`. Let’s see our example in which we add the column `currency`
to the struct country:

```python
(
    df
        .withColumn(
            'country',
            col('country').withField('currency', col('currency'))
        )
).show(truncate=False)
+---+---------------------+--------+
|id |country              |currency|
+---+---------------------+--------+
|1  |{Italy, Rome, euro}  |euro    |
|2  |{France, Paris, euro}|euro    |
|3  |{Japan, Tokyo, yen}  |yen     |
+---+---------------------+--------+
```

Before Spark 3.1, the situation was more complex, and adding a new field to a struct
was possible by redefining the entire struct:

```python
new_df = (
  df.withColumn('country', struct(
    col('country.name'),
    col('country.capital'),
    col('currency')
  ))
)
```

As you can see, we had to list all the struct subfields and after that add the new
one — this can be quite cumbersome especially for large structs with many subfields.
In this case, there is however a nice trick by which you can handle all subfields
at once — using the star notation:

```python
new_df = (
  df.withColumn('country', struct(
    col('country.*'),
    col('currency')
  ))
)
```

The asterisk in the `country.*` will take all subfields of the original struct. The
situation will however become more complicated in the next example where we want
to remove a field.

## Removing elements

Dropping subfields from a struct is again a simple task since Spark 3.1 because
the function `dropFields()` was released. Let’s now work with the modified DataFrame
new_df where the struct contains three subfields `name`, `capital`, and `currency`.
Removing a subfield, for example, capital can be done as follows:

```python
new_df.withColumn('country',col('country').dropFields('capital')) \
.show(truncate=False)
+---+--------------+--------+
|id |country       |currency|
+---+--------------+--------+
|1  |{Italy, euro} |euro    |
|2  |{France, euro}|euro    |
|3  |{Japan, yen}  |yen     |
+---+--------------+--------+
```

As we can see the subfield `capital` was dropped. The situation gets complicated
again in previous versions before Spark 3.1 where we have to redefine the entire
struct and leave out the subfield that we want to drop:

```python
(
    new_df
    .withColumn('country', struct(
        col('country.name'),
        col('country.currency')
    ))
)
```

For large structs this is again tedious, so we can make this more feasible by
listing all the subfields as follows:

```python
# list all fields in the struct:
subfields = new_df.schema['country'].dataType.fieldNames()
# remove the subfield from the list:
subfields.remove('capital')
# use the new list to recreate the struct:
(
    new_df.withColumn(
        'country',
        struct(
            ['country.{}'.format(x) for x in subfields]
        )
    )
).show()
+---+--------------+--------+
| id|       country|currency|
+---+--------------+--------+
|  1| {Italy, euro}|    euro|
|  2|{France, euro}|    euro|
|  3|  {Japan, yen}|     yen|
+---+--------------+--------+
```

Notice that both functions `withField` and `dropFields` are members of the Column class,
therefore they are called as methods on the column object (to understand more how
methods from the _**Column**_ class are used, check my recent [article](https://towardsdatascience.com/a-decent-guide-to-dataframes-in-spark-3-0-for-beginners-dcc2903345a5)
where I discuss it more in detail).

## Structs in SQL expressions

When you check the _**SQL**_ documentation you will find that there are two functions
that can be used to create structs, namely, it is `struct()` and `named_struct()` and
they differ in the syntax because named_struct requires also passing a name for
each subfield:

```python
(
  df
  .selectExpr("struct(id, currency) as my_struct")
).show(truncate=False)
+---------+
|my_struct|
+---------+
|{1, euro}|
|{2, euro}|
|{3, yen} |
+---------+
(
  df.selectExpr(
    "named_struct('id', id, 'currency', currency) as my_struct")
).show()
+---------+
|my_struct|
+---------+
|{1, euro}|
|{2, euro}|
| {3, yen}|
+---------+
```

## Conclusion

In this article, we continued our description of complex data types in Spark SQL.
In the previous [article](https://towardsdatascience.com/higher-order-functions-with-spark-3-1-7c6cf591beaa),
we covered arrays, here we focused on structs, and in the future post, we will cover maps.
We have seen two important functions `withField()`and `dropFields()` that were
released in the recent version 3.1.1 and that can simplify the code quite a bit
when manipulating subfields of an existing struct.

## References

- https://towardsdatascience.com/nested-data-types-in-spark-3-1-663e5ed2f2aa
