# Amazon Business Intelligence & Revenue Forecasting

A professional end-to-end data science project analyzing Amazon's segment-level financial performance across **North America**, **International**, and **AWS**. The project uses public company data from Amazon SEC filings, builds analytical features, compares segment profitability, forecasts future revenue, and provides an interactive Streamlit dashboard.

> Portfolio angle: this project is designed for **data analyst**, **business intelligence**, **financial data science**, and **junior data scientist** GitHub portfolios.

---

## 1. Business problem

Amazon is often described as an e-commerce company, but its profit structure is strongly influenced by AWS and the operating leverage of its retail segments.

This project answers:

1. Which Amazon segment contributes most to revenue growth?
2. Which segment contributes most to operating income?
3. How has AWS changed Amazon's profit mix over time?
4. Can we forecast Amazon segment revenue for the next three years?
5. What business insights would be useful for an investor, analyst, or strategy team?

---

## 2. Data

The included offline dataset covers Amazon's annual segment data from **2019 to 2025**.

| Field | Meaning |
|---|---|
| `year` | Fiscal year |
| `segment` | North America, International, or AWS |
| `net_sales_musd` | Net sales in millions of USD |
| `operating_expenses_musd` | Operating expenses in millions of USD |
| `operating_income_musd` | Operating income/loss in millions of USD |
| `source` | Filing source note |

Primary sources:

- Amazon 2021 Form 10-K, Note 10 Segment Information: 2019-2021 segment data.
- Amazon 2024 Form 10-K, Note 10 Segment Information: 2022-2024 segment data.
- Amazon 2025 Form 10-K, Note 10 Segment Information: 2023-2025 segment data.
- SEC EDGAR XBRL APIs can be used to extend the project with broader company-level facts.

The raw file is here:

```text
/data/raw/amazon_segment_annual_2019_2025.csv
```

---

## 3. Key methods

This project includes:

- Data cleaning and validation
- KPI feature engineering
- Segment-level exploratory analysis
- Revenue share and profit share analysis
- Operating margin analysis
- YoY growth analysis
- Baseline forecasting
- Ridge regression forecasting
- Model evaluation using MAE, RMSE, and MAPE
- Streamlit dashboard
- Automated report generation

---

## 4. Repository structure

```text
amazon-business-intelligence-forecasting/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   │   └── amazon_segment_annual_2019_2025.csv
│   └── processed/
│
├── images/
│   ├── segment_revenue_trend.png
│   ├── operating_margin_trend.png
│   └── revenue_forecast.png
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_segment_analysis.ipynb
│   └── 03_forecasting.ipynb
│
├── reports/
│   ├── data_sources.md
│   └── executive_summary.md
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── features.py
│   ├── modeling.py
│   ├── sec_client.py
│   └── visualization.py
│
├── tests/
│   └── test_features.py
│
├── .github/workflows/python-tests.yml
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run_pipeline.py
```

---

## 5. How to run

### Option A: Jupyter Notebook

```bash
pip install -r requirements.txt
jupyter notebook
```

Open the notebooks in this order:

```text
notebooks/01_data_understanding.ipynb
notebooks/02_segment_analysis.ipynb
notebooks/03_forecasting.ipynb
```

### Option B: Python pipeline

```bash
pip install -r requirements.txt
python run_pipeline.py
```

This creates:

```text
data/processed/amazon_segment_features.csv
reports/executive_summary.md
images/segment_revenue_trend.png
images/operating_margin_trend.png
images/revenue_forecast.png
```

### Option C: Streamlit dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

---

## 6. Example business insights

Based on the included data:

- North America remains the largest revenue segment.
- AWS has a much higher operating margin than Amazon's retail segments.
- AWS contributes a disproportionately large share of operating income compared with its revenue share.
- International moved from operating losses in several years to positive operating income by 2024-2025.
- Amazon's profit mix is increasingly shaped by cloud infrastructure and high-margin services.

---

## 7. Limitations

This is a compact public-data project. Annual data provides a clean strategic view, but it is not enough for precise short-term forecasting. For a stronger production version, extend the dataset using quarterly SEC filings and add macroeconomic indicators, cloud-market data, ad revenue trends, and stock-market features.

---

## 8. Skills demonstrated

- Financial data analysis
- Business intelligence
- Exploratory data analysis
- Time-series feature engineering
- Forecasting
- Regression modeling
- Dashboard development
- Executive reporting
- Clean GitHub project organization

---

## 9. Disclaimer

This project is for educational and portfolio purposes only. It is not investment advice.
