from fastapi import APIRouter, Query
from typing import Optional, List
import pandas as pd
import numpy as np
from backend.services.data_service import data_service

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("")
def get_dashboard_data(
    category: Optional[str] = Query(None),
    store: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    product: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    df = data_service.get_retail_data()
    dml_results = data_service.get_dml_results()

    if df.empty:
        return {"error": "Dataset not available"}

    # Available filter values
    all_categories = sorted(df["Category"].dropna().unique().tolist())
    all_stores = sorted(df["Store ID"].dropna().unique().tolist())
    all_regions = sorted(df["Region"].dropna().unique().tolist())
    all_products = sorted(df["Product ID"].dropna().unique().tolist())
    min_date = df["Date"].min().strftime("%Y-%m-%d") if not df.empty else ""
    max_date = df["Date"].max().strftime("%Y-%m-%d") if not df.empty else ""

    # Apply filters
    filtered_df = df.copy()
    if category and category != "All":
        filtered_df = filtered_df[filtered_df["Category"] == category]
    if store and store != "All":
        filtered_df = filtered_df[filtered_df["Store ID"] == store]
    if region and region != "All":
        filtered_df = filtered_df[filtered_df["Region"] == region]
    if product and product != "All":
        filtered_df = filtered_df[filtered_df["Product ID"] == product]
    if start_date:
        filtered_df = filtered_df[filtered_df["Date"] >= pd.to_datetime(start_date)]
    if end_date:
        filtered_df = filtered_df[filtered_df["Date"] <= pd.to_datetime(end_date)]

    # Compute KPIs
    total_products = int(filtered_df["Product ID"].nunique())
    total_sales_units = int(filtered_df["Units Sold"].sum())
    total_revenue = float(filtered_df["Revenue"].sum())
    avg_price = float(round(filtered_df["Price"].mean(), 2)) if not filtered_df.empty else 0.0
    avg_demand = float(round(filtered_df["Units Sold"].mean(), 2)) if not filtered_df.empty else 0.0
    total_records = len(filtered_df)

    # DML effect from actual spec 1
    spec1 = dml_results.get("spec1", {})
    dml_theta = spec1.get("theta", 0.0107)
    dml_ci_low = spec1.get("ci_low", -0.0197)
    dml_ci_high = spec1.get("ci_high", 0.0411)
    dml_p_value = spec1.get("p_value", 0.4899)

    # Monthly Trend (aggregate by Year-Month)
    monthly_trend = []
    if not filtered_df.empty:
        temp_df = filtered_df.copy()
        temp_df["YearMonth"] = temp_df["Date"].dt.to_period("M").astype(str)
        monthly_grp = temp_df.groupby("YearMonth").agg(
            revenue=("Revenue", "sum"),
            units_sold=("Units Sold", "sum"),
            avg_price=("Price", "mean"),
            avg_demand=("Units Sold", "mean")
        ).reset_index()
        for _, row in monthly_grp.iterrows():
            monthly_trend.append({
                "period": row["YearMonth"],
                "revenue": round(float(row["revenue"]), 2),
                "units_sold": int(row["units_sold"]),
                "avg_price": round(float(row["avg_price"]), 2),
                "avg_demand": round(float(row["avg_demand"]), 2)
            })

    # Category Breakdown
    category_breakdown = []
    if not filtered_df.empty:
        cat_grp = filtered_df.groupby("Category").agg(
            revenue=("Revenue", "sum"),
            units_sold=("Units Sold", "sum"),
            avg_price=("Price", "mean"),
            record_count=("Product ID", "count")
        ).reset_index()
        for _, row in cat_grp.iterrows():
            category_breakdown.append({
                "category": row["Category"],
                "revenue": round(float(row["revenue"]), 2),
                "units_sold": int(row["units_sold"]),
                "avg_price": round(float(row["avg_price"]), 2),
                "record_count": int(row["record_count"])
            })

    # Regional Breakdown
    regional_breakdown = []
    if not filtered_df.empty:
        reg_grp = filtered_df.groupby("Region").agg(
            revenue=("Revenue", "sum"),
            units_sold=("Units Sold", "sum"),
            avg_price=("Price", "mean")
        ).reset_index()
        for _, row in reg_grp.iterrows():
            regional_breakdown.append({
                "region": row["Region"],
                "revenue": round(float(row["revenue"]), 2),
                "units_sold": int(row["units_sold"]),
                "avg_price": round(float(row["avg_price"]), 2)
            })

    # Price vs Demand Binned Curve (Deciles / $10 bins)
    price_demand_curve = []
    if not filtered_df.empty:
        bins = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        labels = ["$10-$20", "$20-$30", "$30-$40", "$40-$50", "$50-$60", "$60-$70", "$70-$80", "$80-$90", "$90-$100"]
        temp_df = filtered_df.copy()
        temp_df["PriceBin"] = pd.cut(temp_df["Price"], bins=bins, labels=labels, include_lowest=True)
        bin_grp = temp_df.groupby("PriceBin", observed=False).agg(
            avg_demand=("Units Sold", "mean"),
            avg_price=("Price", "mean"),
            count=("Units Sold", "count")
        ).reset_index()
        for _, row in bin_grp.iterrows():
            if not pd.isna(row["avg_demand"]):
                price_demand_curve.append({
                    "bin": str(row["PriceBin"]),
                    "avg_demand": round(float(row["avg_demand"]), 2),
                    "avg_price": round(float(row["avg_price"]), 2),
                    "count": int(row["count"])
                })

    # Top Product Performance
    product_performance = []
    if not filtered_df.empty:
        prod_grp = filtered_df.groupby(["Product ID", "Category"]).agg(
            revenue=("Revenue", "sum"),
            units_sold=("Units Sold", "sum"),
            avg_price=("Price", "mean")
        ).reset_index().sort_values("revenue", ascending=False).head(10)
        for _, row in prod_grp.iterrows():
            product_performance.append({
                "product_id": row["Product ID"],
                "category": row["Category"],
                "revenue": round(float(row["revenue"]), 2),
                "units_sold": int(row["units_sold"]),
                "avg_price": round(float(row["avg_price"]), 2)
            })

    return {
        "kpis": {
            "total_products": total_products,
            "total_sales_units": total_sales_units,
            "total_revenue": total_revenue,
            "avg_price": avg_price,
            "avg_demand": avg_demand,
            "total_records": total_records,
            "dml_theta": round(dml_theta, 4),
            "dml_ci_low": round(dml_ci_low, 4),
            "dml_ci_high": round(dml_ci_high, 4),
            "dml_p_value": round(dml_p_value, 4),
            "is_significant": dml_p_value < 0.05
        },
        "filters": {
            "categories": all_categories,
            "stores": all_stores,
            "regions": all_regions,
            "products": all_products,
            "min_date": min_date,
            "max_date": max_date
        },
        "charts": {
            "monthly_trend": monthly_trend,
            "category_breakdown": category_breakdown,
            "regional_breakdown": regional_breakdown,
            "price_demand_curve": price_demand_curve,
            "product_performance": product_performance
        }
    }
