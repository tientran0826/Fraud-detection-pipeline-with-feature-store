import pandas as pd


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
):

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")
