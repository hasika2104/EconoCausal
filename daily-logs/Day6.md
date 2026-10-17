# Day 6 – Causal Data Assessment

**Project:** EconoCausal – Dynamic Pricing via Double Machine Learning  
**Date:** 15 October 2026  
**Duration:** 2 hours

## 1. Objective

To assess whether the retail inventory dataset contains sufficient price variation and relevant information for estimating the relationship between product prices and units sold using causal machine learning techniques.
## 2. Tasks Completed

1. Loaded the cleaned retail inventory dataset.
2. Converted date, price, and units sold columns to appropriate data types.
3. Examined price variation for each product-store pair.
4. Identified product-store pairs with changing and constant prices.
5. Calculated the overall correlation between price and units sold.
6. Reviewed potential confounding factors and limitations affecting causal estimation.

## 3. Results and Key Values

| Metric | Observed value |
|---|---:|
| Total product-store pairs | 100 |
| Pairs with changing prices | 100 |
| Pairs with constant prices | 0 |
## 4. Findings

The assessment examined whether prices varied over time within the same product-store combinations. Such variation is important for distinguishing price changes from persistent differences between products and stores.

The overall correlation between price and units sold was **[correlation value]**. This represents an observed statistical relationship and does not establish that changing prices causes demand to increase or decrease.

## 5. Potential Confounding Factors

The dataset contains product, store, date, price, inventory, and demand-related information. However, important factors may be unavailable, including:

- Promotions and discounts.
- Competitor prices.
- Holidays and special events.
- Unit costs and profit margins.
- Unobserved demand shocks and managerial pricing decisions.

Inventory availability may also constrain observed sales. Therefore, units sold should not automatically be treated as the same as unconstrained customer demand.

## 6. Conclusion

The Day 6 assessment established a preliminary understanding of price variation and the observed price-sales relationship. Further validation is required to determine whether the dataset supports a defensible causal estimation strategy using Double Machine Learning.

The current analysis is exploratory. Correlation and price variation alone are insufficient to establish causal effects.

## 7. Next Steps

- Establish a regression baseline for the price-sales relationship.
- Compare estimates before and after adding appropriate controls.
- Evaluate whether the available variables and price variation support credible causal identification.
- Document limitations before developing the Double Machine Learning model.