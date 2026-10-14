# Power BI Semantic Data Model & Implementation Architecture
**Author:** Senior Data Analyst (Google BI Standard)  
**Standard:** Enterprise Kimball Star Schema Architecture

---

## 1. Dimensional Architecture Overview

To support executive-level reporting with sub-second analytical query performance, the Power BI data model implements a classic **Kimball Star Schema**:

```
                       ┌───────────────────────┐
                       │       dim_date        │
                       │───────────────────────│
                       │ Date (PK)             │
                       │ Year, Quarter, Month  │
                       │ MonthName, DayOfWeek  │
                       └───────────┬───────────┘
                                   │ 1:N
                                   ▼
┌───────────────────────┐      ┌────────────────────────┐      ┌───────────────────────┐
│      dim_region       │      │       fact_sales       │      │      dim_product      │
│───────────────────────│ 1:N  │────────────────────────│  1:N │───────────────────────│
│ region_code (PK)      ├─────►│ order_id (PK)          │◄─────┤ category_code (PK)    │
│ region_name           │      │ order_date (FK)        │      │ category_name         │
│ country               │      │ customer_id (FK)       │      │ product_sku           │
│ regional_target_k     │      │ region_code (FK)       │      │ unit_price_base       │
└───────────────────────┘      │ category_code (FK)     │      │ target_margin_pct     │
                               │ quantity, unit_price   │      └───────────────────────┘
┌───────────────────────┐      │ net_revenue, cogs      │
│     dim_customer      │ 1:N  │ gross_profit           │
│───────────────────────├─────►│ discount_pct           │
│ customer_id (PK)      │      │ order_status           │
│ customer_segment      │      └────────────────────────┘
│ sales_channel         │
└───────────────────────┘
```

---

## 2. Table Relationships & Cardinality Configuration

| From Table (Dimension) | From Column (PK) | To Table (Fact) | To Column (FK) | Cardinality | Cross Filter Direction | Active |
|:---|:---|:---|:---|:---|:---|:---|
| `dim_date` | `Date` | `fact_sales` | `order_date` | 1 to Many ($1:*$) | Single | Yes |
| `dim_product` | `category_code` | `fact_sales` | `category_code` | 1 to Many ($1:*$) | Single | Yes |
| `dim_region` | `region_code` | `fact_sales` | `region_code` | 1 to Many ($1:*$) | Single | Yes |
| `dim_customer` | `customer_id` | `fact_sales` | `customer_id` | 1 to Many ($1:*$) | Single | Yes |

---

## 3. Power BI Visual Configuration for IBCS Dashboard Replication

To achieve the exact layout seen in executive reporting:
1. **Top-Left (Yearly Revenue Generated):**
   - Visual: **Waterfall Chart** (native Power BI or Zebra BI Charts visual).
   - Category: Period (`PY`, `Variance Bridge`, `AC`).
   - Y-Axis: `[Total Net Revenue]` with conditional color rules (Navy `#0A3663`, Light Blue `#A4D2F6`, Favorable Bridge `#7CC444`).
2. **Top-Right (Monthly Sales):**
   - Visual: **Clustered Column Chart with Error Bars or Zebra BI IBCS Chart**.
   - X-Axis: `dim_date[MonthName]` sorted by `dim_date[MonthNumber]`.
   - Y-Axis: `[Total Net Revenue]` (Navy bars) + `[Revenue Variance % (Delta PL %)]` (Green/Red variance callouts).
3. **Bottom-Left (Sales – Region):**
   - Visual: **Matrix Visual / Zebra BI Tables**.
   - Rows: `dim_region[region_code]` or `dim_region[region_name]`.
   - Values: `[Total Net Revenue]`, `[Revenue Variance (Delta PL)]`, `[Revenue Variance % (Delta PL %)]`.
   - Formatting: Data bars enabled for `[Total Net Revenue]` (Navy blue) and diverging bars for `[Delta PL]` (Green right for surplus, Red left for deficit).
4. **Bottom-Right (Sales – Product Category):**
   - Visual: **Matrix Visual / Zebra BI Tables**.
   - Rows: `dim_product[category_code]`.
   - Values: `[Planned Category Revenue]`, `[Total Net Revenue]`, `[Revenue Variance (Delta PL)]`, `[Revenue Variance % (Delta PL %)]`.
   - Total Row: Highlighted in light blue (`#E6F2FA`) with bold summary typography.
