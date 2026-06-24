import pandas as pd
from .config import DATA_RAW

REQUIRED_COLUMNS = {
    "year",
    "segment",
    "net_sales_musd",
    "operating_expenses_musd",
    "operating_income_musd",
    "source",
}


def load_raw_data(path=DATA_RAW) -> pd.DataFrame:
    """Load Amazon segment data from CSV and validate the schema."""
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    numeric_cols = ["year", "net_sales_musd", "operating_expenses_musd", "operating_income_musd"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="raise")

    df["year"] = df["year"].astype(int)
    df["segment"] = df["segment"].astype(str)
    return df.sort_values(["segment", "year"]).reset_index(drop=True)
