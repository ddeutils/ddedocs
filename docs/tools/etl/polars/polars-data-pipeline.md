# Polars: _Data Pipeline_

**Polars** way of working with data lends itself quite nicely to building scalable data
pipelines. First of all, the fact that we can chain the methods so easily allows
for some fairly complicated pipelines to be written quite elegantly.

Notice that these functions take a Polars DataFrame as input (together with some
other arguments) and output already altered Polars Data Frame. Chaining these
methods together is a piece of cake with `.pipe()`.

```python
import poloars as pl

def process_date(df, date_column, format):
    result = df.with_columns(pl.col(date_column).str.to_date(format))
    return result


def filter_year(df, date_column, year):
    result = df.filter(pl.col(date_column).dt.year() == year)
    return result


def get_first_by_month(df, date_column, metric):
    result = df.with_columns(
        pl.col(metric)
        .rank(method="ordinal", descending=True)
        .over(pl.col(date_column).dt.month())
        .alias("rank")
    ).filter(pl.col("rank") == 1)

    return result

def select_data_to_write(df, columns):
    result = df.select([pl.col(c) for c in columns])
    return result
```

=== "Normal"

    ```python
    (
        pl.read_csv('folder/file.csv')
            .pipe(process_date, date_column="trending_date", format="%y.%d.%m")
            .pipe(filter_year, date_column="trending_date", year=2018)
            .pipe(get_first_by_month, date_column="trending_date", metric="views")
            .pipe(
                select_data_to_write,
                columns=["trending_date", "title", "channel_title", "views"],
            )
    ).write_parquet("top_monthly_videos.parquet")
    ```

=== "Lazy"

    ```python
    (
        pl.scan_csv('folder/file.csv')
            .pipe(process_date, date_column="trending_date", format="%y.%d.%m")
            .pipe(filter_year, date_column="trending_date", year=2018)
            .pipe(get_first_by_month, date_column="trending_date", metric="views")
            .pipe(
                select_data_to_write,
                columns=["trending_date", "title", "channel_title", "views"],
            )
    ).collect().write_parquet("top_monthly_videos.parquet")
    ```

## Example: Machine Learning Features

![Data Pipeline Flow](./images/polars-data-pipeline-example.png)

=== "Reading"

    ```yaml
    data_path: "./youtube/videos.csv"
    category_map_path: "./youtube/category_id.json"
    ```

    ```python
    def read_category_mappings(path: str) -> Dict[int, str]:
        with open(path, "r") as f:
            categories = json.load(f)

        id_to_category = {}
        for c in categories["items"]:
            id_to_category[int(c["id"])] = c["snippet"]["title"]

        return id_to_category
    ```

=== "Data Cleaning"

    ```yaml
    # Pre-processing config
    date_column_format:
      trending_date: "%y.%d.%m"
      publish_time: "%Y-%m-%dT%H:%M:%S%.fZ"
    ```

    ```python
    def parse_dates(date_cols: Dict[str, str]) -> List[pl.Expr]:
        expressions = []
        for date_col, fmt in date_cols.items():
            expressions.append(pl.col(date_col).str.to_date(format=fmt))

        return expressions

    def map_dict_columns(
        mapping_cols: Dict[str, Dict[str | int, str | int]]
    ) -> List[pl.Expr]:
        expressions = []
        for col, mapping in mapping_cols.items():
            expressions.append(pl.col(col).map_dict(mapping))
        return expressions

    def clean_data(
        df: pl.DataFrame,
        date_cols_config: Dict[str, str],
        mapping_cols_config: Dict[str, Dict[str | int, str | int]],
    ) -> pl.DataFrame:
        parse_dates_expressions = parse_dates(date_cols=date_cols_config)
        mapping_expressions = map_dict_columns(mapping_cols_config)

        df = df.with_columns(parse_dates_expressions + mapping_expressions)
        return df
    ```

=== "Basic Feature"

    ```yaml
    # Feature engineering config
    ratio_features:
      # feature name
      likes_to_dislikes:
        # features used in calculation
        - likes
        - dislikes
      likes_to_views:
        - likes
        - views
      comments_to_views:
        - comment_count
        - views

    difference_features:
      days_to_trending:
        - trending_date
        - publish_time

    date_features:
      trending_date:
        - weekday
    ```

    ```python
    def ratio_features(features_config: Dict[str, List[str]]) -> List[pl.Expr]:
        expressions = []
        for name, cols in features_config.items():
            expressions.append((pl.col(cols[0]) / pl.col(cols[1])).alias(name))

        return expressions

    def diff_features(features_config: Dict[str, List[str]]) -> List[pl.Expr]:
        expressions = []
        for name, cols in features_config.items():
            expressions.append((pl.col(cols[0]) - pl.col(cols[1])).alias(name))

        return expressions

    def date_features(features_config: Dict[str, List[str]]) -> List[pl.Expr]:
        expressions = []
        for col, features in features_config.items():
            if "weekday" in features:
                expressions.append(pl.col(col).dt.weekday().alias(f"{col}_weekday"))
            if "month" in features:
                expressions.append(pl.col(col).dt.month().alias(f"{col}_month"))
            if "year" in features:
                expressions.append(pl.col(col).dt.year().alias(f"{col}_year"))

        return expressions

    def basic_feature_engineering(
        data: pl.DataFrame,
        ratios_config: Dict[str, List[str]],
        diffs_config: Dict[str, List[str]],
        dates_config: Dict[str, List[str]],
    ) -> pl.DataFrame:
        ratio_expressions = ratio_features(ratios_config)
        date_diff_expressions = diff_features(diffs_config)
        date_expressions = date_features(dates_config)

        data = data.with_columns(
            ratio_expressions + date_diff_expressions + date_expressions
        )
        return data
    ```

=== "Data Transform"

    ```yaml
    # Filter videos
    max_time_to_trending: 60

    # Features to join to the transformed data
    base_columns:
      - views
      - likes
      - dislikes
      - comment_count
      - comments_disabled
      - ratings_disabled
      - video_error_or_removed
      - likes_to_dislikes
      - likes_to_views
      - comments_to_views
      - trending_date_weekday
      - channel_title
      - tags
      - description
      - category_id

    # Use these columns to join transformed data with original
    join_columns:
      - video_id
      - trending_date
    ```

    ```python
    def join_original_features(
        main: pl.DataFrame,
        original: pl.DataFrame,
        main_join_cols: List[str],
        original_join_cols: List[str],
        other_cols: List[str],
    ) -> pl.DataFrame:
        original_features = original.select(original_join_cols + other_cols).unique(
            original_join_cols
        )  # unique ensures one row per video + date
        main = main.join(
            original_features,
            left_on=main_join_cols,
            right_on=original_join_cols,
            how="left",
        )
        return main

    def create_target_df(
        df: pl.DataFrame,
        time_to_trending_thr: int,
        original_join_cols: List[str],
        other_cols: List[str],
    ) -> pl.DataFrame:
        # Create a DF with video ID per row and corresponding days to trending and days in trending (target)
        target = (
            df.groupby(["video_id"])
            .agg(
                pl.col("days_to_trending").min().dt.days(),
                pl.col("trending_date").min().dt.date().alias("first_day_in_trending"),
                pl.col("trending_date").max().dt.date().alias("last_day_in_trending"),
                # our TARGET
                (pl.col("trending_date").max() - pl.col("trending_date").min()).dt.days().alias("days_in_trending"),
            )
            .filter(pl.col("days_to_trending") <= time_to_trending_thr)
        )

        # Join features to the aggregates
        target = join_original_features(
            main=target,
            original=df,
            main_join_cols=["video_id", "first_day_in_trending"],
            original_join_cols=original_join_cols,
            other_cols=other_cols,
        )
        return target
    ```

=== "Advanced Agg"

    ```yaml
    aggregate_windows:
      - 7
      - 30
      - 180
    ```

    ```python
    def build_channel_rolling(df: pl.DataFrame, date_col: str, period: int) -> pl.DataFrame:
        channel_aggs = (
            df.sort(date_col)
            .groupby_rolling(
                index_column=date_col,
                period=f"{period}d",
                by="channel_title",
                closed="left",  # only left to not include the actual day
            )
            .agg(
                pl.col("video_id").n_unique().alias(f"channel_num_trending_videos_last_{period}_days"),
                pl.col("days_in_trending").max().alias(f"channel_max_days_in_trending_{period}_days"),
                pl.col("days_in_trending").mean().alias(f"channel_avg_days_in_trending_{period}_days"),
            )
            .fill_null(0)
        )
        return channel_aggs

    def add_rolling_features(
        df: pl.DataFrame, date_col: str, periods: List[int]
    ) -> pl.DataFrame:
        for period in periods:
            rolling_features = build_channel_rolling(df, date_col, period)
            df = df.join(rolling_features, on=["channel_title", "first_day_in_trending"])
        return df
    ```

=== "Period Agg"

    ```yaml
    aggregate_windows:
      - 7
      - 30
      - 180
    ```

    ```python
    def build_period_features(df: pl.DataFrame, date_col: str, period: int) -> pl.DataFrame:
        general_aggs = (
            df.sort(date_col)
            .groupby_dynamic(
                index_column=date_col,
                every="1d",
                period=f"{period}d",
                closed="left",
            )
            .agg(
                pl.col("video_id").n_unique().alias(f"general_num_trending_videos_last_{period}_days"),
                pl.col("days_in_trending").max().alias(f"general_max_days_in_trending_{period}_days"),
                pl.col("days_in_trending").mean().alias(f"general_avg_days_in_trending_{period}_days"),
            )
            .with_columns(
                # shift match values with previous period
                pl.col(f"general_num_trending_videos_last_{period}_days").shift(period),
                pl.col(f"general_max_days_in_trending_{period}_days").shift(period),
                pl.col(f"general_avg_days_in_trending_{period}_days").shift(period),
            )
            .fill_null(0)
        )
        return general_aggs

    def add_period_features(
        df: pl.DataFrame, date_col: str, periods: List[int]
    ) -> pl.DataFrame:
        for period in periods:
            rolling_features = build_period_features(df, date_col, period)
            df = df.join(rolling_features, on=["first_day_in_trending"])
        return df
    ```

??? full-examples

    ```yaml title="pipe_config.yaml"
    data_path: "./youtube/videos.csv"
    category_map_path: "./youtube/category_id.json"

    date_column_format:
      trending_date: "%y.%d.%m"
      publish_time: "%Y-%m-%dT%H:%M:%S%.fZ"

    # Feature engineering config
    ratio_features:
      # feature name
      likes_to_dislikes:
        # features used in calculation
        - likes
        - dislikes
      likes_to_views:
        - likes
        - views
      comments_to_views:
        - comment_count
        - views

    difference_features:
      days_to_trending:
        - trending_date
        - publish_time

    date_features:
      trending_date:
        - weekday

    # Filter videos
    max_time_to_trending: 60

    # Features to join to the transformed data
    base_columns:
      - views
      - likes
      - dislikes
      - comment_count
      - comments_disabled
      - ratings_disabled
      - video_error_or_removed
      - likes_to_dislikes
      - likes_to_views
      - comments_to_views
      - trending_date_weekday
      - channel_title
      - tags
      - description
      - category_id

    # Use these columns to join transformed data with original
    join_columns:
      - video_id
      - trending_date

    aggregate_windows:
      - 7
      - 30
      - 180
    ```

    ```python
    import time
    import json
    from typing import Dict, List

    import yaml
    import polars as pl


    def read_category_mappings(path: str) -> Dict[int, str]:
        with open(path, "r") as f:
            categories = json.load(f)

        id_to_category = {}
        for c in categories["items"]:
            id_to_category[int(c["id"])] = c["snippet"]["title"]

        return id_to_category


    def parse_dates(date_cols: Dict[str, str]) -> List[pl.Expr]:
        expressions = []
        for date_col, fmt in date_cols.items():
            expressions.append(pl.col(date_col).str.to_date(format=fmt))

        return expressions


    def map_dict_columns(
        mapping_cols: Dict[str, Dict[str | int, str | int]]
    ) -> List[pl.Expr]:
        expressions = []
        for col, mapping in mapping_cols.items():
            expressions.append(pl.col(col).map_dict(mapping))
        return expressions


    def clean_data(
        df: pl.DataFrame,
        date_cols_config: Dict[str, str],
        mapping_cols_config: Dict[str, Dict[str | int, str | int]],
    ) -> pl.DataFrame:
        parse_dates_expressions = parse_dates(date_cols=date_cols_config)
        mapping_expressions = map_dict_columns(mapping_cols_config)

        df = df.with_columns(parse_dates_expressions + mapping_expressions)
        return df

    def ratio_features(features_config: Dict[str, List[str]]) -> List[pl.Expr]:
        expressions = []
        for name, cols in features_config.items():
            expressions.append((pl.col(cols[0]) / pl.col(cols[1])).alias(name))

        return expressions


    def diff_features(features_config: Dict[str, List[str]]) -> List[pl.Expr]:
        expressions = []
        for name, cols in features_config.items():
            expressions.append((pl.col(cols[0]) - pl.col(cols[1])).alias(name))

        return expressions

    def date_features(features_config: Dict[str, List[str]]) -> List[pl.Expr]:
        expressions = []
        for col, features in features_config.items():
            if "weekday" in features:
                expressions.append(pl.col(col).dt.weekday().alias(f"{col}_weekday"))
            if "month" in features:
                expressions.append(pl.col(col).dt.month().alias(f"{col}_month"))
            if "year" in features:
                expressions.append(pl.col(col).dt.year().alias(f"{col}_year"))

        return expressions

    def basic_feature_engineering(
        data: pl.DataFrame,
        ratios_config: Dict[str, List[str]],
        diffs_config: Dict[str, List[str]],
        dates_config: Dict[str, List[str]],
    ) -> pl.DataFrame:
        ratio_expressions = ratio_features(ratios_config)
        date_diff_expressions = diff_features(diffs_config)
        date_expressions = date_features(dates_config)

        data = data.with_columns(
            ratio_expressions + date_diff_expressions + date_expressions
        )
        return data


    def join_original_features(
        main: pl.DataFrame,
        original: pl.DataFrame,
        main_join_cols: List[str],
        original_join_cols: List[str],
        other_cols: List[str],
    ) -> pl.DataFrame:
        original_features = original.select(original_join_cols + other_cols).unique(
            original_join_cols
        )  # unique ensures one row per video + date
        main = main.join(
            original_features,
            left_on=main_join_cols,
            right_on=original_join_cols,
            how="left",
        )

        return main


    def create_target_df(
        df: pl.DataFrame,
        time_to_trending_thr: int,
        original_join_cols: List[str],
        other_cols: List[str],
    ) -> pl.DataFrame:
        # Create a DF with video ID per row and corresponding days to trending and days in trending (target)
        target = (
            df.groupby(["video_id"])
            .agg(
                pl.col("days_to_trending").min().dt.days(),
                pl.col("trending_date").min().dt.date().alias("first_day_in_trending"),
                pl.col("trending_date").max().dt.date().alias("last_day_in_trending"),
                # our TARGET
                (pl.col("trending_date").max() - pl.col("trending_date").min()).dt.days().alias("days_in_trending"),
            )
            .filter(pl.col("days_to_trending") <= time_to_trending_thr)
        )

        # Join features to the aggregates
        target = join_original_features(
            main=target,
            original=df,
            main_join_cols=["video_id", "first_day_in_trending"],
            original_join_cols=original_join_cols,
            other_cols=other_cols,
        )

        return target


    def build_channel_rolling(df: pl.DataFrame, date_col: str, period: int) -> pl.DataFrame:
        channel_aggs = (
            df.sort(date_col)
            .groupby_rolling(
                index_column=date_col,
                period=f"{period}d",
                by="channel_title",
                closed="left",  # only left to not include the actual day
            )
            .agg(
                pl.col("video_id").n_unique().alias(f"channel_num_trending_videos_last_{period}_days"),
                pl.col("days_in_trending").max().alias(f"channel_max_days_in_trending_{period}_days"),
                pl.col("days_in_trending").mean().alias(f"channel_avg_days_in_trending_{period}_days"),
            )
            .fill_null(0)
        )

        return channel_aggs


    def add_rolling_features(
        df: pl.DataFrame, date_col: str, periods: List[int]
    ) -> pl.DataFrame:
        for period in periods:
            rolling_features = build_channel_rolling(df, date_col, period)
            df = df.join(rolling_features, on=["channel_title", "first_day_in_trending"])

        return df


    def build_period_features(df: pl.DataFrame, date_col: str, period: int) -> pl.DataFrame:
        general_aggs = (
            df.sort(date_col)
            .groupby_dynamic(
                index_column=date_col,
                every="1d",
                period=f"{period}d",
                closed="left",
            )
            .agg(
                pl.col("video_id").n_unique().alias(f"general_num_trending_videos_last_{period}_days"),
                pl.col("days_in_trending").max().alias(f"general_max_days_in_trending_{period}_days"),
                pl.col("days_in_trending").mean().alias(f"general_avg_days_in_trending_{period}_days"),
            )
            .with_columns(
                # shift match values with previous period
                pl.col(f"general_num_trending_videos_last_{period}_days").shift(period),
                pl.col(f"general_max_days_in_trending_{period}_days").shift(period),
                pl.col(f"general_avg_days_in_trending_{period}_days").shift(period),
            )
            .fill_null(0)
        )

        return general_aggs


    def add_period_features(
        df: pl.DataFrame, date_col: str, periods: List[int]
    ) -> pl.DataFrame:
        for period in periods:
            rolling_features = build_period_features(df, date_col, period)
            df = df.join(rolling_features, on=["first_day_in_trending"])

        return df
    ```

```python
def pipeline():
    """Pipeline that reads, cleans, and transofrms data into
    the format we need for modelling
    """
    # Read and unwrap the config
    with open("pipe_config.yaml", "r") as file:
        pipe_config = yaml.safe_load(file)

    date_column_format = pipe_config["date_column_format"]
    ratios_config = pipe_config["ratio_features"]
    diffs_config = pipe_config["difference_features"]
    dates_config = pipe_config["date_features"]

    id_to_category = read_category_mappings(pipe_config["category_map_path"])
    col_mappings = {"category_id": id_to_category}

    output_data = (
        pl.scan_csv(pipe_config["data_path"])
        .pipe(clean_data, date_column_format, col_mappings)
        .pipe(basic_feature_engineering, ratios_config, diffs_config, dates_config)
        .pipe(
            create_target_df,
            time_to_trending_thr=pipe_config["max_time_to_trending"],
            original_join_cols=pipe_config["join_columns"],
            other_cols=pipe_config["base_columns"],
        )
        .pipe(
            add_rolling_features,
            "first_day_in_trending",
            pipe_config["aggregate_windows"],
        )
        .pipe(
            add_period_features,
            "first_day_in_trending",
            pipe_config["aggregate_windows"],
        )
    ).collect()

    return output_data


if __name__ == "__main__":
    t0 = time.time()
    output = pipeline()
    t1 = time.time()
    print("Pipeline took", t1 - t0, "seconds")
    print("Output shape", output.shape)
    print("Output columns:", output.columns)
    output.write_parquet("./data/modelling_data.parquet")
```

## Noted

Make sure to apply these learnings to your own data. I recommend starting small
(2–3 steps) and then expanding the pipeline as your needs grow. Make sure to keep
it modular, lazy, and group as many operations into `.with_columns()` as possible
to ensure proper parallelization.

## References

* [:simple-medium: TowardDS - Data Pipelines with Polars: Step-by-Step Guide](https://towardsdatascience.com/data-pipelines-with-polars-step-by-step-guide-f5474accacc4)
