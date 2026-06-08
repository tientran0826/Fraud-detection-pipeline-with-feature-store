import numpy as np
import pandas as pd


def build_features(
    df: pd.DataFrame,
) -> pd.DataFrame:

    df = df.copy()

    df["Amount_log"] = np.log1p(df["Amount"])

    df["Amount_sqrt"] = np.sqrt(df["Amount"])

    seconds_per_day = 86400

    df["Hour"] = ((df["Time"] % seconds_per_day) // 3600).astype(int)

    df["Day"] = (df["Time"] // seconds_per_day).astype(int)

    df["V1_V2"] = df["V1"] * df["V2"]

    df["V4_V11"] = df["V4"] * df["V11"]

    df["V10_V14"] = df["V10"] * df["V14"]

    return df
