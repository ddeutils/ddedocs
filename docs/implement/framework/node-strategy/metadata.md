# Metadata

## Schema Config

### Node

|     Column      | Data Type | PK | Description                             |
|:---------------:|-----------|:--:|-----------------------------------------|
|    node_name    | STRING    | Y  | Node process name                       |
| node_group_name | STRING    |    |                                         |
|    priority     | INTEGER   |    |                                         |
|    load_type    | STRING    |    |                                         |
| data_load_type  | STRING    |    | T, D, F, SCD1, SCD2_D, SCD2_F, SCD2_T   |
|     extras      | JSON      |    |                                         |
|   active_flag   | BOOLEAN   |    | Active flag for this config data        |
|    update_by    | STRING    |    | Who that add or update this config data |
|   update_date   | DATETIME  |    | Update datetime of this config data     |

### Node Dependency

|        Column        | Data Type | PK | Description                                                  |
|:--------------------:|-----------|:--:|--------------------------------------------------------------|
|      node_name       | STRING    | Y  | Node process name                                            |
| node_dependency_name | STRING    | Y  | Node process dependency name                                 |
| dependency_set_date  | INTEGER   |    | A number for decrease dependency process date before running |
|     active_flag      | BOOLEAN   |    | Active flag for this config data                             |
|      update_by       | STRING    |    | Who that add or update this config data                      |
|     update_date      | DATETIME  |    | Update datetime of this config data                          |


!!! note

    The `extras` field on the node table contain all of necessary node arguments;

    ```text
    extras
      ├─ files
      │   ├─ name
      │   ├─ path
      │   ├─ header
      │   ╰─ encoding
      ├─ storage
      │   ├─ system
      │   ╰─ container
      ╰─ framwork
          ├─ archiving
          ╰─ timeout
    ```

## Schema Data

### Node Logging

|    Column    | Data Type | PK | Description                             |
|:------------:|-----------|:--:|-----------------------------------------|
|  node_name   | STRING    | Y  | Node process name                       |
|  process_id  | INTEGER   | Y  |                                         |
|  start_date  | DATETIME  |    |                                         |
|   end_date   | DATETIME  |    |                                         |
| process_date | DATETIME  |    |                                         |
|    status    | STRING    |    | Success, Failed, Start                  |
|     log      | STRING    |    |                                         |
|   records    | JSON      |    |                                         |
|  update_by   | STRING    |    | Who that add or update this config data |
| update_date  | DATETIME  |    | Update datetime of this config data     |


!!! note

    The `records` field on the node log table contain all of necessary result records;

    ```text
    records
      ├─ src
      │   ├─ count
      │   ╰─ control_count
      ╰─ tgt
          ├─ count
          ╰─ control_count
    ```
