# Day 17 — Improved Pricing Decision Engine

**Date:** 31 October 2026  
**Internship Role:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal — Causal Demand Estimation and Dynamic Pricing  

---

## Objective

The objective of Day 17 is to upgrade the preliminary single-product pricing simulator into an **Improved Pricing Decision Engine**. The enhanced engine evaluates candidate pricing scenarios across multiple categories, integrates validated Double Machine Learning (DML) causal treatment effects and confidence intervals, enforces hard physical business and inventory constraints, formally evaluates the gap between revenue maximization and profit optimization, and establishes an operational governance framework that protects the business from naive algorithmic price hikes.

---

## Work Performed

1. **Review of Upstream Causal Models and Baseline Simulator:**
   - Audited the validated DML results from Day 10 (`data/processed/dml_validated_results.json`) and the 18 robustness specifications from Day 15 (`reports/day15_robustness_results.csv`).
   - Reused the verified baseline values for Benchmark Product P0001 at Store S001 (Baseline Price: $\$55.13$, Baseline Units: $173.00$, Available Inventory: $195.00$ units, Baseline Daily Revenue: $\$9,537.49$).

2. **Causal Parameter Formulation and Dimensional Audit:**
   - Treatment variable ($P$): Selling price per unit in dollars ($\$$).
   - Outcome variable ($Y$): Units sold per day (count).
   - Causal Treatment Effect ($\theta$): $+0.010699$ units per $\$1.00$ price increase (HC3 SE: $0.015495$, 95% CI: $[-0.019671, +0.041069]$, $p = 0.4899$).
   - Physical Interpretation: Price adjustments within historical empirical support have near-zero structural impact on daily sales volume. We cannot reject the null hypothesis of perfectly inelastic demand ($\theta = 0$).

3. **Multi-Scenario Decision Engine Implementation:**
   - Formulated candidate price scenarios: $-10\%$, $-5\%$, Baseline ($0\%$), $+5\%$, $+10\%$.
   - Computed point estimate demand: $\hat{D}(P) = \max(0, D_0 + \theta \cdot \Delta P)$.
   - Constructed conservative (lower-bound) and optimistic (upper-bound) demand trajectories using the 95% confidence interval bounds.
   - Evaluated 30 total pricing scenarios spanning the benchmark item and representative products across all 5 retail categories (Clothing, Electronics, Furniture, Groceries, Toys).

4. **Business Constraints & Inventory Timing Enforcement:**
   - Enforced price positivity ($P > 0$) and demand non-negativity ($\hat{D} \ge 0$).
   - Enforced operational stock limits: $\text{Sales} = \min(\hat{D}, I_{\text{avail}})$.
   - Investigated the inventory measurement timing caveat: clarified that applying inventory caps requires stock to be recorded at start-of-day before trading begins ($I_t^{\text{start}}$), as capping by end-of-day stock artificially truncates demand.

5. **Revenue vs. Profit Analysis & Dataset Cost Audit:**
   - Derived the mathematical divergence between revenue maximization ($\max P \cdot Q$) and gross operating profit maximization ($\max (P - c) \cdot Q - F$).
   - Performed an exhaustive audit of `data/processed/retail_inventory_cleaned.csv`.
   - **Confirmed Critical Limitation:** Unit procurement cost ($c$) and COGS are completely absent from the dataset.
   - Explicitly documented that formal profit optimization cannot yet be performed until product cost accounting data is integrated.

6. **Deliverables Created:**
   - Executed and validated notebook: `notebooks/14_improved_pricing_decision_engine.ipynb`.
   - Scenario results dataset: `reports/day17_pricing_scenarios.csv`.
   - Executive decision summary: `reports/day17_pricing_summary.md`.
   - Daily engineering log: `daily-logs/Day17.md`.

---

## Key Results & Decision Matrix

### Benchmark Product P0001 (Store S001) Scenario Summary

| Scenario | Candidate Price | $\Delta P$ ($) | Est. Demand (Units) | 95% CI Demand Bounds | Realized Sales (Capped) | Est. Revenue ($) | Revenue $\Delta$ (%) | Risk Rating & Recommended Action |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **$-10\%$** | $\$49.62$ | $-\$5.51$ | $172.94$ | $[172.77, 173.11]$ | $172.94$ | $\$8,581.33$ | $-10.03\%$ | **High Risk:** Severe revenue collapse without volume stimulation. Reject. |
| **$-5\%$** | $\$52.37$ | $-\$2.76$ | $172.97$ | $[172.89, 173.05]$ | $172.97$ | $\$9,058.46$ | $-5.02\%$ | **High Risk:** Uncompensated margin forfeiture. Reject. |
| **Baseline (0%)** | $\$55.13$ | $\$0.00$ | $173.00$ | $[173.00, 173.00]$ | $173.00$ | $\$9,537.49$ | $0.00\%$ | **Recommended (Status Quo):** Verified operating stability. |
| **$+5\%$** | $\$57.89$ | $+\$2.76$ | $173.03$ | $[172.95, 173.11]$ | $173.03$ | $\$10,016.68$ | $+5.02\%$ | **Moderate Risk:** Positive simulated revenue, but $\theta$ is noisy. Test in pilot only. |
| **$+10\%$** | $\$60.64$ | $+\$5.51$ | $173.06$ | $[172.89, 173.23]$ | $173.06$ | $\$10,494.29$ | $+10.03\%$ | **Moderate-High Risk:** Do not deploy catalog-wide without cost data. |

---

## Managerial Insights and Governance Principles

1. **The Inelasticity Trap:**
   - When demand elasticity is near zero, discounting does not stimulate sales volume. A $-10\%$ price cut yields an immediate $-10.03\%$ loss in revenue. The decision engine rules out broad discount promotions for inelastic product lines.
2. **The Danger of Naive Top-Line Optimization:**
   - A superficial reading of the $+10\%$ price increase scenario suggests an "easy" $+10.03\%$ revenue increase ($+\$956.80$).
   - However, this projection relies on the mathematical assumption that $\theta \ge 0$. Because the true parameter could be negative ($\theta_{\text{low}} = -0.0197$) and unit costs are unobserved, an uncritical catalog-wide price hike could induce unobserved customer churn and damage customer lifetime value.
3. **Operational Policy:**
   - The decision engine recommends **maintaining baseline pricing as default**, accompanied by **controlled micro-pilots ($\pm 2\%$)** in select test stores before any wider price adjustments are considered.

---

## Artifacts and Deliverables

- `notebooks/14_improved_pricing_decision_engine.ipynb`
- `reports/day17_pricing_scenarios.csv`
- `reports/day17_pricing_summary.md`
- `daily-logs/Day17.md`
