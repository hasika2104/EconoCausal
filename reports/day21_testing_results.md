# Day 21 — EconoCausal Product-Level AI Testing Results

**Date:** 2026-11-05  
**Tester:** Automated — `test_dashboard.py`  
**Dashboard:** `app.py` (Day 21 Product-Level AI Integration)

## Summary

| Metric | Count |
|--------|-------|
| Total Tests | 87 |
| Passed | 87 |
| Failed | 0 |
| Skipped (env limits) | 0 |

## Detailed Results

| Status | Test | Detail |
|--------|------|--------|
| PASS | File exists: Raw Data | data/retail_store_inventory-selected-columns.csv |
| PASS | File exists: Cleaned Data | data/processed/retail_inventory_cleaned.csv |
| PASS | File exists: DML Prep Data | data/processed/dml_preparation.csv |
| PASS | File exists: DML Results JSON | data/processed/dml_validated_results.json |
| PASS | File exists: Pricing Simulator JSON | data/processed/pricing_simulator_results.json |
| PASS | File exists: Baseline Model (Joblib) | models/baseline_demand_model.joblib |
| PASS | File exists: Sensitivity Results CSV | reports/day13_sensitivity_results.csv |
| PASS | File exists: Robustness Results CSV | reports/day15_robustness_results.csv |
| PASS | File exists: Model Performance CSV | reports/day16_model_performance.csv |
| PASS | File exists: Feature Analysis CSV | reports/day16_feature_analysis.csv |
| PASS | File exists: Pricing Scenarios CSV | reports/day17_pricing_scenarios.csv |
| PASS | File exists: Day 21 Product Analysis CSV | reports/day21_product_pricing_analysis.csv |
| PASS | File exists: Day 21 AI Recommendations CSV | reports/day21_ai_pricing_recommendations.csv |
| PASS | File exists: Day 21 Notebook | notebooks/15_product_level_pricing_analysis.ipynb |
| PASS | File exists: Day 21 Business Insights | reports/day21_business_insights.md |
| PASS | File exists: Day 21 Daily Log | daily-logs/Day21.md |
| PASS | Cleaned dataset rows | 73100 rows |
| PASS | Null values | 0 nulls |
| PASS | Duplicate rows | 0 dupes |
| PASS | Price positivity | Min price: 10.0 |
| PASS | Revenue column present |  |
| PASS | Required columns | All 14 cols verified |
| PASS | Calendar span 731 days | 731 unique dates |
| PASS | Date range starts 2022 | Start: 2022-01-01 |
| PASS | 20 unique products | 20 |
| PASS | 5 unique stores |  |
| PASS | 5 categories |  |
| PASS | Revenue = Price * Units Sold | Max deviation: 0.0000 |
| PASS | DML JSON has spec1 |  |
| PASS | DML JSON has spec2 |  |
| PASS | DML JSON has validated flag |  |
| PASS | spec1 theta ≈ 0.0107 | Actual: 0.0107 |
| PASS | spec1 p-value ≈ 0.4899 | Actual: 0.4899 |
| PASS | spec1 95% CI spans zero | CI: [-0.0197, 0.0411] |
| PASS | spec1 n_obs = 73100 |  |
| PASS | spec2 theta ≈ -0.0195 | Actual: -0.0195 |
| PASS | spec2 p-value ≈ 0.1193 | Actual: 0.1193 |
| PASS | spec2 95% CI spans zero | CI: [-0.0440, 0.0050] |
| PASS | spec2 n_obs = 73100 |  |
| PASS | Scenario table rows | 30 rows (expected 30) |
| PASS | Scenario revenue = Price * Sales (tol 0.3) | Max deviation: 0.2410 (floating-point rounding from Day-17 notebook) |
| PASS | All candidate prices positive |  |
| PASS | No extrapolation in core scenarios |  |
| PASS | Realized sales <= inventory cap |  |
| PASS | Robustness table 18 rows | 18 |
| PASS | No spec statistically significant |  |
| PASS | All p-values present and positive |  |
| PASS | Model perf table 4 rows | 4 |
| PASS | Random Forest R² ≈ 0.3184 | 0.3184 |
| PASS | Top perm feature = Inventory Level | Inventory Level |
| PASS | Price perm importance near-zero (< 0.01) | 0.0029 |
| PASS | Model loaded successfully | Pipeline |
| PASS | Model prediction returns finite value | Prediction: 97.09 |
| PASS | Prediction is positive |  |
| PASS | What-if revenue calculation (+5%) | Rev: $10016.68 |
| PASS | Day 21 Product Analysis 100 segments | 100 rows |
| PASS | Day 21 AI Recommendations 100 rows | 100 rows |
| PASS | Day 21 Analysis required columns | All verified |
| PASS | Day 21 Recommendations required columns | All verified |
| PASS | All 5 recommendation strategies present | Found: {'Consider a price increase', 'Maintain the current price', 'Consider a price decrease', 'Collect more data before making a recommendation', 'Review inventory before changing the price'} |
| PASS | All suggested prices positive | Min: 51.09 |
| PASS | Realized sales capped at inventory |  |
| PASS | Zero revenue change when price unchanged | Max deviation: 0.0000 |
| PASS | Inventory review items have binding considerations |  |
| PASS | Section: 📌 1. Project Overview |  |
| PASS | Section: 📊 2. Dataset Overview |  |
| PASS | Section: 🔍 3. Exploratory Data Analysis |  |
| PASS | Section: 🧹 4. Data Preprocessing |  |
| PASS | Section: 🎯 5. Demand Prediction |  |
| PASS | Section: 🔬 6. Causal Effect Estimation |  |
| PASS | Section: 🛡️ 7. DML Validation and Robustness |  |
| PASS | Section: 📈 8. Model Performance |  |
| PASS | Section: 🎛️ 9. Dynamic Pricing Simulator |  |
| PASS | Section: 💡 10. Pricing Recommendations |  |
| PASS | Section: ⚠️ 11. Business Insights and Limitations |  |
| PASS | Section: 🎯 12. Product-Level AI Pricing Recommendations |  |
| PASS | Cleaned data missing-file guard | Guard: `DATA_CLEANED_PATH.exists()` |
| PASS | DML results missing-file guard | Guard: `DML_RESULTS_PATH.exists()` |
| PASS | Baseline model missing-file guard | Guard: `BASELINE_MODEL_PATH.exists()` |
| PASS | Model performance missing-file guard | Guard: `MODEL_PERF_PATH.exists()` |
| PASS | Robustness results missing-file guard | Guard: `ROBUSTNESS_PATH.exists()` |
| PASS | Pricing scenarios missing-file guard | Guard: `PRICING_SCENARIOS_PATH.exists()` |
| PASS | Product analysis missing-file guard | Guard: `PRODUCT_ANALYSIS_PATH.exists()` |
| PASS | Product recommendations missing-file guard | Guard: `PRODUCT_REC_PATH.exists()` |
| PASS | st.error() calls for missing files |  |
| PASS | No hardcoded API keys or secrets |  |
| PASS | No hardcoded model metrics in results sections | Values sourced from loaded CSV/JSON files |

## Notes

- All 12 dashboard sections passed headless AppTest smoke tests without unhandled exceptions.
- All 100 SKU operational segments verified across demand tiers, inventory buffers, and DML estimates.
- All 5 recommendation strategies validated with zero revenue changes under price maintain rules.
- The serialized baseline model (`models/baseline_demand_model.joblib`, 522 MB) is excluded from git per `.gitignore`.
