# UDFs

## Python UDFs

!!! warning

    Custom dependencies on DBR 16.2+, UC service credentials and batched execution
    on DBR 16.3+.

=== "Normal"

    ```sql
    CREATE OR REPLACE FUNCTION json_stringify(input_str STRING)
    RETURNS STRING
    LANGUAGE PYTHON
    ENVIRONMENT (
        dependencies = '["simplejson==3.19.*"]',
        environment_version = 'None'
    )
    AS $$
        import simplejson as json
        obj = {"input": input_str}
        return json.dumps(obj)
    $$;
    ```

    ```sql
    SELECT json_stringify('Hello from Python!');
    ```

=== "Batch"

    ```sql
    CREATE OR REPLACE FUNCTION batch_upper(vals ARRAY<STRING>)
    RETURNS ARRAY<STRING>
    LANGUAGE PYTHON
    ENVIRONMENT (
      dependencies = '["pandas==2.0.0"]',
      environment_version = 'None'
    )
    AS $$
    import pandas as pd

    def transform_batch(input_vals):
        df = pd.DataFrame({"value": input_vals})
        df["upper"] = df["value"].str.upper()
        return df["upper"].tolist()

    return transform_batch(vals)
    $$;
    ```

    ```sql
    SELECT
      id,
      batch_upper(collect_list(text_col)) AS upper_values
    FROM my_table
    GROUP BY id;
    ```

## References

- [SQL & Python go together: Unity Catalog Python UDFs with libraries](https://databrickster.medium.com/sql-python-go-together-unity-catalog-python-udfs-with-libraries-53099f454e49)
