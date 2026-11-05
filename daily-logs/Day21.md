# Day 21 — Product-Level Analysis and AI-Driven Pricing Recommendations

**Date:** 05 November 2026  
**Internship Role:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal — AI-Integrated Causal Demand Estimation and Dynamic Pricing  
**Repository:** `hasika2104/EconoCausal`  

---

## 1. Objective

The objective of Day 21 is to design, implement, and integrate a **Product-Level Pricing Analysis and AI-Driven Pricing Recommendation Engine** into the EconoCausal platform.

While earlier milestones (Days 6–15) established portfolio-level Double Machine Learning (DML) causal effects and Day 20 integrated the core dashboard, enterprise retail execution requires granular, SKU-by-SKU decisions. Day 21 bridges econometric rigor with practical retail operations by evaluating all 20 catalog products across 5 merchandise categories (100 discrete product-category operating segments), incorporating supervised baseline demand forecasts, physical inventory constraints, estimation uncertainty, and multi-scenario revenue impacts to generate transparent, auditable business recommendations.

---

## 2. Tasks Completed

### 2.1 Project Inspection & Reuse of Validated Outputs
- Audited existing project structure, notebooks (`01`–`14`), reports (`day13_`–`day20_`), and models (`baseline_demand_model.joblib`).
- Reused validated DML results from `data/processed/dml_validated_results.json` (Specification 1: $\theta = +0.0107$, $p = 0.490$) and category-specific robustness estimates from `reports/day15_robustness_results.csv` (Clothing $\theta = -0.0220$, Electronics $\theta = -0.0005$, Furniture $\theta = -0.0158$, Groceries $\theta = +0.0432$, Toys $\theta = +0.0021$).
- Preserved existing project functionality and avoided redundant model retraining.

### 2.2 Granular Product-Level Pricing Analysis
- Analyzed all 20 products ($P0001$–$P0020$) across 5 merchandise categories (100 operational segments) over 73,100 store-day observations.
- Characterized historical price corridors ($[\$10.00, \$100.00]$), sales velocity ($130.8$ to $146.1$ units/day), and inventory buffer ratios ($1.90\times$ to $2.13\times$).
- Segmented the catalog into three demand velocity tiers:
  - **High Demand Tier ($\ge 138.0$ units/day, 35 segments)**
  - **Moderate Demand Tier ($134.0 - 138.0$ units/day, 33 segments)**
  - **Low Demand Tier ($\le 134.0$ units/day, 32 segments)**
- Audited inventory constraints, finding that 27 segments experience elevated binding frequency ($\ge 0.75\%$) or tight inventory buffers ($< 1.95\times$), capping peak sales.
- Evaluated product-level OLS regressions with HC3 robust standard errors, confirming that no product exhibits statistically significant price sensitivity after Bonferroni correction for multiple testing ($\alpha = 0.05 / 20 = 0.0025$).

### 2.3 AI-Driven Pricing Recommendation Engine
- Formulated an uncertainty-aware recommendation module applying five explicit business strategies:
  1. **Review inventory before changing the price (27 segments):** Triggered when inventory binding rate $\ge 0.75\%$ or buffer ratio $< 1.95\times$. Physical stock shortages limit realized volume, overriding price adjustments.
  2. **Collect more data before making a recommendation (28 segments):** Triggered by severe parameter noise ($p > 0.85$ in Electronics & Toys), where observational data cannot determine true elasticity direction. Recommends randomized A/B trials.
  3. **Consider a price increase (10 segments):** Triggered by high demand velocity ($\ge 138.0$ units/day), healthy inventory buffer ($\ge 1.98\times$), and inelastic demand. Suggests a conservative $+5\%$ micro-pilot within historical support.
  4. **Consider a price decrease (13 segments):** Triggered by low demand velocity ($\le 134.0$ units/day) and excess inventory buffer ($\ge 2.02\times$). Focuses on inventory turn, explicitly warning that price cuts alone reduce revenue without promotional merchandising.
  5. **Maintain the current price (22 segments):** Triggered by balanced velocity ($134-138$ units), adequate inventory, and unconfirmed price sensitivity ($p > 0.05$). Maintains operational stability.
- Evaluated five discrete price scenarios ($-10\%$, $-5\%$, $0\%$, $+5\%$, $+10\%$) with physical inventory capping ($\text{Sales} = \min(D, I)$) and non-negativity enforcement.
- Maintained strict analytical separation between top-line revenue ($P \times \text{Sales}$) and operating profit ($\Pi = (P - c) \cdot \text{Sales} - F$), highlighting the absence of wholesale procurement unit cost (COGS).

### 2.4 Explanations & Uncertainty Reporting
- Generated natural-language business explanations for every SKU recommendation.
- Provided explicit confidence ratings, standard errors, 95% confidence intervals, and $p$-values.
- Documented inventory considerations and physical shelf stock constraints for each product.

### 2.5 Dashboard Integration (`app.py`)
- Updated the Streamlit dashboard with a new dedicated section: **🎯 12. Product-Level AI Pricing Recommendations**.
- Implemented interactive product and category multi-select filters, summary KPI metric cards, recommendation distribution charts, product comparison tables, scenario impact visualizations, and individual SKU deep-dive cards.
- Preserved the clean light layout with subtle green business accents (`#1b5e20`, `#2e7d32`, `#f1f8e9`).

### 2.6 Automated Testing & Validation (`test_dashboard.py`)
- Expanded automated testing suite to validate Day 21 outputs:
  - File existence and schema validation for `day21_product_pricing_analysis.csv` and `day21_ai_pricing_recommendations.csv`.
  - Math consistency checks: Revenue $= P \times \text{Sales}$; expected revenue change $= 0$ when suggested price equals current price.
  - Verification that all 5 recommendation strategies are represented without hardcoded fallbacks.
  - AppTest smoke tests across all 12 dashboard sections without unhandled exceptions.

---

## 3. Files Created or Modified

| File | Action | Description |
| :--- | :---: | :--- |
| `notebooks/15_product_level_pricing_analysis.ipynb` | Created | Full 9-section Jupyter notebook with exploratory analysis, causal testing, scenario simulations, and visualizations |
| `reports/day21_product_pricing_analysis.csv` | Created | 100-segment product pricing analysis table with demand tiers, DML estimates, and 5-scenario revenue evaluations |
| `reports/day21_ai_pricing_recommendations.csv` | Created | 100-segment AI pricing recommendation register with suggested prices, demand/revenue deltas, and business explanations |
| `reports/day21_business_insights.md` | Created | Comprehensive analytical report detailing econometric findings, clearance dilemmas, case studies, and missing cost realities |
| `daily-logs/Day21.md` | Created | This daily development log |
| `generate_day21_reports.py` | Created | Reproducible script generating Day 21 CSV datasets and recommendation logic |
| `build_notebook_15.py` | Created | Automated notebook compilation script executing all cells and persisting cell outputs |
| `app.py` | Modified | Added Section 12: Product-Level AI Pricing Recommendations with interactive filters and visual cards |
| `test_dashboard.py` | Modified | Updated test suite to validate Day 21 datasets and execute smoke tests across all 12 sections |

---

## 4. Key Findings & Econometric Insights

1. **Empirical Inelasticity Across All Segments:** 
   Point elasticity estimates across all categories range from $-0.0220$ to $+0.0432$ units per $\$1.00$. All 95% confidence intervals cleanly span zero ($p > 0.20$), indicating that observational demand is statistically indistinguishable from perfectly inelastic demand within historical bounds ($[\$10.00, \$100.00]$).
2. **The Inventory Binding Reality:**
   In $27\%$ of catalog segments, shelf availability limits sales during peak periods. In these SKUs, price changes cannot stimulate realized unit volume without upstream inventory replenishment.
3. **The Clearance Dilemma:**
   Because demand elasticity is near zero, discounting slow-moving products by $-5\%$ or $-10\%$ does not produce compensatory volume expansion in historical data. Top-line revenue falls by $-5\%$ to $-10\%$. Clearance strategies must therefore be paired with marketing and bundles rather than standalone price reductions.
4. **Revenue vs. Profit Divergence:**
   With demand inelastic, raising prices mechanically inflates top-line revenue. However, without Cost of Goods Sold (COGS), the effect on gross margin is unobserved. If margins are tight, minor demand attrition could cause net operating loss. Controlled micro-pilots and enterprise cost audits are mandatory prior to ERP deployment.

---

## 5. Next Steps
- Implement enterprise procurement cost integration when wholesale margin tables become available.
- Design randomized multi-store A/B pricing experiments for noisy categories (Electronics and Toys).
- Continue refining dynamic inventory-aware repricing guardrails.
