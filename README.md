# 📈 EconoCausal – AI-Integrated Retail Pricing & Causal Decision Support System

> **"Make Smarter Pricing Decisions with AI and Causal Intelligence."**

[![API Status](https://img.shields.io/badge/FastAPI-v0.110.0-059669?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Frontend](https://img.shields.io/badge/React%2018-Vite%20%2B%20TailwindCSS-059669?style=flat-square&logo=react)](https://vitejs.dev)
[![Econometrics](https://img.shields.io/badge/Double%20Machine%20Learning-3--Fold%20Cross--Fitting-0284c7?style=flat-square)](https://github.com/hasika2104/EconoCausal)
[![License](https://img.shields.io/badge/License-MIT-slate?style=flat-square)](LICENSE)

EconoCausal is an enterprise-grade, full-stack decision-support platform designed to help retailers, pricing analysts, business owners, and non-technical stakeholders optimize product pricing through empirical causal econometrics (**Double Machine Learning**) rather than misleading historical correlations.

---

## 1. Executive Summary & Problem Statement

### The Predictive Trap in Traditional Retail Pricing
Standard predictive machine learning models optimize for **correlation** rather than **causation**. For example:
- A store runs weekend promotional discounts on popular products during high foot-traffic periods.
- A standard regression or tree-based model observes high sales volume whenever prices were discounted.
- The model mistakenly concludes that *lower prices drove the sales spike*, recommending continuous discounting that leads to severe margin erosion.

### The EconoCausal Solution
EconoCausal uses **Double Machine Learning (DML)** with Neyman orthogonality to isolate genuine consumer price elasticity from store location, category baselines, and calendar seasonality. It couples these causal findings with **physical shelf-inventory constraints** and **margin guardrails**, ensuring that suggested price changes never project unfulfillable sales volumes or violate business thresholds.

---

## 2. Key Platform Features

| Module | Core Capability | Business Value |
|---|---|---|
| **Landing Page** | Clean, light SaaS presentation with English & Telugu localization | Explains causal vs correlation principles to non-technical users |
| **Executive Dashboard** | Real-time KPIs (Revenue, Volume, Average Price, Causal $\theta$) | High-level visibility into multi-store retail health across 73,100 records |
| **Data Upload & Validator** | CSV and Excel (`.xlsx`, `.xls`) drag-and-drop ingestion with Data Quality Score | Auto-detects missing values, duplicates, invalid values, and maps custom schemas |
| **Sales Analytics (EDA)** | Interactive volume, category, regional, and price decile curves | Deep exploratory insights into demand stability and weekly traffic surges |
| **Causal Price Impact** | Double Machine Learning (DML Spec 1 & Spec 2) with 18 robustness checks | Statistically rigorous treatment effects ($\theta = +0.0107, p = 0.490$) with 95% CIs |
| **Price Simulator** | Interactive price sliders with physical inventory truncation | What-if testing comparing -10%, -5%, +5%, +10% scenarios under shelf limits |
| **AI Pricing Assistant** | Grounded retail analyst chatbot with suggested quick prompts | Natural language answers on revenue leaders, 5% price shocks, and dataset audits |
| **AI Recommendations** | 100-SKU rule-guarded pricing strategy table | Prescriptive SKU advice balancing turnover, margins, and historical volatility |
| **Reports Generation** | Multi-tab Excel (`.xlsx`), CSV, and printable executive PDF exports | Audit-ready documentation for executive committees and merchandising teams |
| **Help & Settings** | Bilingual FAQ, Econometric Glossary, and Demo Mode controls | Self-service educational walkthroughs and language selection |

---

## 3. Technology Stack & Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                   CLIENT TIER (React 18 + Vite)                       │
│  • Modern Tailwind CSS (Emerald / Light Theme, Zero Dark Backgrounds)  │
│  • Recharts Data Visualizations • Lucide Icons • Bilingual (EN / TE)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST (/api)
┌───────────────────────────────────▼────────────────────────────────────┐
│                  BACKEND TIER (FastAPI + Python 3)                     │
│  • Route Controllers: /dashboard, /eda, /causal, /simulate, /chat      │
│  • Ingestion & Validator: pandas, openpyxl, auto-schema mapping        │
│  • Conversational Engine: Grounded Analytics Engine + Gemini API opt.  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ In-Memory / Joblib Pipelines
┌───────────────────────────────────▼────────────────────────────────────┐
│                ANALYTICS & CAUSAL ECONOMETRICS CORE                   │
│  • Double Machine Learning (DML): ExtraTreesRegressor 3-Fold           │
│  • Robust Inference: Heteroskedasticity-Consistent (HC3) SEs          │
│  • Benchmark Dataset: 73,100 Store-Day Observations (20 SKUs)         │
│  • Trained Supervised Pipeline: baseline_demand_model.joblib          │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Local Installation & Startup Guide

### Prerequisites
- **Python 3.10+** (Python 3.11 or 3.13 recommended)
- **Node.js 18+** and **npm**

### Step 1: Clone Repository
```bash
git clone https://github.com/hasika2104/EconoCausal.git
cd EconoCausal
```

### Step 2: Set Up Python Backend Environment
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install backend dependencies
pip install -r requirements.txt
```

### Step 3: Set Up React Frontend Environment
```bash
cd frontend
npm install
cd ..
```

### Step 4: Configure Environment Variables (Optional)
```bash
cp .env.example .env
# Optional: add your GEMINI_API_KEY if desired for LLM conversational enhancement
```

### Step 5: Launch the Entire Platform
You can launch both the FastAPI backend (port 8000) and the React frontend (port 5173) with a single command:

```bash
chmod +x run_app.sh
./run_app.sh
```

Alternatively, run each tier in separate terminals:
```bash
# Terminal 1: FastAPI Backend
source .venv/bin/activate
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

# Terminal 2: React Vite Frontend
cd frontend
npm run dev
```

Open your browser at **`http://localhost:5173`** to access the live platform.

---

## 5. Automated Verification & Testing

EconoCausal includes a comprehensive automated test suite verifying all 14 core API endpoints and business logic:

```bash
# Run backend API test suite
.venv/bin/python tests/test_api_endpoints.py
```

Expected output:
```
All 14 API endpoint test suites PASSED perfectly!
```

To test the frontend production build:
```bash
cd frontend
npm run build
```

---

## 6. Dataset Schema & Ingestion Requirements

The platform is designed to ingest standard retail point-of-sale (POS) and inventory records. When uploading non-standard files, the **Column Mapping Wizard** automatically aligns custom names to standard fields:

| Canonical Field | Detected Synonyms | Purpose |
|---|---|---|
| **Product ID\*** | `sku`, `product_id`, `item_id`, `Product` | SKU identification |
| **Price\*** | `unit_price`, `selling_price`, `price` | Treatment variable for elasticity estimation |
| **Units Sold\*** | `demand`, `units_sold`, `quantity`, `sales_volume` | Outcome variable for consumer response |
| **Date** | `date`, `transaction_date`, `day` | Time-series trends and day-of-week seasonality |
| **Inventory Level** | `stock`, `inventory`, `inventory_level` | Physical supply constraint truncation |
| **Category** | `category`, `dept`, `department` | Cross-sector aggregation |
| **Region** | `region`, `market`, `store_region` | Regional demand partitioning |
| **Cost** | `cost`, `unit_cost`, `cogs` | Gross margin and unit profit calculations |

*\* Required columns for pricing simulation and causal elasticity.*

---

## 7. Causal Econometrics & Model Methodology

### Double Machine Learning (DML) Formulation
To estimate the true Average Treatment Effect (ATE) $\theta$ of price on demand without restrictive linear assumptions, EconoCausal implements a partially linear DML model:

$$Y - E[Y | W] = \theta \cdot (P - E[P | W]) + \epsilon$$

Where:
- $Y$: Units Sold (Daily Demand).
- $P$: Shelf Unit Price ($).
- $W$: Vector of observed confounders (Store ID, Product ID, Category, Region, Year, Month, Day of Week, Inventory).
- $\theta$: Causal price elasticity parameter.

### Validated Empirical Results
- **Primary Specification (Spec 1):** $\theta = +0.0107$ ($95\% \text{ CI}: [-0.0197, +0.0411], p = 0.490$).
- **Sensitivity Check (Spec 2 - with Inventory):** $\theta = -0.0195$ ($95\% \text{ CI}: [-0.0440, +0.0050], p = 0.119$).
- **Managerial Implication:** Because the confidence intervals encompass zero, daily demand is statistically inelastic within historical operating price bands ($10.26 to $99.97). Retailers can capture higher revenues through selective price increases (+3% to +5%) without triggering unit volume collapse.

---

## 8. Public Deployment Configuration

EconoCausal is pre-configured for one-click deployment to standard cloud platforms:

### Deploying to Render (`render.yaml`)
1. Fork or push your repository to GitHub.
2. In Render, select **New Blueprint Instance** and connect the repository.
3. Render automatically provisions:
   - Python Web Service running `uvicorn backend.main:app`
   - Static Web Service hosting `frontend/dist` with client-side rewrite rules.

### Deploying Frontend to Vercel (`vercel.json`)
1. Import `frontend/` into Vercel.
2. Build command: `npm run build`, Output directory: `dist`.
3. Set `VITE_API_URL` to your production FastAPI backend URL.

---

## 9. Repository Structure

```
EconoCausal/
├── backend/                  # FastAPI backend server
│   ├── main.py               # Application entrypoint & CORS configuration
│   ├── routes/               # Modular API endpoint routers
│   │   ├── dashboard.py      # KPI cards & trend aggregation
│   │   ├── eda.py            # Summary statistics & correlation
│   │   ├── causal.py         # DML results & 18-spec robustness
│   │   ├── simulation.py     # Constrained price simulator
│   │   ├── recommendations.py# 100-SKU AI advice
│   │   ├── products.py       # Catalog metadata
│   │   ├── dataset.py        # Tabular upload, audit & column mapping
│   │   ├── chat.py           # Conversational AI Pricing Assistant
│   │   └── reports.py        # Multi-tab Excel, CSV, PDF report export
│   └── services/
│       └── data_service.py   # Data caching & pipeline loader
├── frontend/                 # React 18 + Vite web client
│   ├── src/
│   │   ├── components/       # Reusable UI (Sidebar, Navbar, Footer, MetricCard)
│   │   ├── pages/            # 10 Application Modules
│   │   ├── services/api.js   # HTTP client wrapper
│   │   └── utils/            # Bilingual translations (EN/TE)
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
├── data/                     # Raw and processed datasets (73.1k records)
├── models/                   # Serialized baseline demand models (.joblib)
├── notebooks/                # Documented research & DML notebooks (Days 1–15)
├── daily-logs/               # Daily engineering and development logs
├── reports/                  # Validation logs, sensitivity plots, and exports
├── tests/                    # End-to-end API test suites
├── requirements.txt          # Python dependencies
├── run_app.sh                # Single-command runner
└── Procfile / render.yaml    # Production deployment manifests
```

---

## 10. Future Enhancements

- Multi-tenant enterprise authentication (OAuth2 / JWT).
- Real-time competitor price scrapers and automated repricing webhooks.
- Multi-product cross-price elasticity matrices (Substitutes and Complements).
- Edge deployment for retail POS checkout terminals.

---

## 11. Authors & Acknowledgments

- **Lead Analyst & Developer:** Data Analyst Intern at Infotact Solutions
- **Repository:** [https://github.com/hasika2104/EconoCausal](https://github.com/hasika2104/EconoCausal)
