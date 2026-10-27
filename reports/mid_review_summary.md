# EconoCausal: Mid-Review Project Summary

**Project Name:** EconoCausal — Dynamic Pricing via Double Machine Learning  
**Internship Role:** Data Analyst Intern at Infotact Solutions  
**Author:** Hasika Ippili  
**Repository:** [https://github.com/hasika2104/EconoCausal](https://github.com/hasika2104/EconoCausal)  
**Date:** October 2026  

---

## 1. Project Title and Business Problem

In retail environments, setting the right product price is one of the most critical drivers of sales volume, revenue, and market share. However, pricing decisions are frequently made using simple predictive demand forecasting or observational correlations. Standard machine learning models observe what happened in the past, but they often mistake correlation for causation: for example, if ice cream prices are higher in the summer and sales are also higher due to warm weather, a standard model may infer that raising prices increases demand. 

In business reality, price is endogenous—retail managers adjust prices based on expected demand, seasonality, inventory pressures, and store characteristics. If a pricing algorithm ignores these confounding factors, it risks prescribing price increases that damage sales volume or price cuts that destroy revenue. 

**EconoCausal** addresses this business problem by developing a decision-support framework that combines predictive demand modeling with Double Machine Learning (DML) to estimate the true price sensitivity of demand while controlling for high-dimensional confounding, and then uses these estimates to simulate what-if pricing scenarios subject to inventory constraints and statistical uncertainty.

---

## 2. Project Objectives

The project is structured around five primary objectives:
1. **Data Assessment & Preprocessing:** Clean, validate, and explore historical retail inventory and sales transactions across multiple stores and product categories.
2. **Predictive Baseline Demand Modeling:** Build and evaluate a supervised predictive model to forecast unit sales and establish a benchmark for demand predictability.
3. **Causal Identification & Econometric Baselines:** Formalize the causal directed acyclic graph (DAG), establish OLS fixed-effects baselines, and examine price variation across product-store combinations.
4. **Double Machine Learning (DML) Estimation:** Apply semi-parametric DML (Robinson's residualized partially linear model) using cross-fitting to isolate the structural price elasticity of demand from confounding variables.
5. **Scenario Simulation & Decision Support:** Construct a constrained what-if pricing simulator that evaluates candidate price changes ($-10\%$ to $+10\%$), propagates estimation uncertainty (95% confidence intervals), enforces inventory caps, and audits economic breakeven thresholds.

---

## 3. Dataset Description and Important Columns

The project utilizes daily store-level retail inventory records spanning two full years: **January 1, 2022 to January 1, 2024** (731 consecutive days). The dataset comprises 100 unique product-store pairs (20 distinct products across 5 retail stores and 4 geographic regions), totaling **73,100 records**.

### Key Attributes:
- **`Date`:** Transaction date (parsed as ISO timestamp; covers 731 days).
- **`Store ID`:** Unique identifier for retail store (`S001` through `S005`).
- **`Product ID`:** Unique identifier for product (`P0001` through `P0020`).
- **`Category`:** Merchandise department (e.g., Grocery, Electronics, Clothing).
- **`Region`:** Geographic territory (e.g., North, South, East, West).
- **`Price` (Treatment $T$):** Retail unit price, ranging from \$10.00 to \$100.00 (mean: \$55.14, median: \$55.05).
- **`Units Sold` (Outcome $Y$):** Daily quantity sold, ranging from 0 to 499 units (mean: 136.46 units, median: 107.00 units).
- **`Inventory Level`:** Recorded stock on hand, ranging from 50 to 500 units (mean: 274.47 units).
- **`Units Ordered`:** Replenishment stock ordered, ranging from 20 to 200 units (mean: 110.00 units).
- **`Demand Forecast`:** Internal historical forecast value, ranging from -9.99 to 518.55 units (mean: 141.49 units).
- **`Revenue` (Derived):** Calculated directly as `Price * Units Sold` (mean: \$7,527.07, max: \$47,860.47).
- **Derived Temporal Features:** `Year` (2022–2024), `Month` (1–12), `DayOfWeek` (0–6).

---

## 4. Data Cleaning and EDA Workflow

Data quality and structure were examined in `notebooks/01_data_exploration.ipynb` and documented in `daily-logs/Day4.md`.

### Cleaning Decisions and Findings:
- **Completeness:** There were 0 missing values across all columns and 0 duplicate rows in the raw dataset. All 73,100 rows were retained.
- **Data Types:** Converted `Date` to datetime format and validated numeric types for prices, units sold, and inventory.
- **Value Sanity:** Verified that prices and units sold are strictly non-negative. An anomaly in `Demand Forecast` (minimum value of -9.99) was identified in the raw records; because `Demand Forecast` is an upstream artifact and not used in the primary causal model, it was flagged without altering the raw transaction records.
- **Exploratory Data Analysis:**
  - Price distributions across products are wide and relatively uniform, indicating varied price points.
  - Correlation analysis showed an overall linear correlation between `Price` and `Units Sold` very close to zero ($r \approx 0.00$), demonstrating that simple bivariate correlation fails to reveal demand elasticity.
  - 100% of the 100 product-store pairs exhibit price variation over time (between 62 and 94 unique price levels per pair), confirming sufficient intra-pair variation for fixed-effects and causal residualization.

---

## 5. Baseline Demand Model and Evaluation Results

To evaluate how well units sold can be predicted using standard machine learning, a baseline predictive pipeline was implemented in `notebooks/03_baseline_demand_model.ipynb`.

### Methodology:
- **Model:** `RandomForestRegressor(n_estimators=100, random_state=42)` combined with `ColumnTransformer` (One-Hot Encoding for categorical features).
- **Features Used:**
  - *Numeric:* `Price`, `Inventory Level`, `Year`, `Month`, `DayOfWeek`
  - *Categorical:* `Category`, `Region`, `Product ID`, `Store ID`
- **Data Splitting:** Chronological split (80% train = 58,480 rows from Jan 2022 to Aug 2023; 20% test = 14,620 rows from Aug 2023 to Jan 2024) to avoid data leakage from future dates.

### Verified Results:
- **Test Mean Absolute Error (MAE):** **69.51 units**
- **Test Root Mean Squared Error (RMSE):** **89.36 units**
- **Test Coefficient of Determination (R²):** **0.318** (31.8% of variance explained)
- **Benchmark Comparison:** A `DummyRegressor(strategy='mean')` achieved an MAE of **88.81 units**. The Random Forest improves predictive accuracy by ~19.3 units over the baseline mean.
- **Model Storage:** The trained model was serialized to `models/baseline_demand_model.joblib` (498 MB).

### Critical Predictive vs. Causal Distinction:
While the Random Forest provides predictive utility for operational replenishment, it cannot answer the counterfactual business question: *"What will happen to demand if we increase price by 5%?"* In machine learning regression, feature interactions and non-linear splits capture associative conditioning rather than the isolated causal effect ($\frac{\partial Y}{\partial T}$).

---

## 6. Causal Inference Problem: Treatment, Outcome, Confounders, and Controls

### Causal Formalism:
- **Treatment ($T$):** Retail `Price` (continuous variable).
- **Outcome ($Y$):** `Units Sold` (continuous/count variable).
- **Confounders ($W$):** Variables that jointly influence both the pricing decision and consumer demand:
  - Product-level characteristics (inherent brand value, quality, category).
  - Store-level characteristics (location, store size, regional purchasing power).
  - Temporal patterns (annual inflation, seasonal demand shifts, day-of-week shopping habits).

### Baseline Econometric Regression:
In `notebooks/05_causal_baseline.ipynb`, ordinary least squares (OLS) regressions with heteroscedasticity-robust HC3 standard errors were estimated:
1. **Uncontrolled OLS:** $UnitsSold = \alpha + \beta \cdot Price + \varepsilon$
   - $\hat{\beta} = +0.0045$, $p = 0.770$
2. **Fixed Effects OLS (Product, Store, Date controls):**
   - $\hat{\beta} = +0.0045$, $p = 0.774$

In both linear baselines, the estimated price coefficient is statistically indistinguishable from zero ($p > 0.75$), demonstrating that linear regression alone cannot isolate subtle non-linear confounding.

---

## 7. DML Methodology and Actual Estimation Results

Double Machine Learning (Chernozhukov et al., 2018) provides a mathematically principled framework to estimate treatment effects in the presence of high-dimensional non-linear confounders. 

### Implementation Architecture:
Using Robinson's (1988) partially linear model:
$$Y - \mathbb{E}[Y \mid W] = \theta (T - \mathbb{E}[T \mid W]) + \varepsilon, \quad \mathbb{E}[\varepsilon \mid T, W] = 0$$

1. **Nuisance Estimation:** Machine learning regressors (`ExtraTreesRegressor(n_estimators=100, random_state=42)`) predict $Y$ from controls $W$ to form $\hat{Y}(W)$, and predict $T$ from controls $W$ to form $\hat{T}(W)$.
2. **Cross-Fitting:** 3-fold cross-fitting (`KFold(n_splits=3, shuffle=True, random_state=42)`) is employed so that nuisance predictions for each observation are generated strictly out-of-fold. This eliminates overfitting bias and prevents artificial collinearity between residuals.
3. **Treatment Residualization:** Residuals are computed as $\tilde{Y} = Y - \hat{Y}$ and $\tilde{T} = T - \hat{T}$.
4. **Second-Stage Estimation:** OLS regression of $\tilde{Y}$ on $\tilde{T}$ is estimated with HC3 robust standard errors to obtain the structural causal parameter $\hat{\theta}$.

### Verified Estimation Results:

| Specification | Control Variables ($W$) | $\hat{\theta}$ (DML Coeff) | 95% Confidence Interval | Std Error (HC3) | $p$-value | Sample Size ($N$) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Spec 1 (Core)** | Product, Store, Category, Region, Year, Month, DayOfWeek | **+0.0107** | **[-0.0197, +0.0411]** | 0.0155 | 0.4899 | 73,100 |
| **Spec 2 (+Inventory)** | Spec 1 controls + `Inventory Level` | **-0.0195** | **[-0.0440, +0.0050]** | 0.0125 | 0.1193 | 73,100 |

### Critical Econometric Findings:
1. **Statistical Insignificance:** For the primary specification (Spec 1), the coefficient $\hat{\theta} = +0.0107$ has a $p$-value of $0.4899$. The 95% confidence interval $[-0.0197, +0.0411]$ spans zero. We fail to reject the null hypothesis of zero price effect ($H_0: \theta = 0$). In this dataset, demand is estimated to be virtually unresponsive to price.
2. **Inventory Endogeneity & Bad Control Risk:** When `Inventory Level` is added to the control set (Spec 2), the coefficient shifts by $-0.0302$ (a 282% shift) and flips sign to $-0.0195$. In retail data, if inventory is recorded at the end of the day, it is an endogenous collider/outcome ($Inventory_{end} = Inventory_{start} - UnitsSold$). Controlling for post-treatment inventory introduces collider bias. Therefore, Spec 1 is retained as the primary benchmark, and Spec 2 is treated strictly as an exploratory sensitivity check.

---

## 8. Validation and Pricing Scenario Analysis

To test practical business application, a scenario simulation prototype was developed in `notebooks/09_pricing_simulator.ipynb`, `notebooks/10_pricing_recommendations.ipynb`, and `notebooks/11_uncertainty_business_validation.ipynb`.

### Baseline Observation:
- **Target Item:** Product `P0001` at Store `S001` (median price observation).
- **Observed Baseline Price ($P_0$):** \$55.13
- **Observed Baseline Units Sold ($Q_0$):** 173.0 units
- **Observed Baseline Revenue ($Rev_0$):** \$9,537.49
- **Provisional Inventory Cap:** 195.0 units

### Pricing Scenarios Evaluated:
Using the local linear demand approximation $\hat{Q}(P) = \min\left(\text{InventoryCap}, \max(0, Q_0 + \hat{\theta}(P - P_0))\right)$:

| Scenario | Price ($) | $\Delta$ Price ($) | Est. Units Sold | 95% CI Units | Est. Revenue ($) | $\Delta$ Revenue ($) | $\Delta$ Revenue (%) | Constraint Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **-10%** | \$49.62 | -\$5.51 | 172.94 | [172.77, 173.11] | \$8,580.81 | -\$956.68 | -10.03% | Unconstrained |
| **-5%** | \$52.37 | -\$2.76 | 172.97 | [172.89, 173.05] | \$9,059.07 | -\$478.42 | -5.02% | Unconstrained |
| **0% (Base)** | \$55.13 | \$0.00 | 173.00 | [173.00, 173.00] | \$9,537.49 | \$0.00 | 0.00% | Baseline |
| **+5%** | \$57.89 | +\$2.76 | 173.03 | [172.95, 173.11] | \$10,016.07 | +\$478.58 | +5.02% | Unconstrained |
| **+10%** | \$60.64 | +\$5.51 | 173.06 | [172.89, 173.23] | \$10,494.82 | +\$957.33 | +10.04% | Unconstrained |

### Uncertainty & Breakeven Threshold Validation:
1. **Breakeven Elasticity Inversion:** For a $+10\%$ price increase to cause a drop in revenue, the demand sensitivity parameter would need to be $\theta < -2.85$ (or $\theta < -Q_0/P_0 \approx -3.14$). Because the estimated $\hat{\theta} = +0.0107$ and even the pessimistic 95% CI lower bound is $-0.0197$, the estimated revenue gain for $+10\%$ remains positive across the entire confidence interval.
2. **Counterfactual Binding Inventory (Cap = 160 units):** When inventory is restricted below baseline demand (e.g., capped at 160 units), volume cannot expand. Raising the price to $+10\%$ (\$60.64) yields \$9,702.40 without any volume penalty, demonstrating that supply-constrained items strongly favor price increases.

---

## 9. Business Relevance and Potential Use Cases

1. **Evidence-Based Markdown Management:** Prevents retailers from executing aggressive price cuts under the mistaken belief that lower prices will generate massive volume windfalls, when data indicates inelastic demand.
2. **Constrained Pricing Decision Support:** Incorporates inventory availability directly into recommendations, avoiding out-of-stock scenarios.
3. **Transparent Uncertainty Communication:** By presenting 95% confidence intervals and sensitivity shifts rather than single-point forecasts, retail executives are informed of econometric uncertainty before making pricing changes.

---

## 10. Tools and Technologies Used

- **Programming Language:** Python 3.13.7
- **Data Manipulation & Analysis:** `pandas` (3.0.6), `numpy` (2.5.4)
- **Machine Learning & Preprocessing:** `scikit-learn` (1.9.1) (`RandomForestRegressor`, `ExtraTreesRegressor`, `ColumnTransformer`, `OneHotEncoder`, `KFold`)
- **Econometric Modeling:** `statsmodels` (0.15.0) (OLS with HC3 robust standard errors)
- **Scientific Computing:** `scipy` (1.18.1)
- **Data Visualization:** `matplotlib` (3.11.2), `seaborn` (0.13.2)
- **Model Persistence:** `joblib` (1.6.0)
- **Development Environment:** Jupyter Notebook, Git, GitHub

---

## 11. Current Accomplishments Based on Verified Evidence

- Fully functional data processing and cleaning pipeline generating structured analytical datasets (`data/processed/retail_inventory_cleaned.csv` and `dml_preparation.csv`).
- Baseline Random Forest demand forecasting model with verified out-of-sample evaluation ($R^2 = 0.318$, MAE = 69.51).
- Complete Double Machine Learning implementation featuring 3-fold cross-fitting and Robinson residualization.
- Multi-specification sensitivity audit comparing core controls vs. inventory-inclusive controls.
- Functional pricing simulator with uncertainty bounds and provisional inventory caps.
- Reusable modular testing engine in `src/business_validation.py` that validates schemas, parameter ranges, and business constraints.
- Generated sensitivity documentation including visual heatmaps (`reports/day13_sensitivity_analysis.png`) and tabular exports (`reports/day13_sensitivity_results.csv`).

---

## 12. Limitations and Assumptions

1. **Observational Confounding:** Retail sales data is strictly observational. Key demand drivers—including promotions, competitor prices, marketing spend, foot traffic, and macroeconomic shocks—are absent from the dataset.
2. **Lack of Statistical Significance:** With $\hat{\theta} = +0.0107$ and $p = 0.4899$, the price coefficient is not statistically significant. Pricing recommendations must be treated as a prototype rather than an automated production policy.
3. **Revenue vs. Profit:** The dataset does not include Cost of Goods Sold (COGS) or holding costs. Revenue maximization is not profit maximization; raising prices without cost data ignores gross margin impacts.
4. **Inventory Measurement Timing:** The timing of `Inventory Level` is ambiguous. If measured at day end, it is an endogenous collider; if measured at day start, it is an exogenous capacity constraint.
5. **Linear Treatment Effect Assumption:** Robinson's partially linear model assumes a constant marginal treatment effect across candidate price levels, which may break down for large price deviations.

---

## 13. Work Still in Progress

- Integration of non-linear causal modeling techniques (such as Causal Forests or generalized DML) to explore whether price sensitivity varies across specific product subcategories or stores.
- Interactive user interface prototype (such as a Streamlit dashboard) leveraging `app.py` for interactive merchant scenario testing.
- Acquisition or simulation of wholesale cost structures to enable true profit-maximization analysis.

---

## 14. Next Steps

1. **Mid-Review Defense:** Present the empirical findings, econometric distinctions, and project limitations to internship mentors and technical reviewers.
2. **Heterogeneous Treatment Effects (HTE):** Implement subgroup causal analysis to determine if specific high-value products exhibit statistically significant price sensitivity even if the aggregate effect is zero.
3. **Experimental Pilot Design:** Formulate a proposal for a randomized controlled trial (A/B pricing test) across selected store clusters to establish definitive ground-truth causal elasticity.
