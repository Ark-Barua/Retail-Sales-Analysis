# Data Dictionary & Documented Business Assumptions
**Project:** Enterprise Retail Sales & Profitability Analysis  
**Author:** Senior Data Analyst (Google Analytics & Business Intelligence)  
**Standard:** Google BI & Data Governance Framework  
**Scope:** Fiscal Year 2021 & 2022 Performance Review (Closing Dec 2022)

---

## 1. Executive Context & Business Objectives

### 1.1 Core Business Question
> *"What drives revenue and profit across our retail business, and where should leadership focus capital, inventory, and sales resources?"*

This data model and analytics suite serve executive leadership (VP of Sales, Chief Commercial Officer, VP of Finance) to dissect 2022 actual performance ($8.45M total revenue, $1.00M in Dec 2022) against operational budget targets (Plan) and prior-year performance (PY).

---

## 2. Documented Accounting & Analytical Assumptions

### 2.1 Revenue Recognition Standard (ASC 606 / IFRS 15)
1. **Net Revenue Realization:** Revenue is recognized when performance obligations are satisfied (at time of carrier shipment/delivery).
2. **Gross vs. Net Calculation:**
   $$\text{Gross Sales} = \text{Unit Price} \times \text{Quantity}$$
   $$\text{Discount Amount} = \text{Gross Sales} \times \text{Discount Rate}$$
   $$\text{Net Revenue} = \text{Gross Sales} - \text{Discount Amount} - \text{Returns \& Allowances}$$
3. **Returns Policy:** Transactions with `order_status = 'Returned'` are tracked for return-rate telemetry but netted out of finalized realized sales and profit figures.
4. **Currency Standardization:** All global transactions are normalized to USD ($) at monthly spot exchange rates.

### 2.2 Reporting Units & Variance Terminology (IBCS Standards)
Following the **International Business Communication Standards (IBCS)** implemented in the executive dashboard:
- **AC (Actual):** Realized commercial performance achieved in the designated time period.
- **PL (Plan / Budget):** Pre-committed operational baseline established during annual operating planning (AOP).
- **PY (Previous Year):** Actual historical performance for the identical period 12 months prior.
- **$\Delta$ PL (Dollar Variance):**
  $$\Delta \text{PL} = \text{AC} - \text{PL}$$
  *(Positive indicates Surplus/Favorable revenue realization; Negative indicates Deficit/Unfavorable shortfall).*
- **$\Delta$ PL % (Percentage Variance):**
  $$\Delta \text{PL} \% = \left(\frac{\text{AC} - \text{PL}}{\text{PL}}\right) \times 100\%$$
- **YoY Growth %:**
  $$\text{YoY Growth} \% = \left(\frac{\text{AC}_{2022} - \text{PY}_{2021}}{\text{PY}_{2021}}\right) \times 100\%$$
- **Display Scale:** High-level executive charts display figures in thousands of USD (**$K**) or millions (**$M**), where $1,000 = \$1,000,000$ USD.

### 2.3 Profitability & Unit Economics Levers
- **Cost of Goods Sold (COGS):** Includes direct hardware manufacturing costs, assembly, freight-in, and software hosting/licensing fees.
- **Gross Profit:**
  $$\text{Gross Profit} = \text{Net Revenue} - \text{COGS}$$
- **Gross Margin %:**
  $$\text{Gross Margin} \% = \left(\frac{\text{Gross Profit}}{\text{Net Revenue}}\right) \times 100\%$$
- **Average Order Value (AOV):**
  $$\text{AOV} = \frac{\sum \text{Net Revenue}}{\text{Count of Orders}}$$

---

## 3. Entity & Hierarchy Mapping

To maintain confidentiality while reflecting real operational structure, product categories and regional entities carry dual identifiers:

### 3.1 Regional Hierarchy
| Dashboard Label | Territory / Market | Regional Hub | Representative Market | Base Target Share |
|---|---|---|---|---|
| **Region 1** | North America West | Seattle / SF | USA (California, WA, OR) | 27.0% |
| **Region 2** | North America East | New York | USA (NY, MA, PA, NJ) | 20.0% |
| **Region 3** | EMEA Central | Frankfurt | Germany, France, Benelux | 19.0% |
| **Region 4** | APAC North | Tokyo | Japan, South Korea | 10.0% |
| **Region 5** | LATAM South | São Paulo | Brazil, Argentina, Chile | 10.0% |
| **Region 6** | UK & Ireland | London | United Kingdom, Ireland | 8.0% |
| **Region 7** | Emerging Markets | Bengaluru / SG | India, SE Asia | 6.0% |

### 3.2 Product Category Hierarchy
| Dashboard Label | Category Name | Margin Benchmark | Avg Unit Price | Primary Driver |
|---|---|---|---|---|
| **Category 1** | Electronics & Flagship Laptops | 38.0% | $750 | Volume & Core Revenue Anchor |
| **Category 2** | Mobile & Tablets | 35.0% | $550 | Enterprise Device Fleet Refresh |
| **Category 3** | Smart Home & IoT | 42.0% | $180 | High Growth / Ecosystem Pull |
| **Category 4** | Audio & Headphones | 45.0% | $120 | Consumer Accessory Add-on |
| **Category 5** | Gaming & VR Consoles | 28.0% | $400 | Holiday Season Spike Driver |
| **Category 6** | Peripherals & Accessories | 52.0% | $65 | High-Margin Basket Attach Rate |
| **Category 7** | Office Tech & Enterprise Software | 60.0% | $220 | High-Margin Contract Licensing |
| **Category 8** | Subscriptions & Care Services | 75.0% | $95 | Recurring High-Margin ARR |

---

## 4. Comprehensive Data Dictionary

### Table: `fact_sales` (Production Transaction Log)
Target Storage: SQLite / BigQuery / PostgreSQL warehouse.

| Column Name | Data Type | Nullable | Primary / Foreign Key | Description | Example Values |
|---|---|---|---|---|---|
| `order_id` | VARCHAR(30) | NO | PK | Unique identifier for customer purchase | `ORD-2022-10842` |
| `order_date` | DATE | NO | - | Timestamp when customer placed order | `2022-12-14` |
| `ship_date` | DATE | YES | - | Carrier dispatch timestamp | `2022-12-16` |
| `customer_id` | VARCHAR(20) | NO | FK | Unique master customer account identifier | `CUST-2184` |
| `customer_segment` | VARCHAR(30) | NO | - | Customer tier classification | `Consumer`, `Corporate`, `Enterprise` |
| `sales_channel` | VARCHAR(30) | NO | - | Fulfillment channel | `Direct Online`, `Retail Store`, `Partner` |
| `region_code` | VARCHAR(20) | NO | - | Dashboard visual reporting code | `Region 1` to `Region 7` |
| `region_name` | VARCHAR(50) | NO | - | Geographic sales territory | `North America West` |
| `country` | VARCHAR(50) | NO | - | Country destination | `United States`, `Germany` |
| `category_code` | VARCHAR(20) | NO | - | Dashboard visual category code | `Category 1` to `Category 8` |
| `category_name` | VARCHAR(50) | NO | - | Commercial merchandising category | `Electronics & Laptops` |
| `product_sku` | VARCHAR(30) | NO | - | Stock Keeping Unit code | `SKU-1-118` |
| `quantity` | INTEGER | NO | - | Units purchased | `1`, `2`, `5` |
| `unit_price` | DECIMAL(10,2) | NO | - | List selling price per unit in USD | `749.99` |
| `gross_sales` | DECIMAL(12,2) | NO | - | Total sales before discount (`qty * price`) | `1,499.98` |
| `discount_pct` | DECIMAL(5,2) | NO | - | Promotional discount applied (%) | `0.0`, `10.0`, `15.0` |
| `discount_amount` | DECIMAL(10,2) | NO | - | Absolute monetary discount in USD | `149.99` |
| `net_revenue` | DECIMAL(12,2) | NO | - | Net billed revenue realized | `1,349.99` |
| `cogs` | DECIMAL(12,2) | NO | - | Cost of Goods Sold in USD | `836.99` |
| `gross_profit` | DECIMAL(12,2) | NO | - | Dollar gross margin (`net_rev - cogs`) | `513.00` |
| `profit_margin_pct` | DECIMAL(5,2) | NO | - | Margin percentage (`profit / revenue * 100`) | `38.00` |
| `order_status` | VARCHAR(20) | NO | - | Order state | `Completed`, `Returned` |
| `year` | INTEGER | NO | - | Calendar year | `2021`, `2022` |
| `month` | INTEGER | NO | - | Month number (1-12) | `12` |
| `month_name` | VARCHAR(10) | NO | - | Abbreviated month string | `Dec` |

---

## 5. Staging & Quality Assurance Validation Checks

Prior to warehouse ingestion, data undergoes automated validation checks:
1. **Uniqueness:** Zero duplicate `order_id` values permitted in `fact_sales`.
2. **Referential Integrity:** `net_revenue` must equal `gross_sales - discount_amount`.
3. **Margin Consistency:** `profit_margin_pct` must fall within legitimate operational bounds $[0.0\%, 90.0\%]$.
4. **Temporal Logic:** `ship_date >= order_date` for all completed fulfillment.
5. **Categorical Integrity:** Category codes must map exclusively to recognized active SKUs.
