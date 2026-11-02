# Day 19 — Build Interactive Pricing Analytics Dashboard

**Date:** 02 November 2026  
**Internship Role:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal — Retail Demand Estimation and Dynamic Pricing Decision-Support System  
**Repository:** `https://github.com/hasika2104/EconoCausal`  

---

## 1. Executive Summary & Objective

The objective of Day 19 is to design, develop, and test an interactive, production-grade decision-support dashboard (`app.py`) using **Streamlit**, **Pandas**, **NumPy**, and **Plotly**. The dashboard synthesizes the end-to-end analytical findings of the EconoCausal project (Days 1–18), enabling business stakeholders, executive managers, and internship reviewers to explore retail demand, historical pricing patterns, predictive versus causal model performance, statistical uncertainty, inventory constraints, and defensible pricing recommendations.

Crucially, the dashboard operates strictly on **actual verified outputs** from previous sprint deliverables without fabricating data, metrics, causal estimates, confidence intervals, or recommendations.

---

## 2. Technical Stack and Environment

- **Dashboard Framework:** Streamlit (v1.66.1)
- **Data Manipulation & Computation:** Pandas (v3.0.6), NumPy (v2.5.4)
- **Interactive Visualization:** Plotly Graph Objects & Plotly Express (v7.1.0)
- **Econometric & Statistical Models:** Scikit-Learn (v1.9.1), Statsmodels (v0.15.0), SciPy (v1.18.1)
- **Execution Environment:** Python 3.13.7 within project virtual environment (`.venv`)

---

## 3. Dashboard Architecture and Sections

The dashboard is structured into eight modular, navigable sections accessible via the sidebar:

### Section 1: Project Overview (📌)
- **Problem Statement:** Documents the promotional and margin dilemma in retail pricing, detailing the predictive optimization trap, over-discounting risk, naive price hike risk, and the revenue versus profit disconnect.
- **Project Objectives:** Outlines the five core research pillars: observational data audit, supervised demand benchmarking, Double Machine Learning (DML) causal isolation, 18-specification sensitivity testing, and constrained dynamic pricing decision support.
- **Pipeline Architecture:** Interactive Mermaid architecture flowchart illustrating the transition from raw retail logs to governance policies.
- **Technology Stack:** Clean metadata tags specifying core libraries and econometric frameworks.

### Section 2: Retail Data Overview (📊)
- **Empirical KPI Metrics:** Computed in real-time from `data/processed/retail_inventory_cleaned.csv`:
  - Total Transactions: $73,100$ records (0 nulls, 0 duplicates).
  - Cross-Sectional Breadth: $20$ unique products across $5$ merchandise categories (`Clothing`, `Electronics`, `Furniture`, `Groceries`, `Toys`).
  - Store Network: $5$ retail facilities (`S001`–`S005`) across $4$ geographic territories (`East`, `North`, `South`, `West`).
  - Baseline Price: Average retail price of $\$55.03$ (historical range: $[\$10.04, \$99.97]$).
  - Total Volume: $10,250,862$ total units sold (daily average of $140.2$ units per product-store).
  - Stocking Levels: Average daily inventory level of $273.2$ units.
  - Gross Sales Volume: Realized gross daily sales of $\$564.1\text{M}$.
- **Tabular Aggregates:** Category-wise revenue share analysis and regional store network breakdown.
- **Data Quality Verification:** Verified 731 consecutive calendar days (2022-01-01 to 2024-01-01).

### Section 3: Exploratory Data Analysis (🔍)
- **Multi-Dimensional Filtering:** Sidebar controls allowing interactive filtering by Category, Store ID, Region, and Calendar Observation Window.
- **Distribution Analysis:** Histograms with marginal boxplots of Selling Price and Daily Units Sold.
- **Observational Elasticity Scatter:** 2,500-point sample of Price versus Units Sold with OLS trendline, visually illustrating the flat, slightly positive observational association ($\Delta Y / \Delta P \approx +0.01$) induced by store and product confounding.
- **Time-Series Velocity:** Monthly aggregate trends of units sold and gross revenue over the 2-year horizon.
- **Stocking Relationships:** Bivariate scatter plot of Inventory Level versus Units Sold, demonstrating the high correlation ($R^2 \approx 0.32$) that causes supervised algorithms to rely heavily on inventory as a proxy/collider.

### Section 4: Causal Analysis (DML) (🔬)
- **Robinson's Partially Linear DML:** Presents the primary econometric findings from `data/processed/dml_validated_results.json`:
  - **Treatment Variable ($P$):** Unit Selling Price.
  - **Outcome Variable ($Y$):** Daily Units Sold.
  - **Control Covariates ($X$):** `Product ID`, `Store ID`, `Category`, `Region`, `Year`, `Month`, `DayOfWeek`.
  - **Nuisance Learner:** ExtraTreesRegressor ($n=60$) with 3-fold cross-fitting for Neyman orthogonality.
  - **Primary Estimate (Spec 1):** $\hat{\theta} = +0.0107$ units per $\$1.00$ price increase.
  - **HC3 Robust Standard Error:** $0.0155$.
  - **95% Confidence Interval:** $[-0.0197, +0.0411]$.
  - **$p$-Value:** $0.4899$ (statistically insignificant at $\alpha = 0.05$).
  - **Implied Mean Elasticity:** $\epsilon = +0.0042 \approx 0.00$ (perfectly inelastic demand).
- **Sensitivity Check (Spec 2):** Inclusion of `Inventory Level` yields $\hat{\theta} = -0.0195$ ($p = 0.1193$, CI: $[-0.0440, +0.0050]$); explicitly explains the risk of collider / post-treatment bias when conditioning on inventory.
- **18-Specification Forest Plot:** Dynamic Plotly forest plot displaying point estimates and 95% confidence intervals across all 18 sensitivity checks from `reports/day15_robustness_results.csv`, visually verifying that every single confidence interval spans zero.

### Section 5: Model Performance (📈)
- **Holdout Predictive Evaluation:** Presents chronological holdout benchmarks (58,480 train / 14,620 test records) from `reports/day16_model_performance.csv`:
  - Mean Dummy Baseline: $\text{MAE} = 88.81$, $\text{RMSE} = 108.24$, $R^2 = -0.0000$.
  - Random Forest (Baseline): $\text{MAE} = 69.51$, $\text{RMSE} = 89.36$, $R^2 = 0.3184$.
  - HistGradientBoosting: $\text{MAE} = 68.68$, $\text{RMSE} = 87.81$, $R^2 = 0.3419$.
  - RidgeCV (L2 Regularized): $\text{MAE} = 68.65$, $\text{RMSE} = 87.65$, $R^2 = 0.3443$.
- **Feature Diagnostics:** Permutation importance table and chart from `reports/day16_feature_analysis.csv` illustrating that Inventory Level drives a $+0.7118$ test $R^2$ drop, whereas Price exhibits near-zero predictive importance ($+0.0029$).
- **Predictive vs. Causal Distinctions:** Prominent callout explaining why high test $R^2$ does not validate causal price intervention policies.

### Section 6: Pricing Scenario Explorer (🎛️)
- **Interactive Multi-Product Simulation:** Evaluates discrete candidate price scenarios ($-10\%, -5\%, 0\%, +5\%, +10\%$) from `reports/day17_pricing_scenarios.csv`:
  - Benchmark Case: Product `P0001` at Store `S001` (Groceries).
  - Category-Specific Cases: `Clothing`, `Electronics`, `Furniture`, `Groceries`, `Toys`.
- **Outputs Displayed:** Candidate price, estimated demand with 95% confidence bounds, available inventory, realized sales (inventory-capped), estimated revenue ($P \cdot Q$), revenue differences in dollars and percentages, and binding status.
- **Continuous What-If Simulator:** Interactive slider allowing continuous percentage adjustments ($\pm 20\%$) with real-time recalculation of demand, stockout constraints, and top-line revenue.
- **Economic Safety Alert:** Prominent warning explicitly defining revenue as $P \cdot Q$ and declaring profit optimization infeasible due to absent wholesale unit cost data.

### Section 7: Pricing Recommendations & Governance Matrix (💡)
- **Actionable Strategic Policies:**
  1. **Reject Price Cuts:** Demand is structurally inelastic ($\theta \approx 0$); price reductions of $-5\%$ or $-10\%$ trigger $-5.02\%$ to $-10.03\%$ revenue destruction without volume compensation.
  2. **Status Quo Baseline:** Recommended operational default maintaining predictable demand and revenue.
  3. **Controlled Micro-Pilots:** Modest price increases ($+5\%$) show simulated top-line gains ($+5.02\%$), but because $\theta$ is statistically insignificant ($p=0.49$) and COGS is unobserved, broad rollout is restricted in favor of small-scale $\pm 2\%$ store pilots.
- **Decision Matrix Table:** Structured risk ratings and managerial actions across all candidate scenarios.

### Section 8: Limitations & Analytical Caveats (⚠️)
- **Unobserved Confounding:** Explains potential violations of the Conditional Independence Assumption (promotions, competitor actions, local foot traffic, cross-price substitution).
- **Missing Procurement Cost Data:** Documents why revenue maximization $\ne$ profit maximization without wholesale cost data ($c$).
- **Statistical Uncertainty:** Highlights the wide 95% confidence interval spanning zero ($p = 0.4899$).
- **Inventory Measurement Timing:** Explains the risk of post-treatment truncation if inventory reflects end-of-day rather than start-of-day stock.
- **Observational Support:** Flags that pricing recommendations apply only within historical price bounds ($[\$10.04, \$99.97]$).

---

## 4. UI/UX Design Standards

- **Theme & Palette:** Professional light-colored design with corporate forest and emerald green accents (`#1b5e20`, `#2e7d32`, `#388e3c`, `#e8f5e9`, `#f1f8e9`, `#c8e6c9`).
- **Typography & Spacing:** Clear hierarchies, responsive layouts, consistent component padding, and clean KPI card borders.
- **Data Rendering:** Formatted numbers (percentages, currency formatting, commas, 2–4 decimal precision).
- **Graceful Error Handling:** Dynamic file path validation and user-friendly fallback notices if files are moved.

---

## 5. Verification & Testing Performed

1. **Compilation Check:**
   - Ran `python -m py_compile app.py` under Python 3.13.7.
   - Verified 0 syntax warnings, 0 escape sequence warnings, and 0 errors.
2. **Programmatic Headless Testing (`AppTest`):**
   - Executed automated tests using `streamlit.testing.v1.AppTest`.
   - Iterated through all 8 dashboard sections:
     - `📌 1. Project Overview` — **PASSED** (0 exceptions)
     - `📊 2. Retail Data Overview` — **PASSED** (0 exceptions)
     - `🔍 3. Exploratory Data Analysis` — **PASSED** (0 exceptions)
     - `🔬 4. Causal Analysis (DML)` — **PASSED** (0 exceptions)
     - `📈 5. Model Performance` — **PASSED** (0 exceptions)
     - `🎛️ 6. Pricing Scenario Explorer` — **PASSED** (0 exceptions)
     - `💡 7. Pricing Recommendations` — **PASSED** (0 exceptions)
     - `⚠️ 8. Project Limitations` — **PASSED** (0 exceptions)
3. **Interactive Widget & Filter Testing:**
   - Simulated dynamic category and store selection filtering in the sidebar — **PASSED**.
   - Simulated continuous slider adjustments in Section 6 ($-10\%$ to $+5\%$) — **PASSED**.
   - Verified that calculations dynamically align with underlying model outputs and JSON artifacts.

---

## 6. How to Run the Dashboard

To launch the dashboard locally:

```bash
# 1. Activate the project virtual environment
source .venv/bin/activate

# 2. Launch Streamlit
streamlit run app.py
```

The application will open automatically in your browser at `http://localhost:8501`.

---

## 7. Deliverables Summary

- `app.py`: Complete Streamlit interactive analytics application.
- `requirements.txt`: Updated with `streamlit>=1.30.0` and `plotly>=5.18.0`.
- `daily-logs/Day19.md`: Comprehensive engineering log.
- `reports/day19_dashboard_summary.md`: Institutional dashboard summary report.
- `README.md`: Updated with Day 19 progress, architecture, and dashboard startup instructions.
