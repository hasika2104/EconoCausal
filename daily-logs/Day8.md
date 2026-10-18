# Day 8 – Double Machine Learning Data Preparation

**Project:** EconoCausal – Dynamic Pricing via Double Machine Learning  
**Date:** 18 October 2026  


## Objective
Prepare the retail dataset for Double Machine Learning by defining the treatment, outcome, candidate controls, and checking price variation.

## Tasks Completed
- Loaded the cleaned retail inventory dataset.
- Defined Price as the treatment and Units Sold as the outcome.
- Inspected missing values in required columns.
- Prepared date-based features.
- Checked price variation within product-store pairs.
- Saved the prepared dataset for subsequent modeling.

## Results
- Original observations: 73100
- Retained observations: 73100
- Removed observations: 0
- Unique product-store pairs: 100
- Pairs with changing prices: 100
- Pairs with constant prices: 100
- Unique dates: 731
- Prepared dataset shape: (73100,14)


## Limitations
Price variation and observed associations do not establish causality. Potential confounders such as promotions, competitor prices, and demand shocks may be unavailable. The timing and validity of candidate controls, particularly inventory, must be assessed before causal estimation.

## Next Steps
Evaluate the DML specification, select appropriate nuisance models, and plan out-of-sample validation without interpreting observational estimates as causal effects prematurely.