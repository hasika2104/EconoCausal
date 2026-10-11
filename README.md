# EconoCausal – Dynamic Pricing Using Double Machine Learning

## 1. Project Overview

EconoCausal is a data-driven dynamic-pricing decision-support system that aims to estimate how product price changes affect demand and help businesses compare pricing strategies.

The project uses Double Machine Learning (DML), where appropriate, to estimate price effects while accounting for relevant business factors. It also aims to consider profitability, inventory constraints, and uncertainty when evaluating potential prices.

## 2. Problem Statement

Retail businesses need to set product prices that balance customer demand and profitability. However, sales are also affected by factors such as inventory, promotions, competitor prices, and seasonal demand. A pricing decision based only on historical sales patterns may therefore be misleading.

This project aims to develop a pricing decision-support system that analyzes retail data, estimates price effects where the data supports causal analysis, and evaluates alternative prices under business constraints.

## 3. Project Objectives

- Understand and analyze historical retail data.
- Clean and preprocess the dataset.
- Perform exploratory data analysis (EDA).
- Build a baseline demand-prediction model.
- Investigate Double Machine Learning for estimating price effects.
- Simulate demand and profitability under alternative prices.
- Develop a dashboard for comparing pricing scenarios.
- Evaluate model performance and document limitations.

## 4. Dataset

**Dataset:** Retail Store Inventory and Demand Forecasting

**Format:** CSV

**Main columns:**
- Date
- Product ID
- Store ID
- Category
- Price
- Units Sold
- Inventory Level
- Demand Forecast
- Units Ordered
- Region

The dataset will be inspected and validated before model development. Missing business variables and data limitations will be documented.

## 5. Technology Stack

- **Programming:** Python
- **Data analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn
- **Machine learning:** Scikit-learn
- **Causal analysis:** DoubleML or EconML, subject to compatibility and data suitability
- **Dashboard:** Streamlit
- **Version control:** Git and GitHub

## 6. Planned Features

1. Retail data analysis and visualization.
2. Baseline demand prediction.
3. Price-effect estimation using DML, if supported by the data.
4. What-if pricing simulation.
5. Profit and inventory constraints.
6. Uncertainty-aware pricing recommendations.
7. Interactive dashboard.

## 7. Current Progress

- [x] Initial problem statement defined.
- [x] Initial dataset selected.
- [x] Project scope and planned features documented.
- [ ] Dataset validation and preprocessing.
- [ ] Exploratory data analysis.
- [ ] Baseline demand model.
- [ ] DML model and diagnostics.
- [ ] Pricing simulator.
- [ ] Dashboard and evaluation.
- [ ] Final report and presentation.

## 8. Important Limitations

Causal estimates depend on the quality of the data, the availability of relevant control variables, and the assumptions required for causal identification. Predictive accuracy alone does not establish that a price change causes a change in demand.

Pricing recommendations will be treated as estimates for decision support rather than guaranteed optimal prices.

## 9. Project Structure

```text
EconoCausal/
├── data/
├── notebooks/
├── src/
├── daily-logs/
├── report/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 10. Development Plan

The project will be developed incrementally, with daily progress logs, version-controlled code, testing, documentation, and final evaluation.