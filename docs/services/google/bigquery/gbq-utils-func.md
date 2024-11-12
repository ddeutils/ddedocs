# Utilities Function

## Text normaliser

```sql
CREATE OR REPLACE FUNCTION project.dataset.text_normaliser (x STRING)
RETURNS STRING
AS (
    TRIM(LOWER(
        REGEXP_REPLACE(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(
                            REGEXP_REPLACE(x, r"[éèêë]", "e"),
                                r"[áàâäãå]", "a"),
                            r"[ç]", "c"),
                        r"[ïîíì]", "i"),
                    r"[ôöòóõ]", "o"),
                r"[üùúû]", "u")
        )
    ))
);
```

```text
Input: ' CaFé '
Output: 'cafe'
```

## Unicode decoder

```sql
CREATE OR REPLACE FUNCTION project.dataset.unicode_to_fr (x STRING)
RETURNS STRING
AS (
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
    REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
    REPLACE(
    REPLACE(x, '\u00e9', 'é'),  -- é
           '\u00ea', 'ê'),       -- ê
           '\u00e0', 'à'),       -- à
           '\u00e8', 'è'),       -- è
           '\u00e2', 'â'),       -- â
           '\u00f4', 'ô'),       -- ô
           '\u00e7', 'ç'),       -- ç
           '\u00e9', 'é'),       -- é
           '\u00f9', 'ù'),       -- ù
           '\u00fb', 'û'),       -- û
           '\u00ee', 'î'),       -- î
           '\u00ef', 'ï'),       -- ï
           '\u00eb', 'ë'),       -- ë
           '\u00e4', 'ä'),       -- ä
           '\u00e3', 'ã'),       -- ã
           '\u00f6', 'ö'),       -- ö
           '\u00fc', 'ü'),       -- ü
           '\u00e5', 'å'),       -- å
           '\u2019', "'"),       -- ’
           '\u2013', "-")        -- –
);
```

```text
Input: “J\u2019adore coder, surtout cr\u00e9er des fonctions.
Output: J’adore coder, surtout créer des fonctions.
```

## A function that splits the string

```sql
CREATE OR REPLACE FUNCTION project.dataset.alpha_sort(input_string STRING, separator STRING)
RETURNS STRING
LANGUAGE js AS """
  if (input_string === null || input_string === '') {
    return '';
  }

  // Split the input string by the provided separator
  let splitArray = input_string.split(separator);

  // Trim any extra spaces around the items and sort alphabetically
  let sortedArray = splitArray.map(item => item.trim()).sort();

  // Join the sorted array back into a string using the provided separator
  return sortedArray.join(separator);
""";
```

```text
Input: 'banana|apple|cherry' and separator: '|'
Output: 'apple|banana|cherry'
```

## Number of days without weekends

```sql
CREATE OR REPLACE FUNCTION project.dataset.unicode_to_fr (x STRING)
RETURNS int64
AS
(DATE_DIFF(date(end_date), date(start_date), day) + 1)
    -(DATE_DIFF(date(end_date), date(start_date), week ) * 2) --minus weekends
    -(CASE WHEN FORMAT_DATE('%A',start_date) = 'Sunday' THEN 1 ELSE 0 END) --in case beginning or ending are weekends
    -(CASE WHEN FORMAT_DATE('%A', end_date) = 'Saturday' THEN 1 ELSE 0 END)
);
```

```text
Input: start_date = '2024-10-08' (Tuesday), end_date = '2024-10-14' (Monday)
Output: Weekdays: 5 (Tuesday to Monday, excluding the weekend)
```

## Number of days without weekends AND holidays

```sql
CREATE OR REPLACE FUNCTION project.dataset.nb_days_without_weekends_and_holidays (start_date timestamp, end_date timestamp, holiday_country string)
returns int64
as
 (
    -- Subquery to calculate the working days
   ( SELECT
      `project.dataset.nb_days_without_weekends`(start_date, end_date)
      - COALESCE(COUNT(holiday_date), 0) -- Handle cases with no holidays
    FROM (
      -- Subquery to select holidays
      SELECT holiday_date
      FROM `dataset_of_public_holidays`
      WHERE date(holiday_date) BETWEEN date(start_date) AND date(end_date)
        AND country = holiday_country
        AND EXTRACT(DAYOFWEEK FROM holiday_date) NOT IN (1, 7) -- Exclude weekends
        AND is_solidarity_day IS NULL
    ) AS holidays)
  )
```

```text
Input:start_date = '2024-11-10 00:00:00' (Sunday),end_date = '2024-11-15 23:59:59' (Friday),holiday_country = 'FR'
Output: Working Days: 5 (Monday to Friday, assuming November 11 (Armistice Day) is a holiday)
```

## Complete Years Difference

```sql
CREATE OR REPLACE FUNCTION project.dataset.complete_years_diff (start_date DATE, end_date DATE)
returns int64
as
 (
CASE
    WHEN EXTRACT(MONTH FROM end_date) > EXTRACT(MONTH FROM start_date)
      OR (EXTRACT(MONTH FROM end_date) = EXTRACT(MONTH FROM start_date)
          AND EXTRACT(DAY FROM end_date) >= EXTRACT(DAY FROM start_date))
    THEN EXTRACT(YEAR FROM end_date) - EXTRACT(YEAR FROM start_date)
    ELSE EXTRACT(YEAR FROM end_date) - EXTRACT(YEAR FROM start_date) - 1
  END
)
```

```text
Input: start_date = '2016-01-01' , end_date = '2024-01-01'
Output: Age: 8 (8 full years from January 1, 2016, to January 1, 2024)
```

## Read Mores

- [6 UDF ideas in BigQuery](https://blog.devgenius.io/6-udf-ideas-in-bigquery-funwithsql-918cf2dc6496)
