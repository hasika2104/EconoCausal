from fastapi import APIRouter, Query
from typing import Optional, List, Dict, Any
import pandas as pd
from backend.services.data_service import data_service

router = APIRouter(prefix="/api/recommendations", tags=["AI Pricing Recommendations"])

@router.get("")
def get_recommendations(
    category: Optional[str] = Query(None),
    strategy: Optional[str] = Query(None),
    product_id: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("product_id")
):
    recs_df = data_service.get_recommendations()
    if recs_df.empty:
        return {"error": "Recommendations data not available", "items": [], "summary": {}}

    filtered_df = recs_df.copy()

    # Strategy counts overall
    strategy_counts = recs_df["recommendation_strategy"].value_counts().to_dict()
    categories_list = sorted(recs_df["category"].dropna().unique().tolist())
    strategies_list = sorted(recs_df["recommendation_strategy"].dropna().unique().tolist())

    # Apply filters
    if category and category != "All":
        filtered_df = filtered_df[filtered_df["category"] == category]
    if strategy and strategy != "All":
        filtered_df = filtered_df[filtered_df["recommendation_strategy"] == strategy]
    if product_id and product_id != "All":
        filtered_df = filtered_df[filtered_df["product_id"].str.contains(product_id, case=False, na=False)]

    # Sort
    if sort_by in filtered_df.columns:
        filtered_df = filtered_df.sort_values(sort_by)

    items = []
    for _, row in filtered_df.iterrows():
        items.append({
            "product_id": str(row["product_id"]),
            "category": str(row["category"]),
            "recommendation_strategy": str(row["recommendation_strategy"]),
            "current_price": round(float(row["current_price"]), 2),
            "suggested_price": round(float(row["suggested_price"]), 2),
            "price_change_pct": round(float(row["price_change_pct"]), 2),
            "baseline_units_sold": round(float(row["baseline_units_sold"]), 2),
            "expected_demand_change_units": round(float(row["expected_demand_change_units"]), 2),
            "expected_demand": round(float(row["expected_demand"]), 2),
            "realized_sales_capped": round(float(row["realized_sales_capped"]), 2),
            "baseline_revenue": round(float(row["baseline_modeled_revenue"]), 2),
            "expected_revenue": round(float(row["expected_revenue"]), 2),
            "expected_revenue_change_dollars": round(float(row["expected_revenue_change_dollars"]), 2),
            "expected_revenue_change_pct": round(float(row["expected_revenue_change_pct"]), 2),
            "inventory_buffer_ratio": round(float(row["inventory_buffer_ratio"]), 2),
            "inventory_binding_rate_pct": round(float(row["inventory_binding_rate_pct"]), 2),
            "inventory_considerations": str(row["inventory_considerations"]),
            "dml_theta_used": round(float(row["dml_theta_used"]), 6),
            "dml_p_value": round(float(row["dml_p_value"]), 4),
            "confidence_and_uncertainty": str(row["confidence_and_uncertainty"]),
            "recommendation_explanation": str(row["recommendation_explanation"])
        })

    summary = {
        "total_segments": len(recs_df),
        "filtered_count": len(items),
        "strategy_counts": strategy_counts,
        "categories": categories_list,
        "strategies": strategies_list,
        "avg_current_price": round(float(recs_df["current_price"].mean()), 2),
        "avg_suggested_price": round(float(recs_df["suggested_price"].mean()), 2),
    }

    return {
        "summary": summary,
        "items": items
    }
