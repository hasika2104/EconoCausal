# Day 7 – Causal Analysis Baseline

**Project:** EconoCausal – Dynamic Pricing via Double Machine Learning

## Objective
Establish a regression baseline and investigate the sensitivity of the observed price-sales relationship to product, store, and date controls.

## Tasks Completed
- Checked price variation within product-store pairs.
- Estimated a simple regression of units sold on price.
- Estimated a regression with product, store, and date controls.
- Compared price coefficients and p-values.
- Reviewed potential confounding and inventory limitations.

## Results
- Product-store pairs: 100
- Pairs with changing prices: 100
- Simple regression price coefficient: 0.0045
- Controlled regression price coefficient: 0.7736


## Limitations
The regression results are observational associations. The available data may omit important confounders, including promotions, competitor prices, and demand shocks. The estimates should not be interpreted as causal effects without further justification.

## Next Steps
Assess whether the data supports a defensible Double Machine Learning specification and establish a suitable evaluation strategy.