# Day 3 — Dataset Validation and EDA

Date: 14 October 2026

## Objective
Validate the retail dataset and explore price and sales patterns.

## Tasks Performed
- Checked dataset columns and data types.
- Checked missing values and duplicate rows.
- Examined prices, units sold, and inventory.
- Checked dates and product coverage.
- Investigated price variation across products.
- Created price and sales histograms.
- Created a price-versus-sales scatter plot.
- Compared sales across product categories.

## Findings
- Rows and columns: 73100
- Missing values: NON
- Duplicate rows: NON
- Date range: 2022-01-01 to 2024-01-01
- Products with changing prices: clothing,toys,groceries,electronics,furniture
- Price distribution: The histogram shows that retail prices range from approximately 10 to 100, with observations distributed almost uniformly across the price range. There are around 2,300–2,550 observations for each price interval, indicating no significant concentration of data at any particular price.
- Sales distribution:The histogram shows that units sold range from 0 to 500, with the highest number of observations occurring at lower sales volumes. As units sold increase, the number of observations gradually decreases, indicating a right-skewed distribution where lower sales quantities are more common than higher sales quantities.
- Price-versus-sales pattern: The scatter plot shows the relationship between price and units sold, with prices ranging from 10 to 100 and sales varying from 0 to 500 units. The points are widely scattered across the graph, indicating no clear relationship between price and units sold in the current dataset.

## Limitations
The dataset does not include all potentially important business variables, including unit cost, promotions, and competitor prices.

## Next Steps
Investigate repeated product-store-date observations, price variation, and suitable control variables before modeling.