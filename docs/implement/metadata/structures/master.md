# Master

| Field Name       |  Alias  | Data Type  | PK | Description                              |
|:-----------------|:-------:|:-----------|:--:|:-----------------------------------------|
| **business_id**  | buz_id  | STRING     | Y  | Business key that is the unique key      |
| **created_at**   | created | DATETIME   |    | Timestamp when the data was created      |
| **updated_at**   | updated | DATETIME   |    | Timestamp when the data was last updated |

## SCD1 (Full-Dump)

| Field Name       |   Alias   | Data Type  | PK | Description                                  |
|:-----------------|:---------:|:-----------|:--:|:---------------------------------------------|
| **business_id**  |  buz_id   | STRING     | Y  | Business key that is the unique key          |
| **deleted_flag** | deleted_f | BOOLEAN    |    | Delete flag that the data does not available |
| **created_at**   |  created  | DATETIME   |    | Timestamp when the data was created          |
| **updated_at**   |  updated  | DATETIME   |    | Timestamp when the data was last updated     |

## SCD2

| Field Name      |    Alias    | Data Type | PK  | Description                                                                              |
|:----------------|:-----------:|:----------|:---:|:-----------------------------------------------------------------------------------------|
| **id**          |     id      | STRING    |  Y  | Surrogate key that unique per row of data                                                |
| **business_id** |   buz_id    | STRING    |     | Business key that is the identify key for data when you fiter **active_flag** equal true |
| **active_flag** |  active_f   | BOOLEAN   |     | Active flag that the data is the current update                                          |
| **start_date**  | valid_start | DATETIME  |     | Timestamp when the data start to use                                                     |
| **end_date**    |  valid_end  | DATETIME  |     | Timestamp when the data end to use                                                       |
