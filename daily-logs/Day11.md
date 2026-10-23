# Day 11: What-If Pricing Simulator

**Date:** 23 October 2026

## Objective
Build a scenario-based pricing simulator using the validated Day 10 DML coefficient. For a selected baseline product-store observation, generate candidate prices at −10%, −5%, 0% (baseline), +5%, and +10% relative to the baseline price, and estimate demand and revenue for each scenario.

## Tasks Completed
- Loaded and validated the Day 10 DML results from `data/processed/dml_validated_results.json`.
- Loaded `data/processed/dml_preparation.csv` and validated the dataset.
- Selected baseline observation: **Product P0001, Store S001** — median price row for the product-store combination.
- Generated five candidate price scenarios using the DML coefficient as a local linear demand approximation.
- Estimated demand uncertainty by propagating the 95% CI endpoints through the approximation.
- Validated non-negativity of estimated units and prices for all scenarios.
- Produced a scenario comparison table and two charts (demand/revenue vs price, revenue change bar chart).
- Saved simulator outputs to `data/processed/pricing_simulator_results.json`.
- Issued warnings about coefficient sensitivity, statistical significance, and absence of unit costs.

## Actual Results

**Baseline observation (P0001, Store S001):**
- Baseline price: $55.13
- Baseline units sold: 173
- Baseline revenue: $9,537.49
- Inventory Level: 195 (timing uncertain — provisional constraint)
- Observed price range for this product-store: $10.26 – $99.97

**DML coefficient used (Spec 1):**  θ = +0.010699 (p = 0.4899, NOT statistically significant)  
**95% CI:** [−0.019671, +0.041069]

| Scenario | Price ($) | Est. Units | Est. Revenue ($) | Rev Change ($) | Rev Change (%) | Extrapolates |
|---|---|---|---|---|---|---|
| −10% | 49.62 | 172.9 | 8,580.81 | −956.68 | −10.03% | False |
| −5% | 52.37 | 173.0 | 9,059.07 | −478.42 | −5.02% | False |
| 0% (baseline) | 55.13 | 173.0 | 9,537.49 | 0.00 | 0.00% | False |
| +5% | 57.89 | 173.0 | 10,016.07 | +478.58 | +5.02% | False |
| +10% | 60.64 | 173.1 | 10,494.82 | +957.33 | +10.04% | False |

*All candidate prices lie within the observed price range — no extrapolation.*

**Highest estimated revenue:** +10% scenario at $10,494.82. This reflects the near-zero DML coefficient — because θ ≈ 0, estimated demand barely changes with price, so the revenue curve is almost entirely driven by the price increase itself.

## Key Findings
1. Because the DML coefficient is very close to zero (+0.0107) and not statistically significant, estimated demand is nearly flat across scenarios.
2. Revenue increases with price simply because the price increase is not offset by a meaningful demand reduction under this point estimate.
3. The wide 95% CI means demand at any given scenario spans a large range; the true revenue effect is highly uncertain.
4. All five candidate prices fall within the historically observed range — no extrapolation warning.
5. Coefficient sensitivity (Spec 1 vs Spec 2: 282% change in θ) means simulator results must be interpreted with extreme caution.

## Limitations and Assumptions
- The simulator uses a **local linear approximation** only — not a trained demand model.
- The DML coefficient is NOT statistically significant (p ≈ 0.49). Demand estimates could be in any direction.
- Revenue ≠ Profit. Unit cost data is unavailable.
- Missing confounders: promotions, competitor prices, holidays.
- A different control specification (Spec 2) gives a negative coefficient — results could reverse.
- The highest-revenue scenario is not proven optimal.

## Next Steps
- Day 12: Apply inventory constraints and produce ranked pricing recommendations as a research prototype.
