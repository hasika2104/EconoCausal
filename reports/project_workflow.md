# EconoCausal — End-to-End Project Workflow

**Author:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal — Causal Demand Estimation and Dynamic Pricing  
**Date:** 01 November 2026  

---

## 1. Executive Workflow Diagram

The flowchart below visualizes the complete analytical, econometric, and decision-engineering pipeline implemented across the 18 development days of the EconoCausal project:

```mermaid
flowchart TD
    subgraph Data_Engineering ["1. Data Engineering & Exploration"]
        A["Raw Transaction Logs<br/>(retail_store_inventory.csv)"] --> B["Data Cleaning & Standardization<br/>(01_data_exploration.ipynb)"]
        B --> C["Cleaned Dataset<br/>(retail_inventory_cleaned.csv<br/>73,100 rows, 20 products, 5 stores)"]
        C --> D["Exploratory Data Analysis<br/>(Correlation, Distributions, Seasonality)"]
    end

    subgraph Predictive_Modeling ["2. Predictive Modeling & Evaluation"]
        C --> E["Chronological Train/Test Split<br/>(Train: 58,480 rows | Test: 14,620 rows)"]
        E --> F["Baseline Demand Model<br/>(RandomForestRegressor n=100<br/>03_baseline_demand_model.ipynb)"]
        F --> G["Predictive Benchmarking & Diagnostics<br/>(HistGB, RidgeCV, Permutation Importance<br/>13_demand_model_performance.ipynb)"]
    end

    subgraph Causal_Inference ["3. Econometric Causal Inference"]
        C --> H["Causal Data Assessment & DAG<br/>(Confounder Isolation, Collider Identification<br/>04_causal_data_assessment.ipynb)"]
        H --> I["Causal OLS Baseline<br/>(05_causal_baseline.ipynb)"]
        I --> J["DML Data Preparation<br/>(06_dml_data_preparation.ipynb)"]
        J --> K["Double Machine Learning (DML) Estimation<br/>(Robinson's Partially Linear Model<br/>3-Fold Cross-Fitting, ExtraTrees Nuisance<br/>07_dml_estimation.ipynb)"]
        K --> L["DML Statistical Validation<br/>(Spec 1: θ = +0.0107, p = 0.490<br/>08_dml_validation.ipynb)"]
        L --> M["Model Robustness Stress-Testing<br/>(18 Specifications across Models, Controls, Subgroups<br/>12_model_robustness_analysis.ipynb)"]
    end

    subgraph Decision_Engine ["4. Pricing Decision Engine & Governance"]
        L --> N["Preliminary What-If Simulator<br/>(09_pricing_simulator.ipynb)"]
        M --> O["Improved Pricing Decision Engine<br/>(Multi-Product Scenarios, CI Bounds, Inventory Caps<br/>14_improved_pricing_decision_engine.ipynb)"]
        N --> O
        O --> P["Business & Constraint Analysis<br/>(Positivity, Timing, Missing Unit Cost Audit)"]
        P --> Q["Decision Recommendations & Governance Matrix<br/>(Reject Discounting | Status Quo | Phased Micro-Pilot)"]
    end

    subgraph Final_Integration ["5. Final Quality & Documentation"]
        G --> R["Final Integration & Quality Review<br/>(Reproducibility, Environment, Git Organization)"]
        Q --> R
        R --> S["Final Project Deliverables<br/>(final_project_report.md<br/>project_quality_checklist.md<br/>Daily Logs Days 1-18)"]
    end

    style Data_Engineering fill:#e1f5fe,stroke:#0288d1,stroke-width:2px
    style Predictive_Modeling fill:#ede7f6,stroke:#512da8,stroke-width:2px
    style Causal_Inference fill:#e8f5e9,stroke:#388e3c,stroke-width:2px
    style Decision_Engine fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style Final_Integration fill:#fce4ec,stroke:#c2185b,stroke-width:2px
```

---

## 2. Stage-by-Stage Implementation Summary

### Stage 1: Data Cleaning & Preprocessing (Days 1–4)
- **Input:** Raw retail store inventory records.
- **Actions:** Deduplication, missing value verification, date casting, temporal feature engineering (`Year`, `Month`, `DayOfWeek`).
- **Output:** Cleaned analysis dataset `data/processed/retail_inventory_cleaned.csv` ($N = 73,100$).

### Stage 2: Baseline Predictive Modeling (Days 5 & 16)
- **Input:** Cleaned transaction table.
- **Actions:** Evaluated supervised regression models (`RandomForest`, `HistGradientBoosting`, `RidgeCV`) on an $80/20$ chronological holdout test set ($N_{\text{test}} = 14,620$).
- **Findings:** Random Forest achieves holdout $R^2 = 0.3184$ (MAE $69.51$ units). Decomposed feature importance: `Inventory Level` drives predictive power (test permutation drop in $R^2 = +0.7118$), while `Price` is minimal ($+0.0029$). Identified severe regression to the mean in prediction residuals.

### Stage 3: Causal Identification & Double Machine Learning (Days 6–10, 15)
- **Input:** Preprocessed feature matrices.
- **Actions:** Formulated DAG; isolated confounding fixed effects; applied Robinson's partially linear model with $3$-fold cross-fitting and HC3 standard errors.
- **Findings:** Baseline treatment effect $\theta = +0.0107$ ($p = 0.490$, 95% CI: $[-0.0197, +0.0411]$). Verified robustness across 18 specifications (models, controls, categories, regions, years, price trimming); $0$ out of $18$ specifications are statistically significant at $\alpha = 0.05$. Demand is structurally price-inelastic.

### Stage 4: Pricing Decision Engine & Business Constraints (Days 11–13, 17)
- **Input:** Validated DML parameters and inventory levels.
- **Actions:** Evaluated candidate pricing scenarios ($\pm 5\%, \pm 10\%$), applied hard inventory caps ($\text{Sales} = \min(\hat{D}, I)$), audited the dataset for unit cost data, and derived the profit vs. revenue divergence.
- **Findings:** Inelastic demand renders discounting destructive ($-10\%$ price cuts reduce revenue by $-10.03\%$). Confirmed that unit procurement cost ($c$) is missing from the data, establishing that formal profit optimization cannot yet be performed. Recommended maintaining status-quo pricing while initiating controlled micro-pilots ($\pm 2\%$).

### Stage 5: Final Review, Quality Assurance & Documentation (Days 14 & 18)
- **Actions:** Audited repository reproducibility, verified relative paths across all 13 notebooks, validated virtual environment packages, confirmed `.gitignore` hygiene, and published comprehensive project documentation.
