from pathlib import Path

import pandas as pd

from src.config import DATA_PROCESSED, REPORT_PATH
from src.data_loader import load_raw_data
from src.features import add_segment_features, latest_year_summary
from src.modeling import forecast_revenue
from src.visualization import plot_forecast, plot_margin_trend, plot_revenue_trend


def money_b(value_musd: float) -> str:
    return f"${value_musd / 1000:,.1f}B"


def pct(value: float) -> str:
    return f"{value * 100:,.1f}%"


def build_report(features: pd.DataFrame, forecast: pd.DataFrame, metrics: pd.DataFrame) -> str:
    latest = latest_year_summary(features)
    latest_year = int(latest["year"].iloc[0])
    top_profit = latest.iloc[0]
    top_revenue = latest.sort_values("net_sales_musd", ascending=False).iloc[0]

    total_sales = latest["net_sales_musd"].sum()
    total_income = latest["operating_income_musd"].sum()

    forecast_total = forecast.groupby("year", as_index=False)["forecast_net_sales_musd"].sum()
    final_forecast = forecast_total.iloc[-1]

    lines = [
        "# Executive Summary",
        "",
        f"Latest fiscal year in the dataset: **{latest_year}**.",
        "",
        "## Latest-year business snapshot",
        "",
        f"- Total segment net sales: **{money_b(total_sales)}**.",
        f"- Total segment operating income: **{money_b(total_income)}**.",
        f"- Largest revenue segment: **{top_revenue['segment']}** with **{money_b(top_revenue['net_sales_musd'])}** in net sales.",
        f"- Largest operating-income segment: **{top_profit['segment']}** with **{money_b(top_profit['operating_income_musd'])}** in operating income.",
        f"- AWS operating margin in {latest_year}: **{pct(float(latest.loc[latest['segment'].eq('AWS'), 'operating_margin'].iloc[0]))}**.",
        "",
        "## Forecasting result",
        "",
        f"- Revenue forecast for {int(final_forecast['year'])}: **{money_b(final_forecast['forecast_net_sales_musd'])}** total segment net sales.",
        f"- Backtest MAE: **{money_b(float(metrics['mae_musd'].iloc[0]))}**.",
        f"- Backtest RMSE: **{money_b(float(metrics['rmse_musd'].iloc[0]))}**.",
        f"- Backtest MAPE: **{pct(float(metrics['mape'].iloc[0]))}**.",
        "",
        "## Interpretation",
        "",
        "Amazon's North America segment remains the largest source of net sales. However, AWS has historically delivered much higher operating margins and contributes a disproportionate share of operating income. International profitability improved in the latest years, but remains much smaller than AWS in profit contribution.",
        "",
        "## Methodological note",
        "",
        "This model uses annual data and should be treated as a portfolio forecasting demonstration, not as an investment model. A production-grade version should include quarterly data, macroeconomic variables, cloud market indicators, advertising revenue, capital expenditure, and model uncertainty intervals.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    raw = load_raw_data()
    features = add_segment_features(raw)
    DATA_PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(DATA_PROCESSED, index=False)

    result = forecast_revenue(features)
    result.forecast.to_csv(DATA_PROCESSED.parent / "amazon_segment_forecast.csv", index=False)
    result.metrics.to_csv(DATA_PROCESSED.parent / "model_backtest_metrics.csv", index=False)

    plot_revenue_trend(features)
    plot_margin_trend(features)
    plot_forecast(features, result.forecast)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(build_report(features, result.forecast, result.metrics), encoding="utf-8")

    print("Pipeline complete.")
    print(f"Processed features: {DATA_PROCESSED}")
    print(f"Executive summary: {REPORT_PATH}")


if __name__ == "__main__":
    main()
