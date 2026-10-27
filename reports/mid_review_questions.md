# EconoCausal: Mid-Review Technical Question Bank

**Role:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal — Dynamic Pricing via Double Machine Learning  
**Author:** Hasika Ippili  
**Repository:** [https://github.com/hasika2104/EconoCausal](https://github.com/hasika2104/EconoCausal)  
**Date:** October 2026  

This document provides a comprehensive set of 15 technical and business questions with detailed, defensible answers for the internship mid-review presentation and technical audit.

---

### Question 1: What is the primary business problem and core objective of the EconoCausal project?
**Answer:**  
The primary business problem is setting retail prices that maximize revenue and profitability without inadvertently hurting sales volume. In retail, historical sales and prices are confounded by seasonal trends, product quality, store geography, and inventory decisions. Standard forecasting models capture associations, not counterfactual responses to price interventions.  
The core objective of EconoCausal is to build an end-to-end analytical framework that:
1. Explores and cleans retail inventory and sales data.
2. Builds a predictive demand baseline to forecast volume.
3. Applies Double Machine Learning (DML) to isolate the causal price elasticity of demand from high-dimensional confounding.
4. Uses this estimated elasticity in a what-if pricing simulator with inventory caps, uncertainty intervals, and business constraints to guide merchant decisions.

---

### Question 2: Can you describe the dataset, its dimensions, and key data quality findings?
**Answer:**  
The project uses daily retail transaction records from `data/retail_store_inventory-selected-columns.csv`:
- **Dimensions:** 73,100 records covering 731 consecutive days (January 1, 2022 to January 1, 2024), 20 unique products (`P0001` to `P0020`), and 5 stores (`S001` to `S005`) across 4 regions.
- **Key Columns:** `Date`, `Store ID`, `Product ID`, `Category`, `Region`, `Inventory Level`, `Units Sold`, `Units Ordered`, `Demand Forecast`, and `Price`.
- **Quality Checks:**
  - Missing values: 0 across all columns.
  - Duplicate rows: 0 duplicate rows.
  - Price and sales ranges: Prices range from \$10.00 to \$100.00 (mean: \$55.14); units sold range from 0 to 499 (mean: 136.46 units); inventory level ranges from 50 to 500 units.
  - Anomaly noted: `Demand Forecast` contained negative values (down to -9.99). This column was retained for auditing but excluded from core causal estimation.
  - Cleaning produced `data/processed/retail_inventory_cleaned.csv` (14 columns, including derived `Year`, `Month`, `DayOfWeek`, and `Revenue`).

---

### Question 3: What did the Exploratory Data Analysis (EDA) reveal regarding price variation and demand?
**Answer:**  
Key EDA findings from `notebooks/01_data_exploration.ipynb` and `notebooks/04_causal_data_assessment.ipynb`:
1. **Intra-Pair Price Variation:** 100% of the 100 product-store pairs exhibit price variation over time (between 62 and 94 unique prices per pair). This confirmed that price changes occur within items, satisfying the basic empirical requirement for panel fixed effects and causal estimation.
2. **Orthogonal Overall Correlation:** The overall linear correlation between raw `Price` and `Units Sold` is virtually zero ($r \approx 0.00$). 
3. **Product-Level Variation:** Across individual products, correlations between price and sales fluctuate around zero, indicating that simple bivariate analysis cannot detect price elasticity due to unobserved confounding.

---

### Question 4: How was the baseline demand model constructed, and what were its evaluation results?
**Answer:**  
Implemented in `notebooks/03_baseline_demand_model.ipynb`:
- **Architecture:** `RandomForestRegressor(n_estimators=100, random_state=42)` wrapped in a pipeline with `OneHotEncoder` for categorical variables (`Product ID`, `Store ID`, `Category`, `Region`) and numeric features (`Price`, `Inventory Level`, `Year`, `Month`, `DayOfWeek`).
- **Splitting Strategy:** Chronological 80/20 train/test split (Train: 58,480 rows from Jan 2022 to Aug 2023; Test: 14,620 rows from Aug 2023 to Jan 2024) to prevent temporal data leakage.
- **Actual Evaluation Metrics:**
  - **Mean Absolute Error (MAE):** 69.51 units
  - **Root Mean Squared Error (RMSE):** 89.36 units
  - **$R^2$ Score:** 0.318 (31.8% of demand variance explained)
  - **Benchmark Comparison:** A `DummyRegressor(strategy='mean')` achieved an MAE of 88.81 units, proving the Random Forest captured meaningful operational patterns.

---

### Question 5: Why are MAE, RMSE, and $R^2$ useful metrics, and how do they differ in interpretation?
**Answer:**  
- **MAE (Mean Absolute Error):** Represents the average magnitude of absolute forecasting errors in the original units (units sold). It treats all errors linearly and is robust to outliers. Our test MAE of 69.51 indicates that on average, our prediction misses actual daily sales by ~70 units.
- **RMSE (Root Mean Squared Error):** Squares errors before averaging, penalizing large forecasting errors heavily. Our test RMSE of 89.36 is higher than MAE, indicating occasional larger forecast misses during demand surges.
- **$R^2$ (Coefficient of Determination):** Quantifies the proportion of outcome variance explained by the model relative to a horizontal mean line. Our $R^2$ of 0.318 indicates that seasonal, store, and product features account for roughly 32% of daily demand fluctuation, leaving 68% unexplained due to idiosyncratic shopper behavior or unrecorded factors.

---

### Question 6: Why can't a predictive machine learning model be used directly for pricing decisions? (Correlation vs. Causation)
**Answer:**  
Predictive machine learning models estimate the conditional expectation $\mathbb{E}[Y \mid X, T]$. They capture correlations present in historical data. In pricing, price is often adjusted in response to anticipated demand (e.g., higher prices during peak shopping periods or holidays). As a result, the model observes that higher prices coincide with higher sales, leading it to learn a positive correlation.  
If a retailer uses this predictive association to set prices, it commits the *conflation of correlation and causation*: raising the price when peak demand is absent will not generate the predicted sales increase. Causal inference aims to estimate the counterfactual structural derivative $\frac{\partial Y}{\partial T}$ under intervention, holding all confounders constant.

---

### Question 7: What are the treatment, outcome, and confounders in this causal analysis?
**Answer:**  
- **Treatment ($T$):** Retail `Price` (continuous variable).
- **Outcome ($Y$):** `Units Sold` (continuous volume).
- **Confounders ($W$):** Variables influencing both price setting and customer purchases:
  - Product identity (`Product ID`, `Category`) influencing baseline willingness-to-pay and baseline demand.
  - Store characteristics (`Store ID`, `Region`) reflecting local demographics, foot traffic, and operating costs.
  - Temporal patterns (`Year`, `Month`, `DayOfWeek`) capturing seasonality, holiday spikes, and weekly shopping rhythms.
- **Inventory ($Z$):** Handled as a physical constraint post-estimation rather than a baseline confounder due to timing ambiguity (see Question 10).

---

### Question 8: How does Double Machine Learning (DML) work, and why is it superior to simple linear regression?
**Answer:**  
DML, introduced by Chernozhukov et al. (2018), estimates causal effects in high-dimensional partially linear models:
$$Y - \mathbb{E}[Y \mid W] = \theta (T - \mathbb{E}[T \mid W]) + \varepsilon$$
1. **Nuisance Estimation:** Instead of assuming a rigid linear relationship between controls and the outcome/treatment, DML uses flexible machine learning models (`ExtraTreesRegressor`) to predict $Y$ from $W$ and $T$ from $W$.
2. **Frisch-Waugh-Lovell Residualization:** By subtracting these predictions, we obtain orthogonal residuals: $\tilde{Y} = Y - \hat{Y}(W)$ and $\tilde{T} = T - \hat{T}(W)$, stripping away all confounding captured by $W$.
3. **Neyman Orthogonality:** The moment condition is locally insensitive to first-order errors in the nuisance functions, ensuring that regularization bias from machine learning does not contaminate the treatment effect parameter $\theta$.
4. **OLS on Residuals:** A simple linear regression of $\tilde{Y}$ on $\tilde{T}$ yields the unbiased causal parameter $\hat{\theta}$.

---

### Question 9: What is cross-fitting, and why is it mandatory in DML?
**Answer:**  
Cross-fitting is an out-of-fold estimation procedure analogous to $K$-fold cross-validation. In our implementation (`notebooks/08_dml_validation.ipynb`), we use 3-fold cross-fitting (`KFold(n_splits=3, shuffle=True, random_state=42)`):
- For each fold $k$, nuisance models are trained on the remaining $K-1$ folds and used strictly to predict $\hat{Y}$ and $\hat{T}$ on fold $k$.
- **Why it is mandatory:** If nuisance models were evaluated on the same data used to train them, flexible tree ensembles would overfit. Overfitted predictions $\hat{T}$ would absorb genuine variation in $T$, creating artificial correlation between the residuals $\tilde{Y}$ and $\tilde{T}$ (own-observation bias). Cross-fitting guarantees that the residuals are statistically independent of the nuisance training sample, restoring standard $\sqrt{N}$-consistency and valid asymptotic normality.

---

### Question 10: What were the actual DML estimation results, and how do you interpret the coefficient and confidence interval?
**Answer:**  
From `notebooks/08_dml_validation.ipynb` and `data/processed/dml_validated_results.json`:
- **Specification 1 (Primary Core Controls: Product, Store, Category, Region, Year, Month, DayOfWeek):**
  - $\hat{\theta} = +0.0107$ units per \$1 price increase
  - Heteroscedasticity-robust HC3 Standard Error: $0.0155$
  - 95% Confidence Interval: $[-0.0197, +0.0411]$
  - $p$-value: $0.4899$ ($N = 73,100$)
- **Interpretation:**
  - The point estimate indicates that a \$1 increase in price is associated with $+0.01$ additional units sold—a practically negligible effect.
  - Because $p = 0.4899 > 0.05$, the coefficient is **not statistically significant**.
  - The 95% confidence interval $[-0.0197, +0.0411]$ spans zero, meaning we cannot reject the null hypothesis $H_0: \theta = 0$. The data is consistent with demand being completely price-inelastic.

---

### Question 11: Why does adding `Inventory Level` cause the DML coefficient to shift from $+0.0107$ to $-0.0195$? (Endogeneity and Bad Controls)
**Answer:**  
In Specification 2, adding `Inventory Level` shifts the coefficient by $-0.0302$ to $\hat{\theta} = -0.0195$ ($p = 0.1193$).  
This sensitivity is a classic example of **bad control / collider bias**:
- In retail inventory datasets, if `Inventory Level` is recorded at the end of the day, it is an outcome of sales: $Inventory_{closing} = Inventory_{opening} - UnitsSold$.
- Conditioning on closing inventory controls for the outcome itself and opens an endogenous non-causal path between price and unobserved demand shocks.
- Because the dataset metadata does not specify whether `Inventory Level` represents opening or closing stock, Spec 1 is selected as the primary unbiased specification, and Spec 2 is documented as a sensitivity stress-test.

---

### Question 12: How does the pricing simulator compute demand and revenue for candidate price changes?
**Answer:**  
Implemented in `notebooks/09_pricing_simulator.ipynb` and `src/business_validation.py`:
- For a baseline observation (Product `P0001`, Store `S001`: $P_0 = \$55.13$, $Q_0 = 173.0$ units, $Rev_0 = \$9,537.49$, $Inventory = 195$ units), candidate prices are generated at $-10\%, -5\%, 0\%, +5\%, +10\%$.
- Demand is estimated using the local linear causal formula:
  $$\hat{Q}(P) = \min\left(\text{Inventory Cap}, \max(0, Q_0 + \hat{\theta}(P - P_0))\right)$$
- Revenue is computed as $\hat{\text{Rev}}(P) = P \times \hat{Q}(P)$.
- Because $\hat{\theta} = +0.0107 \approx 0$, estimated demand remains virtually unchanged across scenarios (~172.94 to 173.06 units).
- Consequently, estimated revenue scales almost linearly with price: $-10\%$ yields \$8,580.81 (-10.03%), while $+10\%$ yields \$10,494.82 (+10.04%).

---

### Question 13: What is the critical breakeven elasticity threshold, and why does $+10\%$ remain optimal across the DML confidence interval?
**Answer:**  
In `notebooks/11_uncertainty_business_validation.ipynb`:
- Revenue is $Rev(P) = P \cdot (Q_0 + \theta \Delta P)$. Differentiating with respect to $P$ at baseline yields $\frac{d(Rev)}{dP} = Q_0 + \theta P_0$.
- For a price increase to cause revenue to decrease, demand must drop fast enough to satisfy:
  $$\theta < -\frac{Q_0}{P_0} = -\frac{173.0}{55.13} \approx -3.138 \quad (\text{or finite-difference threshold } \theta \approx -2.85)$$
- In our DML model, $\hat{\theta} = +0.0107$, and the lower bound of the 95% confidence interval is $-0.0197$.
- Even under the most pessimistic CI bound ($\theta = -0.0197$), a \$5.51 price increase only reduces sales by $0.11$ units, so revenue still rises to \$10,488.37. Because $-0.0197 \gg -2.85$, the $+10\%$ price recommendation is mathematically stable across the entire 95% confidence interval.

---

### Question 14: Why must we never conflate revenue maximization with profit maximization in this project?
**Answer:**  
Revenue is defined as $\text{Gross Receipts} = \text{Price} \times \text{Units Sold}$. Profit is defined as:
$$\text{Profit} = (\text{Price} - \text{Unit Cost}) \times \text{Units Sold} - \text{Fixed/Holding Costs}$$
The dataset contains **no cost information** (no Cost of Goods Sold, wholesale acquisition prices, or inventory carrying costs).  
If an item has very high marginal cost (e.g., unit cost = \$50 on a \$55 item), a small volume drop can disproportionately destroy gross profit even if revenue rises. Presenting revenue recommendations as "profit maximizing" would mislead business managers. Therefore, all recommendations are explicitly documented as *revenue-focused prototypes under zero-cost assumptions*.

---

### Question 15: What are the main limitations of this analysis, and what are the recommended next steps?
**Answer:**  
**Key Limitations:**
1. **Unobserved Confounders:** Observational retail records omit promotional discounts, competitor pricing, marketing campaigns, foot traffic, and regional macroeconomic factors.
2. **Statistically Insignificant Estimate:** With $p = 0.4899$, the price sensitivity parameter cannot be proven to be non-zero.
3. **Inventory Timing Ambiguity:** Undocumented inventory capture time creates endogeneity concerns.
4. **Local Linearity:** Assuming constant marginal elasticity across large price shifts may fail if consumers exhibit non-linear psychological price thresholds.

**Recommended Next Steps:**
1. **Heterogeneous Treatment Effects (HTE):** Implement Causal Forests or EconML to explore whether specific product categories or high-traffic stores exhibit significant price elasticity even if aggregate elasticity is zero.
2. **Cost Data Acquisition:** Integrate wholesale supplier costs to transition from revenue estimation to true profit optimization.
3. **Field Experimentation (A/B Testing):** Propose a randomized price-band pilot across matched store clusters to obtain clean, unconfounded causal benchmarks.
