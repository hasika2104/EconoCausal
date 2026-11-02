# Day 19 — Interactive Pricing Analytics Dashboard Summary

**Date:** 02 November 2026  
**Internship Role:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal — Retail Demand Estimation and Dynamic Pricing Decision-Support System  
**Repository:** `https://github.com/hasika2104/EconoCausal`  

---

## 1. Executive Summary

As part of the final integration and deployment phase of the EconoCausal research sprint at Infotact Solutions, Day 19 delivered a comprehensive, production-grade interactive dashboard implemented in `app.py`. Built using **Streamlit**, **Pandas**, **NumPy**, and **Plotly**, the dashboard serves as an interactive decision-support interface for executive leadership, pricing analysts, and store merchandising managers.

Rather than presenting mock data or naive machine learning projections, the dashboard directly incorporates:
1. Complete transactional aggregates from the $73,100$-row audited enterprise dataset (`data/processed/retail_inventory_cleaned.csv`).
2. Validated Double Machine Learning (DML) semiparametric treatment effects ($\hat{\theta} = +0.0107$, $p = 0.4899$, 95% CI: $[-0.0197, +0.0411]$) and 18 robustness checks.
3. Chronological holdout benchmarking across four predictive regression architectures (RidgeCV $R^2 = 0.3443$, Random Forest $R^2 = 0.3184$) and permutation importance diagnostics.
4. Physical retail inventory bounds ($\text{Sales} \le \text{Inventory}$), demand non-negativity, and price positivity constraints.
5. An executive governance matrix explicitly delineating why price discounting causes immediate revenue destruction under inelastic demand and why wholesale cost data is mandatory for profit optimization.

---

## 2. Technical Stack & Deployment Architecture

| Component | Library / Framework | Version | Purpose in Dashboard |
| :--- | :--- | :---: | :--- |
| **Application Server** | Streamlit | `1.66.1` | Reactive web interface, caching, sidebar navigation, parameter inputs |
| **Data Engine** | Pandas | `3.0.6` | Data slicing, filtering, multi-level aggregations |
| **Numerical Processing** | NumPy | `2.5.4` | Statistical array computations, scenario bounds |
| **Interactive Plotting** | Plotly (Graph Objects & Express) | `7.1.0` | Forest plots, time-series, histograms, error bars |
| **Core Statistical Models** | Scikit-Learn & Statsmodels | `1.9.1` / `0.15.0` | Regression benchmarks, DML nuisance modeling, HC3 covariance |
| **Language Runtime** | Python | `3.13.7` | Base environment running in isolated project virtual environment (`.venv`) |

---

## 3. Detailed Dashboard Modules & Actual Outputs Displayed

### Module 1: Project Overview
- **Strategic Context:** Explains the core business problem facing omnichannel retailers—the trade-off between volume stimulation and gross margin preservation.
- **The Predictive Optimization Trap:** Clarifies why supervised regression models latch onto post-treatment inventory colliders and why counterfactual price interventions require causal identification.
- **System Architecture:** Visualizes the analytical pipeline from raw transaction data to Double Machine Learning, holdout benchmarking, and managerial pricing governance.

### Module 2: Retail Data Overview
Presents empirical dataset figures calculated dynamically from `retail_inventory_cleaned.csv`:
- **Total Transactions:** $73,100$ complete records spanning 731 consecutive days (2022-01-01 to 2024-01-01).
- **Merchandise Breadth:** $20$ unique products across $5$ merchandise categories (`Clothing`, `Electronics`, `Furniture`, `Groceries`, `Toys`).
- **Store Footprint:** $5$ regional retail stores (`S001` to `S005`) across $4$ territories (`East`, `North`, `South`, `West`).
- **Average Retail Price:** $\$55.03$ (observed support: $[\$10.04, \$99.97]$).
- **Total Units Sold:** $10,250,862$ units (daily average of $140.2$ units per product-store).
- **Average Daily Inventory:** $273.2$ units.
- **Total Gross Revenue:** $\$564,136,878.50$.
- **Aggregations:** Dynamic breakdowns of revenue share by category and store transaction counts.

### Module 3: Exploratory Data Analysis (EDA)
- **Interactive Multi-Parameter Filters:** Global sidebar filters for Category, Store ID, Region, and Date Range.
- **Price and Volume Distributions:** Histograms with marginal boxplots illustrating symmetrical pricing ($\text{median} = \$55.01$) and positive demand skew.
- **Observational Correlation:** Scatter plot showing the flat, unadjusted empirical slope ($\Delta Y / \Delta P \approx +0.01$) resulting from confounding between store prestige, seasonality, and pricing tiers.
- **Time-Series Velocity:** Monthly aggregate trends of units sold and gross sales dollar volume across 2022–2024.
- **Inventory Stocking Relationship:** Visualizes the strong linear association between on-hand inventory and realized sales, demonstrating why supervised models over-rely on inventory.

### Module 4: Causal Analysis (Double Machine Learning)
Displays validated econometric outputs from `dml_validated_results.json` and `reports/day15_robustness_results.csv`:
- **Primary Specification (Spec 1):**
  - **Estimated Treatment Effect ($\hat{\theta}$):** $+0.0107$ units per $\$1.00$ price increase.
  - **Heteroskedasticity-Robust Standard Error (HC3):** $0.0155$.
  - **95% Confidence Interval:** $[-0.0197, +0.0411]$.
  - **$p$-Value:** $0.4899$ (Statistically insignificant at $\alpha = 0.05$).
  - **Implied Elasticity at Mean:** $+0.0042 \approx 0.00$ (Structurally inelastic demand).
  - **Control Variables:** `Product ID`, `Store ID`, `Category`, `Region`, `Year`, `Month`, `DayOfWeek`.
  - **Cross-Fitting:** 3-fold cross-fitting using `ExtraTreesRegressor(n_estimators=60)`.
- **Collider Sensitivity Check (Spec 2):**
  - Incorporating `Inventory Level` yields $\hat{\theta} = -0.0195$ ($p = 0.1193$, CI: $[-0.0440, +0.0050]$). Explicitly flags that conditioning on inventory introduces potential post-treatment collider bias.
- **18-Specification Robustness Forest Plot:** Visualizes point estimates and 95% confidence intervals across all 18 specifications (alternative nuisance models, control sets, categories, calendar years, regions, and price support trimming). Confirms that **all 18 specifications cleanly span zero**, proving that demand inelasticity is robust.

### Module 5: Model Performance Benchmarks
Presents supervised demand model holdout results from `reports/day16_model_performance.csv` (58,480 train / 14,620 test records):
- **Mean Dummy Baseline:** $\text{MAE} = 88.81$, $\text{RMSE} = 108.24$, $R^2 = -0.0000$.
- **Random Forest Baseline:** $\text{MAE} = 69.51$, $\text{RMSE} = 89.36$, $R^2 = 0.3184$.
- **HistGradientBoosting:** $\text{MAE} = 68.68$, $\text{RMSE} = 87.81$, $R^2 = 0.3419$.
- **RidgeCV (L2 Regularized):** $\text{MAE} = 68.65$, $\text{RMSE} = 87.65$, $R^2 = 0.3443$.
- **Feature Importance Diagnostics:** Shows that `Inventory Level` drives a $+0.7118$ test $R^2$ drop in permutation importance, whereas `Price` accounts for only $+0.0029$.
- **Predictive vs. Causal Callout:** Explains why predictive regression cannot guide price setting.

### Module 6: Pricing Scenario Explorer
- **Discrete Scenarios Evaluated:** $-10\%, -5\%, 0\%, +5\%, +10\%$ candidate price adjustments across Benchmark Case (`P0001` at `S001`) and category-specific cases (`Clothing`, `Electronics`, `Furniture`, `Groceries`, `Toys`).
- **Operational Metrics Displayed:** Candidate price, estimated demand, 95% confidence bounds, available inventory cap, realized sales (inventory-capped), projected gross revenue ($P \cdot Q$), dollar variance, and percentage revenue shift.
- **Continuous What-If Slider:** Allows analysts to test continuous price changes ($\pm 20\%$) in real time with dynamic stockout checks.
- **Prominent Cost Warning:** Clearly states that revenue $\ne$ profit and highlights the absence of wholesale procurement unit cost data.

### Module 7: Pricing Recommendations & Governance Matrix
- **Policy 1 — Strictly Reject Price Cuts:** Because demand is inelastic ($\theta \approx 0$), price reductions of $-5\%$ or $-10\%$ trigger immediate $-5.02\%$ to $-10.03\%$ revenue loss with zero volume offset.
- **Policy 2 — Maintain Status Quo Baseline:** Recommended operational default ensuring steady volume and predictable cash flow.
- **Policy 3 — Restrict Price Increases to Micro-Pilots:** Projected revenue gains from $+5\%$ or $+10\%$ price increases are statistically noisy ($p=0.49$) and ignore unobserved customer defection and procurement costs. Restricts price increases to controlled $\pm 2\%$ store pilots.
- **Detailed Scenario Table:** Formatted tabular view with risk classifications and managerial guidance.

### Module 8: Project Limitations & Analytical Caveats
Detailed tabbed interface delineating the core project boundaries:
1. **Unobserved Confounders:** Omitted marketing campaigns, competitor pricing actions, foot traffic, and cross-SKU substitution.
2. **Missing Cost Data:** Inability to optimize gross profit without wholesale cost (COGS).
3. **Statistical Uncertainty:** Treatment effect is statistically indistinguishable from zero ($p=0.4899$).
4. **Inventory Measurement Timing:** Post-treatment truncation risk if inventory is recorded at end-of-day rather than start-of-day.
5. **Observational Pricing Support:** Validated recommendations apply only within $[\$10.04, \$99.97]$.

---

## 4. Quality Assurance and Validation

The dashboard underwent rigorous automated and manual validation:
- **Syntax and Type Safety:** Compiled with Python 3.13.7 (`python -m py_compile app.py`); 0 syntax warnings, 0 escape sequence issues, 0 runtime syntax errors.
- **Automated Headless Testing (`AppTest`):** Streamlit's official testing framework (`streamlit.testing.v1.AppTest`) verified all 8 sections and interactive widgets with 0 exceptions.
- **Filter and State Verification:** Validated that interactive filtering by category, store, region, date range, and scenario slider re-renders without state corruption.
- **Concordance with Project Artifacts:** Verified that all printed values match `retail_inventory_cleaned.csv`, `dml_validated_results.json`, `day16_model_performance.csv`, `day15_robustness_results.csv`, and `day17_pricing_scenarios.csv` exactly.

---

## 5. How to Run the Dashboard

```bash
# 1. Activate the project environment
source .venv/bin/activate

# 2. Run the Streamlit application
streamlit run app.py
```

The application runs on local port 8501 (`http://localhost:8501`).
