"""
Business Validation and Uncertainty Analysis Module for EconoCausal.

Provides reusable utilities for:
1. Validating upstream model results and retail datasets.
2. Running multi-scenario sensitivity analyses across DML coefficient bounds.
3. Computing economic threshold boundaries (where recommendations flip).
4. Enforcing business constraints (price bounds, inventory caps, non-negativity).
5. Documenting causal limitations and commercial readiness criteria.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json
import numpy as np
import pandas as pd


def load_and_validate_inputs(
    dml_path: Path,
    sim_path: Path,
    data_path: Optional[Path] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any], Optional[pd.DataFrame]]:
    """
    Load and rigorously validate inputs from Day 10 DML results, Day 11 simulator outputs,
    and optional processed dataset.
    """
    if not dml_path.exists():
        raise FileNotFoundError(
            f"Required DML results file not found at: {dml_path}. "
            "Ensure Day 10 notebook (08_dml_validation.ipynb) has been executed."
        )
    with open(dml_path, "r", encoding="utf-8") as f:
        dml_data = json.load(f)

    # Validate DML schema
    required_dml_keys = ["spec1", "spec2", "validated"]
    for k in required_dml_keys:
        if k not in dml_data:
            raise ValueError(f"DML results file missing expected key '{k}'.")
    for spec_name in ["spec1", "spec2"]:
        for metric in ["theta", "ci_low", "ci_high", "std_err", "p_value"]:
            if metric not in dml_data[spec_name]:
                raise ValueError(f"DML specification '{spec_name}' missing metric '{metric}'.")
            val = dml_data[spec_name][metric]
            if not isinstance(val, (int, float)) or np.isnan(val) or np.isinf(val):
                raise ValueError(f"Invalid numeric value for {spec_name}.{metric}: {val}")

    if not sim_path.exists():
        raise FileNotFoundError(
            f"Required simulator results file not found at: {sim_path}. "
            "Ensure Day 11 notebook (09_pricing_simulator.ipynb) has been executed."
        )
    with open(sim_path, "r", encoding="utf-8") as f:
        sim_data = json.load(f)

    required_sim_keys = [
        "product_id",
        "store_id",
        "baseline_price",
        "baseline_units",
        "baseline_revenue",
        "baseline_inventory",
        "scenarios",
    ]
    for k in required_sim_keys:
        if k not in sim_data:
            raise ValueError(f"Simulator results file missing expected key '{k}'.")

    # Validate baseline values
    if sim_data["baseline_price"] <= 0:
        raise ValueError(f"Baseline price must be positive, got {sim_data['baseline_price']}")
    if sim_data["baseline_units"] < 0:
        raise ValueError(f"Baseline units must be non-negative, got {sim_data['baseline_units']}")
    if sim_data["baseline_revenue"] <= 0:
        raise ValueError(f"Baseline revenue must be positive, got {sim_data['baseline_revenue']}")

    # Load dataset if requested
    df = None
    if data_path is not None:
        if not data_path.exists():
            raise FileNotFoundError(f"Processed dataset file not found at: {data_path}")
        df = pd.read_csv(data_path)
        required_cols = ["Price", "Units Sold", "Inventory Level", "Product ID", "Store ID"]
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Dataset missing required columns: {missing_cols}")

    return dml_data, sim_data, df


def run_uncertainty_sensitivity(
    base_price: float,
    base_units: float,
    base_revenue: float,
    base_inventory: float,
    dml_results: Dict[str, Any],
    percentage_changes: List[float] = [-0.10, -0.05, 0.00, 0.05, 0.10],
    observed_price_min: Optional[float] = None,
    observed_price_max: Optional[float] = None,
    include_threshold_analysis: bool = True,
) -> pd.DataFrame:
    """
    Run multi-scenario sensitivity analysis across:
    1. Spec 1 Point Estimate
    2. Spec 1 95% CI Lower Bound
    3. Spec 1 95% CI Upper Bound
    4. Spec 2 Point Estimate (Sensitivity check)
    5. Spec 2 95% CI Lower Bound
    6. Spec 2 95% CI Upper Bound
    7. Critical Inversion Threshold (Breakeven elasticity where +10% ceases to be optimal)

    Applies non-negativity constraints and inventory caps.
    """
    coefficient_scenarios = [
        ("Spec 1 (Core)", "Point Estimate", dml_results["spec1"]["theta"], "DML primary point estimate"),
        ("Spec 1 (Core)", "CI Lower 95%", dml_results["spec1"]["ci_low"], "Lower bound of 95% HC3 CI"),
        ("Spec 1 (Core)", "CI Upper 95%", dml_results["spec1"]["ci_high"], "Upper bound of 95% HC3 CI"),
        ("Spec 2 (+Inventory)", "Point Estimate", dml_results["spec2"]["theta"], "Alternative control specification"),
        ("Spec 2 (+Inventory)", "CI Lower 95%", dml_results["spec2"]["ci_low"], "Lower bound of Spec 2 95% CI"),
        ("Spec 2 (+Inventory)", "CI Upper 95%", dml_results["spec2"]["ci_high"], "Upper bound of Spec 2 95% CI"),
    ]

    # Calculate analytical threshold where +10% price yields revenue <= baseline revenue
    # R(P_1) = P_1 * (Y_0 + theta * (P_1 - P_0)) <= P_0 * Y_0
    # theta <= (P_0 * Y_0 / P_1 - Y_0) / (P_1 - P_0)
    p_high = base_price * 1.10
    delta_p_high = p_high - base_price
    theta_breakeven_baseline = ((base_revenue / p_high) - base_units) / delta_p_high

    if include_threshold_analysis:
        coefficient_scenarios.append(
            (
                "Stress-Test (Elastic)",
                "Breakeven Threshold",
                theta_breakeven_baseline,
                "Critical theta where +10% price produces zero revenue gain over baseline",
            )
        )

    records = []
    for spec_name, coef_type, theta, description in coefficient_scenarios:
        for pct in percentage_changes:
            candidate_price = round(base_price * (1.0 + pct), 2)
            delta_p = candidate_price - base_price

            # Rounded demand and inventory constraint
            raw_demand = max(0.0, base_units + theta * delta_p)
            rounded_demand = round(raw_demand, 2)
            inv_constrained_demand = min(rounded_demand, base_inventory)
            is_inv_binding = rounded_demand > base_inventory

            # Calculate revenue under inventory constraint
            estimated_revenue = round(candidate_price * inv_constrained_demand, 2)
            revenue_change_abs = round(estimated_revenue - base_revenue, 2)
            revenue_change_pct = (
                round((revenue_change_abs / base_revenue) * 100, 2) if base_revenue > 0 else 0.0
            )

            # Check extrapolation beyond observed historical range
            extrapolates = False
            if observed_price_min is not None and candidate_price < observed_price_min:
                extrapolates = True
            if observed_price_max is not None and candidate_price > observed_price_max:
                extrapolates = True

            records.append(
                {
                    "specification": spec_name,
                    "coefficient_scenario": coef_type,
                    "scenario_description": description,
                    "theta": round(theta, 6),
                    "pricing_scenario": f"{pct:+.0%}",
                    "candidate_price": candidate_price,
                    "baseline_units": base_units,
                    "estimated_demand": round(raw_demand, 2),
                    "inventory_cap": base_inventory,
                    "inventory_constrained_demand": round(inv_constrained_demand, 2),
                    "inventory_binding": is_inv_binding,
                    "estimated_revenue": estimated_revenue,
                    "revenue_change_dollars": revenue_change_abs,
                    "revenue_change_pct": revenue_change_pct,
                    "extrapolates": extrapolates,
                }
            )

    results_df = pd.DataFrame(records)

    # Rank scenarios within each (specification, coefficient_scenario) group
    results_df["rank_in_scenario"] = results_df.groupby(
        ["specification", "coefficient_scenario"]
    )["estimated_revenue"].rank(ascending=False, method="min").astype(int)

    return results_df


def validate_business_rules(
    sensitivity_df: pd.DataFrame,
    product_df: Optional[pd.DataFrame] = None,
    dataset_has_costs: bool = False,
) -> Dict[str, Any]:
    """
    Rigorously audit business constraints and statistical integrity rules.
    """
    audit = {}

    # 1. Price positivity
    audit["all_prices_positive"] = bool((sensitivity_df["candidate_price"] > 0).all())
    audit["min_candidate_price"] = float(sensitivity_df["candidate_price"].min())
    audit["max_candidate_price"] = float(sensitivity_df["candidate_price"].max())

    # 2. Demand non-negativity
    audit["all_demand_non_negative"] = bool((sensitivity_df["estimated_demand"] >= 0).all())
    audit["min_estimated_demand"] = float(sensitivity_df["estimated_demand"].min())

    # 3. Revenue calculation correctness
    expected_rev = (
        sensitivity_df["candidate_price"] * sensitivity_df["inventory_constrained_demand"]
    ).round(2)
    audit["revenue_calculation_correct"] = bool(
        np.allclose(sensitivity_df["estimated_revenue"], expected_rev, atol=0.02)
    )

    # 4. Inventory constraint audit
    audit["inventory_binding_count"] = int(sensitivity_df["inventory_binding"].sum())
    audit["any_demand_exceeds_inventory"] = bool(
        (sensitivity_df["inventory_constrained_demand"] > sensitivity_df["inventory_cap"]).any()
    )

    # 5. Extrapolation check
    audit["any_extrapolation"] = bool(sensitivity_df["extrapolates"].any())

    # 6. Recommendation stability across statistical bounds
    stat_scenarios = sensitivity_df[
        sensitivity_df["specification"].isin(["Spec 1 (Core)", "Spec 2 (+Inventory)"])
    ]
    top_per_stat = stat_scenarios[stat_scenarios["rank_in_scenario"] == 1]
    unique_top_scenarios = top_per_stat["pricing_scenario"].unique().tolist()
    audit["stat_scenarios_top_recommendation"] = unique_top_scenarios
    audit["is_stable_across_dml_bounds"] = len(unique_top_scenarios) == 1

    # 7. Cost / Profit audit
    audit["dataset_has_costs"] = dataset_has_costs
    audit["profit_optimization_possible"] = False
    audit["profit_warning"] = (
        "CRITICAL: Dataset contains no cost of goods sold (COGS), carrying costs, or margins. "
        "Estimated revenue CANNOT be interpreted as profit. A higher price may reduce sales volume "
        "and total revenue while increasing or decreasing profit depending on unit margins."
    )

    # 8. Causal validity audit
    audit["causal_validity_confirmed"] = False
    audit["causal_warning"] = (
        "Double Machine Learning controls for observable features (store, product, category, region, time). "
        "However, key unobserved confounders (promotions, competitor prices, marketing campaigns, "
        "localized weather/holidays) are absent from this dataset. The DML estimate cannot be "
        "interpreted as a true causal elasticity without randomized price experiments (A/B testing)."
    )

    return audit
