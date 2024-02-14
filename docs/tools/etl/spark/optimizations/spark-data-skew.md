# Spark: _Data Skew_

**Data skew** in Spark occurs when one or a few partitions have much more data than
others. It usually happens during shuffling operations (like `.join` or `.agg`)
when a disproportionate amount of data gets assigned to certain keys.

Skewed data can lead to a few tasks taking much longer to run than others, resulting
in inefficient resource utilization and increased overall processing time.

**Consequences of Data Skew**:

- Performance Bottleneck: Tasks dealing with larger partitions take disproportionately
  longer to complete, causing other tasks and resources to idle.

- Out of Memory (OOM) Errors: Excessive data in certain tasks can lead to memory
  overflow, causing OOM errors and task failures.

## Handling Data Skew

### Salting Keys

**Salting** involves adding a random value to the join key, which helps distribute
the data more evenly across the partitions.

!!! note

    Use salting in join operations where you have a skewed key. By appending a
    random value to the key, you can prevent a large number of values from being
    mapped to the same key.

!!! example

    If joining on a highly skewed customer ID, append a random number
    (like customer ID + “_1”, customer ID + “_2”, etc.) to distribute the load.

    !!! quote

        **Problem**: A significant data skew is present with customer_id = 123.

    **Original Datasets**:

    === "ordersDF"

        ```text
        | order_id | customer_id | amount |
        +----------+-------------+--------+
        | O1       | 123         | 150    |
        | O2       | 123         | 200    |
        | O3       | 456         | 50     |
        | O4       | 789         | 100    |
        | O5       | 123         | 300    |
        ```

    === "customersDF"

        ```text
        | customer_id | name      |
        +-------------+-----------+
        | 123         | John Doe  |
        | 456         | Tom Smith |
        | 789         | Bob Brown |
        ```

    **Applying Salting Technique**:

    1. Modify customer_id by appending a random number

        === "ordersDF"

            ```text
            | order_id | customer_id_salted | amount |
            +----------+--------------------+--------+
            | O1       | 123_1              | 150    |
            | O2       | 123_2              | 200    |
            | O3       | 456_1              | 50     |
            | O4       | 789_1              | 100    |
            | O5       | 123_1              | 300    |
            ```

        === "customersDF"

            ```text
            | customer_id_salted | name      |
            +--------------------+-----------+
            | 123_1              | John Doe  |
            | 123_2              | John Doe  |
            | 456_1              | Tom Smith |
            | 789_1              | Bob Brown |
            ```

    2. Perform the Join Operation

        After joining `ordersDF` with `customersDF` on `customer_id_salted`,
        the skew towards `customer_id = 123` is reduced as the orders for this customer
        are now distributed across two keys (`123_1` and `123_2`).

    3. Remove the Salted Component

        After joining, you can remove the appended random number to get the original
        `customer_id`.

### Increasing Parallelism

Increasing the level of parallelism can help distribute skewed data across more
partitions.

!!! note

    Adjust the `spark.default.parallelism` and `spark.sql.shuffle.partitions` properties
    to increase the number of partitions.

!!! example

    For a large skewed dataset, increasing the shuffle partitions can help distribute
    data more evenly across the cluster.

    !!! quote

        **Problem**: A significant data skew is present in the sales dataset,
        particularly for a few region IDs, causing uneven load distribution.

    **Original Datasets**:

    === "salesDF"

        ```text
        | sale_id | region_id | amount |
        +---------+-----------+--------+
        | S1      | R1        | 500    |
        | S2      | R1        | 450    |
        | S3      | R2        | 300    |
        | S4      | R3        | 200    |
        | S5      | R1        | 550    |
        ```

    === "regionsDF"

        ```text
        | region_id | name  |
        +-----------+-------+
        | 1         | North |
        | 2         | South |
        | 3         | East  |
        ```

    **Increasing Parallelism**:

    1. Adjust Spark Configurations

        Increase the number of partitions by adjusting `spark.sql.shuffle.partitions`.
        Suppose we increase it from the default value to a higher number, say 50.

    2. Perform the Join Operation

        After adjusting the number of partitions, perform the join operation. The
        sales data will now be distributed across more partitions, reducing the
        load on individual tasks.

    **Effect of Increased Parallelism**:

    * By increasing the number of partitions, the data for the skewed key (`region_id = R1`)
      is spread across more tasks, preventing any single task from being overloaded.
    * This results in more uniform execution times across tasks and better resource
      utilization, improving overall performance.

Increasing parallelism is a straightforward way to mitigate the impact of data skew
in Spark applications. It does not alter the data itself but optimizes how data
is distributed and processed across the cluster. This strategy is particularly
effective when dealing with large datasets with skewed distributions, as it can
lead to more balanced workload distribution and prevent bottlenecks in specific
tasks.

### Broadcast Join for Skewed Keys

For a skewed join where one side of the join is much smaller than the other,
broadcasting the smaller table can prevent skew.

!!! note

    Force a broadcast join for the smaller DataFrame to avoid shuffling the larger
    DataFrame.

!!! example

    In a join between a large transactions table and a small customers table,
    broadcasting the customers table can avoid data skew.

    !!! quote

        **Problem**: A significant data skew is present in the product sales dataset
        for a few customer IDs, leading to inefficient processing during the join
        operation.

    **Original Datasets**:

    === "salesDF"

        ```text
        | sale_id | customer_id | amount |
        +---------+-------------+--------+
        | S1      | C123        | 600    |
        | S2      | C123        | 450    |
        | S3      | C456        | 150    |
        | S4      | C789        | 200    |
        | S5      | C123        | 250    |
        ```

    === "customersDF"

        ```text
        | customer_id | name      |
        +-------------+-----------+
        | C123        | John Doe  |
        | C456        | Tom Smith |
        | C789        | Bob Brown |
        ```

    **Using Broadcast Join**:

    1. Identify the Smaller DataFrame

        The `customersDF` is identified as the smaller DataFrame suitable for broadcasting.

    2. Perform the Broadcast Join

        Explicitly broadcast the `customersDF` during the join operation with `salesDF`.

        ```python
        from pyspark.sql.functions import broadcast

        joinedDF = (
            salesDF.join(
                broadcast(customersDF),
                on=(salesDF.customer_id == customersDF.customer_id)
            )
        )
        ```

    **Effect of Broadcast Join**:

    * By broadcasting the smaller `customersDF`, Spark sends this DataFrame to each
      node only once, significantly reducing the shuffle needed for the join.
    * The skew in `salesDF` is less impactful, as the larger dataset does not need
      to be shuffled. This results in a more efficient join operation, especially
      when the skew is present in the larger DataFrame.

Utilizing a Broadcast Join is particularly effective in scenarios where one of the
DataFrames involved in the join is significantly smaller and can fit into the memory
of each worker node. This technique is a powerful tool to combat the challenges
posed by data skew, as it avoids the expensive operation of shuffling the larger
skewed DataFrame, leading to more efficient and faster join operations in Spark.

### Filtering and Splitting Skewed Keys

Identify skewed keys and process them separately from the rest of the data.

!!! note

    Filter out the skewed keys, process them separately, and then union the result
    with the rest of the processed data.

!!! example

    If a particular customer ID is responsible for most of the data, filter out
    this ID, perform necessary operations, and then union the result with the
    operations performed on the rest of the data.

    !!! quote

        **Problem**: In an e-commerce order dataset, there is significant skew due
        to a few customers placing an unusually high number of orders, resulting
        in inefficient processing during join operations.

    **Original Datasets**:

    === "ordersDF"

        ```text
        | order_id | customer_id | amount |
        +----------+-------------+--------+
        | O1       | 123         | 150    |
        | O2       | 123         | 200    |
        | O3       | 456         | 50     |
        | O4       | 789         | 100    |
        | O5       | 123         | 300    |
        ```

    === "customersDF"

        ```text
        | customer_id | name      |
        +-------------+-----------+
        | 123         | John Doe  |
        | 456         | Tom Smith |
        | 789         | Bob Brown |
        ```

    **Applying Filtering and Splitting Skewed Keys**:

    1. Identify the Skewed Key

        Detect the skewed key (e.g., `customer_id = 123`) causing the skew.

    2. Split and Process the Data

      * Filter out the skewed key from the main DataFrame and process these records separately.
      * Perform join operations on the non-skewed part and the skewed part independently.
      * Union the results to get the final output.

    **Effect of Filtering and Splitting Skewed Keys**:

    * By separating the skewed data (customer_id = C100), the join operation is more balanced and efficient.
    * The skewed part can be processed using specialized strategies, such as increasing parallelism or using broadcast joins, to manage the heavier load.
    * This approach leads to better performance and resource utilization during the join operation.

Filtering and splitting skewed keys is an effective strategy to address data skew
in Spark. It involves identifying the skew-causing keys, processing the skewed
and non-skewed data separately, and then combining the results. This method not
only alleviates the impact of skew on performance but also offers the flexibility
to apply different optimization techniques to the skewed subset of the data.
It’s particularly useful in scenarios where a small subset of keys disproportionately
affects the performance of join operations.

### Custom Partitioning

Use custom partitioning logic to distribute data more evenly across partitions.

!!! note

    Implement a custom partitioner that can distribute data more uniformly, even
    when dealing with skewed keys.

!!! example

    Create a partitioner that assigns data to partitions based on a custom logic
    that accounts for the skewness in the key distribution.

    !!! quote

        **Problem**: In a large transaction dataset, there is significant skew due
        to a few customers having a disproportionately high number of transactions,
        leading to inefficient processing during join operations.

    === "transactionsDF"

        ```text
        | transaction_id | customer_id | amount |
        +----------------+-------------+--------+
        | T1             | 123         | 150    |
        | T2             | 123         | 200    |
        | T3             | 456         | 50     |
        | T4             | 789         | 100    |
        | T5             | 123         | 300    |
        ```

    === "customersDF"

        ```text
        | customer_id | name    |
        +-------------+---------+
        | 123         | Alice   |
        | 456         | Bob     |
        | 789         | Charlie |
        ```

    **Applying Custom Partitioning**:

    1. Define Custom Partitioning Logic

        Create a custom partitioner that distributes the data based on some logic
        that accounts for the skew. For example, you might create partitions based
        on a hash of the `customer_id` or use some domain knowledge to distribute
        the data more evenly.

    2. Apply Custom Partitioning to DataFrames

        Apply this custom partitioning to both `transactionsDF` and `customerDF` before
        the join operation. This ensures that the data for each customer is distributed
        across multiple partitions if needed.

    **Effect of Custom Partitioning**:

    * By using custom partitioning, the transactions for the heavily skewed `customer_id` (e.g., C001)
      are distributed across multiple partitions.
    * This results in a more even distribution of the workload across the cluster,
      preventing individual tasks from becoming bottlenecks due to processing a large portion of skewed data.
    * Custom partitioning leads to better parallelism and more efficient utilization
      of cluster resources during the join operation.

Custom partitioning in Spark is a powerful technique to address data skew, especially
in large-scale join operations. By distributing data more evenly across partitions
based on a custom-defined logic, it mitigates the impact of skew and ensures more
balanced processing. This approach requires an understanding of the data distribution
and might involve some experimentation to identify the most effective partitioning
strategy. However, when properly implemented, custom partitioning can significantly
enhance the performance and efficiency of Spark applications dealing with skewed
datasets.

## References

- [:simple-medium: Spark - Data Skew Odyssey Conquering the Chaos](https://medium.com/@BharathkumarV/sparks-data-skew-odyssey-conquering-the-chaos-d7c3c03e6121)
- [:simple-medium: Spark Data Skew Solution (With Examples)](https://medium.com/@patrickwork0001/spark-data-skew-solution-with-examples-5643c9402938)
