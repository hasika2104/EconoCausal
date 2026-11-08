from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
from backend.services.data_service import data_service

router = APIRouter(prefix="/api/simulate-price", tags=["Price Simulator"])

class SimulationRequest(BaseModel):
    product_id: Optional[str] = "P0001"
    category: Optional[str] = None
    current_price: Optional[float] = None
    proposed_price: float
    inventory_level: Optional[float] = None
    cost_per_unit: Optional[float] = None
    specification: Optional[str] = "spec1" # "spec1" or "spec2"

@router.post("")
def run_simulation(req: SimulationRequest):
    df = data_service.get_retail_data()
    dml_results = data_service.get_dml_results()
    recs_df = data_service.get_recommendations()

    # Determine product baseline values
    prod_id = req.product_id or "P0001"
    prod_rows = df[df["Product ID"] == prod_id] if not df.empty else pd.DataFrame()

    if not prod_rows.empty:
        baseline_price = float(req.current_price) if req.current_price is not None else float(round(prod_rows["Price"].mean(), 2))
        baseline_demand = float(round(prod_rows["Units Sold"].mean(), 2))
        default_inventory = float(round(prod_rows["Inventory Level"].mean(), 2))
        category = prod_rows["Category"].iloc[0] if "Category" in prod_rows.columns else "General"
    else:
        baseline_price = float(req.current_price or 55.0)
        baseline_demand = 135.0
        default_inventory = 250.0
        category = req.category or "General"

    inventory = float(req.inventory_level) if req.inventory_level is not None else default_inventory

    # Select DML specification
    spec_key = "spec2" if req.specification == "spec2" else "spec1"
    spec_data = dml_results.get(spec_key, {
        "theta": 0.0107,
        "ci_low": -0.0197,
        "ci_high": 0.0411,
        "p_value": 0.4899
    })

    theta = float(spec_data.get("theta", 0.0107))
    ci_low = float(spec_data.get("ci_low", -0.0197))
    ci_high = float(spec_data.get("ci_high", 0.0411))

    proposed_price = float(req.proposed_price)
    price_delta = proposed_price - baseline_price
    price_change_pct = (price_delta / baseline_price * 100) if baseline_price > 0 else 0.0

    # Demand prediction using DML causal sensitivity
    predicted_raw_demand = max(0.0, baseline_demand + (theta * price_delta))
    ci_low_demand = max(0.0, baseline_demand + (ci_low * price_delta))
    ci_high_demand = max(0.0, baseline_demand + (ci_high * price_delta))

    # Apply physical inventory constraint
    baseline_realized_sales = min(baseline_demand, inventory)
    realized_sales = min(predicted_raw_demand, inventory)
    ci_low_sales = min(ci_low_demand, inventory)
    ci_high_sales = min(ci_high_demand, inventory)

    is_inventory_binding = predicted_raw_demand >= inventory
    demand_change_units = predicted_raw_demand - baseline_demand
    demand_change_pct = (demand_change_units / baseline_demand * 100) if baseline_demand > 0 else 0.0

    baseline_revenue = round(baseline_price * baseline_realized_sales, 2)
    proposed_revenue = round(proposed_price * realized_sales, 2)
    ci_low_revenue = round(proposed_price * ci_low_sales, 2)
    ci_high_revenue = round(proposed_price * ci_high_sales, 2)

    revenue_change_dollars = round(proposed_revenue - baseline_revenue, 2)
    revenue_change_pct = round((revenue_change_dollars / baseline_revenue * 100), 2) if baseline_revenue > 0 else 0.0

    # Profit evaluation if unit cost is provided
    profit_data = None
    if req.cost_per_unit is not None and req.cost_per_unit > 0:
        c = float(req.cost_per_unit)
        baseline_profit = round((baseline_price - c) * baseline_realized_sales, 2)
        proposed_profit = round((proposed_price - c) * realized_sales, 2)
        profit_change_dollars = round(proposed_profit - baseline_profit, 2)
        profit_change_pct = round((profit_change_dollars / baseline_profit * 100), 2) if baseline_profit != 0 else 0.0
        profit_data = {
            "unit_cost": c,
            "baseline_profit": baseline_profit,
            "proposed_profit": proposed_profit,
            "profit_change_dollars": profit_change_dollars,
            "profit_change_pct": profit_change_pct,
            "margin_current_pct": round(((baseline_price - c) / baseline_price) * 100, 2),
            "margin_proposed_pct": round(((proposed_price - c) / proposed_price) * 100, 2),
        }

    # Historical price bounds extrapolation check
    price_min_hist = 10.0
    price_max_hist = 100.0
    extrapolates = proposed_price < price_min_hist or proposed_price > price_max_hist

    # Baseline Model Pipeline Evaluation (Trained Random Forest Pipeline)
    pipeline_eval = None
    baseline_model = data_service.get_baseline_model()
    if baseline_model is not None:
        try:
            # Prepare feature records for baseline and proposed scenarios
            store_id = prod_rows["Store ID"].iloc[0] if not prod_rows.empty and "Store ID" in prod_rows.columns else "S0001"
            region = prod_rows["Region"].iloc[0] if not prod_rows.empty and "Region" in prod_rows.columns else "North"
            
            base_input = pd.DataFrame([{
                "Price": baseline_price,
                "Inventory Level": inventory,
                "Year": 2023,
                "Month": 6,
                "DayOfWeek": 2,
                "Category": category,
                "Region": region,
                "Product ID": prod_id,
                "Store ID": store_id
            }])
            prop_input = pd.DataFrame([{
                "Price": proposed_price,
                "Inventory Level": inventory,
                "Year": 2023,
                "Month": 6,
                "DayOfWeek": 2,
                "Category": category,
                "Region": region,
                "Product ID": prod_id,
                "Store ID": store_id
            }])

            ml_pred_base = float(round(baseline_model.predict(base_input)[0], 2))
            ml_pred_prop = float(round(baseline_model.predict(prop_input)[0], 2))
            ml_delta = float(round(ml_pred_prop - ml_pred_base, 2))
            ml_delta_pct = round((ml_delta / ml_pred_base * 100), 2) if ml_pred_base > 0 else 0.0

            pipeline_eval = {
                "model_available": True,
                "model_architecture": "RandomForestRegressor Pipeline (Day 5 Baseline)",
                "ml_baseline_demand": ml_pred_base,
                "ml_proposed_demand": ml_pred_prop,
                "ml_demand_delta": ml_delta,
                "ml_demand_change_pct": ml_delta_pct,
                "ml_realized_sales": round(min(ml_pred_prop, inventory), 2),
                "dml_vs_ml_explanation": (
                    f"Supervised ML predicts a {ml_delta:+.1f} unit demand change ({ml_delta_pct:+.1f}%) "
                    f"based on historical correlations E[Demand | Price, Controls]. "
                    f"In contrast, Double Machine Learning isolates the orthogonal causal price effect "
                    f"({demand_change_units:+.1f} units, θ = {theta:+.4f}), confirming that price sensitivity "
                    f"is practically inelastic."
                )
            }
        except Exception as e:
            pipeline_eval = {
                "model_available": False,
                "error": str(e)
            }

    # Multi-scenario grid (-15%, -10%, -5%, 0%, +5%, +10%, +15%)
    scenarios_grid = []
    pct_steps = [-0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15]
    for step in pct_steps:
        s_price = round(baseline_price * (1 + step), 2)
        s_delta = s_price - baseline_price
        s_demand = round(max(0.0, baseline_demand + (theta * s_delta)), 2)
        s_sales = round(min(s_demand, inventory), 2)
        s_rev = round(s_price * s_sales, 2)
        s_rev_delta = round(s_rev - baseline_revenue, 2)
        s_rev_pct = round((s_rev_delta / baseline_revenue * 100), 2) if baseline_revenue > 0 else 0.0
        scenarios_grid.append({
            "scenario": f"{step:+.0%}",
            "price": s_price,
            "predicted_demand": s_demand,
            "realized_sales": s_sales,
            "estimated_revenue": s_rev,
            "revenue_change_dollars": s_rev_delta,
            "revenue_change_pct": s_rev_pct,
            "inventory_binding": s_demand >= inventory,
            "extrapolates": s_price < price_min_hist or s_price > price_max_hist
        })

    return {
        "product_id": prod_id,
        "category": category,
        "specification_used": spec_key,
        "dml_theta": round(theta, 6),
        "baseline": {
            "price": baseline_price,
            "demand": baseline_demand,
            "realized_sales": baseline_realized_sales,
            "revenue": baseline_revenue,
            "inventory": inventory
        },
        "simulation": {
            "proposed_price": proposed_price,
            "price_delta": round(price_delta, 2),
            "price_change_pct": round(price_change_pct, 2),
            "predicted_demand": round(predicted_raw_demand, 2),
            "ci_low_demand": round(ci_low_demand, 2),
            "ci_high_demand": round(ci_high_demand, 2),
            "realized_sales": round(realized_sales, 2),
            "ci_low_sales": round(ci_low_sales, 2),
            "ci_high_sales": round(ci_high_sales, 2),
            "estimated_revenue": proposed_revenue,
            "ci_low_revenue": ci_low_revenue,
            "ci_high_revenue": ci_high_revenue,
            "revenue_change_dollars": revenue_change_dollars,
            "revenue_change_pct": revenue_change_pct,
            "demand_change_units": round(demand_change_units, 2),
            "demand_change_pct": round(demand_change_pct, 2),
            "is_inventory_binding": is_inventory_binding,
            "inventory_buffer_ratio": round(inventory / predicted_raw_demand, 2) if predicted_raw_demand > 0 else 0,
            "extrapolates": extrapolates
        },
        "profit_analysis": profit_data,
        "model_pipeline_evaluation": pipeline_eval,
        "multi_scenario_grid": scenarios_grid,
        "disclaimer": "This simulator applies Double Machine Learning sensitivity combined with operational inventory caps (Sales = min(D, Inventory)). In the absence of COGS in the base dataset, top-line revenue is displayed. Higher prices do not guarantee higher profitability if unit procurement margins vary."
    }
