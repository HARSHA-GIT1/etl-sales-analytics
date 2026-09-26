# ETL Sales Analytics Dashboard

This project is an end-to-end sales analytics pipeline built to show how raw sales data can be turned into a clean database and then into a useful Power BI dashboard.

The idea is simple: start with a CSV sales dataset, bring in a live USD-to-INR exchange rate from a REST API, clean and validate the data with Python and Pandas, store it in a normalized SQLite database, and expose an analytics-friendly view for Power BI.

It is intentionally built with a small number of practical tools: Python, Pandas, SQLite, a REST API, and Power BI.

---

## What the project does

The pipeline follows this flow:

```text
Superstore CSV ───────┐
                      ├──> Extract ──> Transform ──> Validate ──> SQLite
USD → INR REST API ───┘                                      │
                                                              ↓
                                                   sales_analytics view
                                                              │
                                                              ↓
                                                        Power BI
```

The current sample run processes:

- 10,194 sales line items
- 5,111 orders
- 804 customers
- 1,862 products
- 21 raw CSV columns

The Power BI report then presents the data as an interactive sales dashboard.

---

## Main features

### 1. Two different data sources

The project uses a local CSV file for the sales data and a REST API for currency conversion.

The sales file is the Superstore sales dataset and is expected at:

```text
data/raw/samplesuperstore.csv
```

For currency conversion, the project calls the Frankfurter API with USD as the base currency and INR as the target currency. The current implementation uses the Frankfurter v1 API endpoint.

Frankfurter is a free exchange-rate API and does not require an API key. Its current documentation recommends v2 for new work, while v1 is still available. The extractor in this project currently uses v1 so the implementation and documentation match the code that was built.

### 2. Python and Pandas transformations

The transformation step prepares the raw data for analysis. It:

- Converts `Order Date` and `Ship Date` into proper date values.
- Converts USD sales and profit into INR using the API rate.
- Calculates shipping time in days.
- Calculates profit margin at the row level.
- Adds year and month fields for reporting.
- Keeps the original USD values as well as the INR values.

The transformed dataset is then passed through validation before anything is loaded into the database.

### 3. Data-quality checks

The validator checks several practical problems before the database load is allowed to continue:

- Required columns are present.
- Required fields do not contain missing values.
- Duplicate rows are detected.
- Sales are not negative.
- Quantity is greater than zero.
- Discount stays between 0 and 1.
- Order and ship dates are valid.

If validation fails, the pipeline raises an error and stops instead of loading bad data.

### 4. Normalized SQLite database

The raw sales file is not copied directly into one large table. Instead, the data is split into related tables:

```text
customers
    │
    └── orders
            │
            └── order_items
                    │
                    └── products
```

The main tables are:

| Table | Purpose |
|---|---|
| `customers` | Customer identity, name, and segment |
| `products` | Product information and category details |
| `orders` | Order dates, shipping details, and customer/location information |
| `order_items` | Product-level sales, quantity, discount, profit, and calculated fields |

This structure avoids repeating customer and product information on every sales row and gives the project a proper relational design.

### 5. Analytics view for Power BI

Power BI does not need to understand the normalized tables separately for every visual. The project creates a view called:

```text
sales_analytics
```

The view joins customers, orders, products, and order items into one reporting-friendly dataset.

This gives us two useful layers:

- normalized tables for data storage and integrity
- one denormalized analytics view for reporting

### 6. Logging and tests

The pipeline writes its activity to:

```text
logs/pipeline.log
```

The project also contains tests for transformations, database loading, analytics, and the end-to-end pipeline.

The end-to-end test can be run with:

```powershell
python -m tests.test_pipeline
```

A successful run ends with:

```text
End-to-end pipeline test passed.
```

---

## Power BI dashboard

The dashboard was built from the `sales_analytics` view and includes:

### KPI cards

- Total Sales
- Total Profit
- Profit Margin
- Total Orders

### Charts

- Sales & Profit Trend by Year and Month
- Sales by Region
- Sales by Category
- Top Products by Profit

### Interactive filters

- Year
- Region
- Category

The report uses INR for the main financial measures and has been formatted as a clean, blue-and-white analytics dashboard.

The main Power BI measures are:

```DAX
Total Sales = SUM(sales_analytics[sales_inr])

Total Profit = SUM(sales_analytics[profit_inr])

Profit Margin = DIVIDE([Total Profit], [Total Sales])

Total Orders = DISTINCTCOUNT(sales_analytics[order_id])
```

A sample full-data run produced approximately:

| Metric | Example result |
|---|---:|
| Total Sales | 222.93M INR |
| Total Profit | 28.01M INR |
| Profit Margin | 12.56% |
| Total Orders | 5.11K |

These numbers can change because the exchange rate comes from a live API when the pipeline runs.

---

## Project structure

```text
etl-sales-analytics/
├── data/
│   ├── raw/
│   │   └── samplesuperstore.csv
│   └── processed/
│       └── sales.db
│
├── src/
│   ├── extraction/
│   │   ├── csv_extractor.py
│   │   └── api_extractor.py
│   │
│   ├── transformation/
│   │   └── sales_transformer.py
│   │
│   ├── validation/
│   │   └── data_validator.py
│   │
│   ├── loading/
│   │   ├── database_schema.py
│   │   ├── normalized_loader.py
│   │   └── analytics_view.py
│   │
│   ├── pipeline.py
│   └── logging_config.py
│
├── dashboard/
│   └── Sales_Analytics_Dashboard.pbix
│
├── tests/
│   ├── test_sales_transformer.py
│   ├── test_database.py
│   ├── test_analytics.py
│   ├── test_pipeline.py
│   └── project_check.py
│
├── config/
│   └── config.py
│
├── logs/
│   └── pipeline.log
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Setup

### 1. Clone or download the project

Open a terminal in the project folder.

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

```powershell
pip install -r requirements.txt
```

The project uses Pandas and Requests for the ETL work, together with the other packages listed in `requirements.txt`.

### 4. Add the raw CSV

Make sure the sales dataset is here:

```text
data/raw/samplesuperstore.csv
```

The extractor expects that exact filename.

---

## Run the ETL pipeline

From the project root:

```powershell
python -m src.pipeline
```

The pipeline will:

1. Read the CSV.
2. Call the exchange-rate API.
3. Transform the data.
4. Run data-quality checks.
5. Recreate the SQLite schema.
6. Load the normalized tables.
7. Recreate the `sales_analytics` view.
8. Write pipeline activity to the log.

If the pipeline finishes successfully, the SQLite database will be created at:

```text
data/processed/sales.db
```

---

## Run the tests

The most useful test is the end-to-end test:

```powershell
python -m tests.test_pipeline
```

You can also run the individual test modules directly, for example:

```powershell
python -m tests.test_sales_transformer
python -m tests.test_database
python -m tests.test_analytics
```

There is also a project structure/database check:

```powershell
python -m tests.project_check
```

---

## Power BI connection

The Power BI report connects to the SQLite database through ODBC and loads the `sales_analytics` view.

The local Windows setup used for this project has an ODBC data source named:

```text
ETL_Sales_Analytics
```

The SQLite database used by that connection is:

```text
data/processed/sales.db
```

Only the `sales_analytics` view is loaded into the Power BI model for the dashboard.

After the Python pipeline has been run, open:

```text
dashboard/Sales_Analytics_Dashboard.pbix
```

and use **Home → Refresh** in Power BI Desktop to pull the current data from the SQLite source.

---

## Important limitation: exchange rates

There is one important limitation in the current version of the project.

The pipeline fetches the **latest available USD-to-INR rate when it runs** and uses that rate to convert the historical sales and profit values in the dataset.

That means the INR figures are useful for demonstrating the ETL and analytics workflow, but they should not be interpreted as historically accurate currency conversions for each individual order date.

A stronger production-style version would fetch the historical USD-to-INR rate for each order date (or load a time series of rates once and join it to the sales data).

---

## Refresh approach

The pipeline itself is ready to be run again whenever the source data needs to be refreshed, and the Power BI report can then be refreshed from the SQLite database.

This version does **not** include Windows Task Scheduler or another automatic scheduling service. That was intentionally kept out of the current implementation rather than claiming that a daily refresh has been automated when it has not.

---

## Why this project is useful

This project is more than a dashboard. It demonstrates the complete path from raw data to reporting:

```text
Raw data
   ↓
Extraction
   ↓
Transformation
   ↓
Data quality checks
   ↓
Relational database
   ↓
Analytics view
   ↓
Power BI dashboard
```

It also shows some practical engineering decisions:

- keeping extraction separate from transformation
- validating data before loading it
- using a normalized database instead of one large repeated table
- creating a separate analytics view for reporting
- keeping configuration and logging outside the main pipeline logic
- testing the important pieces instead of relying only on manual checks

---

## Possible next improvements

If this project is taken further, the most useful improvements would be:

1. Use historical USD-to-INR rates based on each order date.
2. Move from SQLite to PostgreSQL for a multi-user or production-style environment.
3. Add an automated scheduler or orchestration tool.
4. Add incremental loading instead of rebuilding the database on every run.
5. Add a proper date dimension for more advanced Power BI time analysis.
6. Add deployment and monitoring around the pipeline.

---

## A note on project metrics

No claim of an “80% reduction in manual effort” is included here because that number has not been measured in this implementation.

If that metric is needed for a resume or interview discussion, it is better to measure the old manual process and compare it with the actual automated workflow first.

---

## Project status

The current version has:

- working CSV extraction
- working REST API extraction
- Pandas transformations
- data-quality validation
- normalized SQLite storage
- Power BI analytics view
- Power BI dashboard
- automated test coverage for the main pipeline pieces
- logging

The dashboard has been refreshed successfully after the final pipeline update and is saved as:

```text
dashboard/Sales_Analytics_Dashboard.pbix
```
