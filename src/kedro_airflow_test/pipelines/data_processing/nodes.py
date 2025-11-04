"""Data processing nodes."""

import polars as pl


def process_data(input_data: pl.DataFrame) -> pl.DataFrame:
    """Process input data with Polars transformations.

    Args:
        input_data: Input Polars DataFrame from S3

    Returns:
        Processed Polars DataFrame
    """
    # Example transformations - filter, add columns, aggregate
    processed = (
        input_data
        .filter(pl.col("some_column") > 0)  # Filter out negative values
        .with_columns([
            (pl.col("numeric_col") * 2).alias("doubled_col"),
            pl.col("date_col").str.strptime(pl.Date, "%Y-%m-%d").dt.year().alias("year")
        ])
        .group_by("category_col")
        .agg([
            pl.col("doubled_col").sum().alias("total_doubled"),
            pl.col("doubled_col").mean().alias("avg_doubled"),
            pl.col("category_col").count().alias("count")
        ])
        .sort("total_doubled", descending=True)
    )

    return processed