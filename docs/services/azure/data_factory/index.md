# Azure Data Factory

## :material-arrow-down-right: Getting Started

## :material-code-tags: Syntax

### Coalesce

=== "Exists"

    ```json title="P_EXTRACT"
    {
        "parent": {
          "child": {
            "key": "value"
          }
        }
    }
    ```

    ```cs
    @coalesce(parameters.P_EXTRACT.parent.child?.key, 'default')
    ```

    Output:

    ```text
    value
    ```

=== "Not Exists"

    ```json title="P_EXTRACT"
    {
        "parent": {
          "child": {
            "foo": "bar"
          }
        }
    }
    ```

    ```cs
    @coalesce(parameters.P_EXTRACT.parent.child?.key, 'default')
    ```

    Output:

    ```text
    default
    ```

## :material-playlist-plus: Read Mores
