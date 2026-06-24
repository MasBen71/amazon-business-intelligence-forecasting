from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class ForecastResult:
    forecast: pd.DataFrame
    metrics: pd.DataFrame


def _mape(y_true, y_pred) -> float:
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    mask = y_true != 0
    if mask.sum() == 0:
        return np.nan
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])))


def build_revenue_model() -> Pipeline:
    """Build a compact regression model suitable for small segment-level data."""
    numeric_features = ["year", "sales_lag_1", "operating_income_lag_1", "margin_lag_1"]
    categorical_features = ["segment"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    model = Ridge(alpha=1.0)
    return Pipeline(steps=[("preprocess", preprocessor), ("model", model)])


def train_test_backtest(features: pd.DataFrame, holdout_year: int | None = None) -> Tuple[Pipeline, pd.DataFrame]:
    """Train model and evaluate it on the latest available year by default."""
    df = features.dropna(subset=["sales_lag_1", "operating_income_lag_1", "margin_lag_1"]).copy()
    if holdout_year is None:
        holdout_year = int(df["year"].max())

    train = df[df["year"] < holdout_year]
    test = df[df["year"] == holdout_year]

    feature_cols = ["year", "segment", "sales_lag_1", "operating_income_lag_1", "margin_lag_1"]
    target_col = "net_sales_musd"

    model = build_revenue_model()
    model.fit(train[feature_cols], train[target_col])

    pred = model.predict(test[feature_cols])
    metrics = pd.DataFrame(
        [
            {
                "holdout_year": holdout_year,
                "mae_musd": mean_absolute_error(test[target_col], pred),
                "rmse_musd": float(np.sqrt(mean_squared_error(test[target_col], pred))),
                "mape": _mape(test[target_col], pred),
            }
        ]
    )

    # Refit on all available data for future forecasting.
    model.fit(df[feature_cols], df[target_col])
    return model, metrics


def forecast_revenue(features: pd.DataFrame, forecast_years=None) -> ForecastResult:
    """Forecast annual segment revenue recursively for future fiscal years."""
    if forecast_years is None:
        forecast_years = [2026, 2027, 2028]

    model, metrics = train_test_backtest(features)
    feature_cols = ["year", "segment", "sales_lag_1", "operating_income_lag_1", "margin_lag_1"]

    history = features.copy().sort_values(["segment", "year"])
    forecasts = []

    for year in forecast_years:
        latest = history.sort_values("year").groupby("segment").tail(1).copy()
        scoring = pd.DataFrame(
            {
                "year": year,
                "segment": latest["segment"].values,
                "sales_lag_1": latest["net_sales_musd"].values,
                "operating_income_lag_1": latest["operating_income_musd"].values,
                "margin_lag_1": latest["operating_margin"].values,
            }
        )
        scoring["forecast_net_sales_musd"] = model.predict(scoring[feature_cols])

        # Estimate operating income using the latest three-year average margin by segment.
        margin_assumption = (
            history.groupby("segment")
            .tail(3)
            .groupby("segment")["operating_margin"]
            .mean()
            .rename("assumed_operating_margin")
            .reset_index()
        )
        scoring = scoring.merge(margin_assumption, on="segment", how="left")
        scoring["forecast_operating_income_musd"] = (
            scoring["forecast_net_sales_musd"] * scoring["assumed_operating_margin"]
        )
        forecasts.append(scoring)

        # Add forecast to history for recursive lags.
        add = scoring.rename(
            columns={
                "forecast_net_sales_musd": "net_sales_musd",
                "forecast_operating_income_musd": "operating_income_musd",
            }
        )[["year", "segment", "net_sales_musd", "operating_income_musd"]]
        add["operating_expenses_musd"] = add["net_sales_musd"] - add["operating_income_musd"]
        add["operating_margin"] = add["operating_income_musd"] / add["net_sales_musd"]
        history = pd.concat([history, add], ignore_index=True)

    forecast_df = pd.concat(forecasts, ignore_index=True)
    return ForecastResult(forecast=forecast_df, metrics=metrics)
