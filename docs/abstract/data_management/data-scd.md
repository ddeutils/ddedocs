# Slowly Changing Dimension

## Getting Started

**Slowly Changing Dimension (SCD)**

## Types of SCD

### Type 2

Before I can implement a type 2 slowly changing dimension, I first fill the target
table with an initial data load. However, a couple of metadata fields are required
in order to track changes:

| Column       | Description                                                                           |
|--------------|---------------------------------------------------------------------------------------|
| `is_current` | Whether the record has the currently valid information for the specific product code. |
| `valid_from` | The timestamp from which the record was/is current.                                   |
| `valid_to`   | The timestamp until which the record was/is current.                                  |
| `is_deleted` | Whether the product code no longer exists in the source data.                         |

## Read Mores

- [:simple-medium: Unlocking the Secrets of Slowly Changing Dimension (SCD): A Comprehensive View of 8 Types](https://towardsdatascience.com/unlocking-the-secrets-of-slowly-changing-dimension-scd-a-comprehensive-view-of-8-types-a5ea052e4b36)
- [:simple-medium: Navigating Slowly Changing Dimensions (SCD) and Data Restatement: A Comprehensive Guide](https://towardsdatascience.com/navigating-slowly-changing-dimensions-scd-and-data-reinstatement-a-comprehensive-guide-f8b72ff90d98)
