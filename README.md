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
- [x] Dataset validation and preprocessing (Days 1–4).
- [x] Exploratory data analysis and temporal auditing (Days 1–4).
- [x] Baseline demand prediction models (Days 5, 16).
- [x] Causal DAG formulation & confounder isolation (Days 6–7).
- [x] Double Machine Learning (DML) model and HC3 diagnostics (Days 8–10).
- [x] Causal uncertainty propagation & sensitivity analysis (Days 11–13).
- [x] 18-specification model robustness analysis (Days 14–15).
- [x] Multi-model holdout benchmarking & feature diagnostics (Day 16).
- [x] Improved constrained pricing decision engine (Day 17).
- [x] Project integration, reproducibility & final report (Day 18).
- [x] Interactive Pricing Analytics Dashboard (`app.py`) (Day 19).

## 8. Important Limitations

Causal estimates depend on the quality of the data, the availability of relevant control variables, and the assumptions required for causal identification. Predictive accuracy alone does not establish that a price change causes a change in demand.

Pricing recommendations will be treated as estimates for decision support rather than guaranteed optimal prices. Furthermore, gross revenue ($P \cdot Q$) is not operating profit; wholesale procurement costs (COGS) are absent from the dataset.

## 9. Project Structure

```text
EconoCausal/
├── app.py                     # Streamlit interactive pricing analytics dashboard
├── daily-logs/                # Daily engineering logs (Day 1 to Day 19)
├── data/
│   ├── processed/             # Cleaned datasets and JSON model outputs
│   └── retail_store_inventory-selected-columns.csv
├── models/                    # Serialized baseline models (gitignored)
├── notebooks/                 # 13 chronologically sequenced Jupyter notebooks
├── reports/                   # Technical summaries, robustness audits, final report
├── src/                       # Reusable validation and business logic modules
├── requirements.txt           # Project environment dependencies
├── README.md                  # Project overview and instructions
└── .gitignore                 # Security and artifact exclusions
```

## 10. Running the Applications

### A. Professional Web Application (React + FastAPI + Tailwind CSS)

To launch the full modern web application:

```bash
# Simply run the integrated launcher:
./run_app.sh
```

Or start the backend and frontend separately:

```bash
# 1. Start FastAPI backend (Port 8000)
source .venv/bin/activate
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

# 2. In a second terminal, start React frontend (Port 5173)
cd frontend
npm run dev
```

* **Frontend URL:** [http://localhost:5173](http://localhost:5173)
* **Backend API Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### B. Legacy Streamlit Dashboard

To launch the earlier Streamlit dashboard:

```bash
source .venv/bin/activate
streamlit run app.py
```

The Streamlit dashboard runs at `http://localhost:8501`.

## 11. Development Plan

The project was developed incrementally across a 19-day research and implementation sprint, with daily progress logs, version-controlled code, rigorous testing, econometric validation, and institutional documentation.