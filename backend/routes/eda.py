from fastapi import APIRouter
import pandas as pd
import numpy as np
from backend.services.data_service import data_service

router = APIRouter(prefix="/api/eda", tags=["Exploratory Data Analysis"])

@router.get("")
def get_eda_data():
    df = data_service.get_retail_data()
    if df.empty:
        return {"error": "Dataset not available"}

    numeric_cols = ["Price", "Units Sold", "Inventory Level", "Units Ordered", "Demand Forecast", "Revenue"]
    available_num_cols = [c for c in numeric_cols if c in df.columns]

    # Summary Statistics
    summary_stats = []
    for col in available_num_cols:
        series = df[col]
        summary_stats.append({
            "column": col,
            "count": int(series.count()),
            "mean": round(float(series.mean()), 2),
            "std": round(float(series.std()), 2),
            "min": round(float(series.min()), 2),
            "q25": round(float(series.quantile(0.25)), 2),
            "median": round(float(series.median()), 2),
            "q75": round(float(series.quantile(0.75)), 2),
            "max": round(float(series.max()), 2),
        })

    # Missing Value Analysis
    missing_analysis = []
    for col in df.columns:
        null_count = int(df[col].isna().sum())
        missing_analysis.append({
            "column": col,
            "data_type": str(df[col].dtype),
            "null_count": null_count,
            "null_pct": round(float(null_count / len(df) * 100), 2),
            "unique_values": int(df[col].nunique())
        })

    # Correlation Matrix
    corr_df = df[available_num_cols].corr()
    correlation_matrix = []
    for row_col in available_num_cols:
        row_dict = {"feature": row_col}
        for col_name in available_num_cols:
            row_dict[col_name] = round(float(corr_df.loc[row_col, col_name]), 3)
        correlation_matrix.append(row_dict)

    # Histograms (Price, Demand, Inventory)
    def compute_hist(series, num_bins=12):
        counts, bin_edges = np.histogram(series.dropna(), bins=num_bins)
        hist_data = []
        for i in range(len(counts)):
            hist_data.append({
                "range": f"${round(bin_edges[i], 1)} - ${round(bin_edges[i+1], 1)}" if "Price" in series.name else f"{int(bin_edges[i])} - {int(bin_edges[i+1])}",
                "min": round(float(bin_edges[i]), 1),
                "max": round(float(bin_edges[i+1]), 1),
                "count": int(counts[i])
            })
        return hist_data

    price_hist = compute_hist(df["Price"], 12)
    demand_hist = compute_hist(df["Units Sold"], 12)
    inventory_hist = compute_hist(df["Inventory Level"], 12)

    # Seasonal Analysis: Day of Week
    dow_map = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    temp_df = df.copy()
    temp_df["DayName"] = temp_df["Date"].dt.dayofweek.map(dow_map)
    dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow_grp = temp_df.groupby("DayName").agg(
        avg_units=("Units Sold", "mean"),
        avg_revenue=("Revenue", "mean"),
        avg_price=("Price", "mean")
    ).reindex(dow_order).reset_index()

    dow_seasonal = []
    for _, row in dow_grp.iterrows():
        dow_seasonal.append({
            "day": row["DayName"],
            "avg_units": round(float(row["avg_units"]), 2) if not pd.isna(row["avg_units"]) else 0,
            "avg_revenue": round(float(row["avg_revenue"]), 2) if not pd.isna(row["avg_revenue"]) else 0
        })

    # Seasonal Analysis: Month of Year
    month_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    temp_df["MonthName"] = temp_df["Date"].dt.month.map(month_map)
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_grp = temp_df.groupby("MonthName").agg(
        avg_units=("Units Sold", "mean"),
        avg_revenue=("Revenue", "mean")
    ).reindex(month_order).reset_index()

    month_seasonal = []
    for _, row in month_grp.iterrows():
        month_seasonal.append({
            "month": row["MonthName"],
            "avg_units": round(float(row["avg_units"]), 2) if not pd.isna(row["avg_units"]) else 0,
            "avg_revenue": round(float(row["avg_revenue"]), 2) if not pd.isna(row["avg_revenue"]) else 0
        })

    # Outlier Analysis using IQR
    outlier_analysis = []
    for col in ["Price", "Units Sold", "Inventory Level"]:
        s = df[col]
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = df[(s < lower_bound) | (s > upper_bound)]
        outlier_analysis.append({
            "feature": col,
            "q1": round(float(q1), 2),
            "q3": round(float(q3), 2),
            "iqr": round(float(iqr), 2),
            "lower_bound": round(float(lower_bound), 2),
            "upper_bound": round(float(upper_bound), 2),
            "outlier_count": int(len(outliers)),
            "outlier_pct": round(float(len(outliers) / len(df) * 100), 2)
        })

    # Inventory vs Demand Sample (150 stratified points for responsive charting)
    inv_demand_sample = []
    sample_df = df.sample(n=min(200, len(df)), random_state=42)
    for _, row in sample_df.iterrows():
        is_binding = row["Units Sold"] >= row["Inventory Level"]
        inv_demand_sample.append({
            "inventory": int(row["Inventory Level"]),
            "units_sold": int(row["Units Sold"]),
            "price": round(float(row["Price"]), 2),
            "category": row["Category"],
            "is_binding": bool(is_binding)
        })

    # Overall dataset metrics
    dataset_metrics = {
        "total_records": len(df),
        "total_columns": len(df.columns),
        "columns_list": df.columns.tolist(),
        "date_range_start": df["Date"].min().strftime("%Y-%m-%d"),
        "date_range_end": df["Date"].max().strftime("%Y-%m-%d"),
        "stores_count": int(df["Store ID"].nunique()),
        "products_count": int(df["Product ID"].nunique()),
        "categories_count": int(df["Category"].nunique()),
        "regions_count": int(df["Region"].nunique()),
        "inventory_binding_rate": round(float((df["Units Sold"] >= df["Inventory Level"]).mean() * 100), 2)
    }

    # Promotion Impact note
    promotion_notes = {
        "status": "Omitted / Not Tracked",
        "description": "Promotional campaign tags, markdown discounts, and circular ad flags were not captured in this transactional system.",
        "econometric_impact": "In retail econometrics, unobserved promotions can bias naive OLS estimates because promotions correlate simultaneously with price cuts and demand spikes. DML partially absorbs store-week temporal confounders to mitigate this bias, but randomized micro-pilots (A/B testing) remain recommended."
    }

    return {
        "dataset_metrics": dataset_metrics,
        "summary_stats": summary_stats,
        "missing_analysis": missing_analysis,
        "correlation_matrix": correlation_matrix,
        "numeric_features": available_num_cols,
        "distributions": {
            "price": price_hist,
            "demand": demand_hist,
            "inventory": inventory_hist
        },
        "seasonality": {
            "day_of_week": dow_seasonal,
            "month": month_seasonal
        },
        "outlier_analysis": outlier_analysis,
        "inventory_demand_sample": inv_demand_sample,
        "promotion_notes": promotion_notes
    }
