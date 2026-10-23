# Day 10: DML Validation and Robustness

**Date:** 23 October 2026

## Objective
Validate the Double Machine Learning (DML) price-effect estimate from Day 9 by checking data quality, examining residual price variation, re-estimating with three-fold cross-fitting, and comparing two control specifications.

## Tasks Completed
- Loaded `data/processed/dml_preparation.csv` using a reliable project-root-based path.
- Verified all required columns, checked missing values and invalid entries.
- Examined price variation across Product ID and Store ID combinations.
- Checked residualised price and units-sold distributions and standard deviations.
- Re-estimated the DML coefficient using three-fold cross-fitting and ExtraTreesRegressor nuisance models.
- Compared two control specifications:
  - **Spec 1 (core controls):** Product ID, Store ID, Category, Region, Year, Month, DayOfWeek
  - **Spec 2 (sensitivity check):** Spec 1 + Inventory Level
- Reported actual coefficient, 95% CI, standard error, p-value, and sample size for each specification.
- Visualised residual distributions, coefficient estimates, confidence intervals, and the residualised price-demand scatter.
- Saved validated results to `data/processed/dml_validated_results.json` for downstream notebooks.

## Actual Results

| Specification | θ (DML coeff) | CI lower | CI upper | Std Err (HC3) | p-value | N |
|---|---|---|---|---|---|---|
| Spec 1 — Core controls | +0.010699 | −0.019671 | +0.041069 | 0.015495 | 0.4899 | 73,100 |
| Spec 2 — + Inventory Level | −0.019468 | −0.043963 | +0.005027 | 0.012498 | 0.1193 | 73,100 |

- Product-store combinations: 100 (all 100 with price variation)
- Price residual SD (Spec 1): 26.37
- Price residual SD (Spec 2): 26.28
- Coefficient shift Spec 1 → Spec 2: −0.030167 (282% relative change)

## Key Findings
1. **Neither specification produces a statistically significant price effect** (p > 0.10 in both).
2. The Spec 1 coefficient (+0.0107) is near zero and positive, while Spec 2 (−0.0195) matches the Day 9 sign. The reversal in sign between specifications is striking.
3. The **282% relative shift** in the coefficient when Inventory Level is added as a control confirms that results are **highly sensitive to control selection**.
4. Confidence intervals are wide and span zero in both specifications, indicating high uncertainty.
5. Residual price variation is substantial (SD ≈ 26), so the identification failure is not due to lack of treatment variation.

## Limitations and Assumptions
- HC3 standard errors are used on a pooled residual regression, not a purpose-built DML standard error formula.
- Inventory Level timing is ambiguous (may be end-of-period stock, partially affected by sales), introducing potential bad-control bias in Spec 2.
- Key variables not available: promotions, competitor prices, holidays, unit costs.
- The large coefficient shift between specifications is a warning signal — not a validation of either estimate.
- Coefficient stability does not establish causality.

## Next Steps
- Day 11: Use Spec 1 coefficient as primary estimate for a what-if pricing simulator.
- Day 12: Apply inventory constraints and produce a ranked recommendation prototype.
