# Day 13: Complete Uncertainty and Business Validation

**Date:** 25 October 2026

## Objective
Rigorously stress-test and audit the Day 12 inventory-constrained pricing recommendations against statistical estimation uncertainty from the Day 10 Double Machine Learning (DML) models, validate all operational and business constraints, perform analytical elasticity breakeven threshold testing, and establish explicit causal vs. observational criteria for commercial deployment.

---

## Files Created or Updated
1. `notebooks/11_uncertainty_business_validation.ipynb`: Complete executable validation notebook with multi-scenario sensitivity tables, visualizations, business rules audit, and counterfactual inventory testing.
2. `src/business_validation.py`: Reusable validation and sensitivity modeling module implementing schema validation, parameter propagation, threshold calculations, and business constraint audits.
3. `src/__init__.py`: Package initialization for reusable project modules.
4. `reports/day13_sensitivity_results.csv`: Saved multi-scenario validation dataset containing 35 rows across 7 parameter scenarios and 5 price levels.
5. `reports/day13_sensitivity_analysis.png`: High-resolution three-panel visualization showing demand curves, revenue trajectories, and percentage changes vs. baseline.
6. `daily-logs/Day13.md`: Detailed documentation of tasks, exact numerical results, methodological interpretation, and commercial readiness assessment.

---

## Tasks Performed
- **Workspace and Repository Inspection:** Verified the local project environment, Git history (commit `835ccf9`), and upstream data artifacts (`data/processed/dml_validated_results.json`, `data/processed/pricing_simulator_results.json`, `data/processed/dml_preparation.csv`).
- **Input Integrity & Schema Audit:** Verified expected columns, numeric ranges, non-null values, positive baseline prices, non-negative baseline demand, and baseline revenue consistency.
- **Estimator Scale & Units Verification:** Verified that treatment (`Price`) and outcome (`Units Sold`) are entered in unscaled natural units, confirming that $\theta \equiv \frac{\partial Y}{\partial P}$ represents units sold per $1.00 price change.
- **Multi-Scenario Sensitivity Analysis:** Propagated point estimates and 95% HC3 confidence interval bounds for Spec 1 (core controls) and Spec 2 (with inventory control) across pricing scenarios ($-10\%$, $-5\%$, $0\%$, $+5\%$, $+10\%$).
- **Analytical Breakeven Threshold Derivation:** Derived and computed the critical price sensitivity threshold $\theta^* = -2.8528$ units/\$ (elasticity $\epsilon^* \approx -0.91$), where raising price by $+10\%$ yields zero incremental revenue over baseline.
- **Business Constraint & Operational Audit:** Verified candidate price positivity, non-extrapolation within observed support ($[\$10.26, \$99.97]$), non-negativity of demand, exact revenue calculation ($P \times \min(\hat{Y}, \text{Inv})$), and documented absence of COGS/margin data.
- **Counterfactual Inventory Stockout Test:** Simulated a scenario with a binding inventory restriction (Cap = 160 units) to demonstrate how hard inventory limits alter the revenue curve and pricing ranking.
- **Exported Deliverables:** Saved the sensitivity results table to `reports/day13_sensitivity_results.csv` and visualization to `reports/day13_sensitivity_analysis.png`.

---

## Data and Model Inputs Used

- **Baseline Observation (Product P0001, Store S001):**
  - Baseline Price: \$55.13 (median observed historical price)
  - Baseline Demand: 173.0 units sold
  - Baseline Revenue: \$9,537.49
  - Baseline Inventory Level: 195.0 units (provisional constraint; timing unverified)
  - Observed Historical Price Range for (P0001, S001): \$10.26 to \$99.97
- **DML Specifications (from Day 10 Validation):**
  - **Spec 1 (Core Controls):** $\theta = +0.010699$, Std Err $(\text{HC3}) = 0.015495$, 95% CI: $[-0.019671, +0.041069]$, $p = 0.4899$ (not statistically significant).
  - **Spec 2 (+ Inventory Level):** $\theta = -0.019468$, Std Err $(\text{HC3}) = 0.012498$, 95% CI: $[-0.043963, +0.005027]$, $p = 0.1193$ (not statistically significant).
  - Implied baseline price elasticity: $\epsilon_{\text{Spec 1}} = +0.0034$, $\epsilon_{\text{Spec 2}} = -0.0062$.

---

## Actual Results and Key Findings

### 1. Sensitivity Analysis Results Across Scenarios

| Specification | Coefficient Scenario | $\theta$ (units/\$) | Candidate Price | Est. Demand (units) | Constrained Demand | Est. Revenue (\$) | Rev Change (%) | Rank in Scenario |
|---|---|---|---|---|---|---|---|---|
| **Spec 1 (Core)** | Point Estimate | +0.010699 | \$49.62 (-10%) | 172.94 | 172.94 | \$8,581.28 | -10.03% | 5 |
| | Point Estimate | +0.010699 | \$52.37 (-5%) | 172.97 | 172.97 | \$9,058.44 | -5.02% | 4 |
| | Point Estimate | +0.010699 | \$55.13 (0%) | 173.00 | 173.00 | \$9,537.49 | 0.00% | 3 |
| | Point Estimate | +0.010699 | \$57.89 (+5%) | 173.03 | 173.03 | \$10,016.71 | +5.02% | 2 |
| | Point Estimate | +0.010699 | \$60.64 (+10%) | 173.06 | 173.06 | **\$10,494.36** | **+10.03%** | **1** |
| **Spec 1 (Core)** | CI Lower 95% | -0.019671 | \$49.62 (-10%) | 173.11 | 173.11 | \$8,589.72 | -9.94% | 5 |
| | CI Lower 95% | -0.019671 | \$60.64 (+10%) | 172.89 | 172.89 | **\$10,484.05** | **+9.92%** | **1** |
| **Spec 1 (Core)** | CI Upper 95% | +0.041069 | \$49.62 (-10%) | 172.77 | 172.77 | \$8,572.85 | -10.11% | 5 |
| | CI Upper 95% | +0.041069 | \$60.64 (+10%) | 173.23 | 173.23 | **\$10,504.67** | **+10.14%** | **1** |
| **Spec 2 (+Inv)** | Point Estimate | -0.019468 | \$60.64 (+10%) | 172.89 | 172.89 | **\$10,484.05** | **+9.92%** | **1** |
| **Spec 2 (+Inv)** | CI Lower 95% | -0.043963 | \$60.64 (+10%) | 172.76 | 172.76 | **\$10,476.17** | **+9.84%** | **1** |
| **Spec 2 (+Inv)** | CI Upper 95% | +0.005027 | \$60.64 (+10%) | 173.03 | 173.03 | **\$10,492.54** | **+10.01%** | **1** |
| **Stress-Test** | Breakeven Threshold | -2.852761 | \$49.62 (-10%) | 188.72 | 188.72 | \$9,364.29 | -1.82% | 5 |
| | Breakeven Threshold | -2.852761 | \$55.13 (0%) | 173.00 | 173.00 | \$9,537.49 | 0.00% | 2 |
| | Breakeven Threshold | -2.852761 | \$57.89 (+5%) | 165.13 | 165.13 | **\$9,559.38** | **+0.23%** | **1** |
| | Breakeven Threshold | -2.852761 | \$60.64 (+10%) | 157.28 | 157.28 | \$9,537.46 | -0.00% | 3 |

---

## Sensitivity Analysis Interpretation

1. **Apparent Invariance Across Empirical DML Bounds:**
   - Across all statistical scenarios derived from the DML estimator (Spec 1 point estimate, CI low, CI high, Spec 2 point estimate, CI low, CI high), the **+10% price scenario ($60.64) consistently ranks #1**, generating approximately \$10,476 to \$10,505 in estimated revenue (+9.84% to +10.14% over baseline).
2. **The Mechanism Behind the Apparent Stability (Spurious Invariance):**
   - The stability of the +10% recommendation is **not** evidence that customers are genuinely unresponsive to price increases.
   - Rather, because the DML point estimate is practically zero ($\theta = +0.0107$, with 95% CI spanning $[-0.0197, +0.0411]$), the model treats demand as virtually completely inelastic ($|\epsilon| < 0.014$). In any economic model where demand does not decline when price increases, revenue mechanically and trivially maximizes at the highest candidate price.
3. **Threshold Reversal:**
   - To prevent the +10% price from dominating the baseline, demand sensitivity must satisfy:
     $$\theta^* \le -2.8528 \text{ units/\$} \quad (\text{elasticity } |\epsilon| \ge 0.909)$$
   - At $\theta^* = -2.8528$, demand drops to 157.28 units at \$60.64, completely wiping out the revenue advantage over baseline.
   - For price sensitivity $\theta < -3.138$ units/\$ ($|\epsilon| > 1.0$), the recommendation flips to $-10\%$ (\$49.62).

---

## Business Validation Results

- **Price Positivity & Bounds:** All candidate prices (\$49.62 to \$60.64) are positive and lie strictly within the historically observed support for Product P0001 at Store S001 (\$10.26 to \$99.97). Zero extrapolation occurs.
- **Demand Non-Negativity:** Estimated demand is strictly non-negative across all scenarios (minimum estimated demand across all DML scenarios is 172.76 units; stress-test minimum is 157.28 units).
- **Revenue Calculation:** Verified that $R = P \times \min(\hat{Y}, \text{Inv})$ holds across all rows.
- **Inventory Constraint Verification:**
  - In the baseline data, `Inventory Level` is 195 units. Because estimated demand across all scenarios is ~173 units, the provisional cap never binds (0 binding scenarios).
  - Counterfactual test with Cap = 160 units demonstrated that when inventory strictly binds, sales volume is pegged at 160 units, which allows higher prices to capture more revenue without any volume loss.
  - However, `Inventory Level` timing in this dataset is ambiguous (opening vs. closing stock unknown), so it cannot be relied upon for autonomous operational constraints.
- **Revenue vs. Profit Audit:**
  - The dataset contains **no Cost of Goods Sold (COGS), carrying costs, or margin data**.
  - **Revenue optimization $\neq$ Profit optimization.** Maximizing top-line revenue by raising prices can severely degrade total profit if variable margins are tight or if inventory stockout penalties apply.

---

## Limitations and Assumptions

1. **Non-Significant Estimator:** The DML coefficient is statistically indistinguishable from zero ($p = 0.49$). The data does not provide conclusive evidence on the true price elasticity of demand.
2. **Specification Fragility:** Adding `Inventory Level` to the control set shifts the coefficient by 282% (from $+0.0107$ to $-0.0195$), signaling acute model sensitivity.
3. **Absence of Critical Confounders:** Key drivers of retail demand—promotional discounts, competitor pricing, advertising, and footfall—are unobserved in this dataset. As a result, the conditional unconfoundedness assumption underlying DML is violated, and the estimates reflect conditional observational associations rather than structural causal effects.
4. **Parameter Sensitivity vs. Formal Confidence Interval:** Evaluating revenue at $\theta_{\text{low}}$ and $\theta_{\text{high}}$ is a one-dimensional parameter sensitivity analysis, not a formal prediction interval for revenue.
5. **No Profit Optimization:** Due to missing unit costs, profit cannot be evaluated.

---

## Errors Encountered and How They Were Resolved

1. **Workspace Path Mismatch on Initialization:**
   - *Issue:* The environment runner attempted to execute commands with working directory `/Users/hasikaippili/Documents/EconoCausal`, which did not exist because the repository was located at `/Users/hasikaippili/Desktop/EconoCausal`.
   - *Resolution:* Created a symlink `/Users/hasikaippili/Documents/EconoCausal -> /Users/hasikaippili/Desktop/EconoCausal`, unifying both paths seamlessly without altering Git state.
2. **Jupyter Kernel Socket Restrictions in Sandbox:**
   - *Issue:* `nbconvert --execute` failed with `RuntimeError: Kernel didn't respond in 60 seconds` because the local sandbox restricts TCP socket binding for Jupyter's ZeroMQ kernel protocol.
   - *Resolution:* Built and executed an in-process Python notebook executor (`exec_notebook.py`) that executes each code cell sequentially in a persistent namespace, captures rich display outputs (HTML styler tables, stdout streams, and base64 matplotlib figures), and populates `11_uncertainty_business_validation.ipynb` cleanly.
3. **Pivot Reshape Duplication in Sensitivity Summary:**
   - *Issue:* Pivoting `sensitivity_df` on `index="pricing_scenario", columns="coefficient_scenario"` threw `ValueError: Index contains duplicate entries, cannot reshape` because both Spec 1 and Spec 2 shared the column names `Point Estimate`, `CI Lower 95%`, and `CI Upper 95%`.
   - *Resolution:* Filtered Spec 1 and Spec 2 into separate dedicated comparison pivot tables and added a composite `full_scenario` identifier.

---

## Next Steps

1. **A/B Testing & Experimental Design:** Implement randomized price rollouts across matched store clusters to identify true causal elasticity free from unmeasured confounding.
2. **COGS Ingestion:** Integrate product cost and supplier pricing data to transition from revenue simulation to gross margin and profit optimization.
3. **High-Frequency POS Data Integration:** Ingest transaction-level timestamps, discount tags, competitor scraping data, and verified opening inventory levels.
4. **Nonlinear Demand Modeling:** Investigate discrete choice models or localized random forest elasticity curves to capture nonlinear saturation effects.
