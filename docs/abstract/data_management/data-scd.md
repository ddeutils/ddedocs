# Slowly Changing Dimension

## :material-arrow-down-right: Getting Started

A **Slowly Changing Dimension (SCD)** is a dimension that stores and manages both
current and historical data over time in a data warehouse.

## :material-format-list-bulleted: Types

### Type 1 (Overwriting)

If a record in a dimension table changes, the existing record is updated or overwritten.
Otherwise, the new record is inserted into the dimension table. This means records
in the dimension table always reflect the current state and no historical data
is maintained.

### Type 2 (History Row-Based)

While having a table that reflects only the current state may be useful, there are
times when it’s convenient, and even essential, to track historical changes to a
dimension.
With SCD type 2, historical data is maintained by adding a new row when a dimension
changes and properly denoting this new row as current while denoting the newly
historical record accordingly.

However, a couple of metadata fields are required in order to track changes:

| Column       | Description                                                                           | Alias                    |
|--------------|---------------------------------------------------------------------------------------|--------------------------|
| `is_current` | Whether the record has the currently valid information for the specific product code. | CurrentFlag              |
| `valid_from` | The timestamp from which the record was/is current.                                   | EffectiveData, StartDate |
| `valid_to`   | The timestamp until which the record was/is current.                                  | EndDate                  |
| `is_deleted` | Whether the product code no longer exists in the source data.                         | DeleteFlag               |

### Type 3 (History Column-Based)

| Column           | Description                       | Alias         |
|------------------|-----------------------------------|---------------|
| `current_field`  | The current value of this field.  |               |
| `previous_field` | The previous value of this field. | OriginalField |

### Type 4 (History Table)

This method resembles how database audit tables and **change data capture** techniques
function.

### Type 5 (4 + 1)

The type 5 technique builds on the type 4 mini-dimension by embedding a
"current profile" mini-dimension key in the base dimension that's overwritten as
a type 1 attribute.

### Type 6 (1 + 2 + 3)

### Type 7 (Hybrid)

An alternative implementation is to place both the surrogate key and the natural
key into the fact table.

## :material-playlist-plus: Read Mores

- [:simple-medium: Unlocking the Secrets of Slowly Changing Dimension (SCD): A Comprehensive View of 8 Types](https://towardsdatascience.com/unlocking-the-secrets-of-slowly-changing-dimension-scd-a-comprehensive-view-of-8-types-a5ea052e4b36)
- [:simple-medium: Navigating Slowly Changing Dimensions (SCD) and Data Restatement: A Comprehensive Guide](https://towardsdatascience.com/navigating-slowly-changing-dimensions-scd-and-data-reinstatement-a-comprehensive-guide-f8b72ff90d98)
- [:material-wikipedia: Wikipedia: Slowly changing dimension](https://en.wikipedia.org/wiki/Slowly_changing_dimension)
