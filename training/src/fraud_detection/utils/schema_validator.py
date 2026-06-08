import pandas as pd


def validate_columns(
    df: pd.DataFrame,
    required_columns: list[str],
):

    missing = set(required_columns) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")


def validate_schema(
    df: pd.DataFrame,
    schema,
) -> None:
    """
    Validate dataframe against schema.
    """

    missing = set(schema.REQUIRED_COLUMNS) - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    for column, expected_dtype in schema.COLUMNS.items():
        actual_dtype = str(df[column].dtype)

        if actual_dtype != expected_dtype:
            raise ValueError(
                f"Column '{column}' has dtype "
                f"'{actual_dtype}' "
                f"but expected "
                f"'{expected_dtype}'"
            )
