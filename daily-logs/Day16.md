# Day 16 — Demand Model Performance and Feature Analysis

**Date:** 30 October 2026  
**Internship Role:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal — Causal Demand Estimation and Dynamic Pricing  

---

## Objective

The objective of Day 16 is to rigorously evaluate the predictive performance of the baseline demand regression model trained on Day 5, benchmark it against alternative statistical learning algorithms on an identical chronological holdout set, decompose predictive feature importances, and clearly articulate the methodological boundary between predictive power and causal policy relevance.

---

## Work Performed

1. **Model Architecture and Pipeline Inspection:**
   - Inspected the serialized Day 5 baseline model (`models/baseline_demand_model.joblib`).
   - Verified that the pipeline comprises a `ColumnTransformer` (passthrough for numeric features, `OneHotEncoder(handle_unknown='ignore')` for categorical features) feeding into a `RandomForestRegressor` ($n=100$, `random_state=42`, all cores).
   - Target variable: `Units Sold` (daily sales volume per product-store).
   - Input features: `Price`, `Inventory Level`, `Year`, `Month`, `DayOfWeek` (numeric) and `Category`, `Region`, `Product ID`, `Store ID` (categorical).

2. **Data Leakage and Temporal Splitting Audit:**
   - Verified that the dataset is split chronologically rather than randomly to eliminate temporal lookahead leakage:
     - **Training Set:** 2022-01-01 to 2023-08-08 ($N = 58,480$, 80.0%).
     - **Testing Set:** 2023-08-08 to 2024-01-01 ($N = 14,620$, 20.0%).
   - Assessed target leakage risks:
     - `Demand Forecast`: Successfully excluded from the feature matrix to avoid circularity with management expectations.
     - `Inventory Level`: Flagged as an operational upper bound / potential collider. While highly predictive of observed sales, inventory stock levels are determined by supply chain managers based on anticipated velocity, creating an endogenous relationship rather than a causal driver.

3. **Multi-Model Holdout Performance Evaluation:**
   - Evaluated the Day 5 Random Forest baseline against a naive mean baseline (`DummyRegressor`) and two alternative model families:
     - **Alternative 1 — HistGradientBoostingRegressor:** Modern histogram-binned gradient boosting ($100$ iterations).
     - **Alternative 2 — RidgeCV:** L2-regularized linear regression with cross-validated shrinkage across $\alpha \in [10^{-2}, 10^{3}]$.

4. **Feature Importance Decomposition (MDI vs. Permutation):**
   - Computed in-sample Mean Decrease in Impurity (MDI / Gini variance reduction).
   - Computed out-of-sample Permutation Importance on the unseen holdout test set across 5 random shuffling repeats with $R^2$ scoring.
   - Identified the massive divergence between predictive signal and causal leverage.

5. **Residual Diagnostics and Error Analysis:**
   - Analyzed residual distribution ($e_i = Y_i - \hat{Y}_i$).
   - Diagnosed error patterns across actual demand quartiles, uncovering severe regression to the mean.

6. **Deliverables Created:**
   - Executed and validated notebook: `notebooks/13_demand_model_performance.ipynb`.
   - Quantitative evaluation report: `reports/day16_model_performance.csv`.
   - Feature decomposition report: `reports/day16_feature_analysis.csv`.

---

## Quantitative Results

### 1. Model Evaluation Metrics (Holdout Test Set, $N = 14,620$)

| Model | Model Family | MAE (units) | MSE | RMSE (units) | $R^2$ Score | Mean Residual Bias |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Naive Mean Baseline** | Heuristic Mean | $88.81$ | $11,716.17$ | $108.24$ | $-0.0000$ | $-0.7371$ |
| **Random Forest (Baseline)** | Bagging Ensemble | $69.51$ | $7,985.24$ | $89.36$ | $0.3184$ | $-1.3614$ |
| **HistGradientBoosting** | Boosting Ensemble | $68.68$ | $7,710.19$ | $87.81$ | $0.3419$ | $-0.3451$ |
| **RidgeCV** | Regularized Linear | $68.65$ | $7,682.42$ | $87.65$ | $0.3443$ | $-0.1614$ |

*Key finding:* Both regularized linear modeling (`RidgeCV`) and histogram gradient boosting (`HistGradientBoosting`) marginally outperform the deep unpruned Random Forest baseline on holdout test data ($R^2 = 0.3443$ and $0.3419$ vs. $0.3184$), indicating that unconstrained tree bagging experiences slight variance overfitting on one-hot categorical store/product identifiers.

### 2. Feature Importance Decomposition

| Predictive Rank | Feature | Type | RF MDI Importance | Test Permutation Mean ($\Delta R^2$) | Test Permutation Std | Causal / Methodological Role |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| **1** | `Inventory Level` | Numerical | $0.4402$ | **$+0.7118$** | $0.0106$ | **Capacity constraint / collider proxy.** Highly predictive, but not a causal policy lever. |
| **2** | `Price` | Numerical | $0.1495$ | **$+0.0029$** | $0.0020$ | **True decision lever.** Low predictive traction; DML confirmed $\theta = +0.0107$ ($p = 0.490$). |
| **3** | `Category` | Categorical | $0.0522$ | **$+0.0019$** | $0.0007$ | Macro product group classification. |
| **4** | `Month` | Numerical | $0.0615$ | **$+0.0015$** | $0.0007$ | Annual seasonal cycle. |
| **5** | `Product ID` | Categorical | $0.1380$ | **$+0.0007$** | $0.0010$ | Individual SKU baseline velocity fixed effects. |
| **6** | `DayOfWeek` | Numerical | $0.0494$ | **$+0.0006$** | $0.0010$ | Intra-week shopping variation. |
| **7** | `Year` | Numerical | $0.0135$ | **$+0.0000$** | $0.0000$ | Constant year in holdout test set (no marginal variance). |
| **8** | `Region` | Categorical | $0.0430$ | **$-0.0003$** | $0.0009$ | Geographic cluster; negligible out-of-sample impact. |
| **9** | `Store ID` | Categorical | $0.0527$ | **$-0.0018$** | $0.0017$ | Specific store location; slight negative generalization impact. |

### 3. Prediction Error Diagnostics Across Demand Quartiles

| Demand Quartile | Range (Units) | Actual Mean | Predicted Mean | Mean Residual ($Y - \hat{Y}$) | MAE | Bias Pattern |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Q1 (Low Demand)** | $[0, 48]$ | $24.03$ | $98.27$ | $-74.24$ | $75.54$ | Severe Overprediction |
| **Q2 (Mid-Low)** | $(48, 109]$ | $75.79$ | $112.09$ | $-36.30$ | $53.20$ | Moderate Overprediction |
| **Q3 (Mid-High)** | $(109, 203]$ | $150.75$ | $144.90$ | $+5.85$ | $47.52$ | Near-Zero Bias |
| **Q4 (High Demand)** | $(203, 792]$ | $293.33$ | $193.84$ | $+99.49$ | $101.73$ | Severe Underprediction |

---

## Key Insights and Critical Distinctions

1. **Predictive vs. Causal Importance:**
   - In standard predictive machine learning, `Inventory Level` appears overwhelmingly dominant, accounting for $44.0\%$ of tree split impurity and causing a catastrophic $0.7118$ drop in holdout $R^2$ if shuffled.
   - However, from a causal inference and dynamic pricing standpoint, **inventory is not a causal demand driver**. A retailer cannot generate consumer demand simply by piling excess inventory onto shelves. Rather, inventory is an endogenous capacity ceiling and a reflection of supplier replenishment cycles.
   - Conversely, `Price` has a low predictive importance ($0.0029$ test permutation impact), consistent with Day 10 DML estimation where the residual price variation has near-zero structural correlation with residual unit demand ($\theta = +0.0107, p = 0.490$).

2. **Systematic Regression to the Mean:**
   - Minimizing squared loss ($L_2$) drives tree ensembles to predict the conditional expectation $\mathbb{E}[Y \mid X]$, which aggressively compresses variance.
   - The model overpredicts slow-moving items by $+74.2$ units on average while underpredicting high-velocity surge events by $-99.5$ units.
   - Consequently, **direct simulation using raw machine learning predictions will distort dynamic pricing evaluations**. Causal simulation must instead apply the residualized treatment effect $\Delta Y = \theta \cdot \Delta P$ to an established baseline sales volume.

---

## Artifacts and Deliverables

- `notebooks/13_demand_model_performance.ipynb`
- `reports/day16_model_performance.csv`
- `reports/day16_feature_analysis.csv`
- `daily-logs/Day16.md`
