from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.data_loader import load_raw_data
from src.features import add_segment_features, latest_year_summary
from src.modeling import forecast_revenue

st.set_page_config(page_title="Amazon BI & Forecasting", layout="wide")

st.title("Amazon Business Intelligence & Revenue Forecasting")
st.caption("Segment-level analysis of North America, International, and AWS using public Amazon filings.")

raw = load_raw_data(ROOT / "data" / "raw" / "amazon_segment_annual_2019_2025.csv")
features = add_segment_features(raw)
forecast_result = forecast_revenue(features)
forecast = forecast_result.forecast
metrics = forecast_result.metrics

latest = latest_year_summary(features)
latest_year = int(features["year"].max())

st.sidebar.header("Controls")
selected_segments = st.sidebar.multiselect(
    "Segments",
    options=sorted(features["segment"].unique()),
    default=sorted(features["segment"].unique()),
)
filtered = features[features["segment"].isin(selected_segments)]
filtered_forecast = forecast[forecast["segment"].isin(selected_segments)]

col1, col2, col3 = st.columns(3)
col1.metric("Latest year", latest_year)
col2.metric("Total net sales", f"${latest['net_sales_musd'].sum() / 1000:,.1f}B")
col3.metric("Total operating income", f"${latest['operating_income_musd'].sum() / 1000:,.1f}B")

st.subheader("Segment revenue trend")
fig = px.line(
    filtered,
    x="year",
    y="net_sales_musd",
    color="segment",
    markers=True,
    labels={"net_sales_musd": "Net sales, USD millions", "year": "Fiscal year"},
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Operating margin")
margin_df = filtered.copy()
margin_df["operating_margin_pct"] = margin_df["operating_margin"] * 100
fig = px.line(
    margin_df,
    x="year",
    y="operating_margin_pct",
    color="segment",
    markers=True,
    labels={"operating_margin_pct": "Operating margin, %", "year": "Fiscal year"},
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Latest-year KPI table")
display_latest = latest.copy()
display_latest["operating_margin"] = display_latest["operating_margin"].map(lambda x: f"{x * 100:,.1f}%")
display_latest["revenue_share"] = display_latest["revenue_share"].map(lambda x: f"{x * 100:,.1f}%")
display_latest["operating_income_share"] = display_latest["operating_income_share"].map(lambda x: f"{x * 100:,.1f}%")
display_latest["sales_yoy_growth"] = display_latest["sales_yoy_growth"].map(lambda x: f"{x * 100:,.1f}%")
st.dataframe(display_latest, use_container_width=True)

st.subheader("Revenue forecast")
actual_plot = filtered[["year", "segment", "net_sales_musd"]].rename(columns={"net_sales_musd": "sales_musd"})
actual_plot["type"] = "Actual"
forecast_plot = filtered_forecast[["year", "segment", "forecast_net_sales_musd"]].rename(columns={"forecast_net_sales_musd": "sales_musd"})
forecast_plot["type"] = "Forecast"
combined = pd.concat([actual_plot, forecast_plot], ignore_index=True)
fig = px.line(
    combined,
    x="year",
    y="sales_musd",
    color="segment",
    line_dash="type",
    markers=True,
    labels={"sales_musd": "Net sales, USD millions", "year": "Fiscal year"},
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Model backtest metrics")
st.dataframe(metrics, use_container_width=True)

st.info(
    "This dashboard is a portfolio-grade analytical demonstration. Annual data is useful for strategic analysis, "
    "but quarterly data and external features should be added for production forecasting."
)
