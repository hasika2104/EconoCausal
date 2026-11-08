from fastapi import APIRouter
import pandas as pd
import numpy as np
from backend.services.data_service import data_service

router = APIRouter(prefix="/api/causal-analysis", tags=["Causal Impact Analysis"])

@router.get("")
def get_causal_analysis():
    dml_results = data_service.get_dml_results()
    robustness_df = data_service.get_robustness_results()
    model_perf_df = data_service.get_model_performance()
    feature_analysis_df = data_service.get_feature_analysis()
    retail_df = data_service.get_retail_data()

    avg_price = float(retail_df["Price"].mean()) if not retail_df.empty else 55.14
    avg_demand = float(retail_df["Units Sold"].mean()) if not retail_df.empty else 136.46

    # Primary and secondary specs
    spec1 = dml_results.get("spec1", {
        "theta": 0.010698790902889818,
        "ci_low": -0.019671462460535295,
        "ci_high": 0.04106904426631493,
        "std_err": 0.015495311956230726,
        "p_value": 0.48990910213657757,
        "n_obs": 73100,
        "t_res_std": 26.374327969251556,
        "controls": ["Product ID", "Store ID", "Category", "Region", "Year", "Month", "DayOfWeek"]
    })

    spec2 = dml_results.get("spec2", {
        "theta": -0.01946812241439891,
        "ci_low": -0.043963267495602004,
        "ci_high": 0.005027022666804191,
        "std_err": 0.012497752649751566,
        "p_value": 0.11929730032847857,
        "n_obs": 73100,
        "t_res_std": 26.27760110137302,
        "controls": ["Product ID", "Store ID", "Category", "Region", "Year", "Month", "DayOfWeek", "Inventory Level"]
    })

    elasticity_spec1 = (spec1["theta"] * avg_price) / avg_demand if avg_demand > 0 else 0.0
    elasticity_spec2 = (spec2["theta"] * avg_price) / avg_demand if avg_demand > 0 else 0.0

    # 18 Robustness Specifications formatting for Forest Plot
    specs_list = []
    if not robustness_df.empty:
        for _, row in robustness_df.iterrows():
            specs_list.append({
                "specification_id": str(row["specification_id"]),
                "specification_name": str(row["specification_name"]),
                "group_type": str(row["group_type"]),
                "group_name": str(row["group_name"]),
                "sample_size": int(row["sample_size"]),
                "treatment": str(row["treatment"]),
                "outcome": str(row["outcome"]),
                "nuisance_model": str(row["nuisance_model"]),
                "control_variables": str(row["control_variables"]),
                "theta_estimate": round(float(row["theta_estimate"]), 4),
                "std_error_hc3": round(float(row["std_error_hc3"]), 4),
                "ci_lower_95": round(float(row["ci_lower_95"]), 4),
                "ci_upper_95": round(float(row["ci_upper_95"]), 4),
                "p_value": round(float(row["p_value"]), 4),
                "statistically_significant": bool(row["statistically_significant_05"]),
                "elasticity_at_mean": round(float(row["elasticity_at_mean"]), 4),
                "notes": str(row["warnings_limitations"])
            })

    # Benchmark Predictive Models
    benchmarks = []
    if not model_perf_df.empty:
        for _, row in model_perf_df.iterrows():
            benchmarks.append({
                "model_name": str(row["model_name"]),
                "model_type": str(row["model_type"]),
                "mae": round(float(row["mae"]), 2),
                "rmse": round(float(row["rmse"]), 2),
                "r2_score": round(float(row["r2_score"]), 4),
                "mean_residual_bias": round(float(row["mean_residual_bias"]), 4),
                "notes": str(row["notes"])
            })

    # Day 16 Feature Permutation Diagnostics & Causal Role Distinction
    features_list = []
    if not feature_analysis_df.empty:
        for _, row in feature_analysis_df.iterrows():
            features_list.append({
                "feature": str(row["feature"]),
                "feature_type": str(row["feature_type"]),
                "rf_mdi_importance": round(float(row["rf_mdi_importance"]), 4),
                "rf_perm_importance_mean": round(float(row["rf_perm_importance_mean"]), 4),
                "rf_perm_importance_std": round(float(row["rf_perm_importance_std"]), 4),
                "predictive_rank": int(row["predictive_rank"]),
                "causal_role_and_distinction": str(row["causal_role_and_distinction"])
            })

    methodology = {
        "title": "Double Machine Learning (DML) / Orthogonalized Neyman Machine Learning",
        "formula_outcome": "Y = θ · Price + g(W) + U",
        "formula_treatment": "Price = m(W) + V",
        "orthogonality_condition": "E[V · U] = 0",
        "cross_fitting": "3-Fold Cross-Fitting with ExtraTrees / Ensemble nuisance regressions",
        "variance_covariance": "Heteroskedasticity-Consistent (HC3) White standard errors",
        "core_explanation": "Unlike ordinary correlation analysis, DML attempts to isolate the causal effect of pricing while controlling for observed business conditions. By residualizing both Price and Demand on observed confounders (W), DML strips out confounding bias before estimating θ.",
        "limitations": [
            "Missing Confounders: Promotional circulars, local marketing campaigns, and competitor price actions were unobserved.",
            "Absence of COGS: Without wholesale purchase costs, top-line revenue cannot be interpreted as bottom-line profit.",
            "Observational Nature: All estimates are observational. Experimental pricing micro-pilots (A/B testing) are required before high-stakes repricing."
        ]
    }

    return {
        "methodology": methodology,
        "spec1": {
            **spec1,
            "theta_rounded": round(spec1["theta"], 4),
            "ci_low_rounded": round(spec1["ci_low"], 4),
            "ci_high_rounded": round(spec1["ci_high"], 4),
            "p_value_rounded": round(spec1["p_value"], 4),
            "std_err_rounded": round(spec1["std_err"], 4),
            "elasticity": round(elasticity_spec1, 4),
            "is_significant": spec1["p_value"] < 0.05
        },
        "spec2": {
            **spec2,
            "theta_rounded": round(spec2["theta"], 4),
            "ci_low_rounded": round(spec2["ci_low"], 4),
            "ci_high_rounded": round(spec2["ci_high"], 4),
            "p_value_rounded": round(spec2["p_value"], 4),
            "std_err_rounded": round(spec2["std_err"], 4),
            "elasticity": round(elasticity_spec2, 4),
            "is_significant": spec2["p_value"] < 0.05
        },
        "robustness_specifications": specs_list,
        "predictive_benchmarks": benchmarks,
        "feature_analysis": features_list
    }
