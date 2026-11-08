# Day 22 — Web Application Startup Fixes, Model Pipeline Integration, and UI Modernization

**Date:** 08 November 2026  
**Internship Role:** Data Analyst Intern at Infotact Solutions  
**Project:** EconoCausal – AI-Integrated Retail Pricing & Causal Decision Support System  
**Repository:** `hasika2104/EconoCausal`  
**Branch:** `main`

---

## 1. Objective

The objective of Day 22 was to diagnose and resolve critical website startup failures, modernize the full-stack web application interface (React + Vite + Tailwind CSS with FastAPI backend), and directly integrate existing empirical data analysis, trained machine learning pipelines, and Double Machine Learning (DML) econometrics into the web platform.

All changes strictly preserve previously completed work across Days 1–21, adhere to professional SaaS design guidelines (clean white/light backgrounds, green primary accent `#15803d`, no dark/black backgrounds), and ensure seamless local execution on macOS.

---

## 2. Problems Identified & Root Causes

### 2.1 Virtual Environment Shebangs & Missing Module Resolution
* **Symptom:** Executing `./run_app.sh`, `uvicorn`, or test scripts threw `ModuleNotFoundError: No module named 'backend'` or referenced stale absolute directory paths.
* **Root Cause:** 
  1. Virtual environment binaries had hardcoded absolute interpreter paths from an earlier directory path (`/Users/hasikaippili/Desktop/EconoCausal`), failing when invoked in alternate environments without exported paths.
  2. The project root was not on `PYTHONPATH` during subprocess reloads by Uvicorn, causing child worker processes to fail when resolving `backend.main:app` and internal package modules.

### 2.2 CORS Misconfiguration Blocking Browser Requests
* **Symptom:** Browser console network errors preventing the React frontend from fetching data from the FastAPI backend.
* **Root Cause:** In `backend/main.py`, `CORSMiddleware` was configured with `allow_origins=["*"]` while `allow_credentials=True`. Modern browser security standards strictly forbid wildcard origins when credentials are included, blocking client-side HTTP requests.

### 2.3 Frontend Crash Vulnerabilities Leading to Blank Screens
* **Symptom:** The website would occasionally display a completely blank white screen without rendering UI components.
* **Root Cause:** 
  1. Multiple React page components (`DashboardOverview.jsx`, `EDAPage.jsx`, `CausalAnalysisPage.jsx`, `RecommendationsPage.jsx`) destructured nested API response objects immediately upon load without defensive null-safety checks (e.g., `const { kpis } = data; kpis.total_products`). When the backend was connecting, reloading, or returning an error dictionary, unhandled JavaScript `TypeError` exceptions unmounted the React DOM tree.
  2. An asynchronous state race condition in `PriceSimulationPage.jsx` executed simulations with stale product parameters when toggling SKUs.
  3. `Tooltip.jsx` and `LandingPage.jsx` contained dark backgrounds (`bg-slate-900`, `bg-slate-800`), conflicting with the mandated light SaaS design system.

### 2.4 Dataset Search Regex Vulnerability
* **Symptom:** Entering special characters (such as parentheses, brackets, or currency symbols) in the Dataset Explorer search filter crashed the FastAPI backend with `re.error: missing ), unterminated subpattern`.
* **Root Cause:** Pandas `Series.str.contains(search)` was invoked without `regex=False`, erroneously parsing literal search strings as regular expressions.

---

## 3. Fixes Implemented

### 3.1 Backend & Runtime Startup
* **CORS Compliance (`backend/main.py`):** Configured explicit origin whitelisting (`http://localhost:5173`, `http://127.0.0.1:5173`, `http://localhost:3000`, `http://127.0.0.1:3000`, `http://localhost:8000`, `http://127.0.0.1:8000`) and regex pattern `^https?://(localhost|127\.0\.0\.1)(:\d+)?$` with `allow_credentials=True`, completely resolving browser fetch blockage.
* **Portable Process Runner (`run_app.sh`):** Added explicit `export PYTHONPATH="$DIR:${PYTHONPATH:-}"`, automated Python binary detection (`.venv/bin/python` or system `python3`), and graceful process termination traps.
* **Safe Search Filtering (`backend/routes/dataset.py`):** Enforced `regex=False` in all `str.contains()` invocations for dataset preview and export filters.
* **Standalone Test Client (`tests/test_api_endpoints.py`):** Added automated `sys.path` bootstrapping so tests can execute from any working directory without environment configuration.

### 3.2 Machine Learning & Econometric Integration
* **Trained Pipeline Evaluation in Simulator (`backend/routes/simulation.py`):**
  - Integrated the serialized Day 5 `baseline_demand_model.joblib` pipeline (`RandomForestRegressor` with numeric and categorical encoders) into the price simulation service.
  - Generates side-by-side counterfactual predictions comparing **Supervised ML Forecasts** ($E[Y | \text{Price}, X]$) against **Double Machine Learning (DML) Causal Estimates** ($\theta = +0.0107$).
  - Clearly distinguishes empirical correlation from orthogonal causal elasticity, providing actionable managerial takeaways.
* **Feature Diagnostics Integration (`backend/routes/causal.py`):**
  - Integrated `reports/day16_feature_analysis.csv` to expose test $R^2$ permutation importance drops alongside the 18 DML robustness specifications.
  - Highlights the econometric distinction between predictive proxies (e.g., Inventory Level, permutation drop $= 0.712$) and true causal levers (Price, $\theta = +0.0107, p = 0.490$).

### 3.3 UI Modernization & Blank Screen Prevention
* **Light SaaS Visual Theme:** Removed all dark/black backgrounds (`bg-slate-900`) from `LandingPage.jsx` and `Tooltip.jsx`, replacing them with crisp white containers, subtle slate borders (`border-slate-200/90`), and green primary accents (`text-emerald-700`, `bg-emerald-50`).
* **Defensive Error & Loading Guards:**
  - Added structured fallback cards and retry actions in `DashboardOverview.jsx`, `EDAPage.jsx`, `CausalAnalysisPage.jsx`, and `RecommendationsPage.jsx` to prevent unhandled React exceptions.
* **Atomic Simulation Controls (`PriceSimulationPage.jsx`):** Refactored SKU parameter updates into an atomic parameterized function (`runSimulationWithParams`), eliminating stale state race conditions. Added the new **Model Pipeline Evaluation** panel showing Random Forest predictions vs DML causal estimates.
* **Causal Analysis Enhancements (`CausalAnalysisPage.jsx`):** Added the interactive **Predictive Importance vs Causal Policy Levers** table illustrating permutation importance against causal roles.

---

## 4. Verification & Testing Performed

1. **Frontend Production Build:**
   - Ran `npm run build` in `frontend/`. Built successfully in 2.48s without errors (all 2,183 modules transformed).
2. **Backend API End-to-End Test Suite:**
   - Ran `.venv/bin/python tests/test_api_endpoints.py`.
   - Verified 8 comprehensive test suites:
     - `test_health`: Status 200, healthy response.
     - `test_dashboard_default`: 20 products, 73,100 records, Spec 1 $\theta = +0.0107$.
     - `test_dashboard_with_filters`: Correct filtering by category and region.
     - `test_eda`: Summary statistics, correlations, histograms, seasonality.
     - `test_causal_analysis`: Spec 1, Spec 2, 18 robustness specifications, and 9 Day 16 feature diagnostics.
     - `test_simulation_spec1`: Multi-scenario matrix, profit analysis, and active `baseline_demand_model.joblib` pipeline evaluation.
     - `test_recommendations`: 100 SKU segments with strategic classifications.
     - `test_products`: Catalog retrieval.
     - `test_dataset_preview`: Paginated preview of 73,100 cleaned transaction rows.
   - Result: **All 8 API endpoint test suites PASSED with 100% success.**

---

## 5. Summary of Verified Startup Commands

To launch both tiers simultaneously:
```bash
./run_app.sh
```

Or run the tiers in separate terminals:
```bash
# Terminal 1 — FastAPI Backend (Port 8000)
export PYTHONPATH=.
.venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2 — React Vite Frontend (Port 5173)
cd frontend
npm run dev
```

* **Frontend:** http://localhost:5173
* **API Documentation:** http://127.0.0.1:8000/docs

---

## 6. Remaining Tasks

- [x] Identify and fix website startup failures.
- [x] Eliminate dark backgrounds and enforce light SaaS design system.
- [x] Connect real `baseline_demand_model.joblib` pipeline and Day 16 feature diagnostics.
- [x] Fix CORS, shebangs, and process launch commands.
- [x] Perform automated testing and build validation.
- [x] Document fixes in `daily-logs/Day-22.md`.
- [ ] Push verified changes to GitHub `main` branch.
