"""
Generate a production Jupyter Notebook for Data Science Portfolio.
"""
import json
import os

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Enterprise Retail Data Science: Predictive Modeling, Customer Segmentation & Statistical Testing\n",
    "**Project:** Retail Sales & Profitability Optimization  \n",
    "**Author:** Senior Data Analyst & Data Scientist (Google Standard)  \n",
    "**Techniques:** Time Series Forecasting, K-Means RFM Clustering, Random Forest Feature Importance, Two-Sample Welch's T-Test  \n",
    "**Stack:** Python (`pandas`, `numpy`, `scipy`, `scikit-learn`, `matplotlib`, `seaborn`)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Executive Context & Analytical Objectives\n",
    "This data science project addresses key executive commercial challenges:\n",
    "1. **Revenue Forecasting:** Predict Q1-Q2 2023 sales trajectory with 95% confidence intervals to guide supply chain replenishment.\n",
    "2. **Customer Segmentation:** Identify high-LTV customer cohorts through unsupervised RFM (Recency, Frequency, Monetary) clustering.\n",
    "3. **Profitability Attribution:** Quantify the predictive power of pricing, discounts, and merchandising categories on operating gross margin.\n",
    "4. **Statistical Rigor:** Test the promotional discount elasticity hypothesis to determine whether discounts drive statistically significant unit volume."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "import datetime\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "from scipy import stats\n",
    "from sklearn.cluster import KMeans\n",
    "from sklearn.preprocessing import StandardScaler\n",
    "from sklearn.ensemble import RandomForestRegressor\n",
    "from sklearn.metrics import silhouette_score, r2_score, mean_absolute_error\n",
    "\n",
    "# Plotting aesthetics\n",
    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
    "plt.rcParams['figure.figsize'] = (12, 6)\n",
    "plt.rcParams['font.size'] = 11\n",
    "\n",
    "# Load clean transactions\n",
    "DATA_PATH = os.path.join('..', 'data', 'processed', 'retail_sales_clean.csv')\n",
    "df = pd.read_csv(DATA_PATH)\n",
    "df['order_date'] = pd.to_datetime(df['order_date'])\n",
    "print(f\"Loaded {len(df):,} transactions across {df['order_date'].dt.year.nunique()} years.\")\n",
    "df.head(3)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Exploratory Data Analysis & Seasonality Decomposition"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Monthly aggregation for completed orders\n",
    "df_completed = df[df['order_status'] == 'Completed'].copy()\n",
    "df_completed['year_month'] = df_completed['order_date'].dt.to_period('M')\n",
    "monthly_ts = df_completed.groupby('year_month')['net_revenue'].sum() / 1000.0\n",
    "\n",
    "plt.figure(figsize=(14, 5))\n",
    "monthly_ts.plot(kind='bar', color='#0A3663', width=0.7)\n",
    "plt.title('Monthly Realized Sales ($K USD) - 2021 to 2022', fontsize=14, fontweight='bold', pad=15)\n",
    "plt.ylabel('Net Revenue ($K USD)')\n",
    "plt.xlabel('Fiscal Month')\n",
    "plt.xticks(rotation=45)\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Time Series Revenue Forecasting (Q1 & Q2 2023 with 95% Confidence Intervals)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Linear trend + seasonal multiplier model\n",
    "t_idx = np.arange(len(monthly_ts))\n",
    "y_vals = monthly_ts.values\n",
    "slope, intercept, r_val, p_val, std_err = stats.linregress(t_idx, y_vals)\n",
    "\n",
    "# Seasonality relative to 12-month trailing mean\n",
    "annual_mean = np.mean(y_vals[-12:])\n",
    "seasonality_factors = {}\n",
    "for i, p in enumerate(monthly_ts.index[-12:]):\n",
    "    seasonality_factors[p.month] = y_vals[-12 + i] / annual_mean\n",
    "\n",
    "# Forecast forward 6 months\n",
    "forecast_periods = [monthly_ts.index[-1] + step for step in range(1, 7)]\n",
    "predictions = []\n",
    "residuals_std = np.std(y_vals - (intercept + slope * t_idx))\n",
    "\n",
    "for step, p in enumerate(forecast_periods, start=1):\n",
    "    base = intercept + slope * (t_idx[-1] + step)\n",
    "    seasonal_pred = base * seasonality_factors.get(p.month, 1.0)\n",
    "    predictions.append({\n",
    "        'Period': str(p),\n",
    "        'Forecast ($K)': round(seasonal_pred, 1),\n",
    "        'CI Lower 95% ($K)': round(max(100, seasonal_pred - 1.96 * residuals_std), 1),\n",
    "        'CI Upper 95% ($K)': round(seasonal_pred + 1.96 * residuals_std, 1)\n",
    "    })\n",
    "\n",
    "df_forecast_res = pd.DataFrame(predictions)\n",
    "display(df_forecast_res)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Unsupervised ML: Customer RFM Segmentation via K-Means"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "snapshot = df['order_date'].max() + datetime.timedelta(days=1)\n",
    "rfm = df_completed.groupby('customer_id').agg({\n",
    "    'order_date': lambda x: (snapshot - x.max()).days,\n",
    "    'net_revenue': ['count', 'sum', 'mean']\n",
    "}).reset_index()\n",
    "rfm.columns = ['customer_id', 'recency', 'frequency', 'monetary', 'aov']\n",
    "\n",
    "scaler = StandardScaler()\n",
    "X_scaled = scaler.fit_transform(rfm[['recency', 'frequency', 'monetary', 'aov']])\n",
    "\n",
    "kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)\n",
    "rfm['cluster'] = kmeans.fit_predict(X_scaled)\n",
    "sil = silhouette_score(X_scaled, rfm['cluster'])\n",
    "print(f\"K-Means Silhouette Score: {sil:.3f}\")\n",
    "\n",
    "cluster_summary = rfm.groupby('cluster').agg({\n",
    "    'customer_id': 'count',\n",
    "    'monetary': 'mean',\n",
    "    'recency': 'mean',\n",
    "    'frequency': 'mean'\n",
    "}).rename(columns={'customer_id': 'Count', 'monetary': 'Avg Spend ($)', 'recency': 'Avg Recency (Days)', 'frequency': 'Avg Orders'})\n",
    "display(cluster_summary)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Supervised ML: Profitability Drivers via Random Forest"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_ml = df_completed[['profit_margin_pct', 'discount_pct', 'quantity', 'unit_price', 'category_name', 'customer_segment']].dropna()\n",
    "X_rf = pd.get_dummies(df_ml.drop(columns=['profit_margin_pct']), drop_first=True)\n",
    "y_rf = df_ml['profit_margin_pct']\n",
    "\n",
    "rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6)\n",
    "rf.fit(X_rf, y_rf)\n",
    "\n",
    "feat_imp = pd.Series(rf.feature_importances_, index=X_rf.columns).sort_values(ascending=False).head(8)\n",
    "plt.figure(figsize=(10, 4))\n",
    "feat_imp.plot(kind='barh', color='#2563EB')\n",
    "plt.title('Top Drivers of Operating Profit Margin % (Random Forest Gini Importance)', fontsize=12, fontweight='bold')\n",
    "plt.xlabel('Relative Feature Importance')\n",
    "plt.gca().invert_yaxis()\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 6. A/B Testing & Statistical Hypothesis Test: Promotional Discount Elasticity\n",
    "We test whether deep discounts (>10%) produce a statistically significant increase in units sold per order.\n",
    "- $H_0: \\mu_{\\text{Deep Discount}} = \\mu_{\\text{Low/No Discount}}$\n",
    "- $H_1: \\mu_{\\text{Deep Discount}} > \\mu_{\\text{Low/No Discount}}$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "low_disc = df_completed[df_completed['discount_pct'] <= 5.0]['quantity']\n",
    "high_disc = df_completed[df_completed['discount_pct'] > 10.0]['quantity']\n",
    "\n",
    "t_stat, p_val = stats.ttest_ind(high_disc, low_disc, equal_var=False)\n",
    "print(f\"Low Discount (<=5%) Mean Units:  {low_disc.mean():.2f} (n={len(low_disc)})\")\n",
    "print(f\"Deep Discount (>10%) Mean Units: {high_disc.mean():.2f} (n={len(high_disc)})\")\n",
    "print(f\"Welch's T-Statistic: {t_stat:.3f}\")\n",
    "print(f\"p-value: {p_val:.4f}\")\n",
    "\n",
    "if p_val > 0.05:\n",
    "    print(\"\\n=> CONCLUSION: Fail to reject H0 (p > 0.05). Promotional discounting does NOT yield statistically significant volume gains. It is purely margin-dilutive.\")\n",
    "else:\n",
    "    print(\"\\n=> CONCLUSION: Reject H0 (p <= 0.05). Significant volume elasticity observed.\")"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

nb_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "notebooks", "retail_data_science_modeling.ipynb")
with open(nb_path, "w", encoding="utf-8") as f:
    json.dump(notebook_content, f, indent=1)
print(f"Jupyter Notebook successfully written to: {nb_path}")
