from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .config import IMAGE_DIR


def _prepare_dir(path: Path = IMAGE_DIR) -> None:
    path.mkdir(parents=True, exist_ok=True)


def plot_revenue_trend(features: pd.DataFrame, output_path: Path | None = None) -> Path:
    _prepare_dir()
    if output_path is None:
        output_path = IMAGE_DIR / "segment_revenue_trend.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    for segment, group in features.groupby("segment"):
        ax.plot(group["year"], group["net_sales_musd"] / 1000, marker="o", label=segment)

    ax.set_title("Amazon Segment Revenue Trend")
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Net sales, USD billions")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_margin_trend(features: pd.DataFrame, output_path: Path | None = None) -> Path:
    _prepare_dir()
    if output_path is None:
        output_path = IMAGE_DIR / "operating_margin_trend.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    for segment, group in features.groupby("segment"):
        ax.plot(group["year"], group["operating_margin"] * 100, marker="o", label=segment)

    ax.set_title("Amazon Segment Operating Margin")
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Operating margin, %")
    ax.axhline(0, linewidth=1)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_forecast(features: pd.DataFrame, forecast: pd.DataFrame, output_path: Path | None = None) -> Path:
    _prepare_dir()
    if output_path is None:
        output_path = IMAGE_DIR / "revenue_forecast.png"

    fig, ax = plt.subplots(figsize=(10, 6))
    for segment, group in features.groupby("segment"):
        ax.plot(group["year"], group["net_sales_musd"] / 1000, marker="o", label=f"{segment} actual")

    for segment, group in forecast.groupby("segment"):
        ax.plot(group["year"], group["forecast_net_sales_musd"] / 1000, marker="x", linestyle="--", label=f"{segment} forecast")

    ax.set_title("Amazon Segment Revenue Forecast")
    ax.set_xlabel("Fiscal year")
    ax.set_ylabel("Net sales, USD billions")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path
