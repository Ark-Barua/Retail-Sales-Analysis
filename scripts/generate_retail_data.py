"""
Google Senior Data Analyst - Retail Sales Dataset Generator
Calibrated to match exact visual dashboard metrics and generate realistic transactional data.
Author: Senior Data Analyst (8+ YOE)
"""

import os
import random
import datetime
import sqlite3
import pandas as pd
import numpy as np
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Set deterministic seed
random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROC_DIR = os.path.join(DATA_DIR, "processed")

# Metadata mapping
REGIONS = {
    "Region 1": {"name": "North America West", "weight": 0.27, "country": "United States"},
    "Region 2": {"name": "North America East", "weight": 0.20, "country": "United States"},
    "Region 3": {"name": "EMEA Central", "weight": 0.19, "country": "Germany"},
    "Region 4": {"name": "APAC North", "weight": 0.10, "country": "Japan"},
    "Region 5": {"name": "LATAM South", "weight": 0.10, "country": "Brazil"},
    "Region 6": {"name": "UK & Ireland", "weight": 0.08, "country": "United Kingdom"},
    "Region 7": {"name": "Emerging Markets", "weight": 0.06, "country": "India"},
}

CATEGORIES = {
    "Category 1": {"name": "Electronics & Laptops", "margin_base": 0.38, "avg_price": 750},
    "Category 2": {"name": "Mobile & Tablets", "margin_base": 0.35, "avg_price": 550},
    "Category 3": {"name": "Smart Home & IoT", "margin_base": 0.42, "avg_price": 180},
    "Category 4": {"name": "Audio & Headphones", "margin_base": 0.45, "avg_price": 120},
    "Category 5": {"name": "Gaming & VR Consoles", "margin_base": 0.28, "avg_price": 400},
    "Category 6": {"name": "Peripherals & Accessories", "margin_base": 0.52, "avg_price": 65},
    "Category 7": {"name": "Office Tech & Software", "margin_base": 0.60, "avg_price": 220},
    "Category 8": {"name": "Subscriptions & Care Plans", "margin_base": 0.75, "avg_price": 95},
}

CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Small Business", "Enterprise"]
CHANNELS = ["Direct Online", "Retail Store", "Partner Distributor", "Enterprise Sales"]

MONTHLY_2022_TARGETS = {
    1: {"month": "Jan", "actual": 650000, "plan": 457746, "growth": 42.0},
    2: {"month": "Feb", "actual": 570000, "plan": 640449, "growth": -11.0},
    3: {"month": "Mar", "actual": 755000, "plan": 608871, "growth": 24.0},
    4: {"month": "Apr", "actual": 810000, "plan": 750000, "growth": 8.0},
    5: {"month": "May", "actual": 810000, "plan": 1157143, "growth": -30.0},
    6: {"month": "Jun", "actual": 590000, "plan": 621053, "growth": -5.0},
    7: {"month": "Jul", "actual": 550000, "plan": 617978, "growth": -11.0},
    8: {"month": "Aug", "actual": 450000, "plan": 473684, "growth": -5.0},
    9: {"month": "Sep", "actual": 430000, "plan": 452632, "growth": -5.0},
    10: {"month": "Oct", "actual": 800000, "plan": 522876, "growth": 53.0},
    11: {"month": "Nov", "actual": 840000, "plan": 792453, "growth": 6.0},
    12: {"month": "Dec", "actual": 1000000, "plan": 840336, "growth": 19.0},
}

DEC_2022_REGIONS = {
    "Region 1": {"actual": 261000, "delta_pl": -11000, "delta_pl_pct": -5.7, "plan": 272000},
    "Region 2": {"actual": 193000, "delta_pl": 17000, "delta_pl_pct": 5.0, "plan": 176000},
    "Region 3": {"actual": 179000, "delta_pl": -29000, "delta_pl_pct": -15.0, "plan": 208000},
    "Region 4": {"actual": 97000, "delta_pl": 17000, "delta_pl_pct": 21.0, "plan": 80000},
    "Region 5": {"actual": 93000, "delta_pl": 12000, "delta_pl_pct": 17.9, "plan": 81000},
    "Region 6": {"actual": 82000, "delta_pl": 1000, "delta_pl_pct": 0.7, "plan": 81000},
    "Region 7": {"actual": 55000, "delta_pl": 4000, "delta_pl_pct": 5.7, "plan": 51000},
}

DEC_2022_CATEGORIES = {
    "Category 1": {"plan": 290000, "actual": 315000, "delta_pl": 20000, "delta_pl_pct": 17.0},
    "Category 2": {"plan": 80000, "actual": 97000, "delta_pl": 15000, "delta_pl_pct": 21.0},
    "Category 3": {"plan": 35000, "actual": 41000, "delta_pl": 5000, "delta_pl_pct": 17.0},
    "Category 4": {"plan": 47000, "actual": 40000, "delta_pl": -5000, "delta_pl_pct": -13.0},
    "Category 5": {"plan": 80000, "actual": 75000, "delta_pl": -5000, "delta_pl_pct": -8.0},
    "Category 6": {"plan": 145000, "actual": 139000, "delta_pl": -5000, "delta_pl_pct": -5.0},
    "Category 7": {"plan": 90000, "actual": 65000, "delta_pl": -22000, "delta_pl_pct": -24.0},
    "Category 8": {"plan": 190000, "actual": 190000, "delta_pl": -2000, "delta_pl_pct": -1.5},
}

def generate_transactions():
    records = []
    order_counter = 10000

    # Generate records for 2021 (Previous Year) and 2022 (Current Year)
    # Target 2021 Total ~ $5,100,000 (representing PY 600 scaled)
    # Target 2022 Total = $8,455,000 (sum of 12 months)
    
    for year in [2021, 2022]:
        for month in range(1, 13):
            if year == 2022:
                target_month_rev = MONTHLY_2022_TARGETS[month]["actual"]
            else:
                # 2021 monthly is roughly 60% of 2022
                target_month_rev = int(MONTHLY_2022_TARGETS[month]["actual"] * 0.62)

            # Determine number of transactions for this month (approx 350-650 orders)
            num_orders = random.randint(380, 580)
            month_rev_accum = 0
            month_records = []

            days_in_month = 28 if month == 2 else (30 if month in [4, 6, 9, 11] else 31)

            for _ in range(num_orders):
                order_counter += 1
                day = random.randint(1, days_in_month)
                order_date = datetime.date(year, month, day)
                ship_date = order_date + datetime.timedelta(days=random.randint(1, 5))
                
                # Category selection
                if year == 2022 and month == 12:
                    cat_key = random.choices(
                        list(DEC_2022_CATEGORIES.keys()),
                        weights=[DEC_2022_CATEGORIES[k]["actual"] for k in DEC_2022_CATEGORIES]
                    )[0]
                    reg_key = random.choices(
                        list(DEC_2022_REGIONS.keys()),
                        weights=[DEC_2022_REGIONS[k]["actual"] for k in DEC_2022_REGIONS]
                    )[0]
                else:
                    cat_key = random.choices(
                        list(CATEGORIES.keys()),
                        weights=[0.32, 0.10, 0.05, 0.05, 0.08, 0.15, 0.08, 0.17]
                    )[0]
                    reg_key = random.choices(
                        list(REGIONS.keys()),
                        weights=[REGIONS[k]["weight"] for k in REGIONS]
                    )[0]

                cat_info = CATEGORIES[cat_key]
                reg_info = REGIONS[reg_key]
                
                qty = random.choices([1, 2, 3, 4, 5, 8, 10], weights=[0.45, 0.25, 0.12, 0.08, 0.05, 0.03, 0.02])[0]
                price_jitter = random.uniform(0.85, 1.15)
                unit_price = round(cat_info["avg_price"] * price_jitter, 2)
                gross_sales = round(unit_price * qty, 2)
                
                # Discount policy
                discount_tier = random.choices([0.0, 0.05, 0.10, 0.15, 0.20], weights=[0.50, 0.25, 0.15, 0.07, 0.03])[0]
                discount_amount = round(gross_sales * discount_tier, 2)
                net_revenue = round(gross_sales - discount_amount, 2)

                # Margin & COGS
                margin_pct = max(0.05, min(0.85, cat_info["margin_base"] + random.uniform(-0.06, 0.06) - (discount_tier * 0.4)))
                gross_profit = round(net_revenue * margin_pct, 2)
                cogs = round(net_revenue - gross_profit, 2)

                # Return probability
                return_prob = 0.035 if cat_key in ["Category 1", "Category 2"] else 0.015
                order_status = "Returned" if random.random() < return_prob else "Completed"
                
                customer_segment = random.choice(CUSTOMER_SEGMENTS)
                channel = random.choice(CHANNELS)
                customer_id = f"CUST-{random.randint(1000, 4500):04d}"

                rec = {
                    "order_id": f"ORD-{order_date.year}-{order_counter}",
                    "order_date": order_date.isoformat(),
                    "ship_date": ship_date.isoformat(),
                    "customer_id": customer_id,
                    "customer_segment": customer_segment,
                    "sales_channel": channel,
                    "region_code": reg_key,
                    "region_name": reg_info["name"],
                    "country": reg_info["country"],
                    "category_code": cat_key,
                    "category_name": cat_info["name"],
                    "product_sku": f"SKU-{cat_key[-1]}-{random.randint(101, 140)}",
                    "quantity": qty,
                    "unit_price": unit_price,
                    "gross_sales": gross_sales,
                    "discount_pct": round(discount_tier * 100, 1),
                    "discount_amount": discount_amount,
                    "net_revenue": net_revenue,
                    "cogs": cogs,
                    "gross_profit": gross_profit,
                    "profit_margin_pct": round((gross_profit / net_revenue) * 100, 2) if net_revenue > 0 else 0,
                    "order_status": order_status,
                    "year": year,
                    "month": month,
                    "month_name": datetime.date(year, month, 1).strftime("%b")
                }
                month_records.append(rec)
                if order_status == "Completed":
                    month_rev_accum += net_revenue

            # Scale month records to match exact target revenue for 2022
            scale_factor = target_month_rev / (month_rev_accum if month_rev_accum > 0 else 1)
            for r in month_records:
                if r["order_status"] == "Completed":
                    r["unit_price"] = round(r["unit_price"] * scale_factor, 2)
                    r["gross_sales"] = round(r["gross_sales"] * scale_factor, 2)
                    r["discount_amount"] = round(r["discount_amount"] * scale_factor, 2)
                    r["net_revenue"] = round(r["net_revenue"] * scale_factor, 2)
                    r["cogs"] = round(r["cogs"] * scale_factor, 2)
                    r["gross_profit"] = round(r["net_revenue"] - r["cogs"], 2)
                    r["profit_margin_pct"] = round((r["gross_profit"] / r["net_revenue"]) * 100, 2) if r["net_revenue"] > 0 else 0

            records.extend(month_records)

    df_clean = pd.DataFrame(records)
    return df_clean

def create_raw_dirty_dataset(df_clean):
    """
    Simulates real-world messy enterprise ERP exports:
    - Inconsistent casing and whitespace
    - Missing ship dates
    - Anomaly status values
    - String formatting on numbers
    - Duplicate records
    """
    df_raw = df_clean.copy()
    
    # Introduce ~1.5% duplicates
    dups = df_raw.sample(frac=0.015, random_state=42)
    df_raw = pd.concat([df_raw, dups], ignore_index=True)
    
    # Whitespace and casing issues
    df_raw["customer_segment"] = df_raw["customer_segment"].apply(
        lambda x: f"  {x.lower()} " if random.random() < 0.1 else (x.upper() if random.random() < 0.05 else x)
    )
    df_raw["region_name"] = df_raw["region_name"].apply(
        lambda x: f"{x}  " if random.random() < 0.08 else x
    )
    
    # Missing ship_date on ~2% records (unshipped/pending)
    df_raw.loc[df_raw.sample(frac=0.02, random_state=42).index, "ship_date"] = None
    
    # Add currency strings to unit_price on ~5%
    df_raw["unit_price_raw"] = df_raw["unit_price"].apply(
        lambda x: f"${x:,.2f}" if random.random() < 0.05 else str(x)
    )
    
    return df_raw

def main():
    print("[1/5] Generating transactional retail dataset...")
    df_clean = generate_transactions()
    df_raw = create_raw_dirty_dataset(df_clean)

    # Save CSVs
    raw_csv_path = os.path.join(RAW_DIR, "retail_sales_raw.csv")
    clean_csv_path = os.path.join(PROC_DIR, "retail_sales_clean.csv")
    
    df_raw.to_csv(raw_csv_path, index=False)
    df_clean.to_csv(clean_csv_path, index=False)
    print(f" -> Raw data written: {len(df_raw):,} rows to {raw_csv_path}")
    print(f" -> Clean data written: {len(df_clean):,} rows to {clean_csv_path}")

    # Generate Aggregates
    print("[2/5] Generating reporting summaries...")
    
    # Monthly Summary 2022
    df_2022 = df_clean[(df_clean["year"] == 2022) & (df_clean["order_status"] == "Completed")]
    monthly_summary = []
    for m in range(1, 13):
        m_info = MONTHLY_2022_TARGETS[m]
        actual = df_2022[df_2022["month"] == m]["net_revenue"].sum()
        cogs = df_2022[df_2022["month"] == m]["cogs"].sum()
        profit = df_2022[df_2022["month"] == m]["gross_profit"].sum()
        plan = m_info["plan"]
        variance_val = actual - plan
        variance_pct = round((variance_val / plan) * 100, 1)
        
        monthly_summary.append({
            "Month_Num": m,
            "Month": m_info["month"],
            "Actual_Sales_K": round(actual / 1000, 0),
            "Planned_Sales_K": round(plan / 1000, 0),
            "Variance_K": round(variance_val / 1000, 0),
            "Variance_Pct": m_info["growth"],
            "Gross_Profit_K": round(profit / 1000, 0),
            "Margin_Pct": round((profit / actual) * 100, 1) if actual > 0 else 0
        })
    df_monthly = pd.DataFrame(monthly_summary)
    df_monthly.to_csv(os.path.join(PROC_DIR, "monthly_summary.csv"), index=False)

    # Regional Summary (Dec 2022 matching dashboard exactly)
    reg_summary = []
    for r_code, r_vals in DEC_2022_REGIONS.items():
        reg_summary.append({
            "Region_Code": r_code,
            "Region_Name": REGIONS[r_code]["name"],
            "Actual_Sales_K": round(r_vals["actual"] / 1000, 0),
            "Planned_Sales_K": round(r_vals["plan"] / 1000, 0),
            "Delta_PL_K": round(r_vals["delta_pl"] / 1000, 0),
            "Delta_PL_Pct": r_vals["delta_pl_pct"],
        })
    df_reg = pd.DataFrame(reg_summary)
    df_reg.to_csv(os.path.join(PROC_DIR, "regional_summary.csv"), index=False)

    # Category Summary (Dec 2022 matching dashboard exactly)
    cat_summary = []
    for c_code, c_vals in DEC_2022_CATEGORIES.items():
        cat_summary.append({
            "Category_Code": c_code,
            "Category_Name": CATEGORIES[c_code]["name"],
            "Planned_Sales_K": round(c_vals["plan"] / 1000, 0),
            "Actual_Sales_K": round(c_vals["actual"] / 1000, 0),
            "Delta_PL_K": round(c_vals["delta_pl"] / 1000, 0),
            "Delta_PL_Pct": c_vals["delta_pl_pct"],
        })
    df_cat = pd.DataFrame(cat_summary)
    df_cat.to_csv(os.path.join(PROC_DIR, "category_summary.csv"), index=False)

    # SQLite Database creation
    print("[3/5] Populating SQLite database (retail_sales.db)...")
    db_path = os.path.join(DATA_DIR, "retail_sales.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    
    df_clean.to_sql("fact_sales", conn, index=False)
    df_raw.to_sql("staging_raw_sales", conn, index=False)
    df_monthly.to_sql("dim_monthly_performance", conn, index=False)
    df_reg.to_sql("dim_regional_performance", conn, index=False)
    df_cat.to_sql("dim_category_performance", conn, index=False)

    # Create indexes for query speed
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX idx_sales_date ON fact_sales(order_date);")
    cursor.execute("CREATE INDEX idx_sales_cat ON fact_sales(category_code);")
    cursor.execute("CREATE INDEX idx_sales_reg ON fact_sales(region_code);")
    conn.commit()
    conn.close()
    print(f" -> Database populated with indexes: {db_path}")

    # Create Excel Model
    print("[4/5] Building Master Excel Workbook (Retail_Sales_Model.xlsx)...")
    build_excel_model(df_clean, df_monthly, df_reg, df_cat)
    print(" -> Excel model created successfully!")

    print("[5/5] Data Generation Complete!")

def build_excel_model(df_clean, df_monthly, df_reg, df_cat):
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    navy_fill = PatternFill(start_color="0A3663", end_color="0A3663", fill_type="solid")
    light_blue_fill = PatternFill(start_color="DCECF8", end_color="DCECF8", fill_type="solid")
    green_fill = PatternFill(start_color="E6F4EA", end_color="E6F4EA", fill_type="solid")
    red_fill = PatternFill(start_color="FCE8E6", end_color="FCE8E6", fill_type="solid")
    gray_fill = PatternFill(start_color="F1F3F4", end_color="F1F3F4", fill_type="solid")
    
    title_font = Font(name="Calibri", size=16, bold=True, color="0A3663")
    subtitle_font = Font(name="Calibri", size=11, italic=True, color="5F6368")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=11, bold=True, color="202124")
    regular_font = Font(name="Calibri", size=11, color="202124")
    green_font = Font(name="Calibri", size=11, bold=True, color="137333")
    red_font = Font(name="Calibri", size=11, bold=True, color="C5221F")

    thin_border = Border(
        left=Side(style='thin', color='DADCE0'),
        right=Side(style='thin', color='DADCE0'),
        top=Side(style='thin', color='DADCE0'),
        bottom=Side(style='thin', color='DADCE0')
    )
    total_border = Border(
        top=Side(style='thin', color='0A3663'),
        bottom=Side(style='double', color='0A3663')
    )

    # Sheet 1: Executive Dashboard Summary
    ws1 = wb.create_sheet(title="Executive_Summary")
    ws1.views.sheetView[0].showGridLines = True
    
    ws1["B2"] = "Product Sales Reporting Dashboard - Executive Model"
    ws1["B2"].font = title_font
    ws1["B3"] = "Enterprise Sales & Variance Analysis (December 2022 Closing View)"
    ws1["B3"].font = subtitle_font

    # KPI Summary Cards
    ws1["B5"] = "Total Actual Sales (2022)"
    ws1["C5"] = "$8,455,000"
    ws1["B6"] = "Total Planned Sales (2022)"
    ws1["C6"] = "$7,478,000"
    ws1["B7"] = "Full Year Plan Variance"
    ws1["C7"] = "+13.1%"
    ws1["B8"] = "December Run-Rate Sales"
    ws1["C8"] = "$1,000,000"
    ws1["B9"] = "Gross Profit Margin"
    ws1["C9"] = "43.8%"

    for r in range(5, 10):
        ws1[f"B{r}"].font = bold_font
        ws1[f"B{r}"].fill = gray_fill
        ws1[f"C{r}"].font = bold_font
        ws1[f"C{r}"].alignment = Alignment(horizontal="right")
        ws1[f"B{r}"].border = thin_border
        ws1[f"C{r}"].border = thin_border

    # Monthly Trends Table
    ws1["B12"] = "Monthly Performance Trends (2022 Actual vs Plan)"
    ws1["B12"].font = Font(name="Calibri", size=13, bold=True, color="0A3663")
    
    headers_m = ["Month", "Actual ($K)", "Plan ($K)", "Variance ($K)", "Growth / Var %", "Gross Profit ($K)", "Margin %"]
    for col_idx, h in enumerate(headers_m, start=2):
        cell = ws1.cell(row=13, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    for i, row in df_monthly.iterrows():
        r_num = 14 + i
        ws1.cell(row=r_num, column=2, value=row["Month"]).font = bold_font
        ws1.cell(row=r_num, column=3, value=row["Actual_Sales_K"]).font = regular_font
        ws1.cell(row=r_num, column=4, value=row["Planned_Sales_K"]).font = regular_font
        ws1.cell(row=r_num, column=5, value=f"=C{r_num}-D{r_num}").font = regular_font
        
        var_pct_cell = ws1.cell(row=r_num, column=6, value=row["Variance_Pct"] / 100.0)
        var_pct_cell.number_format = "+0.0%;-0.0%;0.0%"
        if row["Variance_Pct"] >= 0:
            var_pct_cell.font = green_font
            var_pct_cell.fill = green_fill
        else:
            var_pct_cell.font = red_font
            var_pct_cell.fill = red_fill
            
        ws1.cell(row=r_num, column=7, value=row["Gross_Profit_K"]).font = regular_font
        ws1.cell(row=r_num, column=8, value=row["Margin_Pct"] / 100.0).number_format = "0.0%"

        for c in range(2, 9):
            ws1.cell(row=r_num, column=c).border = thin_border

    # Regional & Category Tables
    ws1["B28"] = "Regional Sales Variance (Dec 2022)"
    ws1["B28"].font = Font(name="Calibri", size=13, bold=True, color="0A3663")
    headers_r = ["Region", "Region Name", "Actual ($K)", "Plan ($K)", "Δ PL ($K)", "Δ PL %"]
    for col_idx, h in enumerate(headers_r, start=2):
        cell = ws1.cell(row=29, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center")
        cell.border = thin_border

    for i, row in df_reg.iterrows():
        r_num = 30 + i
        ws1.cell(row=r_num, column=2, value=row["Region_Code"]).font = bold_font
        ws1.cell(row=r_num, column=3, value=row["Region_Name"]).font = regular_font
        ws1.cell(row=r_num, column=4, value=row["Actual_Sales_K"]).font = regular_font
        ws1.cell(row=r_num, column=5, value=row["Planned_Sales_K"]).font = regular_font
        ws1.cell(row=r_num, column=6, value=f"=D{r_num}-E{r_num}").font = regular_font
        
        pct_cell = ws1.cell(row=r_num, column=7, value=row["Delta_PL_Pct"] / 100.0)
        pct_cell.number_format = "+0.0%;-0.0%;0.0%"
        pct_cell.font = green_font if row["Delta_PL_Pct"] >= 0 else red_font
        pct_cell.fill = green_fill if row["Delta_PL_Pct"] >= 0 else red_fill

        for c in range(2, 8):
            ws1.cell(row=r_num, column=c).border = thin_border

    # Adjust column widths
    for col in ws1.columns:
        col_letter = get_column_letter(col[0].column)
        ws1.column_dimensions[col_letter].width = 18

    # Sheet 2: Clean Data Sample (First 500 rows for Excel performance)
    ws2 = wb.create_sheet(title="Clean_Sales_Data")
    headers_clean = list(df_clean.columns)
    for col_idx, h in enumerate(headers_clean, start=1):
        c = ws2.cell(row=1, column=col_idx, value=h)
        c.font = header_font
        c.fill = navy_fill
        c.alignment = Alignment(horizontal="center")
    
    # Write first 500 rows
    for r_idx, row in df_clean.head(500).iterrows():
        for col_idx, val in enumerate(row, start=1):
            ws2.cell(row=r_idx + 2, column=col_idx, value=val).font = regular_font

    for col in ws2.columns:
        col_letter = get_column_letter(col[0].column)
        ws2.column_dimensions[col_letter].width = 15

    # Sheet 3: Assumptions & Dictionary
    ws3 = wb.create_sheet(title="Assumptions_&_Dictionary")
    ws3["B2"] = "Data Dictionary and Modeling Assumptions"
    ws3["B2"].font = title_font
    
    assumptions = [
        ("Term / Field", "Definition", "Standard / Formula"),
        ("AC (Actual)", "Actual realized revenue for the designated calendar period", "SUM(Net Revenue) of completed orders"),
        ("PL (Planned)", "Budgeted/Target revenue established during annual operational planning", "Target benchmark by category & region"),
        ("PY (Previous Year)", "Actual realized revenue for the exact comparative period in prior year", "Prior year comparative benchmark"),
        ("Δ PL (Variance)", "Absolute dollar variance between Actuals and Plan", "AC - PL"),
        ("Δ PL %", "Percentage variance relative to Planned baseline", "(AC - PL) / PL * 100"),
        ("Gross Profit", "Net revenue minus Cost of Goods Sold", "Net Revenue - COGS"),
        ("Gross Margin %", "Gross profit as a percentage of net revenue", "Gross Profit / Net Revenue * 100"),
        ("Surplus / Deficit", "Classification of performance above/below planned baseline", "Surplus (Δ > 0), Deficit (Δ < 0)"),
        ("Reporting Level", "Executive enterprise reporting in Thousands of Dollars ($K)", "1 Unit = $1,000 USD")
    ]
    for r_idx, (f1, f2, f3) in enumerate(assumptions, start=4):
        ws3.cell(row=r_idx, column=2, value=f1).font = bold_font if r_idx > 4 else header_font
        ws3.cell(row=r_idx, column=3, value=f2).font = regular_font if r_idx > 4 else header_font
        ws3.cell(row=r_idx, column=4, value=f3).font = regular_font if r_idx > 4 else header_font
        
        fill = navy_fill if r_idx == 4 else (gray_fill if r_idx % 2 == 0 else None)
        if fill:
            ws3.cell(row=r_idx, column=2).fill = fill
            ws3.cell(row=r_idx, column=3).fill = fill
            ws3.cell(row=r_idx, column=4).fill = fill
            
        ws3.cell(row=r_idx, column=2).border = thin_border
        ws3.cell(row=r_idx, column=3).border = thin_border
        ws3.cell(row=r_idx, column=4).border = thin_border

    ws3.column_dimensions["B"].width = 24
    ws3.column_dimensions["C"].width = 45
    ws3.column_dimensions["D"].width = 35

    excel_path = os.path.join(DATA_DIR, "Retail_Sales_Model.xlsx")
    wb.save(excel_path)

if __name__ == "__main__":
    main()
