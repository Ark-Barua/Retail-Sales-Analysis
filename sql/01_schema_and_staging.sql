-- ==============================================================================
-- Enterprise Retail Sales Analytics - Database Schema & Staging DDL
-- Author: Senior Data Analyst (Google Analytics & BI Standard)
-- Engine: SQLite / PostgreSQL / BigQuery Compatible DDL
-- ==============================================================================

-- 1. Create Staging Table for Ingestion from Raw ERP / CSV Extracts
DROP TABLE IF EXISTS staging_raw_sales;
CREATE TABLE staging_raw_sales (
    order_id            TEXT,
    order_date          TEXT,
    ship_date           TEXT,
    customer_id         TEXT,
    customer_segment    TEXT,
    sales_channel       TEXT,
    region_code         TEXT,
    region_name         TEXT,
    country             TEXT,
    category_code       TEXT,
    category_name       TEXT,
    product_sku         TEXT,
    quantity            INTEGER,
    unit_price          REAL,
    unit_price_raw      TEXT,
    gross_sales         REAL,
    discount_pct        REAL,
    discount_amount     REAL,
    net_revenue         REAL,
    cogs                REAL,
    gross_profit        REAL,
    profit_margin_pct   REAL,
    order_status        TEXT,
    year                INTEGER,
    month               INTEGER,
    month_name          TEXT
);

-- 2. Create Production Fact Sales Table (Strictly Typed, Validated & Indexed)
DROP TABLE IF EXISTS fact_sales;
CREATE TABLE fact_sales (
    order_id            TEXT PRIMARY KEY,
    order_date          DATE NOT NULL,
    ship_date           DATE,
    customer_id         TEXT NOT NULL,
    customer_segment    TEXT NOT NULL,
    sales_channel       TEXT NOT NULL,
    region_code         TEXT NOT NULL,
    region_name         TEXT NOT NULL,
    country             TEXT NOT NULL,
    category_code       TEXT NOT NULL,
    category_name       TEXT NOT NULL,
    product_sku         TEXT NOT NULL,
    quantity            INTEGER NOT NULL CHECK(quantity > 0),
    unit_price          DECIMAL(10,2) NOT NULL CHECK(unit_price >= 0),
    gross_sales         DECIMAL(12,2) NOT NULL,
    discount_pct        DECIMAL(5,2) DEFAULT 0.0 CHECK(discount_pct >= 0 AND discount_pct <= 100),
    discount_amount     DECIMAL(10,2) DEFAULT 0.0,
    net_revenue         DECIMAL(12,2) NOT NULL,
    cogs                DECIMAL(12,2) NOT NULL,
    gross_profit        DECIMAL(12,2) NOT NULL,
    profit_margin_pct   DECIMAL(5,2) NOT NULL,
    order_status        TEXT NOT NULL CHECK(order_status IN ('Completed', 'Returned', 'Cancelled')),
    year                INTEGER NOT NULL,
    month               INTEGER NOT NULL,
    month_name          TEXT NOT NULL
);

-- 3. Dimension Performance Tables for Executive Dashboard Benchmarks
DROP TABLE IF EXISTS dim_monthly_performance;
CREATE TABLE dim_monthly_performance (
    Month_Num           INTEGER PRIMARY KEY,
    Month               TEXT NOT NULL,
    Actual_Sales_K      DECIMAL(10,1) NOT NULL,
    Planned_Sales_K     DECIMAL(10,1) NOT NULL,
    Variance_K          DECIMAL(10,1) NOT NULL,
    Variance_Pct        DECIMAL(5,1) NOT NULL,
    Gross_Profit_K      DECIMAL(10,1) NOT NULL,
    Margin_Pct          DECIMAL(5,1) NOT NULL
);

DROP TABLE IF EXISTS dim_regional_performance;
CREATE TABLE dim_regional_performance (
    Region_Code         TEXT PRIMARY KEY,
    Region_Name         TEXT NOT NULL,
    Actual_Sales_K      DECIMAL(10,1) NOT NULL,
    Planned_Sales_K     DECIMAL(10,1) NOT NULL,
    Delta_PL_K          DECIMAL(10,1) NOT NULL,
    Delta_PL_Pct        DECIMAL(5,1) NOT NULL
);

DROP TABLE IF EXISTS dim_category_performance;
CREATE TABLE dim_category_performance (
    Category_Code       TEXT PRIMARY KEY,
    Category_Name       TEXT NOT NULL,
    Planned_Sales_K     DECIMAL(10,1) NOT NULL,
    Actual_Sales_K      DECIMAL(10,1) NOT NULL,
    Delta_PL_K          DECIMAL(10,1) NOT NULL,
    Delta_PL_Pct        DECIMAL(5,1) NOT NULL
);

-- 4. Create Performance Indexes for Fast Analytic Aggregation
CREATE INDEX IF NOT EXISTS idx_fact_sales_order_date ON fact_sales(order_date);
CREATE INDEX IF NOT EXISTS idx_fact_sales_cat ON fact_sales(category_code);
CREATE INDEX IF NOT EXISTS idx_fact_sales_reg ON fact_sales(region_code);
CREATE INDEX IF NOT EXISTS idx_fact_sales_cust ON fact_sales(customer_id);
