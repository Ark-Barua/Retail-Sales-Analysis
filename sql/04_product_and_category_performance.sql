-- ==============================================================================
-- Enterprise Retail Sales Analytics - Product & Category Performance
-- Author: Senior Data Analyst (Google Analytics & BI Standard)
-- Business Question: What products and categories drive revenue and profit,
--                    which are lagging behind plan, and where is margin leaking?
-- ==============================================================================

-- QUERY 1: Product Category Performance vs. Plan (December 2022 Closing View)
-- Directly replicates and reconciles the bottom-right dashboard table
WITH category_dec_actuals AS (
    SELECT 
        category_code,
        category_name,
        ROUND(SUM(net_revenue) / 1000.0, 1) AS ac_sales_k,
        ROUND(SUM(cogs) / 1000.0, 1)        AS cogs_k,
        ROUND(SUM(gross_profit) / 1000.0, 1) AS gross_profit_k,
        COUNT(DISTINCT order_id)             AS order_count,
        SUM(quantity)                        AS units_sold
    FROM fact_sales
    WHERE year = 2022 
      AND month = 12
      AND order_status = 'Completed'
    GROUP BY category_code, category_name
),
category_benchmarks AS (
    SELECT 
        Category_Code AS category_code,
        Category_Name AS category_name,
        Planned_Sales_K AS pl_sales_k,
        Delta_PL_K      AS target_delta_k,
        Delta_PL_Pct    AS target_delta_pct
    FROM dim_category_performance
)
SELECT 
    b.category_code,
    b.category_name,
    b.pl_sales_k,
    a.ac_sales_k,
    ROUND(a.ac_sales_k - b.pl_sales_k, 1) AS delta_pl_k,
    ROUND(((a.ac_sales_k - b.pl_sales_k) / NULLIF(b.pl_sales_k, 0)) * 100.0, 1) AS delta_pl_pct,
    CASE 
        WHEN a.ac_sales_k >= b.pl_sales_k THEN 'Surplus (+)'
        ELSE 'Deficit (-)'
    END AS performance_badge,
    a.gross_profit_k,
    ROUND((a.gross_profit_k / NULLIF(a.ac_sales_k, 0)) * 100.0, 1) AS margin_pct,
    ROUND(a.ac_sales_k / a.units_sold, 2) AS realized_price_per_unit_k
FROM category_benchmarks b
JOIN category_dec_actuals a ON b.category_code = a.category_code
ORDER BY b.pl_sales_k DESC;


-- QUERY 2: Full-Year Category Revenue & Profit Contribution Matrix
-- Decomposes which categories generate high volume vs high profitability
WITH fy_category AS (
    SELECT 
        category_code,
        category_name,
        ROUND(SUM(net_revenue) / 1000.0, 1) AS total_revenue_k,
        ROUND(SUM(gross_profit) / 1000.0, 1) AS total_profit_k,
        ROUND(AVG(profit_margin_pct), 2)     AS avg_margin_pct,
        ROUND(AVG(discount_pct), 2)          AS avg_discount_pct,
        COUNT(DISTINCT order_id)             AS total_orders,
        SUM(quantity)                        AS total_units
    FROM fact_sales
    WHERE year = 2022 
      AND order_status = 'Completed'
    GROUP BY category_code, category_name
),
fy_totals AS (
    SELECT 
        SUM(net_revenue) / 1000.0 AS grand_revenue_k,
        SUM(gross_profit) / 1000.0 AS grand_profit_k
    FROM fact_sales
    WHERE year = 2022 AND order_status = 'Completed'
)
SELECT 
    c.category_code,
    c.category_name,
    c.total_revenue_k,
    ROUND((c.total_revenue_k / t.grand_revenue_k) * 100.0, 2) AS revenue_share_pct,
    c.total_profit_k,
    ROUND((c.total_profit_k / t.grand_profit_k) * 100.0, 2) AS profit_share_pct,
    c.avg_margin_pct,
    c.avg_discount_pct,
    -- Strategic BCG Portfolio Classification
    CASE 
        WHEN (c.total_revenue_k / t.grand_revenue_k) >= 0.15 AND c.avg_margin_pct >= 40 THEN 'Core Engine (High Rev, High Margin)'
        WHEN (c.total_revenue_k / t.grand_revenue_k) >= 0.15 AND c.avg_margin_pct < 40 THEN 'Volume Driver (High Rev, Moderate Margin)'
        WHEN (c.total_revenue_k / t.grand_revenue_k) < 0.15 AND c.avg_margin_pct >= 50 THEN 'Profit Booster (Niche, High Margin)'
        ELSE 'Review / Rationalize (Low Rev, Lower Margin)'
    END AS strategic_quadrant
FROM fy_category c
CROSS JOIN fy_totals t
ORDER BY c.total_revenue_k DESC;


-- QUERY 3: Pareto 80/20 Cumulative Revenue Analysis by Product SKU
-- Calculates cumulative percentage distribution to isolate the top driving SKUs
WITH sku_aggregates AS (
    SELECT 
        product_sku,
        category_name,
        ROUND(SUM(net_revenue) / 1000.0, 2) AS sku_revenue_k,
        SUM(quantity) AS units_sold,
        ROUND(SUM(gross_profit) / 1000.0, 2) AS sku_profit_k
    FROM fact_sales
    WHERE year = 2022 AND order_status = 'Completed'
    GROUP BY product_sku, category_name
),
sku_ranked AS (
    SELECT 
        product_sku,
        category_name,
        sku_revenue_k,
        sku_profit_k,
        SUM(sku_revenue_k) OVER () AS total_enterprise_rev_k,
        SUM(sku_revenue_k) OVER (ORDER BY sku_revenue_k DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_rev_k,
        ROW_NUMBER() OVER (ORDER BY sku_revenue_k DESC) AS sku_rank,
        COUNT(*) OVER () AS total_skus
    FROM sku_aggregates
)
SELECT 
    sku_rank,
    product_sku,
    category_name,
    sku_revenue_k,
    ROUND((running_rev_k / total_enterprise_rev_k) * 100.0, 2) AS cumulative_revenue_pct,
    CASE 
        WHEN (running_rev_k / total_enterprise_rev_k) <= 0.80 THEN 'Top 80% Revenue Driver (Tier 1)'
        ELSE 'Long Tail SKU (Tier 2/3)'
    END AS pareto_tier
FROM sku_ranked
ORDER BY sku_rank ASC
LIMIT 20;


-- QUERY 4: Return Rate & Revenue Leakage Audit by Product Category
-- Isolates quality and return friction points
SELECT 
    category_code,
    category_name,
    COUNT(order_id) AS total_orders_placed,
    SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) AS returned_orders_count,
    ROUND(
        (SUM(CASE WHEN order_status = 'Returned' THEN 1 ELSE 0 END) * 100.0) / COUNT(order_id), 
        2
    ) AS return_rate_pct,
    ROUND(SUM(CASE WHEN order_status = 'Returned' THEN gross_sales ELSE 0 END) / 1000.0, 2) AS returned_gross_value_k
FROM fact_sales
WHERE year = 2022
GROUP BY category_code, category_name
ORDER BY return_rate_pct DESC;
