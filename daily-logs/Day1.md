# Day 1 — EconoCausal

Date: 11 October 2026

## Today's Objective
Understand dynamic pricing, the project problem statement, and the role of Double Machine Learning.
## Indetified Problem Statement
The problem is to develop a data-driven pricing system that estimates the effect of price changes on demand while accounting for other relevant factors, and uses those estimates to recommend suitable prices.
## Evalulating the problem and Solution
I am going to develop a system called EconoCausal Guard: a dynamic-pricing decision-support application powered by Double Machine Learning.
Its purpose is to help a business understand price effects and compare pricing decisions using historical data.
## The four main things:

## 1. Analyze historical data. 
Find patterns in prices, demand, sales and other relevant variables.
## 2. Estimate the effect of price changes. 
Apply Double Machine Learning to estimate how price affects demand under the model's assumptions.
## 3. Compare possible prices. 
Calculate estimated demand, revenue and profit for multiple candidate prices rather than blindly increasing or decreasing prices.
## 4. Recommend a suitable price.
 Consider business constraints such as unit cost, inventory, allowed price ranges and uncertainty.
The system should support human decisions initially; it does not need to change real product prices automatically.
## Work Completed
- Defined the project objective.
- Identified the difference between sales prediction and causal price-effect estimation.
- Proposed the EconoCausal Guard features.
- Reviewed the initial retail dataset option.
- Created the project folder and GitHub repository.

## Key Learnings
Dynamic pricing uses business data to support pricing decisions. Double Machine Learning can help estimate price effects while accounting for observed confounding variables, subject to appropriate assumptions.

## Challenges and Limitations
The initial dataset must be checked for repeated price observations and relevant control variables before it is used for causal estimation.

## Next Session
Set up the Python environment, load the dataset with Pandas, and inspect its columns and missing values.