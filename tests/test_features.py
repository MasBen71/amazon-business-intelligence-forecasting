import pandas as pd

from src.features import add_segment_features


def test_add_segment_features_basic_columns():
    df = pd.DataFrame(
        {
            "year": [2020, 2020, 2021, 2021],
            "segment": ["A", "B", "A", "B"],
            "net_sales_musd": [100, 200, 120, 250],
            "operating_expenses_musd": [80, 190, 90, 220],
            "operating_income_musd": [20, 10, 30, 30],
            "source": ["test"] * 4,
        }
    )
    out = add_segment_features(df)
    assert "operating_margin" in out.columns
    assert "revenue_share" in out.columns
    assert "sales_yoy_growth" in out.columns
    assert out.loc[(out["year"] == 2020) & (out["segment"] == "A"), "operating_margin"].iloc[0] == 0.2


def test_revenue_share_sums_to_one_by_year():
    df = pd.DataFrame(
        {
            "year": [2020, 2020, 2021, 2021],
            "segment": ["A", "B", "A", "B"],
            "net_sales_musd": [100, 300, 200, 200],
            "operating_expenses_musd": [80, 250, 150, 170],
            "operating_income_musd": [20, 50, 50, 30],
            "source": ["test"] * 4,
        }
    )
    out = add_segment_features(df)
    shares = out.groupby("year")["revenue_share"].sum().round(6)
    assert all(shares == 1.0)
