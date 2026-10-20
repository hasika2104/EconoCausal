
# Day 9: Double Machine Learning Estimation

**Date:** 20 October 2026  

## Objective
Implement a first Double Machine Learning (DML) estimator to examine the relationship between retail price and units sold.

## Tasks Completed
- Loaded the prepared retail dataset.
- Checked data quality and price variation by product-store combination.
- Defined Price as the treatment and Units Sold as the outcome.
- Selected observed product, store, category, region, inventory, and time controls.
- Implemented cross-fitting with machine-learning nuisance models.
- Calculated the residualized price coefficient and confidence interval.
- Visualized the residualized price-demand relationship.

## Results
- Rows used: 73100
- Product-store combinations with price variation:  100
- DML coefficient: -0.018961
- 95% confidence interval:  [-0.043456, 0.005534]

## Limitations
The estimate is based on observational data. DML does not eliminate unmeasured confounding. Promotions, competitor prices, holidays, costs, and other demand factors are not available in the current dataset. Inventory timing and the validity of the selected controls also require further investigation.

## Next Steps
- Validate the estimator and its assumptions.
- Examine robustness to different control sets and model settings.
- Investigate uncertainty and the reliability of price-effect estimates.
