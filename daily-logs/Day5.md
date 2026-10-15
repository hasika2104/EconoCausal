# Day 5 – Demand Analysis and Baseline Model

**Project:** EconoCausal – Dynamic Pricing via Double Machine Learning

## Objective
Analyze retail demand patterns and develop a baseline machine learning model to predict units sold.

## Tasks Completed
- Analyzed price and sales patterns.
- Prepared numerical and categorical model features.
- Used a chronological training/testing split.
- Trained a Random Forest regression model.
- Evaluated predictions using MAE, RMSE, and R².
- Compared model performance with a mean-prediction baseline.
- Saved the trained model.

## Results
- Training observations:58480
- Testing observations: 14621
- Random Forest MAE: 69.51
- Random Forest RMSE: 69.51
- Random Forest R²: 0.38
- Mean baseline MAE: 88.81

## Findings
 - Select model features
 - Split data into training and testing sets
 - Train a baseline regression model
 - Evaluate and save results

## Limitations
This model predicts observed units sold. Predictive performance alone does not establish the causal effect of price on demand. Further analysis is needed before using the model for pricing recommendations.

## Next Steps
Investigate whether the data and assumptions are suitable for causal effect estimation.