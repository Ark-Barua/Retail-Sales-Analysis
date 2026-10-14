-- ==============================================================================
-- Enterprise Retail Sales Analytics - Regional Sales Performance & Quota Variance
-- Author: Senior Data Analyst (Google Analytics & BI Standard)
-- Business Question: Where are regional sales teams overperforming vs lagging
--                    budget targets, and what is the margin profile per geography?
-- ==============================================================================

-- QUERY 1: Regional Sales vs Plan Variance (December 2022 Closing View)
-- Exactly reconciles the bottom-left dashboard chart
WITH regional_dec_actuals AS (
    SELECT 
        region_code,
        region_name,
        country,
        ROUND(SUM(net_revenue) / 1000.0, 1) AS ac_sales_k,
        ROUND(SUM(gross_profit) / 1000.0, 1) AS gross_profit_k,
        COUNT(DISTINCT order_id)             AS order_count
    FROM fact_sales
    WHERE year = 2022 
      AND month = 12 
      AND order_status = 'Completed'
    GROUP BY region_code, region_name, country
),
regional_benchmarks AS (
    SELECT 
        Region_Code AS region_code,
        Region_Name AS benchmark_name,
        Planned_Sales_K AS pl_sales_k,
        Delta_PL_K      AS target_delta_k,
        Delta_PL_Pct    AS target_delta_pct
    FROM dim_regional_performance
)
SELECT 
    b.region_code,
    a.region_name,
    a.country,
    a.ac_sales_k,
    b.pl_sales_k,
    ROUND(a.ac_sales_k - b.pl_sales_k, 1) AS delta_pl_k,
    ROUND(((a.ac_sales_k - b.pl_sales_k) / NULLIF(b.pl_sales_k, 0)) * 100.0, 1) AS delta_pl_pct,
    CASE 
        WHEN a.ac_sales_k >= b.pl_sales_k THEN 'Surplus (+)'
        ELSE 'Deficit (-)'
    END AS performance_badge,
    a.gross_profit_k,
    ROUND((a.gross_profit_k / NULLIF(a.ac_sales_k, 0)) * 100.0, 1) AS regional_margin_pct
FROM regional_benchmarks b
JOIN regional_dec_actuals a ON b.region_code = a.region_code
ORDER BY a.ac_sales_k DESC;


-- QUERY 2: Full Year Regional Contribution & Growth Matrix (2022)
WITH fy_regional AS (
    SELECT 
        region_code,
        region_name,
        ROUND(SUM(net_revenue) / 1000.0, 1) AS total_sales_k,
        ROUND(SUM(gross_profit) / 1000.0, 1) AS total_profit_k,
        ROUND(AVG(profit_margin_pct), 2)     AS avg_margin_pct,
        ROUND(AVG(discount_pct), 2)          AS avg_discount_pct,
        COUNT(DISTINCT customer_id)          AS unique_customers,
        COUNT(DISTINCT order_id)             AS total_orders,
        ROUND(SUM(net_revenue) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS regional_aov_usd
    FROM fact_sales
    WHERE year = 2022 
      AND order_status = 'Completed'
    GROUP BY region_code, region_name
),
fy_total AS (
    SELECT 
        SUM(net_revenue) / 1000.0 AS grand_sales_k,
        SUM(gross_profit) / 1000.0 AS grand_profit_k
    FROM fact_sales
    WHERE year = 2022 AND order_status = 'Completed'
)
SELECT 
    r.region_code,
    r.region_name,
    r.total_sales_k,
    ROUND((r.total_sales_k / t.grand_sales_k) * 100.0, 1) AS revenue_share_pct,
    r.total_profit_k,
    ROUND((r.total_profit_k / t.grand_profit_k) * 100.0, 1) AS profit_share_pct,
    r.avg_margin_pct,
    r.avg_discount_pct,
    r.unique_customers,
    r.total_orders,
    r.regional_aov_usd,
    RANK() OVER (ORDER BY r.total_sales_k DESC) AS sales_rank
FROM fy_regional r
CROSS JOIN fy_total t
ORDER BY sales_rank ASC;
