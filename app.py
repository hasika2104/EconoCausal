"""
EconoCausal — Integrated Interactive Decision-Support Dashboard
==============================================================
A comprehensive decision-support system synthesizing empirical retail demand estimation,
Double Machine Learning (DML) causal inference, predictive model benchmarks,
18-specification robustness testing, inventory constraints, and dynamic pricing simulations.

Author: Data Analyst Intern at Infotact Solutions
Repository: https://github.com/hasika2104/EconoCausal
Version: Day 20 Production Integration
"""

from pathlib import Path
import json
import sys
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import joblib

# Ensure local imports work
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from src.business_validation import validate_business_rules
except ImportError:
    validate_business_rules = None

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EconoCausal — Retail Pricing & Demand Decision Engine",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply custom lightweight green business styling
st.markdown(
    """
    <style>
    /* Global accents */
    :root {
        --primary-green: #2e7d32;
        --secondary-green: #388e3c;
        --light-green-bg: #f1f8e9;
        --border-green: #c8e6c9;
        --dark-green: #1b5e20;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 60%, #43a047 100%);
        padding: 24px 28px;
        border-radius: 10px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.06);
    }
    .main-header h1 {
        color: #ffffff !important;
        margin: 0;
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: #e8f5e9 !important;
        margin: 6px 0 0 0;
        font-size: 1.05rem;
    }
    
    /* KPI Card styling */
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #c8e6c9;
        border-left: 5px solid #2e7d32;
        padding: 14px 18px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }
    .kpi-title {
        color: #555555;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .kpi-value {
        color: #1b5e20;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
    }
    .kpi-sub {
        color: #777777;
        font-size: 0.8rem;
        margin-top: 4px;
    }
    
    /* Section callout cards */
    .info-box {
        background-color: #f1f8e9;
        border-left: 4px solid #388e3c;
        padding: 14px 18px;
        border-radius: 6px;
        margin: 14px 0;
        color: #1b5e20;
    }
    .warning-box {
        background-color: #fff8e1;
        border-left: 4px solid #f57f17;
        padding: 14px 18px;
        border-radius: 6px;
        margin: 14px 0;
        color: #b78103;
    }
    .danger-box {
        background-color: #ffebee;
        border-left: 4px solid #c62828;
        padding: 14px 18px;
        border-radius: 6px;
        margin: 14px 0;
        color: #b71c1c;
    }
    
    /* Pill tags */
    .pill {
        display: inline-block;
        padding: 3px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 12px;
        margin-right: 6px;
        margin-bottom: 4px;
    }
    .pill-green { background-color: #e8f5e9; color: #1b5e20; border: 1px solid #a5d6a7; }
    .pill-amber { background-color: #fff8e1; color: #b78103; border: 1px solid #ffe082; }
    .pill-red { background-color: #ffebee; color: #b71c1c; border: 1px solid #ef9a9a; }
    .pill-gray { background-color: #f5f5f5; color: #424242; border: 1px solid #e0e0e0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 2. File Paths and Data Loading Functions
# -----------------------------------------------------------------------------
DATA_RAW_PATH = BASE_DIR / "data" / "retail_store_inventory-selected-columns.csv"
DATA_CLEANED_PATH = BASE_DIR / "data" / "processed" / "retail_inventory_cleaned.csv"
DATA_DML_PREP_PATH = BASE_DIR / "data" / "processed" / "dml_preparation.csv"
DML_RESULTS_PATH = BASE_DIR / "data" / "processed" / "dml_validated_results.json"
SIM_RESULTS_PATH = BASE_DIR / "data" / "processed" / "pricing_simulator_results.json"
BASELINE_MODEL_PATH = BASE_DIR / "models" / "baseline_demand_model.joblib"
MODEL_PERF_PATH = BASE_DIR / "reports" / "day16_model_performance.csv"
FEATURE_ANALYSIS_PATH = BASE_DIR / "reports" / "day16_feature_analysis.csv"
ROBUSTNESS_PATH = BASE_DIR / "reports" / "day15_robustness_results.csv"
SENSITIVITY_PATH = BASE_DIR / "reports" / "day13_sensitivity_results.csv"
PRICING_SCENARIOS_PATH = BASE_DIR / "reports" / "day17_pricing_scenarios.csv"


@st.cache_data(show_spinner=False)
def load_raw_data():
    """Load raw observational retail inventory dataset."""
    if not DATA_RAW_PATH.exists():
        return None
    return pd.read_csv(DATA_RAW_PATH)


@st.cache_data(show_spinner=False)
def load_retail_data():
    """Load cleaned retail inventory dataset."""
    if not DATA_CLEANED_PATH.exists():
        return None
    df = pd.read_csv(DATA_CLEANED_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


@st.cache_data(show_spinner=False)
def load_dml_prep_data():
    """Load DML preparation dataset."""
    if not DATA_DML_PREP_PATH.exists():
        return None
    df = pd.read_csv(DATA_DML_PREP_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    return df


@st.cache_data(show_spinner=False)
def load_dml_results():
    """Load validated Double Machine Learning JSON results."""
    if not DML_RESULTS_PATH.exists():
        return None
    with open(DML_RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_simulator_results():
    """Load benchmark simulator JSON results."""
    if not SIM_RESULTS_PATH.exists():
        return None
    with open(SIM_RESULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_resource(show_spinner=False)
def load_baseline_model():
    """Load serialized RandomForest baseline demand model pipeline."""
    if not BASELINE_MODEL_PATH.exists():
        return None
    try:
        return joblib.load(BASELINE_MODEL_PATH)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_model_performance():
    """Load Day 16 predictive model performance benchmarks."""
    if not MODEL_PERF_PATH.exists():
        return None
    return pd.read_csv(MODEL_PERF_PATH)


@st.cache_data(show_spinner=False)
def load_feature_analysis():
    """Load Day 16 feature diagnostic importance table."""
    if not FEATURE_ANALYSIS_PATH.exists():
        return None
    return pd.read_csv(FEATURE_ANALYSIS_PATH)


@st.cache_data(show_spinner=False)
def load_robustness_results():
    """Load Day 15 sensitivity and robustness analysis table."""
    if not ROBUSTNESS_PATH.exists():
        return None
    return pd.read_csv(ROBUSTNESS_PATH)


@st.cache_data(show_spinner=False)
def load_sensitivity_results():
    """Load Day 13 stress testing and breakeven elasticity table."""
    if not SENSITIVITY_PATH.exists():
        return None
    return pd.read_csv(SENSITIVITY_PATH)


@st.cache_data(show_spinner=False)
def load_pricing_scenarios():
    """Load Day 17 multi-product constrained pricing scenarios table."""
    if not PRICING_SCENARIOS_PATH.exists():
        return None
    return pd.read_csv(PRICING_SCENARIOS_PATH)


# Load all data assets
df_raw = load_raw_data()
df_retail = load_retail_data()
df_dml_prep = load_dml_prep_data()
dml_results = load_dml_results()
sim_results = load_simulator_results()
baseline_model = load_baseline_model()
df_model_perf = load_model_performance()
df_features = load_feature_analysis()
df_robustness = load_robustness_results()
df_sensitivity = load_sensitivity_results()
df_scenarios = load_pricing_scenarios()

# -----------------------------------------------------------------------------
# 3. Sidebar Navigation & Global Filters
# -----------------------------------------------------------------------------
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 6px 0 14px 0;">
        <span style="font-size: 2.2rem;">📊</span>
        <h2 style="margin: 0; color: #1b5e20; font-size: 1.35rem; font-weight: 700;">EconoCausal</h2>
        <span style="font-size: 0.78rem; color: #555;">Causal Demand & Pricing System</span>
    </div>
    """,
    unsafe_allow_html=True,
)

sections = [
    "📌 1. Project Overview",
    "📊 2. Dataset Overview",
    "🔍 3. Exploratory Data Analysis",
    "🧹 4. Data Preprocessing",
    "🎯 5. Demand Prediction",
    "🔬 6. Causal Effect Estimation",
    "🛡️ 7. DML Validation and Robustness",
    "📈 8. Model Performance",
    "🎛️ 9. Dynamic Pricing Simulator",
    "💡 10. Pricing Recommendations",
    "⚠️ 11. Business Insights and Limitations",
]

selected_section = st.sidebar.radio("Navigation", sections, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Global Data Filters")
st.sidebar.caption("Applies to Retail Overview & EDA tabs")

# Setup filters based on real dataset
if df_retail is not None:
    all_categories = sorted(df_retail["Category"].dropna().unique().tolist())
    all_stores = sorted(df_retail["Store ID"].dropna().unique().tolist())
    all_products = sorted(df_retail["Product ID"].dropna().unique().tolist())
    all_regions = sorted(df_retail["Region"].dropna().unique().tolist())

    selected_categories = st.sidebar.multiselect(
        "Product Category",
        options=all_categories,
        default=all_categories,
        help="Filter transactions by retail department",
    )

    selected_stores = st.sidebar.multiselect(
        "Store ID",
        options=all_stores,
        default=all_stores,
        help="Filter transactions by retail store facility",
    )

    selected_regions = st.sidebar.multiselect(
        "Region",
        options=all_regions,
        default=all_regions,
        help="Filter transactions by market territory",
    )

    min_date = df_retail["Date"].min().date()
    max_date = df_retail["Date"].max().date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="Select calendar observation window",
    )

    # Filter df_retail for EDA
    if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
        start_d, end_d = date_range
    else:
        start_d, end_d = min_date, max_date

    filtered_df = df_retail[
        (df_retail["Category"].isin(selected_categories if selected_categories else all_categories))
        & (df_retail["Store ID"].isin(selected_stores if selected_stores else all_stores))
        & (df_retail["Region"].isin(selected_regions if selected_regions else all_regions))
        & (df_retail["Date"].dt.date >= start_d)
        & (df_retail["Date"].dt.date <= end_d)
    ]
else:
    filtered_df = None

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="font-size: 0.75rem; color: #777;">
        <b>Infotact Solutions Internship</b><br>
        Framework: Double Machine Learning (DML)<br>
        Status: Day 20 Production Integrated
    </div>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# SECTION 1: PROJECT OVERVIEW
# =============================================================================
if selected_section == "📌 1. Project Overview":
    st.markdown(
        """
        <div class="main-header">
            <h1>EconoCausal: Causal Demand Estimation & Dynamic Pricing</h1>
            <p>An enterprise-grade econometric and machine learning decision-support framework</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("Business Problem Statement")
        st.markdown(
            r"""
            In modern retail management, pricing decisions are frequently automated using machine learning 
            models optimized strictly for predictive accuracy ($\mathbb{E}[Y \mid P, X]$). However, standard 
            predictive algorithms conflate observational associations with true causal price sensitivity:
            
            * **The Predictive Optimization Trap:** Historical prices are confounded by brand prestige, store tiers, 
              seasonal promotional schedules, and stocking policies. Supervised models often assign near-zero weight 
              to price while latching onto post-treatment inventory colliders.
            * **Over-Discounting Risk:** Lowering prices under the naive belief that volume will surge causes 
              catastrophic revenue and margin collapse if underlying demand is price-inelastic.
            * **Naive Price Hike Risk:** Raising prices because high-end products sell well in affluent stores 
              risks unobserved customer defection and brand damage.
            * **Revenue vs. Profit Disconnect:** Optimizing gross revenue ($P \cdot Q$) without wholesale procurement 
              cost accounting data ($c$) can inadvertently maximize top-line sales while diluting operating margin.
            """
        )

        st.subheader("Core Research Pillars")
        st.markdown(
            r"""
            1. **Observational Data Audit:** Standardize multi-store, multi-product transactions across 731 consecutive days.
            2. **Supervised Demand Benchmarking:** Evaluate Random Forest, HistGradientBoosting, and Ridge regression models.
            3. **Double Machine Learning (DML) Causal Isolation:** Deploy Robinson's semiparametric DML with 3-fold cross-fitting and HC3 standard errors.
            4. **Multi-Specification Robustness:** Execute 18 sensitivity checks across alternative nuisance models, controls, categories, and calendar periods.
            5. **Constrained Decision Support:** Simulate candidate price changes ($\pm 5\%, \pm 10\%$) under hard physical inventory caps and uncertainty intervals.
            """
        )

    with col2:
        st.subheader("End-to-End System Pipeline")
        st.markdown(
            """
            ```mermaid
            flowchart TD
                A["1. Observational Retail Logs (73,100 records)"] --> B["2. Preprocessing & Temporal Feature Extraction"]
                B --> C["3. Baseline Demand Model (Random Forest Pipeline)"]
                B --> D["4. Causal Identification (Robinson PLM & DML)"]
                C --> E["5. Predictive Evaluation (Inventory Dominance)"]
                D --> F["6. Treatment Effect (θ = +0.0107, Inelastic)"]
                F --> G["7. 18-Specification Robustness & Breakeven Checks"]
                G --> H["8. Constrained Simulator (Inventory Capping)"]
                H --> I["9. Governance Matrix (Reject Cuts / Micro-pilots)"]
            ```
            """
        )

        st.markdown(
            """
            <div class="info-box">
                <b>Tech Stack & Libraries:</b><br>
                • <b>Runtime:</b> Python 3.13, Streamlit<br>
                • <b>Data & Modeling:</b> Pandas, NumPy, Scikit-Learn, Statsmodels, SciPy, Joblib<br>
                • <b>Visual Analytics:</b> Plotly Graph Objects & Express<br>
                • <b>Causal Methods:</b> Double Machine Learning (DML), HC3 Robust Covariance, Cross-Fitting
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.subheader("System Artifacts & Component Verification Status")
    
    # Check status of all 11 core components
    artifacts = [
        ("Raw Observational Data", DATA_RAW_PATH, df_raw is not None, "73,100 records, 10 columns"),
        ("Cleaned Retail Dataset", DATA_CLEANED_PATH, df_retail is not None, "73,100 records, 14 columns"),
        ("DML Preparation Data", DATA_DML_PREP_PATH, df_dml_prep is not None, "73,100 records, 100 pairs"),
        ("DML Validated Results (JSON)", DML_RESULTS_PATH, dml_results is not None, "Spec 1 & Spec 2 verified"),
        ("Pricing Simulator Results (JSON)", SIM_RESULTS_PATH, sim_results is not None, "Baseline benchmark P0001"),
        ("Baseline Demand Model (Joblib)", BASELINE_MODEL_PATH, baseline_model is not None, "522 MB Scikit-learn Pipeline"),
        ("Holdout Model Performance", MODEL_PERF_PATH, df_model_perf is not None, "4 models benchmarked"),
        ("Feature Permutation Analysis", FEATURE_ANALYSIS_PATH, df_features is not None, "9 feature diagnostics"),
        ("18-Specification Robustness", ROBUSTNESS_PATH, df_robustness is not None, "18 sensitivity checks"),
        ("Breakeven Stress Testing", SENSITIVITY_PATH, df_sensitivity is not None, "Elastic threshold analysis"),
        ("Multi-Product Pricing Scenarios", PRICING_SCENARIOS_PATH, df_scenarios is not None, "30 discrete evaluations"),
    ]

    art_cols = st.columns(3)
    for idx, (name, path, is_ok, desc) in enumerate(artifacts):
        col = art_cols[idx % 3]
        pill = '<span class="pill pill-green">LOADED</span>' if is_ok else '<span class="pill pill-amber">PENDING</span>'
        rel_path = str(path.relative_to(BASE_DIR)) if path.is_relative_to(BASE_DIR) else str(path)
        col.markdown(
            f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px 14px; margin-bottom: 10px; background: #fafafa;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <b>{name}</b> {pill}
                </div>
                <div style="font-size: 0.78rem; color: #555; margin-top: 4px;"><code>{rel_path}</code></div>
                <div style="font-size: 0.75rem; color: #777; margin-top: 2px;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# SECTION 2: DATASET OVERVIEW
# =============================================================================
elif selected_section == "📊 2. Dataset Overview":
    st.header("📊 Dataset Overview")
    st.markdown(
        "Summary metrics and empirical distributions computed directly from the validated dataset (`retail_inventory_cleaned.csv`)."
    )

    if df_retail is None:
        st.error("Cleaned dataset not found at `data/processed/retail_inventory_cleaned.csv`. Please ensure preprocessing has executed.")
    else:
        # Compute exact dataset metrics
        total_records = len(df_retail)
        num_products = df_retail["Product ID"].nunique()
        num_stores = df_retail["Store ID"].nunique()
        num_categories = df_retail["Category"].nunique()
        num_regions = df_retail["Region"].nunique()
        avg_price = df_retail["Price"].mean()
        min_price = df_retail["Price"].min()
        max_price = df_retail["Price"].max()
        total_units = df_retail["Units Sold"].sum()
        avg_units = df_retail["Units Sold"].mean()
        avg_inventory = df_retail["Inventory Level"].mean()
        total_revenue = df_retail["Revenue"].sum()
        date_start = df_retail["Date"].min().strftime("%Y-%m-%d")
        date_end = df_retail["Date"].max().strftime("%Y-%m-%d")

        # Top KPI row
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        with k1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Total Records</div>
                    <div class="kpi-value">{total_records:,}</div>
                    <div class="kpi-sub">0 nulls, 0 duplicates</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Products & Stores</div>
                    <div class="kpi-value">{num_products} × {num_stores}</div>
                    <div class="kpi-sub">100 product-store pairs</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Mean Unit Price</div>
                    <div class="kpi-value">${avg_price:.2f}</div>
                    <div class="kpi-sub">Range: [${min_price:.2f}, ${max_price:.2f}]</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k4:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Total Units Sold</div>
                    <div class="kpi-value">{total_units/1e6:.2f}M</div>
                    <div class="kpi-sub">Avg {avg_units:.1f} units / store-day</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k5:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Mean Stock Level</div>
                    <div class="kpi-value">{avg_inventory:.1f}</div>
                    <div class="kpi-sub">Units / product-store</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k6:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Gross Volume</div>
                    <div class="kpi-value">${total_revenue/1e6:.1f}M</div>
                    <div class="kpi-sub">731 calendar days</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        tab_cat, tab_reg, tab_raw = st.tabs(["📦 Category Breakdown", "🏬 Store Network & Regions", "📋 Raw Data Sample & Schema"])

        with tab_cat:
            cat_summary = (
                df_retail.groupby("Category")
                .agg(
                    Products=("Product ID", "nunique"),
                    Total_Units=("Units Sold", "sum"),
                    Avg_Daily_Units=("Units Sold", "mean"),
                    Avg_Price=("Price", "mean"),
                    Total_Revenue=("Revenue", "sum"),
                )
                .reset_index()
            )
            cat_summary["Revenue_Share"] = (cat_summary["Total_Revenue"] / cat_summary["Total_Revenue"].sum()) * 100

            col_c1, col_c2 = st.columns([3, 2])
            with col_c1:
                fig_cat = px.bar(
                    cat_summary,
                    x="Category",
                    y="Total_Revenue",
                    color="Total_Revenue",
                    color_continuous_scale="Greens",
                    title="Realized Gross Revenue by Merchandise Category",
                    labels={"Total_Revenue": "Gross Revenue ($)"},
                )
                fig_cat.update_layout(template="plotly_white", showlegend=False)
                st.plotly_chart(fig_cat, use_container_width=True)

            with col_c2:
                st.subheader("Category Aggregate Performance")
                st.dataframe(
                    cat_summary.style.format(
                        {
                            "Total_Units": "{:,.0f}",
                            "Avg_Daily_Units": "{:.1f}",
                            "Avg_Price": "${:.2f}",
                            "Total_Revenue": "${:,.2f}",
                            "Revenue_Share": "{:.1f}%",
                        }
                    ),
                    use_container_width=True,
                    hide_index=True,
                )

        with tab_reg:
            reg_summary = (
                df_retail.groupby(["Region", "Store ID"])
                .agg(
                    Total_Units=("Units Sold", "sum"),
                    Avg_Price=("Price", "mean"),
                    Avg_Inventory=("Inventory Level", "mean"),
                    Total_Revenue=("Revenue", "sum"),
                )
                .reset_index()
            )

            fig_reg = px.bar(
                reg_summary,
                x="Store ID",
                y="Total_Revenue",
                color="Region",
                barmode="group",
                title="Gross Revenue by Store and Market Region",
                color_discrete_sequence=["#1b5e20", "#388e3c", "#66bb6a", "#a5d6a7"],
            )
            fig_reg.update_layout(template="plotly_white")
            st.plotly_chart(fig_reg, use_container_width=True)

            st.dataframe(
                reg_summary.style.format(
                    {
                        "Total_Units": "{:,.0f}",
                        "Avg_Price": "${:.2f}",
                        "Avg_Inventory": "{:.1f}",
                        "Total_Revenue": "${:,.2f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

        with tab_raw:
            st.subheader("Cleaned Dataset First 100 Observations")
            st.dataframe(df_retail.head(100), use_container_width=True)
            st.markdown(
                f"""
                **Schema Summary:**
                - Total Rows: `{len(df_retail):,}` | Total Columns: `{len(df_retail.columns)}`
                - Columns: `{', '.join(df_retail.columns.tolist())}`
                - Observation Range: `{date_start}` to `{date_end}` ({df_retail['Date'].nunique()} unique calendar dates)
                """
            )


# =============================================================================
# SECTION 3: EXPLORATORY DATA ANALYSIS
# =============================================================================
elif selected_section == "🔍 3. Exploratory Data Analysis":
    st.header("🔍 Exploratory Data Analysis & Empirical Relationships")
    st.markdown(
        "Interactive exploratory analysis on the active filtered subset. Use sidebar filters to isolate specific categories, stores, or date ranges."
    )

    if filtered_df is None or len(filtered_df) == 0:
        st.warning("No records match the current sidebar filter configuration. Please broaden your selection.")
    else:
        st.info(
            f"Active Filter Selection: **{len(filtered_df):,}** of {len(df_retail):,} records "
            f"({len(filtered_df)/len(df_retail)*100:.1f}%) | "
            f"Date Range: **{filtered_df['Date'].min().strftime('%Y-%m-%d')}** to **{filtered_df['Date'].max().strftime('%Y-%m-%d')}**"
        )

        tab_dist, tab_bivar, tab_ts = st.tabs(["📊 Distributions", "🔬 Bivariate & Observational Elasticity", "📈 Time-Series Trends"])

        with tab_dist:
            d1, d2, d3 = st.columns(3)
            with d1:
                fig_price = px.histogram(
                    filtered_df,
                    x="Price",
                    nbins=40,
                    marginal="box",
                    title="Unit Selling Price Distribution",
                    color_discrete_sequence=["#2e7d32"],
                )
                fig_price.update_layout(template="plotly_white", xaxis_title="Price ($)", yaxis_title="Count")
                st.plotly_chart(fig_price, use_container_width=True)

            with d2:
                fig_units = px.histogram(
                    filtered_df,
                    x="Units Sold",
                    nbins=40,
                    marginal="box",
                    title="Daily Units Sold Distribution",
                    color_discrete_sequence=["#388e3c"],
                )
                fig_units.update_layout(template="plotly_white", xaxis_title="Units Sold", yaxis_title="Count")
                st.plotly_chart(fig_units, use_container_width=True)

            with d3:
                fig_inv = px.histogram(
                    filtered_df,
                    x="Inventory Level",
                    nbins=40,
                    marginal="box",
                    title="Daily Stock Level Distribution",
                    color_discrete_sequence=["#43a047"],
                )
                fig_inv.update_layout(template="plotly_white", xaxis_title="Inventory Level", yaxis_title="Count")
                st.plotly_chart(fig_inv, use_container_width=True)

        with tab_bivar:
            col_b1, col_b2 = st.columns(2)
            sample_n = min(2500, len(filtered_df))
            sample_df = filtered_df.sample(n=sample_n, random_state=42)

            with col_b1:
                fig_scat_p = px.scatter(
                    sample_df,
                    x="Price",
                    y="Units Sold",
                    trendline="ols",
                    title=f"Price vs. Units Sold (Observational Scatter, n={sample_n:,})",
                    opacity=0.4,
                    color_discrete_sequence=["#2e7d32"],
                )
                fig_scat_p.update_layout(template="plotly_white", xaxis_title="Price ($)", yaxis_title="Units Sold")
                st.plotly_chart(fig_scat_p, use_container_width=True)
                st.caption(
                    "Note the flat/slightly positive regression slope. In naive observational data, higher prices "
                    "correlate with high-volume stores and premium items, obscuring true demand elasticity."
                )

            with col_b2:
                fig_scat_inv = px.scatter(
                    sample_df,
                    x="Inventory Level",
                    y="Units Sold",
                    trendline="ols",
                    title=f"Inventory Level vs. Units Sold (Capacity Reflection, n={sample_n:,})",
                    opacity=0.4,
                    color_discrete_sequence=["#1b5e20"],
                )
                fig_scat_inv.update_layout(template="plotly_white", xaxis_title="Inventory Level", yaxis_title="Units Sold")
                st.plotly_chart(fig_scat_inv, use_container_width=True)
                st.caption(
                    "High correlation between inventory and sales reflects retail stocking policies. "
                    "Conditioning on inventory in causal regressions risks collider / post-treatment bias."
                )

        with tab_ts:
            monthly_trend = (
                filtered_df.set_index("Date")
                .resample("ME")
                .agg(
                    Total_Units=("Units Sold", "sum"),
                    Total_Revenue=("Revenue", "sum"),
                    Avg_Price=("Price", "mean"),
                )
                .reset_index()
            )

            fig_ts = go.Figure()
            fig_ts.add_trace(
                go.Scatter(
                    x=monthly_trend["Date"],
                    y=monthly_trend["Total_Units"],
                    name="Total Units Sold",
                    mode="lines+markers",
                    line=dict(color="#2e7d32", width=3),
                )
            )
            fig_ts.update_layout(
                title="Monthly Aggregated Sales Velocity Across 2-Year Horizon",
                template="plotly_white",
                xaxis_title="Calendar Month",
                yaxis_title="Monthly Volume (Units)",
            )
            st.plotly_chart(fig_ts, use_container_width=True)


# =============================================================================
# SECTION 4: DATA PREPROCESSING
# =============================================================================
elif selected_section == "🧹 4. Data Preprocessing":
    st.header("🧹 Data Preprocessing & Validation Pipeline")
    st.markdown(
        """
        Auditing the raw observational data, temporal transformations, missing-value verifications,
        and common support checks required prior to model training and causal estimation.
        """
    )

    t_prep1, t_prep2, t_prep3 = st.tabs(
        [
            "📋 Raw vs. Cleaned Dataset Comparison",
            "🔍 Missing Values & Outlier Audit",
            "🔄 Common Support & Overlap Check",
        ]
    )

    with t_prep1:
        st.subheader("Data Transformation Lifecycle")
        st.markdown(
            r"""
            1. **Raw Ingestion:** Ingested `retail_store_inventory-selected-columns.csv` (10 raw transactional attributes).
            2. **Temporal Feature Extraction:** Converted `Date` to ISO datetime; extracted `Year`, `Month`, and `DayOfWeek`.
            3. **Target & Revenue Construction:** Formulated realized dollar volume $\text{Revenue} = \text{Price} \times \text{Units Sold}$.
            4. **Cleaned Artifact Serialization:** Saved validated tabular structure to `data/processed/retail_inventory_cleaned.csv`.
            5. **DML Conditioning Subset:** Generated `data/processed/dml_preparation.csv` with confirmed non-zero prices.
            """
        )

        comparison_data = [
            {
                "Dataset Stage": "Raw Selected Columns",
                "File Path": "data/retail_store_inventory-selected-columns.csv",
                "Rows": len(df_raw) if df_raw is not None else "Pending",
                "Columns": len(df_raw.columns) if df_raw is not None else "Pending",
                "Key Features Added": "None (Raw attributes)",
                "Integrity Status": "Validated (0 nulls, 0 duplicates)",
            },
            {
                "Dataset Stage": "Cleaned Retail Inventory",
                "File Path": "data/processed/retail_inventory_cleaned.csv",
                "Rows": len(df_retail) if df_retail is not None else "Pending",
                "Columns": len(df_retail.columns) if df_retail is not None else "Pending",
                "Key Features Added": "Year, Month, DayOfWeek, Revenue",
                "Integrity Status": "Standardized (Datetime parsed)",
            },
            {
                "Dataset Stage": "DML Preparation Dataset",
                "File Path": "data/processed/dml_preparation.csv",
                "Rows": len(df_dml_prep) if df_dml_prep is not None else "Pending",
                "Columns": len(df_dml_prep.columns) if df_dml_prep is not None else "Pending",
                "Key Features Added": "Strict price positivity check (P > 0)",
                "Integrity Status": "100 product-store pairs verified",
            },
        ]
        st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

        if df_raw is not None and df_retail is not None:
            c_r1, c_r2 = st.columns(2)
            with c_r1:
                st.caption("**Raw Dataset Schema (Sample):**")
                st.dataframe(df_raw.head(5), use_container_width=True)
            with c_r2:
                st.caption("**Cleaned Dataset Schema (Sample with Engineered Features):**")
                st.dataframe(df_retail.head(5), use_container_width=True)

    with t_prep2:
        st.subheader("Data Completeness & Range Audits")
        if df_retail is not None:
            null_counts = df_retail.isnull().sum()
            dup_count = df_retail.duplicated().sum()

            k_null1, k_null2, k_null3 = st.columns(3)
            with k_null1:
                st.metric("Total Missing Values", f"{null_counts.sum()}")
            with k_null2:
                st.metric("Duplicate Rows", f"{dup_count}")
            with k_null3:
                st.metric("Negative Values Count", f"{(df_retail[['Price', 'Units Sold', 'Inventory Level']] < 0).sum().sum()}")

            st.markdown("#### Descriptive Percentile Distribution")
            desc_df = df_retail[["Price", "Units Sold", "Inventory Level", "Demand Forecast", "Revenue"]].describe(
                percentiles=[0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
            ).T.reset_index().rename(columns={"index": "Variable"})
            st.dataframe(
                desc_df.style.format(
                    {
                        "mean": "{:.2f}",
                        "std": "{:.2f}",
                        "min": "{:.2f}",
                        "1%": "{:.2f}",
                        "5%": "{:.2f}",
                        "25%": "{:.2f}",
                        "50%": "{:.2f}",
                        "75%": "{:.2f}",
                        "95%": "{:.2f}",
                        "99%": "{:.2f}",
                        "max": "{:.2f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    with t_prep3:
        st.subheader("Common Support & Product-Store Pair Balance")
        st.markdown(
            """
            In observational causal analysis, the **Common Support** (positivity) assumption requires that treatment 
            assignment (price variation) overlaps across all confounder strata (stores and products).
            """
        )
        if df_retail is not None:
            pair_summary = (
                df_retail.groupby(["Product ID", "Store ID"])
                .agg(
                    Observations=("Price", "count"),
                    Min_Price=("Price", "min"),
                    Max_Price=("Price", "max"),
                    Price_Span=("Price", lambda x: x.max() - x.min()),
                )
                .reset_index()
            )

            p_col1, p_col2 = st.columns([1, 2])
            with p_col1:
                st.markdown(
                    f"""
                    <div class="kpi-card">
                        <div class="kpi-title">Product-Store Pairs</div>
                        <div class="kpi-value">{len(pair_summary)}</div>
                        <div class="kpi-sub">20 products × 5 stores</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-title">Records per Pair</div>
                        <div class="kpi-value">{pair_summary['Observations'].iloc[0]}</div>
                        <div class="kpi-sub">Exactly 731 days each</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-title">Average Price Span</div>
                        <div class="kpi-value">${pair_summary['Price_Span'].mean():.2f}</div>
                        <div class="kpi-sub">Substantial within-pair variation</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with p_col2:
                fig_pair = px.histogram(
                    pair_summary,
                    x="Price_Span",
                    nbins=20,
                    title="Distribution of Historical Price Range Within Product-Store Pairs ($)",
                    color_discrete_sequence=["#2e7d32"],
                )
                fig_pair.update_layout(template="plotly_white", xaxis_title="Price Span ($)", yaxis_title="Pair Count")
                st.plotly_chart(fig_pair, use_container_width=True)


# =============================================================================
# SECTION 5: DEMAND PREDICTION
# =============================================================================
elif selected_section == "🎯 5. Demand Prediction":
    st.header("🎯 Baseline Demand Prediction: Supervised Regression")
    st.markdown(
        r"""
        Evaluating supervised machine learning models trained to predict daily sales ($\mathbb{E}[Y \mid P, X]$).
        Includes pipeline architecture inspection, live real-time inference, and holdout predictive metrics.
        """
    )

    t_pred1, t_pred2, t_pred3 = st.tabs(
        [
            "⚡ Live Interactive Inference Engine",
            "🏗️ Pipeline Architecture & Specifications",
            "📊 Holdout Predictive Performance",
        ]
    )

    with t_pred1:
        st.subheader("Real-Time Demand Inference Engine")
        st.markdown(
            "Select transaction parameters below to generate live daily unit sales predictions using the trained model."
        )

        if baseline_model is None:
            st.warning(
                "Serialized model `baseline_demand_model.joblib` is not loaded. "
                "(Note: The 522 MB model file is excluded from git per `.gitignore`). "
                "Displaying precomputed holdout model benchmarks below."
            )
        else:
            st.success("✅ Baseline Demand Pipeline Loaded: `RandomForestRegressor (100 trees)`")

            with st.form("inference_form"):
                f_col1, f_col2, f_col3 = st.columns(3)
                with f_col1:
                    in_prod = st.selectbox("Product ID", options=[f"P{i:04d}" for i in range(1, 21)], index=0)
                    in_cat = st.selectbox("Category", options=["Groceries", "Clothing", "Electronics", "Furniture", "Toys"], index=0)
                    in_price = st.slider("Unit Selling Price ($)", min_value=10.0, max_value=100.0, value=55.0, step=0.5)

                with f_col2:
                    in_store = st.selectbox("Store ID", options=["S001", "S002", "S003", "S004", "S005"], index=0)
                    in_reg = st.selectbox("Region", options=["North", "South", "East", "West"], index=0)
                    in_inv = st.slider("Available Inventory Level", min_value=10, max_value=500, value=200, step=5)

                with f_col3:
                    in_year = st.selectbox("Year", options=[2022, 2023, 2024], index=1)
                    in_month = st.slider("Month", min_value=1, max_value=12, value=6)
                    in_dow = st.selectbox("Day of Week", options=[0, 1, 2, 3, 4, 5, 6], format_func=lambda d: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][d], index=2)

                submit_pred = st.form_submit_button("🚀 Run Demand Inference", use_container_width=True)

            if submit_pred:
                input_df = pd.DataFrame(
                    [
                        {
                            "Price": in_price,
                            "Inventory Level": float(in_inv),
                            "Year": in_year,
                            "Month": in_month,
                            "DayOfWeek": in_dow,
                            "Category": in_cat,
                            "Region": in_reg,
                            "Product ID": in_prod,
                            "Store ID": in_store,
                        }
                    ]
                )

                try:
                    pred_val = float(baseline_model.predict(input_df)[0])
                    realized_sales = min(pred_val, float(in_inv))
                    is_binding = pred_val > in_inv
                    proj_revenue = in_price * realized_sales

                    st.markdown("---")
                    st.subheader("Model Inference Results")
                    out1, out2, out3, out4 = st.columns(4)
                    with out1:
                        st.metric("Unconstrained Demand", f"{pred_val:.1f} units")
                    with out2:
                        st.metric("Inventory Cap", f"{in_inv} units")
                    with out3:
                        st.metric("Realized Sales", f"{realized_sales:.1f} units", "Capped by Stock" if is_binding else "Sufficient Stock")
                    with out4:
                        st.metric("Estimated Gross Revenue", f"${proj_revenue:,.2f}")

                    if is_binding:
                        st.markdown(
                            f'<div class="danger-box">⚠️ <b>Inventory Stockout Warning:</b> Unconstrained predicted demand ({pred_val:.1f}) exceeds shelf inventory ({in_inv}). Realized sales are truncated at available stock.</div>',
                            unsafe_allow_html=True,
                        )
                except Exception as e:
                    st.error(f"Inference error: {str(e)}")

    with t_pred2:
        st.subheader("Pipeline Architecture: Scikit-Learn `ColumnTransformer`")
        st.markdown(
            r"""
            The baseline model was constructed in Day 5 (`03_baseline_demand_model.ipynb`) and benchmarked in Day 16:
            
            ```python
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', 'passthrough', ['Price', 'Inventory Level', 'Year', 'Month', 'DayOfWeek']),
                    ('cat', OneHotEncoder(handle_unknown='ignore'), ['Category', 'Region', 'Product ID', 'Store ID'])
                ]
            )
            pipeline = Pipeline([
                ('preprocessor', preprocessor),
                ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
            ])
            ```
            """
        )
        st.markdown(
            """
            <div class="warning-box">
                <b>Critical Causal Distinction:</b><br>
                The supervised regression model achieves an $R^2 \approx 0.32$. However, permutation feature diagnostics 
                prove that <b>over 95% of its predictive power is driven by `Inventory Level`</b>, which acts as a 
                post-treatment collider and inventory stocking proxy. Unit price exhibits near-zero predictive weight. 
                Optimizing prices using supervised predictions leads directly to the <b>Predictive Optimization Trap</b>.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with t_pred3:
        st.subheader("Holdout Predictive Regression Benchmarks")
        if df_model_perf is not None:
            st.dataframe(
                df_model_perf[
                    ["model_name", "model_type", "train_samples", "test_samples", "mae", "rmse", "r2_score", "mean_residual_bias", "notes"]
                ].style.format(
                    {"mae": "{:.2f}", "rmse": "{:.2f}", "r2_score": "{:.4f}", "mean_residual_bias": "{:.4f}"}
                ),
                use_container_width=True,
                hide_index=True,
            )


# =============================================================================
# SECTION 6: CAUSAL EFFECT ESTIMATION
# =============================================================================
elif selected_section == "🔬 6. Causal Effect Estimation":
    st.header("🔬 Causal Demand Estimation: Double Machine Learning")
    st.markdown(
        """
        To isolate the causal effect of price adjustments on unit sales from confounding store tiers, product prestige, 
        and seasonal schedules, the project deploys **Robinson's Partially Linear Double Machine Learning (DML)** 
        with multi-fold cross-fitting and heteroskedasticity-consistent (HC3) standard errors.
        """
    )

    if dml_results is None:
        st.error("DML results file `dml_validated_results.json` not found at `data/processed/dml_validated_results.json`.")
    else:
        spec1 = dml_results["spec1"]
        spec2 = dml_results["spec2"]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Primary Treatment Effect (θ)</div>
                    <div class="kpi-value">+{spec1['theta']:.4f}</div>
                    <div class="kpi-sub">Units per $1.00 price increase</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">HC3 Robust Std Error</div>
                    <div class="kpi-value">{spec1['std_err']:.4f}</div>
                    <div class="kpi-sub">Heteroskedasticity-consistent</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">95% Confidence Interval</div>
                    <div class="kpi-value">[{spec1['ci_low']:.3f}, +{spec1['ci_high']:.3f}]</div>
                    <div class="kpi-sub">Cleanly crosses zero</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col4:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">p-Value (H₀: θ = 0)</div>
                    <div class="kpi-value">{spec1['p_value']:.4f}</div>
                    <div class="kpi-sub">Statistically Insignificant (α=0.05)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.subheader("Causal Identification and Mathematical Interpretation")
        st.markdown(
            r"""
            Under Robinson's partially linear formulation:
            $$\tilde{Y} = Y - \mathbb{E}[Y \mid X], \quad \tilde{P} = P - \mathbb{E}[P \mid X]$$
            $$\tilde{Y} = \theta \tilde{P} + \varepsilon, \quad \mathbb{E}[\varepsilon \tilde{P}] = 0$$
            
            * **Treatment Variable ($P$):** Unit Selling Price (historical range: $[\$10.04, \$99.97]$).
            * **Outcome Variable ($Y$):** Daily Units Sold.
            * **Nuisance Learners:** ExtraTreesRegressor ($n=60$) with 3-fold cross-fitting to satisfy Neyman orthogonality.
            * **Control Variables ($X$):** `Product ID`, `Store ID`, `Category`, `Region`, `Year`, `Month`, `DayOfWeek`.
            * **Implied Mean Elasticity:** $\epsilon = \hat{\theta} \cdot \frac{\bar{P}}{\bar{Y}} = +0.0107 \cdot \frac{55.03}{140.23} = +0.0042 \approx 0.00$.
            
            **Economic Interpretation:**  
            Every $\$1.00$ increase in product price is estimated to shift daily unit demand by only $+0.0107$ units. 
            Because the 95% confidence interval $[-0.0197, +0.0411]$ spans zero and the $p$-value ($0.4899$) is far above 
            $\alpha = 0.05$, **we cannot reject the null hypothesis of perfectly inelastic demand ($\theta = 0$)**. 
            Consumer purchasing is structurally insensitive to observational price variation within historical pricing support.
            """
        )

        st.subheader("Model Specification Comparison: Spec 1 vs. Spec 2")
        spec_df = pd.DataFrame(
            [
                {
                    "Specification": "Spec 1 (Primary Baseline)",
                    "Controls": "Product, Store, Category, Region, Year, Month, DayOfWeek",
                    "Theta (θ)": f"{spec1['theta']:+.4f}",
                    "HC3 Std Error": f"{spec1['std_err']:.4f}",
                    "95% CI": f"[{spec1['ci_low']:.4f}, {spec1['ci_high']:.4f}]",
                    "p-Value": f"{spec1['p_value']:.4f}",
                    "Significant (α=0.05)": "No",
                    "Methodological Note": "Primary unconfounded specification. Neyman orthogonal.",
                },
                {
                    "Specification": "Spec 2 (Sensitivity Check)",
                    "Controls": "Spec 1 controls + Inventory Level",
                    "Theta (θ)": f"{spec2['theta']:+.4f}",
                    "HC3 Std Error": f"{spec2['std_err']:.4f}",
                    "95% CI": f"[{spec2['ci_low']:.4f}, {spec2['ci_high']:.4f}]",
                    "p-Value": f"{spec2['p_value']:.4f}",
                    "Significant (α=0.05)": "No",
                    "Methodological Note": "Inventory is a potential post-treatment collider; risk of collider bias.",
                },
            ]
        )
        st.dataframe(spec_df, use_container_width=True, hide_index=True)


# =============================================================================
# SECTION 7: DML VALIDATION AND ROBUSTNESS
# =============================================================================
elif selected_section == "🛡️ 7. DML Validation and Robustness":
    st.header("🛡️ DML Validation, Robustness & Economic Stress-Testing")
    st.markdown(
        """
        To confirm whether the finding of near-zero price sensitivity is robust or an artifact of model specification,
        the project conducted an exhaustive **18-specification sensitivity audit** and **breakeven elasticity stress-testing**.
        """
    )

    t_rob1, t_rob2 = st.tabs(["🌲 18-Specification Forest Plot", "⚡ Breakeven Elasticity & Stress Testing"])

    with t_rob1:
        if df_robustness is None:
            st.error("Robustness results not found at `reports/day15_robustness_results.csv`.")
        else:
            st.subheader("Interactive 18-Specification Robustness Matrix")
            st.markdown(
                "Across 18 separate specifications (alternative nuisance models, control sets, product categories, "
                "calendar years, geographic regions, and trimmed price support), **18 out of 18 specifications (100%) cross zero**."
            )

            group_options = ["All Specifications"] + sorted(df_robustness["group_type"].unique().tolist())
            selected_group = st.selectbox("Filter Specification Group", options=group_options, index=0)

            if selected_group == "All Specifications":
                df_plot = df_robustness.copy()
            else:
                df_plot = df_robustness[df_robustness["group_type"] == selected_group].copy()

            df_plot["error_minus"] = df_plot["theta_estimate"] - df_plot["ci_lower_95"]
            df_plot["error_plus"] = df_plot["ci_upper_95"] - df_plot["theta_estimate"]

            fig_forest = go.Figure()
            fig_forest.add_trace(
                go.Scatter(
                    x=df_plot["theta_estimate"],
                    y=df_plot["specification_name"],
                    mode="markers",
                    marker=dict(color="#2e7d32", size=9),
                    error_x=dict(
                        type="data",
                        symmetric=False,
                        array=df_plot["error_plus"],
                        arrayminus=df_plot["error_minus"],
                        color="#2e7d32",
                        thickness=1.8,
                        width=5,
                    ),
                    name="θ Estimate (95% CI)",
                )
            )
            # Add vertical reference line at zero
            fig_forest.add_vline(x=0, line_dash="dash", line_color="#d32f2f", annotation_text="θ = 0 (Null)")
            fig_forest.update_layout(
                title=f"Treatment Effect Estimates (θ) with 95% Confidence Intervals ({selected_group})",
                template="plotly_white",
                xaxis_title="Estimated Price Treatment Effect (θ, Units / $)",
                yaxis_title="Specification / Subgroup",
                height=max(400, len(df_plot) * 32),
            )
            st.plotly_chart(fig_forest, use_container_width=True)

            st.dataframe(
                df_plot[
                    [
                        "specification_name",
                        "group_type",
                        "sample_size",
                        "theta_estimate",
                        "std_error_hc3",
                        "ci_lower_95",
                        "ci_upper_95",
                        "p_value",
                        "statistically_significant_05",
                        "warnings_limitations",
                    ]
                ].style.format(
                    {
                        "sample_size": "{:,}",
                        "theta_estimate": "{:+.4f}",
                        "std_error_hc3": "{:.4f}",
                        "ci_lower_95": "{:.4f}",
                        "ci_upper_95": "{:.4f}",
                        "p_value": "{:.4f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    with t_rob2:
        st.subheader("Breakeven Price Elasticity Stress-Testing")
        st.markdown(
            r"""
            To test how extreme customer behavior would have to be to justify discounting prices, we compute the 
            **Critical Breakeven Threshold**:
            $$\theta_{\text{breakeven}} = \frac{\frac{\text{Rev}_0}{P_1} - Y_0}{P_1 - P_0}$$
            
            For a $10\%$ price cut ($P_1 = \$49.62$ vs $P_0 = \$55.13$), unit demand would have to expand from 
            $173.0$ to at least $188.7$ units ($\Delta Q \ge +15.7$ units) to generate the same gross revenue. 
            This implies an analytical breakeven threshold of **$\theta \le -2.8528$** ($\epsilon \le -1.118$).
            """
        )

        stress_comp = pd.DataFrame(
            [
                {"Metric Scenario": "Spec 1 Core DML Estimate", "Theta (θ)": +0.0107, "Implied Elasticity": "+0.004", "Revenue Impact of -10%": "-10.03%", "Commercial Feasibility": "Severe Revenue Destruction"},
                {"Metric Scenario": "Spec 1 95% CI Lower Bound", "Theta (θ)": -0.0197, "Implied Elasticity": "-0.008", "Revenue Impact of -10%": "-9.94%", "Commercial Feasibility": "Severe Revenue Destruction"},
                {"Metric Scenario": "Spec 2 (+Inventory) Lower Bound", "Theta (θ)": -0.0440, "Implied Elasticity": "-0.018", "Revenue Impact of -10%": "-9.87%", "Commercial Feasibility": "Severe Revenue Destruction"},
                {"Metric Scenario": "Breakeven Threshold Required", "Theta (θ)": -2.8528, "Implied Elasticity": "-1.118", "Revenue Impact of -10%": "0.00%", "Commercial Feasibility": "Theoretical Breakeven"},
            ]
        )
        st.dataframe(stress_comp, use_container_width=True, hide_index=True)

        fig_stress = go.Figure()
        fig_stress.add_trace(
            go.Bar(
                x=stress_comp["Metric Scenario"],
                y=stress_comp["Theta (θ)"],
                marker_color=["#2e7d32", "#66bb6a", "#81c784", "#d32f2f"],
                text=stress_comp["Theta (θ)"],
                textposition="auto",
            )
        )
        fig_stress.update_layout(
            title="Comparison of Empirical DML Estimates vs. Elastic Breakeven Threshold (θ)",
            template="plotly_white",
            yaxis_title="Price Treatment Effect (θ)",
        )
        st.plotly_chart(fig_stress, use_container_width=True)

        st.markdown(
            r"""
            <div class="danger-box">
                <b>Conclusion from Stress-Testing:</b><br>
                The empirical price sensitivity (θ̂ = +0.0107) is <b>two orders of magnitude away</b> from 
                the elastic threshold (θ = -2.8528) needed to offset price cuts. 
                Even at the most pessimistic bound of our 95% confidence intervals, retail demand remains virtually unaffected 
                by price changes. <b>Price discounting is empirically irrational in this catalog</b>.
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# SECTION 8: MODEL PERFORMANCE
# =============================================================================
elif selected_section == "📈 8. Model Performance":
    st.header("📈 Predictive Model Benchmarks vs. Causal Distinctions")
    st.markdown(
        "Supervised regression demand models evaluated on a chronological holdout split (58,480 train / 14,620 test records). "
        "This section highlights why predictive accuracy does not imply causal decision validity."
    )

    if df_model_perf is None:
        st.error("Model performance benchmarks not found at `reports/day16_model_performance.csv`.")
    else:
        # Display Model Performance Metrics Table
        st.subheader("Holdout Predictive Regression Benchmarks")
        st.dataframe(
            df_model_perf[
                ["model_name", "model_type", "train_samples", "test_samples", "mae", "rmse", "r2_score", "mean_residual_bias", "notes"]
            ].style.format(
                {"mae": "{:.2f}", "rmse": "{:.2f}", "r2_score": "{:.4f}", "mean_residual_bias": "{:.4f}"}
            ),
            use_container_width=True,
            hide_index=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            fig_r2 = px.bar(
                df_model_perf,
                x="model_name",
                y="r2_score",
                color="r2_score",
                title="Holdout Out-of-Sample R² Score",
                color_continuous_scale="Greens",
            )
            fig_r2.update_layout(template="plotly_white", xaxis_title="Model", yaxis_title="Test R²", showlegend=False)
            st.plotly_chart(fig_r2, use_container_width=True)

        with c2:
            fig_rmse = px.bar(
                df_model_perf,
                x="model_name",
                y="rmse",
                color="rmse",
                title="Holdout Root Mean Squared Error (RMSE)",
                color_continuous_scale="Greens_r",
            )
            fig_rmse.update_layout(template="plotly_white", xaxis_title="Model", yaxis_title="Test RMSE (Units)", showlegend=False)
            st.plotly_chart(fig_rmse, use_container_width=True)

        st.markdown("---")
        st.subheader("Feature Diagnostics: Permutation Importance vs. Predictive Weight")

        if df_features is not None:
            st.dataframe(
                df_features[["feature", "feature_type", "rf_mdi_importance", "rf_perm_importance_mean", "predictive_rank", "causal_role_and_distinction"]].style.format(
                    {"rf_mdi_importance": "{:.2%}", "rf_perm_importance_mean": "{:.4f}"}
                ),
                use_container_width=True,
                hide_index=True,
            )

            fig_perm = px.bar(
                df_features.sort_values(by="rf_perm_importance_mean", ascending=True),
                x="rf_perm_importance_mean",
                y="feature",
                orientation="h",
                title="Permutation Importance Drop in Test R² (Random Forest)",
                color="rf_perm_importance_mean",
                color_continuous_scale="Greens",
            )
            fig_perm.update_layout(template="plotly_white", xaxis_title="Mean Test R² Score Drop", yaxis_title="Feature")
            st.plotly_chart(fig_perm, use_container_width=True)

        st.markdown(
            """
            <div class="danger-box">
                <b>The Supervised Machine Learning Trap in Dynamic Pricing:</b><br>
                Supervised models optimize for correlation: <code>E[Y | Price, Inventory, Store]</code>. 
                Because stocking managers order inventory proportionally to anticipated sales, <b>Inventory Level</b> 
                exhibits massive predictive importance (0.712 R² drop). Meanwhile, <b>Price</b> exhibits near-zero 
                predictive importance (0.0029). 
                If an algorithm relies on predictive accuracy alone, it will conclude that cutting prices has zero effect 
                or that stocking more items magically causes sales to rise. DML is essential to break this circular confounding.
            </div>
            """,
            unsafe_allow_html=True,
        )


# =============================================================================
# SECTION 9: DYNAMIC PRICING SIMULATOR
# =============================================================================
elif selected_section == "🎛️ 9. Dynamic Pricing Simulator":
    st.header("🎛️ Dynamic Pricing Simulator & Scenario Explorer")
    st.markdown(
        """
        Evaluate candidate price changes under empirical Double Machine Learning elasticity parameters. 
        Simulations strictly enforce physical inventory constraints and statistical uncertainty bounds.
        """
    )

    tab_discrete, tab_whatif = st.tabs(["📋 Multi-Product Discrete Scenarios", "🎛️ Continuous What-If Simulator"])

    with tab_discrete:
        if df_scenarios is None:
            st.error("Precomputed scenarios not found at `reports/day17_pricing_scenarios.csv`.")
        else:
            case_options = sorted(df_scenarios["case_type"].unique().tolist())
            sel_case = st.radio("Select Case Study Subset", options=case_options, horizontal=True)

            sub_scen = df_scenarios[df_scenarios["case_type"] == sel_case]

            if sel_case == "Category Specific":
                cat_choices = sorted(sub_scen["category"].unique().tolist())
                sel_cat = st.selectbox("Filter Category", options=cat_choices)
                view_scen = sub_scen[sub_scen["category"] == sel_cat]
            else:
                view_scen = sub_scen

            st.dataframe(
                view_scen[
                    [
                        "category",
                        "product_id",
                        "store_id",
                        "scenario",
                        "candidate_price",
                        "baseline_price",
                        "baseline_units",
                        "estimated_demand",
                        "available_inventory",
                        "realized_sales",
                        "inventory_binding",
                        "estimated_revenue",
                        "revenue_diff_dollars",
                        "revenue_diff_pct",
                        "risk_rating",
                        "managerial_action",
                    ]
                ].style.format(
                    {
                        "candidate_price": "${:.2f}",
                        "baseline_price": "${:.2f}",
                        "baseline_units": "{:.1f}",
                        "estimated_demand": "{:.2f}",
                        "available_inventory": "{:.1f}",
                        "realized_sales": "{:.2f}",
                        "estimated_revenue": "${:,.2f}",
                        "revenue_diff_dollars": "${:+,.2f}",
                        "revenue_diff_pct": "{:+.2f}%",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

            # Plot revenue comparison
            fig_scen = px.bar(
                view_scen,
                x="scenario",
                y="estimated_revenue",
                color="revenue_diff_pct",
                color_continuous_scale="RdYlGn",
                title=f"Projected Gross Revenue Across Scenarios ({view_scen['product_id'].iloc[0]} at {view_scen['store_id'].iloc[0]})",
                text="estimated_revenue",
            )
            fig_scen.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
            fig_scen.update_layout(template="plotly_white", yaxis_title="Gross Revenue ($)", xaxis_title="Pricing Scenario")
            st.plotly_chart(fig_scen, use_container_width=True)

    with tab_whatif:
        st.subheader("Interactive Single-Product What-If Simulator")
        st.markdown(
            "Test custom price adjustments on Product `P0001` (Store `S001`) with real-time causal bounds and inventory constraints."
        )

        base_p = 55.13
        base_units = 173.0
        base_inv = 195.0
        base_rev = base_p * base_units
        theta_core = 0.0107
        theta_ci_low = -0.0197
        theta_ci_high = 0.0411

        c_w1, c_w2 = st.columns([1, 2])
        with c_w1:
            custom_pct = st.slider("Price Adjustment (%)", min_value=-20.0, max_value=20.0, value=0.0, step=1.0)
            custom_inv = st.number_input("Available Inventory Cap", min_value=50.0, max_value=500.0, value=base_inv, step=10.0)

        cand_price = round(base_p * (1.0 + custom_pct / 100.0), 2)
        delta_p = cand_price - base_p
        custom_est_demand = max(0.0, base_units + theta_core * delta_p)
        custom_demand_low = max(0.0, base_units + theta_ci_low * delta_p)
        custom_demand_high = max(0.0, base_units + theta_ci_high * delta_p)

        custom_realized = min(custom_est_demand, custom_inv)
        is_binding = custom_est_demand > custom_inv
        custom_revenue = cand_price * custom_realized
        delta_rev = custom_revenue - base_rev
        delta_rev_pct = (delta_rev / base_rev) * 100.0 if base_rev > 0 else 0.0

        with c_w2:
            r1, r2, r3 = st.columns(3)
            with r1:
                st.metric("Candidate Price", f"${cand_price:.2f}", f"{custom_pct:+.1f}%")
            with r2:
                st.metric("Estimated Demand", f"{custom_est_demand:.2f} units", f"{custom_est_demand - base_units:+.2f}")
            with r3:
                st.metric("Realized Sales", f"{custom_realized:.2f} units", "Stock Capped" if is_binding else "Non-binding")

            r4, r5, r6 = st.columns(3)
            with r4:
                st.metric("Projected Revenue", f"${custom_revenue:,.2f}", f"${delta_rev:+,.2f}")
            with r5:
                st.metric("Revenue Impact", f"{delta_rev_pct:+.2f}%")
            with r6:
                st.metric("Demand 95% CI", f"[{custom_demand_low:.1f}, {custom_demand_high:.1f}]")

        if custom_pct < 0:
            st.markdown(
                f'<div class="danger-box">🚨 <b>Price Reduction Alert:</b> A {custom_pct:.1f}% discount reduces revenue by ${abs(delta_rev):,.2f} ({delta_rev_pct:.2f}%). Demand expands by only {custom_est_demand - base_units:+.2f} units, failing to compensate for lower price.</div>',
                unsafe_allow_html=True,
            )
        elif custom_pct > 0:
            st.markdown(
                f'<div class="warning-box">⚠️ <b>Micro-Pilot Advisory:</b> A {custom_pct:.1f}% price hike models ${delta_rev:+,.2f} revenue gain. However, because DML θ is statistically insignificant (p=0.49) and COGS is unobserved, restrict to a controlled A/B micro-pilot.</div>',
                unsafe_allow_html=True,
            )


# =============================================================================
# SECTION 10: PRICING RECOMMENDATIONS
# =============================================================================
elif selected_section == "💡 10. Pricing Recommendations":
    st.header("💡 Pricing Recommendations & Executive Governance Matrix")
    st.markdown(
        "Structured pricing policies derived from the Improved Pricing Decision Engine (Day 17). "
        "Recommendations translate empirical inelasticity and inventory realities into defensible business rules."
    )

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(
            """
            <div class="kpi-card" style="border-left-color: #c62828;">
                <div class="kpi-title" style="color: #c62828;">Policy 1: Reject Price Cuts</div>
                <div class="kpi-value" style="color: #c62828; font-size: 1.4rem;">High Commercial Risk</div>
                <div class="kpi-sub">
                    Because demand is structurally inelastic (θ ≈ 0), price cuts of -5% or -10% cause immediate 
                    top-line revenue destruction without volume compensation.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            """
            <div class="kpi-card" style="border-left-color: #2e7d32;">
                <div class="kpi-title" style="color: #2e7d32;">Policy 2: Status Quo Baseline</div>
                <div class="kpi-value" style="color: #2e7d32; font-size: 1.4rem;">Recommended Default</div>
                <div class="kpi-sub">
                    Maintains operationally stable volume, verified stocking continuity, and predictable revenue 
                    across all product categories.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p3:
        st.markdown(
            """
            <div class="kpi-card" style="border-left-color: #f57f17;">
                <div class="kpi-title" style="color: #f57f17;">Policy 3: Controlled Micro-Pilots</div>
                <div class="kpi-value" style="color: #f57f17; font-size: 1.4rem;">Restricted Rollout</div>
                <div class="kpi-sub">
                    Price hikes (+5%) model positive revenue on paper, but DML θ is statistically insignificant (p=0.49). 
                    Deploy only via small-scale ±2% store pilots.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Executive Decision Governance Matrix")
    st.markdown(
        r"""
        | Action Category | Target Scenario | Demand Response | Revenue Impact | Risk Rating | Managerial Decision | Implementation Protocol |
        | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
        | **Price Reduction** | $-10\\%$ to $-5\\%$ | Near Zero ($\Delta Q \le 0.1$) | **$-5.02\\%$ to $-10.03\\%$** | **High** | **Strictly Reject.** Inelastic volume causes direct cash loss. | Enforce system block on markdown promotions without external funding. |
        | **Status Quo** | Baseline ($0\\%$) | Benchmark | Benchmark | **Low** | **Maintain.** Approved operational policy. | Retain current base price; re-evaluate quarterly. |
        | **Price Increase** | $+5\\%$ to $+10\\%$ | Near Zero ($\Delta Q \le 0.1$) | **$+5.02\\%$ to $+10.03\\%$** | **Moderate-High** | **Controlled Micro-Pilot.** Do not deploy catalog-wide without wholesale cost data. | Run randomized 4-week trial on 2 matched stores at $+2\%$ to test demand elasticity. |
        """
    )

    st.markdown("---")
    st.subheader("Operational Category Manager Checklist")
    st.markdown(
        r"""
        Before adjusting retail shelf prices for any product category:
        1. [ ] **Verify Historical Common Support:** Ensure candidate price is within historical $[\$10.04, \$99.97]$ bounds.
        2. [ ] **Confirm Opening Shelf Stock:** Verify start-of-day inventory exceeds projected unconstrained demand.
        3. [ ] **Audit Wholesale Procurement Cost:** Determine unit margin ($P - c$) to avoid selling at a loss.
        4. [ ] **Check Competitor Price Parity:** Audit local territory retail competitors to avoid substitution shifts.
        5. [ ] **Establish Matched Control Stores:** Designate 2 unadjusted control stores to isolate true treatment lift.
        6. [ ] **Set Automated Rollback Criteria:** Revert price immediately if sales volume drops by $> 5\%$ in week 1.
        """
    )


# =============================================================================
# SECTION 11: BUSINESS INSIGHTS AND LIMITATIONS
# =============================================================================
elif selected_section == "⚠️ 11. Business Insights and Limitations":
    st.header("⚠️ Business Insights, Validation & Project Limitations")
    st.markdown(
        """
        A rigorous data science and econometric project must explicitly delineate what the data and models 
        can and cannot establish. The following analytical constraints must be considered prior to commercial deployment.
        """
    )

    t_lim1, t_lim2, t_lim3, t_lim4 = st.tabs(
        [
            "✅ Business Rule Validation Audit",
            "💰 The Missing Procurement Cost Problem",
            "❓ Unobserved Confounding & Identification",
            "🚦 Commercial Readiness Scorecard",
        ]
    )

    with t_lim1:
        st.subheader("Business Rules & Statistical Boundary Validation")
        if df_sensitivity is not None and validate_business_rules is not None:
            audit = validate_business_rules(df_sensitivity)
            b1, b2, b3 = st.columns(3)
            with b1:
                st.metric("Price Positivity Audit", "PASSED" if audit["all_prices_positive"] else "FAILED")
                st.caption(f"Min: ${audit['min_candidate_price']:.2f}, Max: ${audit['max_candidate_price']:.2f}")
            with b2:
                st.metric("Demand Non-Negativity", "PASSED" if audit["all_demand_non_negative"] else "FAILED")
                st.caption(f"Min Demand: {audit['min_estimated_demand']:.1f} units")
            with b3:
                st.metric("Revenue Calculation Audit", "PASSED" if audit["revenue_calculation_correct"] else "FAILED")
                st.caption("P * min(Demand, Inventory) verified")

            st.markdown(
                r"""
                - **Inventory Capping Integrity:** Verified that realized sales respect physical shelf stock: Sales = min(D_hat, I).
                - **Extrapolation Bounds:** Verified that all candidate prices reside within empirical historical support ($10.04 to $99.97.
                - **Recommendation Stability:** Verified that optimal policy ranking remains identical across core DML point estimates and 95% confidence intervals.
                """
            )
        else:
            st.info("Validation module loaded from `src/business_validation.py`.")

    with t_lim2:
        st.subheader("Revenue vs. Profit & The Missing Cost Problem")
        st.markdown(
            r"""
            An exhaustive audit of `retail_inventory_cleaned.csv` confirms that **Wholesale Procurement Unit Cost (COGS) is absent**.
            
            * **Theoretical Divergence:**  
              A commercial firm maximizes gross operating profit:
              $$\Pi(P) = (P - c) \cdot Q(P) - F$$
              First-order conditions demonstrate that profit is maximized at a higher price and lower volume than revenue:
              $$\frac{d\Pi}{dP} = \frac{d\text{Revenue}}{dP} - c \frac{dQ}{dP}$$
            * **Practical Hazard:** Recommending price adjustments solely based on projected gross revenue ($P \cdot Q$) 
              risks inadvertently selling high volumes of margin-dilutive or negative-margin goods.
            """
        )

    with t_lim3:
        st.subheader("Possible Unobserved Confounding Variables")
        st.markdown(
            r"""
            While Double Machine Learning residualizes observed confounders (`Product ID`, `Store ID`, `Category`, `Region`, `Date`), 
            the identification of causal effects rests on the **Conditional Independence Assumption (CIA)**:
            $$\mathbb{E}[\varepsilon \mid P, X] = 0$$
            
            Key omitted variables not captured in the enterprise database include:
            * **Marketing & Promotional Campaigns:** Digital ads, coupon flyers, and end-cap displays that co-occur with price promotions.
            * **Competitor Pricing & Nearby Retailers:** Pricing actions by competing retail chains in the same trade area.
            * **In-Store Foot Traffic:** Footfall counts, weather shocks, and local community events influencing store foot traffic.
            * **Product Substitution / Cross-Price Elasticities:** Price changes in one SKU shifting volume to adjacent substitute items.
            """
        )

    with t_lim4:
        st.subheader("Commercial Readiness Scorecard")
        readiness_data = [
            {"Pillar": "1. Data Cleaning & Integrity", "Readiness": "🟢 Complete", "Rating": "Production-Ready", "Assessment": "Zero nulls, zero duplicates, clean temporal indexing across 731 days."},
            {"Pillar": "2. Supervised Demand Modeling", "Readiness": "🟢 Complete", "Rating": "Production-Ready", "Assessment": "Evaluated Random Forest, HistGradientBoosting, and Ridge regression models."},
            {"Pillar": "3. Causal DML Formulation", "Readiness": "🟢 Complete", "Rating": "Production-Ready", "Assessment": "Neyman-orthogonal Double Machine Learning with HC3 standard errors."},
            {"Pillar": "4. Robustness & Sensitivity", "Readiness": "🟢 Complete", "Rating": "Production-Ready", "Assessment": "18 specifications evaluated; zero-crossing confirmed; breakeven stress-tested."},
            {"Pillar": "5. Decision Support & Dashboard", "Readiness": "🟢 Complete", "Rating": "Production-Ready", "Assessment": "Interactive Streamlit app with scenario testing and inventory capping."},
            {"Pillar": "6. Automated Live Price Execution", "Readiness": "🔴 Restricted", "Rating": "Pilot Guardrails Only", "Assessment": "Requires wholesale cost data (COGS) and randomized A/B trial validation before unassisted deployment."},
        ]
        st.dataframe(pd.DataFrame(readiness_data), use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #888; font-size: 0.8rem; padding: 12px 0;">
        EconoCausal Decision-Support Dashboard • Day 20 Production Integration • Infotact Solutions Internship • 2026
    </div>
    """,
    unsafe_allow_html=True,
)
