# Data Sources

This project uses public Amazon segment data from official Amazon/SEC filings.

## Included offline dataset

File:

```text
data/raw/amazon_segment_annual_2019_2025.csv
```

Coverage:

- Fiscal years: 2019-2025
- Segments: North America, International, AWS
- Metrics: net sales, operating expenses, operating income/loss
- Unit: USD millions

## Official sources used to build the seed dataset

1. **Amazon 2021 Form 10-K**
   - Used for fiscal years 2019, 2020, and 2021.
   - Section: Note 10 — Segment Information.
   - SEC filing URL: https://www.sec.gov/Archives/edgar/data/1018724/000101872422000005/amzn-20211231.htm

2. **Amazon 2024 Form 10-K**
   - Used for fiscal year 2022 and cross-checking 2023-2024.
   - Section: Note 10 — Segment Information.
   - SEC filing URL: https://www.sec.gov/Archives/edgar/data/1018724/000101872425000004/amzn-20241231.htm

3. **Amazon 2025 Form 10-K**
   - Used for fiscal year 2025 and cross-checking 2023-2024.
   - Section: Note 10 — Segment Information.
   - SEC filing URL: https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm

4. **SEC EDGAR XBRL APIs**
   - Included for possible project extension.
   - Official API documentation: https://www.sec.gov/search-filings/edgar-application-programming-interfaces

## Data quality notes

- Amazon reports segment data in millions of USD.
- Segment operating income can be negative for loss-making segments.
- Forecasts in this project are educational demonstrations and should not be used as investment advice.
