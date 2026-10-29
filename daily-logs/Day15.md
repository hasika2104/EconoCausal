# Day 15 — Model Improvement and Robustness Analysis

**Date:** 29 October 2026  
**Internship Role:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal — Causal Demand Estimation and Dynamic Pricing  

---

## Objective

The objective of Day 15 is to rigorously stress-test the stability, interpretability, and robustness of the Double Machine Learning (DML) price-effect estimates established in earlier milestones (Days 9 through 13). Rather than treating the baseline point estimate as a finished commercial pricing rule, we evaluate whether the estimated relationship between retail price and units sold is stable across alternative nuisance model algorithms, alternative control variable sets, product categories, geographic regions, calendar years, and price support trimming.

---

## Work Performed

1. **Repository and Baseline Pipeline Audit:**
   - Inspected the working tree, Git commit history, and upstream datasets (`data/processed/dml_preparation.csv`, `data/processed/retail_inventory_cleaned.csv`, `data/retail_store_inventory-selected-columns.csv`).
   - Verified that the data contains 73,100 complete observations, 0 missing values, and 0 duplicate product-store-date entries across 20 products and 5 stores over 731 days (2022-01-01 to 2024-01-01).
   - Replicated the exact Baseline DML Specification 1 from Day 10 (`data/processed/dml_validated_results.json`) down to 6 decimal places ($\theta = +0.010699$, 95% CI: $[-0.019671, +0.041069]$, $p = 0.4899$).

2. **Executed 18 Comprehensive Robustness Checks:**
   - **Baseline & Control Variations (Specs 1–3, 6):** Evaluated core fixed effects controls, inventory controls (evaluating post-treatment conditioning / collider risks), minimal fixed effects (product and store only), and pre-period management demand forecasts.
   - **Algorithmic Nuisance Model Variations (Specs 4–5):** Compared the non-linear `ExtraTreesRegressor` against regularized linear regression (`RidgeCV`) and gradient boosted decision trees (`HistGradientBoostingRegressor`).
   - **Subgroup & Sample Sensitivity (Subgroups 1–12):** Tested 5 product categories (Clothing, Electronics, Furniture, Groceries, Toys), 2 calendar years (2022 vs. 2023), 4 geographic regions (East, North, South, West), and 1st–99th price percentile trimming ($N = 71,642$).

3. **Created and Executed Day 15 Notebook:**
   - Authored and verified `notebooks/12_model_robustness_analysis.ipynb` with complete theoretical framing, executable cross-fitting pipelines, diagnostic residual distributions, and forest plot visualizations.
   - Executed all 22 cells end-to-end within the project environment without runtime errors.

4. **Persisted Quantitative Deliverables:**
   - Exported the complete 18-specification results table to `reports/day15_robustness_results.csv`.

---

## Model Specifications

All DML specifications were estimated using Robinson's (1988) partially linear model with 3-fold cross-fitting and heteroskedasticity-robust HC3 standard errors:
$$\tilde{Y}_i = \theta \tilde{T}_i + \varepsilon_i, \quad \text{where } \tilde{Y}_i = Y_i - \hat{g}(X_i), \; \tilde{T}_i = T_i - \hat{m}(X_i)$$

1. **Spec 1 (Baseline — Core Controls):**
   - Treatment ($T$): `Price` ($/unit)
   - Outcome ($Y$): `Units Sold` (units)
   - Controls ($X$): Categorical (`Product ID`, `Store ID`, `Category`, `Region`) + Numeric (`Year`, `Month`, `DayOfWeek`).
   - Nuisance Model: `ExtraTreesRegressor` ($n=60$, `min_samples_leaf=10`, `max_features=0.8`).
2. **Spec 2 (Core + Inventory Level):**
   - Controls: Core controls + `Inventory Level`.
   - Methodological Rationale: Tests whether holding on-hand stock constant shifts the price coefficient. Note: Carries high risk of post-treatment conditioning / collider bias if stock responds endogenously to expected sales.
3. **Spec 3 (Minimal Fixed Effects):**
   - Controls: `Product ID` and `Store ID` only.
   - Methodological Rationale: Tests sensitivity to omitting time and regional controls.
4. **Spec 4 (Linear Regularized Nuisance — RidgeCV):**
   - Controls: Core controls.
   - Nuisance Model: `RidgeCV` ($\alpha \in [10^{-2}, 10^{3}]$).
   - Methodological Rationale: Eliminates potential tree overfitting and tests if parametric linear partialling alters the linear slope.
5. **Spec 5 (Gradient Boosted Trees — HistGB):**
   - Controls: Core controls.
   - Nuisance Model: `HistGradientBoostingRegressor` (50 iterations, `min_samples_leaf=15`).
   - Methodological Rationale: Compares bagging against sequential gradient boosting.
6. **Spec 6 (Core + Demand Forecast):**
   - Controls: Core controls + `Demand Forecast`.
   - Methodological Rationale: Controls for pre-period management expectations of demand.
7. **Subgroups (Categories, Years, Regions, Price Trimming):**
   - Evaluated individually using `ExtraTreesRegressor` ($n=30$, 3-fold cross-fitting).

---

## Results

Below is the verified summary of all 18 robustness checks executed on the dataset:

| Specification ID | Specification / Subgroup | Sample Size ($N$) | Nuisance Model | $\theta$ Estimate (Units/$) | Std Error (HC3) | 95% Confidence Interval | $p$-value | Significant ($\alpha=0.05$)? | Implied Elasticity ($\epsilon$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `SPEC_01_BASELINE` | Baseline Spec 1 (Core Controls) | 73,100 | ExtraTrees ($n=60$) | $+0.01070$ | $0.01550$ | $[-0.01967, +0.04107]$ | $0.4899$ | No | $+0.0034$ |
| `SPEC_02_INVENTORY` | Spec 2 (+ Inventory Level) | 73,100 | ExtraTrees ($n=60$) | $-0.01947$ | $0.01250$ | $[-0.04396, +0.00503]$ | $0.1193$ | No | $-0.0062$ |
| `SPEC_03_MINIMAL_FE` | Spec 3 (Minimal Fixed Effects) | 73,100 | ExtraTrees ($n=40$) | $+0.00517$ | $0.01546$ | $[-0.02513, +0.03547]$ | $0.7381$ | No | $+0.0016$ |
| `SPEC_04_RIDGE` | Spec 4 (Linear Nuisance — RidgeCV) | 73,100 | RidgeCV | $+0.00433$ | $0.01547$ | $[-0.02598, +0.03464]$ | $0.7796$ | No | $+0.0014$ |
| `SPEC_05_HISTGB` | Spec 5 (Gradient Boosting — HistGB) | 73,100 | HistGB | $+0.00457$ | $0.01547$ | $[-0.02574, +0.03489]$ | $0.7674$ | No | $+0.0015$ |
| `SPEC_06_FORECAST` | Spec 6 (+ Demand Forecast) | 73,100 | ExtraTrees ($n=40$) | $+0.00214$ | $0.00121$ | $[-0.00023, +0.00450]$ | $0.0769$ | No | $+0.0007$ |
| `SUB_CAT_CLOTHING` | Category: Clothing | 14,626 | ExtraTrees ($n=30$) | $-0.02200$ | $0.03452$ | $[-0.08966, +0.04566]$ | $0.5239$ | No | $-0.0070$ |
| `SUB_CAT_ELECTRONICS`| Category: Electronics | 14,521 | ExtraTrees ($n=30$) | $-0.00053$ | $0.03435$ | $[-0.06786, +0.06680]$ | $0.9877$ | No | $-0.0002$ |
| `SUB_CAT_FURNITURE` | Category: Furniture | 14,699 | ExtraTrees ($n=30$) | $-0.01585$ | $0.03512$ | $[-0.08467, +0.05298]$ | $0.6518$ | No | $-0.0050$ |
| `SUB_CAT_GROCERIES` | Category: Groceries | 14,611 | ExtraTrees ($n=30$) | $+0.04322$ | $0.03470$ | $[-0.02478, +0.11122]$ | $0.2128$ | No | $+0.0138$ |
| `SUB_CAT_TOYS` | Category: Toys | 14,643 | ExtraTrees ($n=30$) | $+0.00211$ | $0.03430$ | $[-0.06512, +0.06934]$ | $0.9510$ | No | $+0.0007$ |
| `SUB_YEAR_2022` | Year: 2022 | 36,500 | ExtraTrees ($n=30$) | $+0.00164$ | $0.02197$ | $[-0.04143, +0.04470]$ | $0.9405$ | No | $+0.0005$ |
| `SUB_YEAR_2023` | Year: 2023 | 36,500 | ExtraTrees ($n=30$) | $+0.00885$ | $0.02178$ | $[-0.03385, +0.05155]$ | $0.6845$ | No | $+0.0028$ |
| `SUB_REG_EAST` | Region: East | 18,349 | ExtraTrees ($n=30$) | $+0.01067$ | $0.03098$ | $[-0.05005, +0.07139]$ | $0.7305$ | No | $+0.0034$ |
| `SUB_REG_NORTH` | Region: North | 18,228 | ExtraTrees ($n=30$) | $-0.01872$ | $0.03116$ | $[-0.07979, +0.04235]$ | $0.5479$ | No | $-0.0060$ |
| `SUB_REG_SOUTH` | Region: South | 18,297 | ExtraTrees ($n=30$) | $+0.04523$ | $0.03107$ | $[-0.01567, +0.10614]$ | $0.1455$ | No | $+0.0144$ |
| `SUB_REG_WEST` | Region: West | 18,226 | ExtraTrees ($n=30$) | $-0.01100$ | $0.03060$ | $[-0.07098, +0.04898]$ | $0.7192$ | No | $-0.0035$ |
| `SUB_PRICE_TRIMMED` | Trimmed Prices (1st–99th %ile)| 71,642 | ExtraTrees ($n=30$) | $+0.00492$ | $0.01599$ | $[-0.02642, +0.03627]$ | $0.7582$ | No | $+0.0016$ |

---

## Key Findings

1. **Directional Instability Around Zero:**
   - The sign of $\theta$ fluctuates between positive and negative values (min: $-0.0220$, max: $+0.0452$).
   - In 17 of 18 specifications, the 95% confidence interval spans zero; in Spec 6 (+ Demand Forecast), the interval is $[-0.00023, +0.00450]$, narrowly missing statistical significance ($p = 0.0769$).
   - Exactly **0 out of 18 specifications** achieve statistical significance at $\alpha = 0.05$.

2. **Economic Insensitivity Across All Subgroups:**
   - The absolute magnitude of $\theta$ is practically negligible across every specification ($|\theta| \le 0.045$ units sold per $\$1.00$ price shift).
   - Implied price elasticities at the mean are constrained within $|\epsilon| \le 0.0144$. A $10\%$ price increase ($\approx \$5.51$) changes predicted volume by less than $\pm 0.25$ units on an average daily demand of 173.1 units.

3. **Subgroup Homogeneity Under the Null:**
   - Subgroup differences between categories (e.g., Groceries $+0.0432$ vs. Clothing $-0.0220$) are not statistically distinguishable from each other ($z = 1.33$, $p = 0.18$).
   - Both calendar years (2022: $+0.00164$; 2023: $+0.00885$) show near-zero slopes.
   - Price trimming (1st to 99th percentiles) yields $\theta = +0.00492$ ($p = 0.7582$), confirming that outliers do not mask an underlying downward-sloping curve.

4. **Business Takeaway:**
   - The slightly positive baseline estimate ($\theta = +0.0107$) should **not** be interpreted as true causal price elasticity or used to justify aggressive price hikes. The empirical evidence demonstrates near-complete price insensitivity within historical ranges.

---

## Challenges

1. **Sandboxed Jupyter Execution:** Running `jupyter nbconvert` in macOS sandbox mode encountered socket-binding timeouts for `ipykernel`'s ZeroMQ loops. This was resolved cleanly by configuring temporary runtime paths (`/tmp/matplotlib`, `/tmp/ipython`) and executing the notebook through an in-process IPython runner, ensuring complete reproducibility without bypassing sandbox isolation.
2. **Computational Load of Multi-Fold Cross-Fitting:** Running 18 DML specifications with cross-fitting required careful optimization of nuisance tree counts ($n=30$–$60$) and parallel worker configurations (`n_jobs=-1`), successfully completing the entire notebook execution in under 115 seconds.

---

## Limitations

1. **Omitted Demand Shifters:** The dataset lacks marketing expenditure, localized promotional campaigns, competitor pricing, and foot-traffic indicators. If price increases coincide with unobserved promotional surges, the price coefficient will be biased upward toward zero.
2. **Post-Treatment Conditioning Risk (Spec 2):** Including `Inventory Level` shifts $\theta$ from $+0.0107$ to $-0.0195$. If inventory is managed dynamically in response to anticipated sales, conditioning on it introduces collider stratification bias.
3. **Absence of Cost and Margins:** Without Cost of Goods Sold (COGS), profit optimization cannot be computed; revenue models remain purely descriptive under volume insensitivity.
4. **Data Generation Characteristics:** The empirical stability near zero across all 18 specifications strongly suggests that the underlying dataset was synthesized with prices fluctuating exogenously without strong structural demand feedback.

---

## Next Steps

1. **Design Controlled In-Store A/B Experiments:** Transition from observational estimation to randomized pricing experiments where prices are randomly assigned across store-product clusters to guarantee unconfoundedness.
2. **Instrumental Variable Strategy:** Identify valid exogenous cost instruments (e.g., supplier wholesale price shifts or regional transport cost indices) to isolate exogenous price variation.
3. **Consolidate Final Project Report:** Synthesize findings from Days 1 through 15 into a clear executive presentation on the limitations of observational causal inference in retail pricing.
EOF