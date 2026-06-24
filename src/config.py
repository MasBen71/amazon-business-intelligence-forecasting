from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw" / "amazon_segment_annual_2019_2025.csv"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed" / "amazon_segment_features.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "executive_summary.md"
IMAGE_DIR = PROJECT_ROOT / "images"

SEGMENT_ORDER = ["North America", "International", "AWS"]
FORECAST_YEARS = [2026, 2027, 2028]
