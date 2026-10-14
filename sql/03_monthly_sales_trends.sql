-- ==============================================================================
-- Enterprise Retail Sales Analytics - Monthly Sales Trends & Seasonality
-- Author: Senior Data Analyst (Google Analytics & BI Standard)
-- Business Question: What are the monthly trends, growth trajectory, and
--                    volatility drivers across the fiscal year?
-- ==============================================================================

-- QUERY 1: Monthly Actual vs. Plan Variance Analysis (Matching Dashboard Visual)
-- Computes Actual Sales, Planned Benchmark, Delta Plan ($K), and Delta Plan %
WITH monthly_actuals AS (
    SELECT 
        month,
        month_name,
        ROUND(SUM(net_revenue) / 1000.0, 1) AS actual_sales_k,
        ROUND(SUM(cogs) / 1000.0, 1)        AS total_cogs_k,
        ROUND(SUM(gross_profit) / 1000.0, 1) AS gross_profit_k,
        COUNT(DISTINCT order_id)             AS total_orders,
        ROUND(AVG(net_revenue), 2)           AS avg_order_value_usd
    FROM fact_sales
    WHERE year = 2022
      AND order_status = 'Completed'
    GROUP BY month, month_name
),
plan_benchmarks AS (
    SELECT 
        Month_Num AS month,
        Month     AS month_name,
        Planned_Sales_K AS planned_sales_k
    FROM dim_monthly_performance
)
SELECT 
    m.month,
    m.month_name,
    m.actual_sales_k,
    p.planned_sales_k,
    ROUND(m.actual_sales_k - p.planned_sales_k, 1) AS delta_plan_k,
    ROUND(((m.actual_sales_k - p.planned_sales_k) / NULLIF(p.planned_sales_k, 0)) * 100.0, 1) AS delta_plan_pct,
    CASE 
        WHEN m.actual_sales_k >= p.planned_sales_k THEN 'Surplus (+)'
        ELSE 'Deficit (-)'
    END AS performance_status,
    m.gross_profit_k,
    ROUND((m.gross_profit_k / NULLIF(m.actual_sales_k, 0)) * 100.0, 1) AS gross_margin_pct,
    m.total_orders,
    m.avg_order_value_usd
FROM monthly_actuals m
JOIN plan_benchmarks p ON m.month = p.month
ORDER BY m.month ASC;


-- QUERY 2: Month-over-Month (MoM) Growth & Rolling 3-Month Moving Average
-- Employs LAG() and rolling window functions to capture momentum and seasonality
WITH monthly_series AS (
    SELECT 
        month,
        month_name,
        ROUND(SUM(net_revenue) / 1000.0, 1) AS monthly_rev_k
    FROM fact_sales
    WHERE year = 2022
      AND order_status = 'Completed'
    GROUP BY month, month_name
)
SELECT 
    month,
    month_name,
    monthly_rev_k,
    LAG(monthly_rev_k, 1) OVER (ORDER BY month) AS prev_month_rev_k,
    ROUND(monthly_rev_k - LAG(monthly_rev_k, 1) OVER (ORDER BY month), 1) AS mom_dollar_change_k,
    ROUND(
        ((monthly_rev_k - LAG(monthly_rev_k, 1) OVER (ORDER BY month)) / 
        NULLIF(LAG(monthly_rev_k, 1) OVER (ORDER BY month), 0)) * 100.0, 
        1
    ) AS mom_growth_pct,
    -- 3-Month Trailing Moving Average (Smoothing Summer Slump vs Q4 Surge)
    ROUND(
        AVG(monthly_rev_k) OVER (
            ORDER BY month 
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 1
    ) AS rolling_3mo_avg_k
FROM monthly_series
ORDER BY month ASC;


-- QUERY 3: Year-over-Year (YoY) Comparative Trajectory (2021 vs. 2022)
-- Explains the top-left executive waterfall chart (+65.5% YoY expansion)
WITH annual_monthly AS (
    SELECT 
        month,
        month_name,
        ROUND(SUM(CASE WHEN year = 2021 THEN net_revenue ELSE 0 END) / 1000.0, 1) AS py_2021_sales_k,
        ROUND(SUM(CASE WHEN year = 2022 THEN net_revenue ELSE 0 END) / 1000.0, 1) AS ac_2022_sales_k
    FROM fact_sales
    WHERE order_status = 'Completed'
    GROUP BY month, month_name
)
SELECT 
    month,
    month_name,
    py_2021_sales_k,
    ac_2022_sales_k,
    ROUND(ac_2022_sales_k - py_2021_sales_k, 1) AS yoy_dollar_expansion_k,
    ROUND(
        ((ac_2022_sales_k - py_2021_sales_k) / NULLIF(py_2021_sales_k, 0)) * 100.0, 
        1
    ) AS yoy_growth_pct
FROM annual_monthly
ORDER BY month ASC;


-- QUERY 4: Cumulative Year-to-Date (YTD) Revenue vs. Target Run-Rate
-- Tracks target achievement and pacing across the year
WITH cumulative_calc AS (
    SELECT 
        m.month,
        m.month_name,
        m.actual_sales_k,
        p.planned_sales_k,
        SUM(m.actual_sales_k) OVER (ORDER BY m.month) AS ytd_actual_sales_k,
        SUM(p.planned_sales_k) OVER (ORDER BY m.month) AS ytd_planned_sales_k
    FROM (
        SELECT 
            month, 
            month_name, 
            ROUND(SUM(net_revenue) / 1000.0, 1) AS actual_sales_k
        FROM fact_sales
        WHERE year = 2022 AND order_status = 'Completed'
        GROUP BY month, month_name
    ) m
    JOIN dim_monthly_performance p ON m.month = p.Month_Num
)
SELECT 
    month,
    month_name,
    actual_sales_k,
    planned_sales_k,
    ytd_actual_sales_k,
    ytd_planned_sales_k,
    ROUND(ytd_actual_sales_k - ytd_planned_sales_k, 1) AS ytd_variance_k,
    ROUND(((ytd_actual_sales_k - ytd_planned_sales_k) / NULLIF(ytd_planned_sales_k, 0)) * 100.0, 1) AS ytd_variance_pct
FROM cumulative_calc
ORDER BY month ASC;
