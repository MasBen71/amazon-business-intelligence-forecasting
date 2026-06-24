import numpy as np
import pandas as pd


def add_segment_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create business KPIs for segment-level analysis."""
    out = df.copy().sort_values(["segment", "year"])

    out["operating_margin"] = out["operating_income_musd"] / out["net_sales_musd"]
    out["expense_ratio"] = out["operating_expenses_musd"] / out["net_sales_musd"]

    out["sales_yoy_growth"] = out.groupby("segment")["net_sales_musd"].pct_change()
    out["operating_income_yoy_growth"] = out.groupby("segment")["operating_income_musd"].pct_change()

    out["sales_lag_1"] = out.groupby("segment")["net_sales_musd"].shift(1)
    out["operating_income_lag_1"] = out.groupby("segment")["operating_income_musd"].shift(1)
    out["margin_lag_1"] = out.groupby("segment")["operating_margin"].shift(1)

    totals = out.groupby("year", as_index=False).agg(
        total_net_sales_musd=("net_sales_musd", "sum"),
        total_operating_income_musd=("operating_income_musd", "sum"),
    )
    out = out.merge(totals, on="year", how="left")
    out["revenue_share"] = out["net_sales_musd"] / out["total_net_sales_musd"]

    # Operating-income share can be unstable when total income is near zero or a segment is loss-making.
    out["operating_income_share"] = np.where(
        out["total_operating_income_musd"].abs() > 1e-9,
        out["operating_income_musd"] / out["total_operating_income_musd"],
        np.nan,
    )

    return out


def latest_year_summary(features: pd.DataFrame) -> pd.DataFrame:
    """Return the latest year, sorted by operating income contribution."""
    latest_year = int(features["year"].max())
    cols = [
        "year",
        "segment",
        "net_sales_musd",
        "operating_income_musd",
        "operating_margin",
        "revenue_share",
        "operating_income_share",
        "sales_yoy_growth",
    ]
    return (
        features.loc[features["year"].eq(latest_year), cols]
        .sort_values("operating_income_musd", ascending=False)
        .reset_index(drop=True)
    )
