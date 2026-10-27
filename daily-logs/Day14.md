# Day 14 — Final Project Review and Documentation

**Date:** 27 October 2026  
**Internship Role:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal — Dynamic Pricing via Double Machine Learning  

---

## Objective

The objective of Day 14 is to conduct a rigorous, end-to-end review and audit of the EconoCausal project across Days 1 through 13. This includes inspecting existing datasets, execution logs, and Jupyter notebooks; testing code reproducibility within the Python virtual environment (`.venv`); auditing predictive and causal model outputs; documenting verified empirical findings; identifying methodology limitations; and preparing comprehensive mid-review documentation and interview questions.

---

## Work Performed

1. **Repository and Environment Audit:**
   - Inspected the repository structure, Git commit history (from Day 1 through Day 13), `.gitignore`, and Python environment.
   - Identified and resolved a syntax formatting issue in `.gitignore` (missing newline separating `.DS_Store` and `models/`).
   - Populated `requirements.txt` with verified project package dependencies (`pandas`, `numpy`, `scikit-learn`, `statsmodels`, `scipy`, `matplotlib`, `seaborn`, `joblib`, `ipykernel`).
   - Verified Python 3.13.7 virtual environment interpreter and package availability.

2. **Full Pipeline and Notebook Review:**
   - **Data Cleaning & Exploration (`notebooks/01_data_exploration.ipynb`):** Audited raw dataset (`data/retail_store_inventory-selected-columns.csv`) vs. cleaned dataset (`data/processed/retail_inventory_cleaned.csv`). Verified row counts (73,100 rows), missing value checks (0 nulls), duplicate checks (0 duplicates), derived temporal features (`Year`, `Month`, `DayOfWeek`), and revenue formula (`Revenue = Price * Units Sold`).
   - **Baseline Demand Modeling (`notebooks/03_baseline_demand_model.ipynb`):** Evaluated Random Forest regression model on chronological 80/20 train/test split. Verified test metrics: MAE = 69.51, RMSE = 89.36, R² = 0.318 against dummy baseline MAE = 88.81.
   - **Causal Data Assessment & Baseline (`notebooks/04_causal_data_assessment.ipynb`, `notebooks/05_causal_baseline.ipynb`):** Audited price variation across 20 products and 100 product-store pairs (100% pairs have price variation). Inspected OLS regressions with HC3 robust standard errors (Simple OLS: $\beta = +0.0045$, $p = 0.770$; Fixed Effects OLS: $\beta = +0.0045$, $p = 0.774$).
   - **DML Preparation & Estimation (`notebooks/06_dml_data_preparation.ipynb`, `notebooks/07_dml_estimation.ipynb`):** Verified data preparation and Robinson partially linear model implementation with 3-fold cross-fitting using `ExtraTreesRegressor`.
   - **DML Validation & Specification Check (`notebooks/08_dml_validation.ipynb`):** Audited primary Specification 1 (core controls) vs. sensitivity Specification 2 (+ Inventory Level). Verified saved results in `data/processed/dml_validated_results.json`.
   - **Pricing Simulator & Recommendations (`notebooks/09_pricing_simulator.ipynb`, `notebooks/10_pricing_recommendations.ipynb`):** Verified candidate scenario calculations ($-10\%$ to $+10\%$), uncertainty propagation, and provisional inventory cap application (195 units) for Product P0001, Store S001.
   - **Uncertainty & Business Validation (`notebooks/11_uncertainty_business_validation.ipynb`, `src/business_validation.py`):** Verified sensitivity grid (35 evaluations), breakeven elasticity threshold calculation ($\theta \approx -2.85$ to $-3.14$), counterfactual inventory restriction (cap = 160 units), and automated business rule assertions.

3. **Mid-Review Preparation:**
   - Authored the mid-review executive and technical summary in `reports/mid_review_summary.md`.
   - Developed a 15-question mid-review technical question bank with detailed answers in `reports/mid_review_questions.md`.

---

## Files Reviewed or Updated

- `daily-logs/Day1.md` through `daily-logs/Day13.md` (Reviewed existing trajectory and milestone logs)
- `daily-logs/Day14.md` (Created Day 14 log)
- `.gitignore` (Corrected formatting for `.DS_Store` and `models/`)
- `requirements.txt` (Populated with project dependencies)
- `notebooks/01_data_exploration.ipynb` (Audited data cleaning and EDA workflow)
- `notebooks/03_baseline_demand_model.ipynb` (Audited Random Forest demand model)
- `notebooks/04_causal_data_assessment.ipynb` (Audited price variation and control assessment)
- `notebooks/05_causal_baseline.ipynb` (Audited OLS regressions with HC3 standard errors)
- `notebooks/06_dml_data_preparation.ipynb` (Audited feature selection and dataset preparation)
- `notebooks/07_dml_estimation.ipynb` (Audited initial DML estimation)
- `notebooks/08_dml_validation.ipynb` (Audited cross-fitting, Specification 1 vs 2, residual distributions)
- `notebooks/09_pricing_simulator.ipynb` (Audited scenario-based demand and revenue estimation)
- `notebooks/10_pricing_recommendations.ipynb` (Audited ranking and inventory constraints)
- `notebooks/11_uncertainty_business_validation.ipynb` (Audited uncertainty boundaries and threshold tests)
- `src/business_validation.py` (Tested and validated reusable auditing module)
- `data/processed/dml_validated_results.json` (Audited model parameters schema and values)
- `data/processed/pricing_simulator_results.json` (Audited scenario outputs schema and values)
- `reports/mid_review_summary.md` (Created mid-review technical summary)
- `reports/mid_review_questions.md` (Created mid-review interview preparation guide)

---

## Testing and Validation

| Test Item | Methodology / Scope | Result | Status |
| :--- | :--- | :--- | :--- |
| **Python Environment & Packages** | Verified imports of `pandas`, `numpy`, `sklearn`, `statsmodels`, `scipy` | Executed without errors | Passed |
| **Data Integrity Check** | Verified 73,100 rows, 0 nulls, 0 duplicate rows, exact revenue formula ($P \times Q$) | Exact match between raw and cleaned records | Passed |
| **Random Forest Baseline** | Chronological 80/20 train/test evaluation | Test MAE = 69.51, RMSE = 89.36, R² = 0.318 | Passed |
| **DML Spec 1 Estimation** | 3-fold cross-fitting, ExtraTreesRegressor nuisance models, HC3 SE | $\theta = +0.0107$, 95% CI $[-0.0197, 0.0411]$, $p = 0.4899$ | Passed |
| **DML Spec 2 Sensitivity** | Added `Inventory Level` control | $\theta = -0.0195$, 95% CI $[-0.0440, 0.0050]$, $p = 0.1193$ | Passed |
| **Business Module Validation** | Executed `src/business_validation.py` audit and sensitivity pipeline | 35 scenarios audited, all business constraints verified | Passed |
| **Breakeven Threshold Test** | Analytical inversion calculation for revenue optimality | Threshold $\theta \approx -2.85$ to $-3.14$ vs. estimated $+0.0107$ | Passed |

---

## Key Findings

1. **Statistical Insignificance of Price Sensitivity:**
   Across 73,100 observations spanning 100 product-store pairs over two years, Double Machine Learning estimates a price-effect coefficient of $\theta = +0.0107$ units per \$1 price increase ($p = 0.4899$). Because the 95% confidence interval $[-0.0197, +0.0411]$ spans zero, the observed price effect is not statistically distinguishable from zero.
2. **Predictive Performance vs. Causal Inference:**
   The Random Forest baseline demand model achieves an R² of 0.318 and an MAE of 69.51 units (an improvement over the dummy mean baseline MAE of 88.81 units). However, the predictive model captures associative patterns rather than causal responsiveness.
3. **Control Sensitivity and Inventory Endogeneity:**
   Adding `Inventory Level` as a control variable causes the DML coefficient to shift from $+0.0107$ to $-0.0195$ (a shift of $-0.0302$). This sensitivity highlights endogeneity risk: if inventory is recorded at the end of the day, it is an endogenous collider/outcome ($Inventory_{end} = Inventory_{start} - UnitsSold$) rather than an exogenous pre-treatment confounder.
4. **Economic Thresholds and Revenue Recommendations:**
   Because demand is estimated to be virtually price-inelastic, estimated revenue mechanically increases with higher prices (+10% scenario yields \$10,494.82 vs. baseline \$9,537.49). For a price increase to reduce revenue, the price coefficient would need to drop below $\theta \approx -2.85$ to $-3.14$. Because the lower bound of the 95% CI is $-0.0197$, the recommendation to raise prices appears robust under revenue maximization, but cannot be considered statistically proven or profit-maximizing.

---

## Limitations

1. **Unobserved Confounders:** Observational retail records lack marketing promotions, discounts, competitor prices, customer foot traffic, and regional macroeconomic events.
2. **Ambiguous Inventory Timing:** The dataset does not distinguish between opening stock and closing stock, creating potential collider bias if inventory is controlled for.
3. **Absence of Cost Data:** The dataset contains no Cost of Goods Sold (COGS), wholesale costs, or holding costs. Revenue is not profit. Maximizing revenue does not maximize profit.
4. **Local Linear Extrapolation:** The DML specification assumes a constant local treatment effect across the candidate price spectrum, which may not hold for larger price deviations.
5. **Statistical Uncertainty:** With $p = 0.4899$, the price response is not statistically significant. Recommendations must be treated as an experimental research prototype rather than an automated production engine.

---

## Challenges and Resolutions

- **Challenge:** The `.gitignore` file contained a merged string `.DS_Storemodels/` causing `.DS_Store` to be improperly parsed, and `requirements.txt` was initially empty.  
  **Resolution:** Cleaned `.gitignore` into distinct rules and populated `requirements.txt` with verified project package specifications.
- **Challenge:** Ambiguity regarding the role of `Inventory Level` in DML estimation.  
  **Resolution:** Designated Specification 1 (excluding inventory) as the primary causal estimate to avoid collider bias, while retaining Specification 2 as a sensitivity benchmark and applying inventory strictly as a physical post-demand constraint cap.

---

## Next Steps

1. Present project findings and technical methodology at the internship mid-review using `reports/mid_review_summary.md` and `reports/mid_review_questions.md`.
2. Explore non-linear and heterogeneous treatment effect estimators (e.g., Causal Forests, Causal Trees, or EconML's `DML` with interactive features).
3. Investigate the feasibility of acquiring unit cost or margin data to transition from revenue estimation to true profit optimization.
4. If business approval is granted, design a small-scale randomized A/B test or price band experiment to validate causal responsiveness in an experimental setting.

---

## Conclusion

At the completion of Day 14, the EconoCausal project has an audited, verified, and reproducible analytical pipeline. The predictive baseline model, DML estimation, validation checks, and pricing scenario simulation have been thoroughly tested. All empirical metrics and limitations are accurately documented, providing a sound, honest foundation for the upcoming internship mid-review.
