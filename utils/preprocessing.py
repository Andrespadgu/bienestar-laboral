import pandas as pd


def get_summary(df: pd.DataFrame) -> dict:
    return {
        "filas": df.shape[0],
        "columnas": df.shape[1],
        "nulos_totales": df.isnull().sum().sum(),
        "duplicados": df.duplicated().sum(),
        "tipos": df.dtypes.value_counts().to_dict(),
    }


def clean_nulls(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
    if strategy == "drop":
        return df.dropna()
    elif strategy == "mean":
        return df.fillna(df.mean(numeric_only=True))
    return df
