-- ==============================================================================
-- Enterprise Retail Sales Analytics - Executive KPIs & Strategic Driver Analysis
-- Author: Senior Data Analyst (Google Analytics & BI Standard)
-- Core Question: What drives revenue and profit, and where should the business focus?
-- ==============================================================================

-- DRIVER 1: Customer Segment Economics (Consumer vs. Corporate vs. Enterprise)
-- Evaluates which customer segment delivers highest LTV and margin stability
SELECT 
    customer_segment,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id)    AS total_transactions,
    ROUND(SUM(net_revenue) / 1000.0, 1) AS total_revenue_k,
    ROUND(SUM(gross_profit) / 1000.0, 1) AS total_profit_k,
    ROUND(AVG(net_revenue), 2)  AS avg_order_value_usd,
    ROUND(AVG(profit_margin_pct), 2) AS avg_margin_pct,
    ROUND(AVG(discount_pct), 2) AS avg_discount_applied_pct,
    ROUND((SUM(net_revenue) * 1.0) / COUNT(DISTINCT customer_id), 2) AS revenue_per_customer_usd
FROM fact_sales
WHERE year = 2022 
  AND order_status = 'Completed'
GROUP BY customer_segment
ORDER BY total_revenue_k DESC;


-- DRIVER 2: Channel Efficiency & Margin Realization
-- Direct Online vs Retail Store vs Partner Distributor vs Enterprise Sales
SELECT 
    sales_channel,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_revenue) / 1000.0, 1) AS channel_revenue_k,
    ROUND(SUM(gross_profit) / 1000.0, 1) AS channel_profit_k,
    ROUND((SUM(gross_profit) / SUM(net_revenue)) * 100.0, 2) AS realized_margin_pct,
    ROUND(AVG(discount_pct), 2) AS avg_discount_pct,
    ROUND(SUM(net_revenue) / COUNT(DISTINCT order_id), 2) AS channel_aov_usd
FROM fact_sales
WHERE year = 2022 
  AND order_status = 'Completed'
GROUP BY sales_channel
ORDER BY channel_revenue_k DESC;


-- DRIVER 3: Discount Elasticity & Margin Dilution Analysis
-- Quantifies how much profit is sacrificed when offering promotions
SELECT 
    CASE 
        WHEN discount_pct = 0.0 THEN '0% (Full Price)'
        WHEN discount_pct <= 5.0 THEN '1% - 5% (Low Discount)'
        WHEN discount_pct <= 10.0 THEN '6% - 10% (Moderate Discount)'
        WHEN discount_pct <= 15.0 THEN '11% - 15% (Heavy Discount)'
        ELSE '> 15% (Deep Clearance)'
    END AS discount_tier,
    COUNT(order_id) AS transaction_count,
    ROUND(SUM(gross_sales) / 1000.0, 1) AS gross_sales_k,
    ROUND(SUM(discount_amount) / 1000.0, 1) AS total_discount_given_k,
    ROUND(SUM(net_revenue) / 1000.0, 1) AS net_revenue_k,
    ROUND(SUM(gross_profit) / 1000.0, 1) AS gross_profit_k,
    ROUND((SUM(gross_profit) / SUM(net_revenue)) * 100.0, 2) AS effective_profit_margin_pct,
    ROUND(AVG(quantity), 2) AS avg_units_per_order
FROM fact_sales
WHERE year = 2022 
  AND order_status = 'Completed'
GROUP BY discount_tier
ORDER BY net_revenue_k DESC;


-- DRIVER 4: High Margin Attachment Opportunity (Category 8 Subscriptions & Care)
-- Measures customer cross-purchase behavior with recurring high-margin care plans
WITH order_composition AS (
    SELECT 
        order_id,
        customer_id,
        net_revenue,
        gross_profit,
        CASE WHEN category_code = 'Category 8' THEN 1 ELSE 0 END AS has_care_subscription,
        CASE WHEN category_code = 'Category 1' THEN 1 ELSE 0 END AS has_hardware_device
    FROM fact_sales
    WHERE year = 2022 AND order_status = 'Completed'
)
SELECT 
    CASE 
        WHEN has_care_subscription = 1 THEN 'Order with Care / Subscription'
        ELSE 'Standalone Hardware Order'
    END AS order_profile,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(net_revenue) / 1000.0, 1) AS total_revenue_k,
    ROUND(SUM(gross_profit) / 1000.0, 1) AS total_profit_k,
    ROUND((SUM(gross_profit) / SUM(net_revenue)) * 100.0, 2) AS realized_margin_pct,
    ROUND(AVG(net_revenue), 2) AS avg_basket_size_usd
FROM order_composition
GROUP BY order_profile;
