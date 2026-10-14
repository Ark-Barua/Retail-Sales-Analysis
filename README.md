# Enterprise Retail Sales Analysis & Predictive Performance Model
**Project:** Project 1: Retail Sales Analysis & Data Science Intelligence  
**Role:** Senior Data Analyst & Data Scientist (Google Standard — 8+ Years Experience)  
**Methodology:** Google BI & Data Governance, IBCS (International Business Communication Standards), Machine Learning & Statistical Inference  
**Tooling Stack:** **Python** (`scikit-learn`, `scipy`, `pandas`, `numpy`), **Jupyter Notebook**, **SQL** (SQLite / BigQuery / PostgreSQL), **Excel**, **Power BI** (DAX Tabular Model), **Modern Web Application** (HTML5 / Vanilla CSS / Interactive JS)  
**🌐 Live Interactive Dashboard:** [https://heartfelt-macaron-5f7810.netlify.app](https://retail-sales-analysis.netlify.app/)
**📂 GitHub Repository:** [https://github.com/Ark-Barua/Retail-Sales-Analysis](https://github.com/Ark-Barua/Retail-Sales-Analysis)  

[![Live Demo on Netlify](https://img.shields.io/badge/Live_Demo-Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white)](https://retail-sales-analysis.netlify.app/)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ark-Barua/Retail-Sales-Analysis)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

---

## 1. Executive Brief & Core Business Question

> ### *"What drives revenue and profit, and where should the business focus?"*

This repository bridges **Enterprise Business Intelligence** with **Advanced Data Science and Machine Learning**. It reconciles full-year retail sales (**$8.455M across 11,491 clean transactions**) against operational budget plans (Plan) and prior-year historical baselines (PY), while providing forward-looking predictive models (Time Series Forecasting, Customer RFM Segmentation, Feature Importance, and Statistical Hypothesis Testing).

### Key Performance & Data Science Highlights
* **Total Realized Sales (2022):** **$8,455,000** (vs. Plan of $7,478,000, **+13.1% full-year surplus**)
* **Year-over-Year Trajectory:** **+65.5% YoY expansion** over prior year ($5.1M base)
* **December Closing Run-Rate:** **$1,000,000** net revenue (+19.0% vs Plan)
* **Gross Profit Margin:** **38.4%** ($3.25M gross operating profit)
* **Forward Revenue Forecast (2023 Q1):** Projected **$2.33M sales** (**+18.5% YoY lift**; 95% Confidence Interval)
* **High-LTV Customer Concentration (K-Means):** **Top 38% of accounts drive 69.5% of total enterprise revenue** (Silhouette Score: 0.314)
* **Statistical Elasticity (Welch's T-Test):** **$p = 0.3127 > 0.05$** — Proves scientifically that discounts >10% do **NOT** yield incremental volume; they cause pure gross margin dilution (731 bps penalty).

---

## 2. Interactive Dashboard (Exact UI Match & Live Capabilities)

> 🚀 **Live Interactive Web Application:** **[https://heartfelt-macaron-5f7810.netlify.app](https://heartfelt-macaron-5f7810.netlify.app)**  
> *(Supports real-time Custom CSV Drag & Drop Ingestion, ML Intelligence Drawer, and Live Excel Data Simulation)*

The web dashboard in [`dashboard/`](dashboard/) replicates the exact layout, colors, and IBCS standards from executive Google reporting:

![Executive Sales Reporting Dashboard](docs/images/dashboard_overview.png)

### Key Visual & Analytical Features:
* **Dual Waterfall Bridge Charts:** Actual vs Previous Year (600 → Bridge +400 → 800 with +65.5% bracket) and Actual vs Plan (800 → Bridge +50 → 800 with +1.0% marker).
* **12-Month IBCS Column Chart:** Jan to Dec base bars (650 to 1,000) with stacked variance blocks (+42%, -11%, +24%, -30%, etc.).
* **Regional & Category Tables:** Horizontal bars, diverging green/red $\Delta$ PL bars, and $\Delta$ PL% lollipop pins.
* **View Mode Toggle:** Switch between **Template Mockup Labels** (`Region 1`, `Category 1`, `Text Here`) and **Enterprise Business Names** (`North America West`, `Electronics & Laptops`).
* **Live Excel Simulator ("Edit Data"):** Modify any cell to simulate the active Excel data link.

---

## 3. Dynamic Custom CSV Ingestion (No Hardcoded Data)

The dashboard includes a full client-side CSV processing engine allowing any recruiter, stakeholder, or user to drag-and-drop their own datasets:

![Custom CSV Drag and Drop Ingestion](docs/images/custom_csv_upload.png)

* **Drag-and-Drop & File Picker:** Upload any raw sales transaction CSV.
* **Intelligent Auto-Mapping:** Automatically identifies Date, Revenue/Sales, Cost/Profit, Category, and Region columns.
* **Real-Time Recalculation:** Instantly updates monthly bars, regional tables, category tables, and variance pins.
* **Active Dataset Banner:** Displays parsed row count, total revenue, and a 1-click **"Reset to Image Default Benchmark"** button.
* **Downloadable Template:** Ready-to-use template [`data/retail_sales_template.csv`](data/retail_sales_template.csv).
* **Pre-loaded Scenarios:** Quick-toggle between *Master Clean Log (11,491 records)*, *Image Benchmark Default*, and *High-Growth Tech Scenario*.

---

## 4. Data Science & Machine Learning Intelligence

A dedicated Data Science suite trained on transaction telemetry to answer predictive and strategic commercial questions:

![Data Science and Machine Learning Intelligence](docs/images/data_science_ml.png)

### 4.1 Time Series Sales Forecasting (Holt-Winters / Trend + Seasonality)
* Predicts monthly net revenue for 2023 with 95% prediction intervals.
* Identifies a **Q1 2023 revenue trajectory of $2.33M** (+18.5% YoY expansion over Q1 2022).
* Run via CLI on any custom CSV:
  ```bash
  python scripts/data_science_pipeline.py --input data/processed/retail_sales_clean.csv
  ```

### 4.2 Unsupervised Customer Segmentation (RFM + K-Means)
* Engineered features: **Recency** (days since last order), **Frequency** (order count), **Monetary** (lifetime spend), and **AOV**.
* Optimal clusters ($k=4$, Silhouette Score = 0.314):
  * **Tier-1 Champions (368 accounts):** $11,209 avg spend, 24 days avg recency (30.2% revenue share).
  * **Loyal Core Customers (914 accounts):** $5,866 avg spend, 48 days recency (39.3% revenue share).
  * **Occasional Buyers (1,362 accounts):** $2,282 avg spend, 82 days recency (22.8% revenue share).
  * **At-Risk / Lapsed Accounts (735 accounts):** $1,426 avg spend, 165 days recency (7.7% revenue share).

### 4.3 Supervised ML: Profit Margin Driver Attribution (Random Forest Regressor)
Attribution ranking on operating profit margin:
1. **Category: Subscriptions & Care Plans (68.0% importance):** Pure recurring high-margin ARR (75% gross margin).
2. **Unit Selling Price (14.3%):** Direct fixed-cost absorption.
3. **Category: Office Tech & Software (8.9%):** High gross margins offset by corporate sales cycles.
4. **Discount Percentage (3.4%):** Strongest negative elasticity driver on gross margins.

### 4.4 Statistical Hypothesis Testing (Discount Elasticity A/B Test)
* **Hypothesis:** Does deep discounting (>10%) produce statistically significant higher unit sales?
* **Welch's Two-Sample T-Test:** $t = -1.010$, $p = 0.3127 \gg 0.05$, Cohen's $d = -0.033$.
* **Conclusion:** **Fail to reject null hypothesis ($H_0$).** Discretionary discounts >10% do not stimulate unit volume; they represent pure profit margin leakage.

---

## 5. Executive Actionable Recommendations

Comprehensive 5-point strategic memorandum for leadership:

![Executive Actionable Recommendations](docs/images/actionable_recommendations.png)

1. **Remediate EMEA Central (Region 3) Deficit (-15.0% / -$29K in Dec):** Reallocate 30% of marketing to direct digital sales; introduce localized Net-60/90 enterprise terms (Projected impact: **+$180K to +$240K** annualized).
2. **Transition Category 7 to SaaS Recurring ARR:** Sunset lumpy perpetual licenses; bundle software into Category 8 subscription care plans (Projected impact: **+$110,000** gross profit; **+180 bps** margin expansion).
3. **Forward-Stage Inventory to APAC (+21.0%) and LATAM (+17.9%):** Shift 15% of safety stock from California to Tokyo and São Paulo hubs to eliminate stockouts (Projected impact: **+$320,000** in uncaptured revenue).
4. **Automate CPQ Discount Governance:** Implement strict approval gates (rep ≤5%, Director ≤10%, VP Finance >10%) to halt margin dilution (Projected impact: **+$145,000+** preserved gross profit).
5. **Smooth Summer Seasonality (-47% Dip):** Launch Mid-Year Enterprise Hardware Refresh campaign in July/August and anchor 2023 budgets to empirical seasonality curves (Projected impact: **+$250,000** summer top-line lift).

---

## 6. Repository Architecture

```
Ark-Barua/Retail-Sales-Analysis
├── .github/workflows/deploy.yml             # GitHub Actions for automated GitHub Pages live hosting
├── vercel.json                              # 1-click Vercel deployment configuration
├── netlify.toml                             # 1-click Netlify deployment configuration
├── DEPLOYMENT_GUIDE.md                      # Live hosting guide (GitHub Pages, Vercel, Netlify)
│
├── data/
│   ├── raw/retail_sales_raw.csv             # Raw ERP extract with anomalies (11,663 rows)
│   ├── processed/retail_sales_clean.csv     # Deduplicated, clean golden record (11,491 rows)
│   ├── processed/forecast_2023.csv          # Q1-Q2 2023 monthly forecasts with 95% CI
│   ├── processed/customer_rfm_clusters.csv  # K-Means customer RFM clusters & segments
│   ├── processed/ml_feature_importance.csv  # Random forest profit driver feature importance
│   ├── retail_sales_template.csv            # Downloadable sample template for custom CSV upload
│   ├── Retail_Sales_Model.xlsx              # Formatted Excel model with formulas & pivot tabs
│   └── retail_sales.db                      # SQLite DB with indexed tables for SQL queries
│
├── notebooks/
│   └── retail_data_science_modeling.ipynb   # Complete Data Science & ML portfolio notebook
│
├── scripts/
│   ├── data_science_pipeline.py             # CLI ML pipeline (accepts custom CSV via --input)
│   ├── generate_retail_data.py              # Synthetic data pipeline & Excel workbook builder
│   └── build_notebook.py                    # Notebook generator script
│
├── sql/
│   ├── 01_schema_and_staging.sql            # Table DDL, constraints & staging schema
│   ├── 02_data_cleaning_and_validation.sql  # Automated deduplication & quality assertions
│   ├── 03_monthly_sales_trends.sql          # MoM growth (LAG), YoY & 3M rolling averages
│   ├── 04_product_and_category_performance.sql # Category vs Plan, Gross Margin & Pareto 80/20
│   ├── 05_regional_performance.sql          # Regional quota attainment & margin profile
│   └── 06_executive_kpis_and_drivers.sql    # Customer economics & discount margin dilution
│
├── dashboard/
│   ├── index.html                           # Executive dashboard markup
│   ├── styles.css                           # Pixel-perfect IBCS styling & responsive grid
│   └── app.js                              # Dynamic state, Custom CSV engine & ML drawer
│
├── powerbi/
│   ├── measures.dax                         # 25+ production-grade DAX measures
│   └── data_model_guide.md                  # Kimball Star Schema model documentation
│
└── docs/
    ├── images/                              # High-resolution screenshots of all UI workflows
    ├── assumptions_and_data_dictionary.md   # ASC 606 revenue recognition & data dictionary
    ├── sql_analysis_report.md               # Executed query results, tables & takeaways
    └── actionable_recommendations.md        # C-Suite memorandum with 5 quantified recommendations
```

---

## 7. Live Deployment Instructions
* **Netlify (Active Production Deployment):** Live at **[https://heartfelt-macaron-5f7810.netlify.app](https://heartfelt-macaron-5f7810.netlify.app)**.
* **GitHub Pages (Automated):** Go to **Settings > Pages > Build and deployment > Source: GitHub Actions**. The CI/CD workflow automatically publishes the dashboard to `https://ark-barua.github.io/Retail-Sales-Analysis/`.
* **Vercel:** 1-Click Import using the included [`vercel.json`](vercel.json).
* See [`DEPLOYMENT_GUIDE.md`](DEPLOYMENT_GUIDE.md) for full deployment details.

---

## 8. License

This project is open-source and licensed under the [MIT License](LICENSE) &copy; 2026 Ark Barua.

