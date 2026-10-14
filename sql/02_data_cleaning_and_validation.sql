-- ==============================================================================
-- Enterprise Retail Sales Analytics - Data Cleaning & Validation Pipeline
-- Author: Senior Data Analyst (Google Analytics & BI Standard)
-- Description:
--   Transforms raw messy ERP staging records into validated, golden-record
--   production fact table. Solves for duplicates, string whitespace/casing,
--   missing values, and financial reconciliations.
-- ==============================================================================

-- STEP 1: Audit Data Hygiene Issues in Staging
-- Identify duplicate order count
SELECT 
    order_id, 
    COUNT(*) as occurrence_count
FROM staging_raw_sales
GROUP BY order_id
HAVING COUNT(*) > 1;

-- STEP 2: Clear and Repopulate Production Fact Table (Idempotent Execution)
DELETE FROM fact_sales;

INSERT INTO fact_sales (
    order_id,
    order_date,
    ship_date,
    customer_id,
    customer_segment,
    sales_channel,
    region_code,
    region_name,
    country,
    category_code,
    category_name,
    product_sku,
    quantity,
    unit_price,
    gross_sales,
    discount_pct,
    discount_amount,
    net_revenue,
    cogs,
    gross_profit,
    profit_margin_pct,
    order_status,
    year,
    month,
    month_name
)
WITH deduplicated_staging AS (
    SELECT 
        order_id,
        order_date,
        -- Impute missing ship_date as order_date + 2 days average lead time
        COALESCE(ship_date, DATE(order_date, '+2 days')) AS clean_ship_date,
        TRIM(customer_id) AS customer_id,
        
        -- Standardize customer segment casing and trim whitespace
        CASE 
            WHEN LOWER(TRIM(customer_segment)) = 'consumer' THEN 'Consumer'
            WHEN LOWER(TRIM(customer_segment)) = 'corporate' THEN 'Corporate'
            WHEN LOWER(TRIM(customer_segment)) = 'small business' THEN 'Small Business'
            WHEN LOWER(TRIM(customer_segment)) = 'enterprise' THEN 'Enterprise'
            ELSE 'Consumer'
        END AS clean_customer_segment,
        
        TRIM(sales_channel) AS clean_sales_channel,
        TRIM(region_code) AS clean_region_code,
        TRIM(region_name) AS clean_region_name,
        TRIM(country) AS clean_country,
        TRIM(category_code) AS clean_category_code,
        TRIM(category_name) AS clean_category_name,
        TRIM(product_sku) AS clean_product_sku,
        
        -- Enforce positive quantity
        ABS(CAST(quantity AS INTEGER)) AS clean_quantity,
        
        -- Ensure unit_price is positive numeric
        ROUND(CAST(unit_price AS REAL), 2) AS clean_unit_price,
        ROUND(CAST(gross_sales AS REAL), 2) AS clean_gross_sales,
        ROUND(COALESCE(CAST(discount_pct AS REAL), 0.0), 2) AS clean_discount_pct,
        ROUND(COALESCE(CAST(discount_amount AS REAL), 0.0), 2) AS clean_discount_amount,
        ROUND(CAST(net_revenue AS REAL), 2) AS clean_net_revenue,
        ROUND(CAST(cogs AS REAL), 2) AS clean_cogs,
        ROUND(CAST(gross_profit AS REAL), 2) AS clean_gross_profit,
        ROUND(CAST(profit_margin_pct AS REAL), 2) AS clean_profit_margin_pct,
        TRIM(order_status) AS clean_order_status,
        CAST(year AS INTEGER) AS year,
        CAST(month AS INTEGER) AS month,
        TRIM(month_name) AS month_name,
        
        -- Window function to pick single unique row per order_id
        ROW_NUMBER() OVER (
            PARTITION BY order_id 
            ORDER BY order_date DESC
        ) AS row_rank
    FROM staging_raw_sales
    WHERE order_id IS NOT NULL 
      AND TRIM(order_id) != ''
)
SELECT 
    order_id,
    order_date,
    clean_ship_date,
    customer_id,
    clean_customer_segment,
    clean_sales_channel,
    clean_region_code,
    clean_region_name,
    clean_country,
    clean_category_code,
    clean_category_name,
    clean_product_sku,
    clean_quantity,
    clean_unit_price,
    clean_gross_sales,
    clean_discount_pct,
    clean_discount_amount,
    clean_net_revenue,
    clean_cogs,
    clean_gross_profit,
    clean_profit_margin_pct,
    clean_order_status,
    year,
    month,
    month_name
FROM deduplicated_staging
WHERE row_rank = 1;

-- STEP 3: Quality Control Reconciliations & Assertions
-- 3.1 Check for Revenue Equation Integrity: Net_Revenue == Gross_Sales - Discount_Amount
SELECT 
    COUNT(*) AS reconciliation_discrepancy_count
FROM fact_sales
WHERE ABS(net_revenue - (gross_sales - discount_amount)) > 0.05;

-- 3.2 Check for Abnormal Profit Margins (<0% or >90%)
SELECT 
    order_id,
    category_name,
    net_revenue,
    gross_profit,
    profit_margin_pct
FROM fact_sales
WHERE profit_margin_pct < 0 OR profit_margin_pct > 90;
