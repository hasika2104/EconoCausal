# Day 20 — Dashboard Integration Report

**Date:** 05 November 2026  
**Project:** EconoCausal — Retail Demand Estimation and Dynamic Pricing  
**Dashboard File:** `app.py` (Day 20 Production Integration)  
**Author:** Infotact Solutions Internship

---

## Executive Summary

Day 20 delivered a fully-integrated, 11-section Streamlit dashboard that connects every analytical output produced across Days 1–19 of the EconoCausal project. The dashboard presents causal demand estimation results, predictive model benchmarks, 18-specification robustness findings, inventory-capped pricing scenarios, and governance recommendations — all sourced from actual validated project artifacts without fabrication.

---

## Integration Architecture

```
app.py
├── load_raw_data()              → data/retail_store_inventory-selected-columns.csv
├── load_retail_data()           → data/processed/retail_inventory_cleaned.csv
├── load_dml_prep_data()         → data/processed/dml_preparation.csv
├── load_dml_results()           → data/processed/dml_validated_results.json
├── load_simulator_results()     → data/processed/pricing_simulator_results.json
├── load_baseline_model()        → models/baseline_demand_model.joblib
├── load_model_performance()     → reports/day16_model_performance.csv
├── load_feature_analysis()      → reports/day16_feature_analysis.csv
├── load_robustness_results()    → reports/day15_robustness_results.csv
├── load_sensitivity_results()   → reports/day13_sensitivity_results.csv
├── load_pricing_scenarios()     → reports/day17_pricing_scenarios.csv
└── src/business_validation.py  → validate_business_rules(df_sensitivity)
```

## Section-Level Integration Summary

### Section 1: Project Overview
- Component status board with live file existence checks for all 11 artifacts
- System pipeline Mermaid flowchart (9 nodes: raw data → governance)
- Tech stack information box

### Section 2: Dataset Overview
- KPIs computed live from `retail_inventory_cleaned.csv`: 73,100 records, 20 products, 5 stores, 5 categories, 4 regions, 731 days, \$55.03 mean price, 10.25M units, \$564.1M gross volume
- Tab 1: Category breakdown bar chart and table
- Tab 2: Store/region revenue bar chart
- Tab 3: Raw data sample and schema documentation

### Section 3: Exploratory Data Analysis
- Interactive sidebar filters (category, store, region, date range)
- Tab 1: Price, Units Sold, Inventory Level distributions (histogram + boxplot)
- Tab 2: Price vs. Units Sold scatter (observational elasticity), Inventory vs. Units Sold scatter
- Tab 3: Monthly time-series volume trend

### Section 4: Data Preprocessing *(New)*
- Dataset transformation lifecycle documentation
- Raw vs. cleaned vs. DML-prep comparison table
- Descriptive statistics with 1st–99th percentile
- Common support histogram: price span across product-store pairs

### Section 5: Demand Prediction *(Expanded)*
- **Live inference engine**: Form with product, category, store, region, price, inventory, year, month, DayOfWeek inputs
- Prediction output with inventory capping visualization and stockout warning
- Pipeline architecture display (ColumnTransformer + RandomForestRegressor)
- Holdout benchmark table (4 models)

### Section 6: Causal Effect Estimation
- DML KPI cards: θ = +0.0107, SE = 0.0155, CI = [-0.0197, +0.0411], p = 0.4899
- Robinson's PLM mathematical formulation in LaTeX
- Spec 1 vs. Spec 2 comparison table (sourced from JSON)

### Section 7: DML Validation & Robustness *(Expanded)*
- Interactive forest plot with group_type filter (5 groups)
- Full 18-row specification table with HC3 errors
- Breakeven stress-test section with analytical threshold
- Bar chart: empirical θ vs. elastic breakeven threshold comparison

### Section 8: Model Performance
- 4-model benchmark table (MAE, RMSE, R², bias)
- R² bar chart and RMSE bar chart
- Permutation importance bar chart (sorted)
- Supervised ML trap callout box

### Section 9: Dynamic Pricing Simulator
- Tab 1: Discrete multi-product scenarios from `day17_pricing_scenarios.csv` with category filter
- Revenue comparison bar chart per scenario
- Tab 2: Continuous slider (±20%) with live DML formula recalculation, CI display, and discount/hike advisory boxes

### Section 10: Pricing Recommendations
- 3 policy cards (Reject Cuts / Status Quo / Micro-pilot)
- Executive governance matrix table (Markdown)
- 6-step operations checklist for category managers

### Section 11: Business Insights & Limitations *(Expanded)*
- Tab 1: Business-rule validation audit (via `src/business_validation.py`)
- Tab 2: Revenue vs. Profit — missing COGS documentation with LaTeX formulation
- Tab 3: Conditional Independence Assumption documentation
- Tab 4: Commercial Readiness Scorecard (6 pillars)

---

## Key Design Decisions

1. **Raw string literals (`r"""..."""`)**: All markdown blocks containing LaTeX `\hat`, `\theta`, `\text`, `\min`, `\$` use raw strings or proper double-escaping to prevent `SyntaxWarning`.
2. **`@st.cache_resource` for model**: The 522 MB joblib pipeline uses `cache_resource` (not `cache_data`) to avoid repeated deserialization.
3. **Graceful degradation**: Every section uses `if data is None: st.error(...)` guards before rendering — no section crashes if a file is missing.
4. **`sys.path` injection**: `BASE_DIR` is added to `sys.path` before `src.business_validation` import to support launching from any working directory.
5. **No hardcoded metrics**: All KPIs, coefficients, confidence intervals, and revenue figures are computed from loaded files — not embedded as literals.
