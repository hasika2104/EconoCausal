"""
EconoCausal — Interactive Pricing Analytics & Demand Estimation Dashboard
========================================================================
A decision-support system presenting empirical retail demand estimation,
Double Machine Learning (DML) causal inference, predictive model benchmarks,
inventory constraints, and uncertainty-aware pricing scenario exploration.

Author: Data Analyst Intern at Infotact Solutions
Repository: https://github.com/hasika2104/EconoCausal
"""

from pathlib import Path
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EconoCausal — Retail Pricing Analytics",
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
        padding: 24px;
        border-radius: 10px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.06);
    }
    .main-header h1 {
        color: #ffffff !important;
        margin: 0;
        font-size: 2.2rem;
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
        padding: 16px 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }
    .kpi-title {
        color: #555555;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
        font-weight: 600;
    }
    .kpi-value {
        color: #1b5e20;
        font-size: 1.85rem;
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
        padding: 2px 10px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 12px;
        margin-right: 6px;
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
BASE_DIR = Path(__file__).resolve().parent
DATA_CLEANED_PATH = BASE_DIR / "data" / "processed" / "retail_inventory_cleaned.csv"
DML_RESULTS_PATH = BASE_DIR / "data" / "processed" / "dml_validated_results.json"
SIM_RESULTS_PATH = BASE_DIR / "data" / "processed" / "pricing_simulator_results.json"
MODEL_PERF_PATH = BASE_DIR / "reports" / "day16_model_performance.csv"
FEATURE_ANALYSIS_PATH = BASE_DIR / "reports" / "day16_feature_analysis.csv"
ROBUSTNESS_PATH = BASE_DIR / "reports" / "day15_robustness_results.csv"
PRICING_SCENARIOS_PATH = BASE_DIR / "reports" / "day17_pricing_scenarios.csv"


@st.cache_data(show_spinner=False)
def load_retail_data():
    """Load cleaned retail inventory dataset."""
    if not DATA_CLEANED_PATH.exists():
        return None
    df = pd.read_csv(DATA_CLEANED_PATH)
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
def load_pricing_scenarios():
    """Load Day 17 multi-product constrained pricing scenarios table."""
    if not PRICING_SCENARIOS_PATH.exists():
        return None
    return pd.read_csv(PRICING_SCENARIOS_PATH)


# Load data assets
df_retail = load_retail_data()
dml_results = load_dml_results()
sim_results = load_simulator_results()
df_model_perf = load_model_performance()
df_features = load_feature_analysis()
df_robustness = load_robustness_results()
df_scenarios = load_pricing_scenarios()

# -----------------------------------------------------------------------------
# 3. Sidebar Navigation & Global Filters
# -----------------------------------------------------------------------------
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 8px 0 16px 0;">
        <span style="font-size: 2.2rem;">📊</span>
        <h2 style="margin: 0; color: #1b5e20; font-size: 1.4rem;">EconoCausal</h2>
        <span style="font-size: 0.8rem; color: #666;">Causal Pricing & Demand Decision Engine</span>
    </div>
    """,
    unsafe_allow_html=True,
)

sections = [
    "📌 1. Project Overview",
    "📊 2. Retail Data Overview",
    "🔍 3. Exploratory Data Analysis",
    "🔬 4. Causal Analysis (DML)",
    "📈 5. Model Performance",
    "🎛️ 6. Pricing Scenario Explorer",
    "💡 7. Pricing Recommendations",
    "⚠️ 8. Project Limitations",
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
        Framework: Double Machine Learning<br>
        Version: 1.0 (Day 19 Production)
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# SECTION 1: PROJECT OVERVIEW
# -----------------------------------------------------------------------------
if selected_section == "📌 1. Project Overview":
    st.markdown(
        """
        <div class="main-header">
            <h1>EconoCausal: Retail Demand & Dynamic Pricing Engine</h1>
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

        st.subheader("Project Objectives")
        st.markdown(
            r"""
            1. **Clean & Audit Observational Data:** Standardize multi-store, multi-product transactions across 731 consecutive days.
            2. **Benchmark Predictive Demand Models:** Train and evaluate supervised regression models (Random Forest, Gradient Boosting, Ridge Regression).
            3. **Isolate Causal Price Elasticity:** Implement Robinson's semiparametric **Double Machine Learning (DML)** with 3-fold cross-fitting and HC3 standard errors.
            4. **Stress-Test Robustness:** Execute 18 specification checks across nuisance learners, control subsets, categories, and calendar periods.
            5. **Deploy Constrained Pricing Engine:** Simulate candidate price changes ($\pm 5\%, \pm 10\%$) with hard inventory caps and uncertainty bounds.
            """
        )

    with col2:
        st.subheader("System Architecture")
        st.markdown(
            """
            ```mermaid
            flowchart TD
                A["Observational Retail Data (73,100 records)"] --> B["Predictive Benchmarks (RF, HistGB, Ridge)"]
                A --> C["Causal Formulation (DAG & Robinson DML)"]
                B --> D["Feature Importance & Collider Diagnostics"]
                C --> E["Validated Treatment Effect (θ = +0.0107)"]
                E --> F["18-Spec Robustness & Sensitivity Checks"]
                F --> G["Constrained Pricing Engine (±10%, Inventory Caps)"]
                G --> H["Governance Matrix (Micro-pilots vs. Discount Rejection)"]
            ```
            """
        )

        st.markdown(
            """
            <div class="info-box">
                <b>Tech Stack:</b><br>
                • <b>Language & Runtime:</b> Python 3.13, Streamlit<br>
                • <b>Data & Modeling:</b> Pandas, NumPy, Scikit-Learn, Statsmodels, SciPy<br>
                • <b>Visual Analytics:</b> Plotly Graph Objects, Altair, Matplotlib<br>
                • <b>Econometric Methods:</b> Double Machine Learning (DML), HC3 Robust Covariance, Cross-Fitting
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.subheader("Project Pipeline & Research Workflow")
    st.markdown(
        """
        The EconoCausal framework spans an intensive 18-day research and validation roadmap:
        - **Days 1–4:** Data cleaning, temporal auditing, and baseline exploratory data analysis.
        - **Day 5:** Supervised demand modeling using Random Forest regression.
        - **Days 6–7:** Causal DAG formulation, confounder isolation, and fixed-effects OLS benchmark.
        - **Days 8–10:** Robinson's partially linear DML cross-fitting, Neyman orthogonality, and HC3 standard errors.
        - **Days 11–13:** Uncertainty propagation, Monte Carlo stress testing, and commercial decision simulation.
        - **Days 14–15:** 18-specification sensitivity and category-subsample robustness analysis.
        - **Day 16:** Chronological holdout benchmarking and permutation importance diagnostics.
        - **Day 17:** Multi-product constrained pricing decision engine and missing cost audit.
        - **Day 18:** End-to-end integration, reproducibility certification, and institutional documentation.
        - **Day 19:** Interactive decision-support dashboard implementation.
        """
    )


# -----------------------------------------------------------------------------
# SECTION 2: RETAIL DATA OVERVIEW
# -----------------------------------------------------------------------------
elif selected_section == "📊 2. Retail Data Overview":
    st.header("📊 Retail Data Overview")
    st.markdown(
        "Summary metrics and empirical distributions computed directly from the validated dataset (`retail_inventory_cleaned.csv`)."
    )

    if df_retail is None:
        st.error("Cleaned dataset not found at `data/processed/retail_inventory_cleaned.csv`. Please ensure Day 1–4 preprocessing has executed.")
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
                    <div class="kpi-title">Unique Products</div>
                    <div class="kpi-value">{num_products}</div>
                    <div class="kpi-sub">{num_categories} merchandise categories</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Retail Stores</div>
                    <div class="kpi-value">{num_stores}</div>
                    <div class="kpi-sub">{num_regions} geographic territories</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k4:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Avg Retail Price</div>
                    <div class="kpi-value">${avg_price:.2f}</div>
                    <div class="kpi-sub">Range: ${min_price:.2f} – ${max_price:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k5:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Total Units Sold</div>
                    <div class="kpi-value">{total_units/1e6:.2f}M</div>
                    <div class="kpi-sub">Daily avg: {avg_units:.1f} units</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with k6:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Avg Inventory</div>
                    <div class="kpi-value">{avg_inventory:.1f}</div>
                    <div class="kpi-sub">Total Rev: ${total_revenue/1e6:.1f}M</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")

        col_l, col_r = st.columns([1, 1])
        with col_l:
            st.subheader("Merchandise Category Breakdown")
            cat_summary = (
                df_retail.groupby("Category")
                .agg(
                    Products=("Product ID", "nunique"),
                    Avg_Price=("Price", "mean"),
                    Total_Units=("Units Sold", "sum"),
                    Total_Revenue=("Revenue", "sum"),
                    Avg_Inventory=("Inventory Level", "mean"),
                )
                .reset_index()
            )
            cat_summary["Revenue_Share_%"] = (cat_summary["Total_Revenue"] / cat_summary["Total_Revenue"].sum()) * 100
            st.dataframe(
                cat_summary.style.format(
                    {
                        "Avg_Price": "${:.2f}",
                        "Total_Units": "{:,.0f}",
                        "Total_Revenue": "${:,.2f}",
                        "Avg_Inventory": "{:.1f}",
                        "Revenue_Share_%": "{:.1f}%",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

        with col_r:
            st.subheader("Regional Store Network Breakdown")
            store_summary = (
                df_retail.groupby(["Store ID", "Region"])
                .agg(
                    Total_Days=("Date", "nunique"),
                    Total_Units=("Units Sold", "sum"),
                    Avg_Price=("Price", "mean"),
                    Total_Revenue=("Revenue", "sum"),
                )
                .reset_index()
            )
            st.dataframe(
                store_summary.style.format(
                    {
                        "Total_Days": "{:,}",
                        "Total_Units": "{:,.0f}",
                        "Avg_Price": "${:.2f}",
                        "Total_Revenue": "${:,.2f}",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

        st.subheader("Dataset Sample & Schema Verification")
        st.dataframe(df_retail.head(10), use_container_width=True, hide_index=True)


# -----------------------------------------------------------------------------
# SECTION 3: EXPLORATORY DATA ANALYSIS
# -----------------------------------------------------------------------------
elif selected_section == "🔍 3. Exploratory Data Analysis":
    st.header("🔍 Exploratory Data Analysis")
    st.markdown(
        "Interactive visualizations of price distributions, unit demand patterns, temporal trends, and stocking relationships. "
        "Use the sidebar to adjust category, store, regional, or date filters."
    )

    if filtered_df is None or len(filtered_df) == 0:
        st.warning("No records match the active filter criteria. Please broaden your selection in the sidebar.")
    else:
        st.markdown(
            f"<div class='info-box'>Showing <b>{len(filtered_df):,}</b> transactions matching active filters.</div>",
            unsafe_allow_html=True,
        )

        tab1, tab2, tab3 = st.tabs(["📊 Distributions & Elasticity", "📈 Time-Series Trends", "📦 Category & Inventory"])

        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Price Distribution")
                fig_price = px.histogram(
                    filtered_df,
                    x="Price",
                    nbins=40,
                    marginal="box",
                    title="Retail Selling Price Distribution ($)",
                    color_discrete_sequence=["#2e7d32"],
                )
                fig_price.update_layout(
                    template="plotly_white",
                    xaxis_title="Price ($)",
                    yaxis_title="Observation Count",
                    bargap=0.05,
                )
                st.plotly_chart(fig_price, use_container_width=True)

            with c2:
                st.subheader("Units Sold Distribution")
                fig_units = px.histogram(
                    filtered_df,
                    x="Units Sold",
                    nbins=40,
                    marginal="box",
                    title="Daily Units Sold Distribution",
                    color_discrete_sequence=["#1b5e20"],
                )
                fig_units.update_layout(
                    template="plotly_white",
                    xaxis_title="Units Sold",
                    yaxis_title="Observation Count",
                    bargap=0.05,
                )
                st.plotly_chart(fig_units, use_container_width=True)

            st.subheader("Observational Relationship: Price vs. Units Sold")
            st.markdown(
                r"A sample of 2,500 points with an ordinary least-squares trendline. Notice that observational "
                r"data exhibits a virtually flat, slightly positive trendline ($\Delta Y / \Delta P \approx +0.01$) "
                r"due to unobserved confounding across store tiers and product quality."
            )
            sample_scatter = filtered_df.sample(min(2500, len(filtered_df)), random_state=42)
            fig_scatter = px.scatter(
                sample_scatter,
                x="Price",
                y="Units Sold",
                color="Category",
                trendline="ols",
                title="Selling Price vs. Daily Units Sold (Observational)",
                opacity=0.6,
                color_discrete_sequence=["#2e7d32", "#388e3c", "#66bb6a", "#81c784", "#a5d6a7"],
            )
            fig_scatter.update_layout(template="plotly_white", xaxis_title="Price ($)", yaxis_title="Units Sold")
            st.plotly_chart(fig_scatter, use_container_width=True)

        with tab2:
            st.subheader("Monthly Demand and Sales Velocity Trends")
            monthly_agg = (
                filtered_df.set_index("Date")
                .resample("ME")
                .agg(
                    Total_Units=("Units Sold", "sum"),
                    Avg_Price=("Price", "mean"),
                    Total_Revenue=("Revenue", "sum"),
                )
                .reset_index()
            )

            fig_monthly = go.Figure()
            fig_monthly.add_trace(
                go.Scatter(
                    x=monthly_agg["Date"],
                    y=monthly_agg["Total_Units"],
                    mode="lines+markers",
                    name="Total Units Sold",
                    line=dict(color="#2e7d32", width=3),
                    marker=dict(size=7),
                )
            )
            fig_monthly.update_layout(
                title="Monthly Total Units Sold (2022 – 2024)",
                template="plotly_white",
                xaxis_title="Date",
                yaxis_title="Aggregate Units Sold",
                hovermode="x unified",
            )
            st.plotly_chart(fig_monthly, use_container_width=True)

            fig_rev = go.Figure()
            fig_rev.add_trace(
                go.Bar(
                    x=monthly_agg["Date"],
                    y=monthly_agg["Total_Revenue"],
                    name="Gross Revenue ($)",
                    marker_color="#81c784",
                )
            )
            fig_rev.update_layout(
                title="Monthly Gross Revenue ($)",
                template="plotly_white",
                xaxis_title="Date",
                yaxis_title="Gross Revenue ($)",
            )
            st.plotly_chart(fig_rev, use_container_width=True)

        with tab3:
            c3, c4 = st.columns(2)
            with c3:
                st.subheader("Category-Wise Demand Comparison")
                fig_cat = px.box(
                    filtered_df,
                    x="Category",
                    y="Units Sold",
                    color="Category",
                    title="Daily Units Sold by Product Category",
                    color_discrete_sequence=["#2e7d32", "#388e3c", "#43a047", "#66bb6a", "#81c784"],
                )
                fig_cat.update_layout(template="plotly_white", showlegend=False)
                st.plotly_chart(fig_cat, use_container_width=True)

            with c4:
                st.subheader("Inventory Level vs. Units Sold (Collider Check)")
                sample_inv = filtered_df.sample(min(2000, len(filtered_df)), random_state=42)
                fig_inv = px.scatter(
                    sample_inv,
                    x="Inventory Level",
                    y="Units Sold",
                    trendline="ols",
                    title="Inventory Level vs. Units Sold (Capacity Reflection)",
                    opacity=0.5,
                    color_discrete_sequence=["#1b5e20"],
                )
                fig_inv.update_layout(template="plotly_white", xaxis_title="Inventory Level", yaxis_title="Units Sold")
                st.plotly_chart(fig_inv, use_container_width=True)
                st.caption(
                    "High correlation between inventory and sales reflects retail stocking policies. "
                    "Conditioning on inventory in causal regressions risks collider / post-treatment bias."
                )


# -----------------------------------------------------------------------------
# SECTION 4: CAUSAL ANALYSIS (DML)
# -----------------------------------------------------------------------------
elif selected_section == "🔬 4. Causal Analysis (DML)":
    st.header("🔬 Causal Demand Analysis: Double Machine Learning")
    st.markdown(
        """
        To isolate the causal effect of price adjustments on unit sales from confounding store tiers, product prestige, 
        and seasonal schedules, the project deploys **Robinson's Partially Linear Double Machine Learning (DML)** 
        with multi-fold cross-fitting and heteroskedasticity-consistent (HC3) standard errors.
        """
    )

    if dml_results is None:
        st.error("DML results file `dml_validated_results.json` not found.")
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

        if df_robustness is not None:
            st.markdown("---")
            st.subheader("Robustness Forest Plot: 18 Specification Sensitivity Analysis")
            st.markdown(
                "Across 18 separate specifications (alternative nuisance models, control sets, product categories, "
                "calendar years, geographic regions, and trimmed price support), **0 out of 18 specifications reject the null hypothesis of zero elasticity**."
            )

            # Forest plot of the 18 specifications
            df_plot = df_robustness.copy()
            df_plot["error_minus"] = df_plot["theta_estimate"] - df_plot["ci_lower_95"]
            df_plot["error_plus"] = df_plot["ci_upper_95"] - df_plot["theta_estimate"]

            fig_forest = go.Figure()
            fig_forest.add_trace(
                go.Scatter(
                    x=df_plot["theta_estimate"],
                    y=df_plot["specification_name"],
                    mode="markers",
                    marker=dict(color="#2e7d32", size=8),
                    error_x=dict(
                        type="data",
                        symmetric=False,
                        array=df_plot["error_plus"],
                        arrayminus=df_plot["error_minus"],
                        color="#2e7d32",
                        thickness=1.5,
                        width=4,
                    ),
                    name="θ Estimate (95% CI)",
                )
            )
            # Add vertical reference line at zero
            fig_forest.add_vline(x=0, line_dash="dash", line_color="#d32f2f", annotation_text="θ = 0 (Null)")
            fig_forest.update_layout(
                title="DML Treatment Effect Estimates Across 18 Specifications (Forest Plot)",
                template="plotly_white",
                xaxis_title="Estimated Price Treatment Effect (θ, Units / $)",
                yaxis_title="Specification / Subgroup",
                height=650,
            )
            st.plotly_chart(fig_forest, use_container_width=True)


# -----------------------------------------------------------------------------
# SECTION 5: MODEL PERFORMANCE
# -----------------------------------------------------------------------------
elif selected_section == "📈 5. Model Performance":
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

        st.markdown(
            """
            <div class="warning-box">
                <b>Critical Methodological Distinction: Predictive vs. Causal Modeling</b><br>
                • <b>Predictive Regression (e.g. Ridge R²=0.344, Random Forest R²=0.318):</b> Answers <i>"Given current features, what sales quantity do we expect?"</i> 
                Models rely overwhelmingly on <b>Inventory Level</b> (Permutation importance: +0.7118 R² drop) as a proxy for retailer demand forecasting. 
                Selling Price has virtually zero predictive signal (+0.0029).<br>
                • <b>Causal Inference (Robinson DML):</b> Answers <i>"If management intervenes and raises price by $5, what counterfactual change occurs?"</i> 
                Because inventory is chosen after observing expected demand, treating inventory as an independent policy lever causes severe collider bias. 
                DML isolates orthogonal variation in Price to establish that demand is structurally inelastic.
            </div>
            """,
            unsafe_allow_html=True,
        )


# -----------------------------------------------------------------------------
# SECTION 6: PRICING SCENARIO EXPLORER
# -----------------------------------------------------------------------------
elif selected_section == "🎛️ 6. Pricing Scenario Explorer":
    st.header("🎛️ Interactive Pricing Scenario Explorer")
    st.markdown(
        "Evaluate the commercial and operational impact of candidate price changes ($-10\\%, -5\\%, 0\\%, +5\\%, +10\\%$) "
        "under verified DML elasticity estimates, physical inventory bounds, and demand non-negativity constraints."
    )

    st.markdown(
        """
        <div class="danger-box">
            <b>Fundamental Economic Rule: Revenue ≠ Profit</b><br>
            Top-line revenue is defined strictly as <code>Price × Realized Units Sold</code>. 
            Because <b>wholesale procurement unit cost (COGS) is absent from the dataset</b>, profit optimization 
            cannot mathematically be performed. Increases in simulated revenue do not automatically translate to increased profit.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if df_scenarios is not None:
        c1, c2 = st.columns([1, 1])
        with c1:
            case_options = df_scenarios["case_type"].unique().tolist()
            selected_case = st.selectbox("Select Case Evaluation Tier", options=case_options, index=0)

        with c2:
            subset_cases = df_scenarios[df_scenarios["case_type"] == selected_case]
            product_labels = [
                f"{row['category']} - Product {row['product_id']} (Store {row['store_id']})"
                for _, row in subset_cases.drop_duplicates(subset=["category", "product_id", "store_id"]).iterrows()
            ]
            selected_prod_label = st.selectbox("Select Merchandise Item", options=product_labels)

        # Extract selected product details
        sel_cat = selected_prod_label.split(" - ")[0]
        sel_pid = selected_prod_label.split("Product ")[1].split(" (")[0]
        sel_sid = selected_prod_label.split("Store ")[1].split(")")[0]

        prod_scenarios = df_scenarios[
            (df_scenarios["case_type"] == selected_case)
            & (df_scenarios["category"] == sel_cat)
            & (df_scenarios["product_id"] == sel_pid)
            & (df_scenarios["store_id"] == sel_sid)
        ].copy()

        baseline_row = prod_scenarios[prod_scenarios["scenario"].str.contains("0%|Baseline")].iloc[0]
        base_price = baseline_row["baseline_price"]
        base_units = baseline_row["baseline_units"]
        base_inv = baseline_row["available_inventory"]
        base_rev = baseline_row["estimated_revenue"]
        theta_used = baseline_row["dml_theta_used"]

        # Display Baseline Snapshot
        st.subheader(f"Baseline Snapshot: {sel_cat} (Product {sel_pid} at Store {sel_sid})")
        b1, b2, b3, b4, b5 = st.columns(5)
        with b1:
            st.metric("Baseline Price", f"${base_price:.2f}")
        with b2:
            st.metric("Baseline Daily Units", f"{base_units:.1f}")
        with b3:
            st.metric("Available Inventory Cap", f"{base_inv:.1f}")
        with b4:
            st.metric("Baseline Gross Revenue", f"${base_rev:,.2f}")
        with b5:
            st.metric("DML Theta Used (θ)", f"{theta_used:+.4f}")

        st.markdown("---")
        st.subheader("Discrete Pricing Scenarios (-10% to +10%)")

        # Format scenario table
        disp_scenarios = prod_scenarios[
            [
                "scenario",
                "candidate_price",
                "estimated_demand",
                "demand_ci_low",
                "demand_ci_high",
                "available_inventory",
                "realized_sales",
                "inventory_binding",
                "estimated_revenue",
                "revenue_diff_dollars",
                "revenue_diff_pct",
                "risk_rating",
                "managerial_action",
            ]
        ].copy()

        st.dataframe(
            disp_scenarios.style.format(
                {
                    "candidate_price": "${:.2f}",
                    "estimated_demand": "{:.2f}",
                    "demand_ci_low": "{:.2f}",
                    "demand_ci_high": "{:.2f}",
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

        # Plotly comparison charts
        col_plot1, col_plot2 = st.columns(2)
        with col_plot1:
            fig_dem = go.Figure()
            fig_dem.add_trace(
                go.Bar(
                    x=prod_scenarios["scenario"],
                    y=prod_scenarios["estimated_demand"],
                    name="Estimated Demand",
                    marker_color="#2e7d32",
                    error_y=dict(
                        type="data",
                        symmetric=False,
                        array=prod_scenarios["demand_ci_high"] - prod_scenarios["estimated_demand"],
                        arrayminus=prod_scenarios["estimated_demand"] - prod_scenarios["demand_ci_low"],
                    ),
                )
            )
            fig_dem.add_hline(
                y=base_inv,
                line_dash="dash",
                line_color="#e65100",
                annotation_text=f"Inventory Cap ({base_inv:.0f})",
            )
            fig_dem.update_layout(
                title="Estimated Demand with 95% Confidence Bounds",
                template="plotly_white",
                xaxis_title="Pricing Scenario",
                yaxis_title="Estimated Units",
            )
            st.plotly_chart(fig_dem, use_container_width=True)

        with col_plot2:
            fig_rev_scen = go.Figure()
            fig_rev_scen.add_trace(
                go.Bar(
                    x=prod_scenarios["scenario"],
                    y=prod_scenarios["estimated_revenue"],
                    name="Estimated Revenue ($)",
                    marker_color=["#ef5350", "#ff7043", "#66bb6a", "#2e7d32", "#1b5e20"],
                )
            )
            fig_rev_scen.add_hline(
                y=base_rev,
                line_dash="dash",
                line_color="#333333",
                annotation_text=f"Baseline (${base_rev:,.0f})",
            )
            fig_rev_scen.update_layout(
                title="Projected Gross Revenue Across Scenarios ($)",
                template="plotly_white",
                xaxis_title="Pricing Scenario",
                yaxis_title="Gross Daily Revenue ($)",
            )
            st.plotly_chart(fig_rev_scen, use_container_width=True)

        # Custom interactive slider
        st.markdown("---")
        st.subheader("Custom Percentage What-If Simulator")
        custom_pct = st.slider(
            "Select Continuous Price Adjustment (%)",
            min_value=-20.0,
            max_value=20.0,
            value=0.0,
            step=1.0,
            format="%+.0f%%",
        )

        cand_price = round(base_price * (1.0 + custom_pct / 100.0), 2)
        delta_p = cand_price - base_price
        custom_est_demand = max(0.0, base_units + theta_used * delta_p)
        custom_realized = min(custom_est_demand, base_inv)
        is_binding = custom_est_demand > base_inv
        custom_revenue = cand_price * custom_realized
        delta_rev = custom_revenue - base_rev
        delta_rev_pct = (delta_rev / base_rev) * 100.0 if base_rev > 0 else 0.0

        r1, r2, r3, r4, r5 = st.columns(5)
        with r1:
            st.metric("Candidate Price", f"${cand_price:.2f}", f"{custom_pct:+.1f}%")
        with r2:
            st.metric("Projected Demand", f"{custom_est_demand:.2f} units", f"{custom_est_demand - base_units:+.2f}")
        with r3:
            st.metric("Realized Sales", f"{custom_realized:.2f} units", "Capped by stock" if is_binding else "Non-binding")
        with r4:
            st.metric("Projected Revenue", f"${custom_revenue:,.2f}", f"${delta_rev:+,.2f}")
        with r5:
            st.metric("Revenue Impact", f"{delta_rev_pct:+.2f}%")


# -----------------------------------------------------------------------------
# SECTION 7: PRICING RECOMMENDATIONS
# -----------------------------------------------------------------------------
elif selected_section == "💡 7. Pricing Recommendations":
    st.header("💡 Pricing Recommendations & Executive Governance Matrix")
    st.markdown(
        "Structured pricing policies derived from the Improved Pricing Decision Engine (Day 17). "
        "Recommendations translate empirical inelasticity and inventory realities into defensible business rules."
    )

    if df_scenarios is None:
        st.error("Precomputed pricing scenarios table not found at `reports/day17_pricing_scenarios.csv`.")
    else:
        # High level policy summary cards
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

        st.subheader("Decision Governance Matrix")
        st.markdown(
            r"""
            | Action Category | Target Scenario | Demand Response | Revenue Impact | Risk Rating | Managerial Decision |
            | :--- | :---: | :---: | :---: | :---: | :--- |
            | **Price Reduction** | $-10\\%$ to $-5\\%$ | Near Zero ($\Delta Q \\le 0.1$) | **$-5.02\\%$ to $-10.03\\%$** | **High** | **Strictly Reject.** Inelastic volume causes direct cash loss. |
            | **Status Quo** | Baseline ($0\\%$) | Benchmark | Benchmark | **Low** | **Maintain.** Approved operational policy. |
            | **Price Increase** | $+5\\%$ to $+10\\%$ | Near Zero ($\Delta Q \\le 0.1$) | **$+5.02\\%$ to $+10.03\\%$** | **Moderate-High** | **Controlled Micro-Pilot.** Do not deploy catalog-wide without wholesale cost data. |
            """
        )

        st.markdown("---")
        st.subheader("Catalog Recommendations: Benchmark & Category Evaluations")

        filter_case = st.radio("Display Subset", options=["All Scenarios", "Benchmark Case (P0001)", "Category Specific"], horizontal=True)

        if filter_case == "Benchmark Case (P0001)":
            recs_view = df_scenarios[df_scenarios["case_type"] == "Benchmark Case"]
        elif filter_case == "Category Specific":
            recs_view = df_scenarios[df_scenarios["case_type"] == "Category Specific"]
        else:
            recs_view = df_scenarios

        st.dataframe(
            recs_view[
                [
                    "category",
                    "product_id",
                    "store_id",
                    "scenario",
                    "candidate_price",
                    "baseline_price",
                    "realized_sales",
                    "estimated_revenue",
                    "revenue_diff_pct",
                    "risk_rating",
                    "managerial_action",
                ]
            ].style.format(
                {
                    "candidate_price": "${:.2f}",
                    "baseline_price": "${:.2f}",
                    "realized_sales": "{:.2f}",
                    "estimated_revenue": "${:,.2f}",
                    "revenue_diff_pct": "{:+.2f}%",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# -----------------------------------------------------------------------------
# SECTION 8: PROJECT LIMITATIONS
# -----------------------------------------------------------------------------
elif selected_section == "⚠️ 8. Project Limitations":
    st.header("⚠️ Project Limitations & Analytical Caveats")
    st.markdown(
        """
        A rigorous data science and econometric project must explicitly delineate what the data and models 
        can and cannot establish. The following analytical limitations must be considered prior to commercial deployment.
        """
    )

    t1, t2, t3, t4, t5 = st.tabs(
        [
            "1. Unobserved Confounders",
            "2. Missing Cost & Profit",
            "3. Statistical Uncertainty",
            "4. Operational & Inventory Timing",
            "5. Observational Scope",
        ]
    )

    with t1:
        st.subheader("1. Possible Unobserved Confounding Variables")
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

    with t2:
        st.subheader("2. Revenue vs. Profit & The Missing Cost Problem")
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

    with t3:
        st.subheader("3. Statistical Uncertainty in Treatment Effects")
        st.markdown(
            r"""
            * **Statistically Insignificant Point Estimate:** The primary DML coefficient $\hat{\theta} = +0.0107$ has a $p$-value of $0.4899$. 
              We cannot statistically distinguish the true price elasticity from zero.
            * **Confidence Interval Span:** The 95% confidence interval spans $[-0.0197, +0.0411]$. The true parameter may be slightly negative 
              or slightly positive.
            * **18 Robustness Specifications:** Across 18 model permutations in Day 15, zero specifications reached statistical significance.
            """
        )

    with t4:
        st.subheader("4. Inventory Constraints & Measurement Timing")
        st.markdown(
            r"""
            * **Physical Bound:** Daily sales cannot exceed available shelf inventory: $\text{Sales} = \min(\hat{D}, I)$.
            * **Timing Caveat:** Physical inventory must reflect **start-of-day opening stock** ($I_t^{\text{start}}$). 
              If a dataset records inventory at end-of-day ($I_t^{\text{end}} = I_t^{\text{start}} - \text{Sales}_t$), 
              capping demand by $I_t^{\text{end}}$ introduces severe post-treatment truncation.
            * **Stockout Masking:** When a store stocks out, recorded sales equal stock, masking true unconstrained customer demand.
            """
        )

    with t5:
        st.subheader("5. Observational Scope & Extrapolation Boundaries")
        st.markdown(
            r"""
            * **Pricing Support:** Historical prices in the dataset range strictly between $\$10.04$ and $\$99.97$. 
              Simulations should not extrapolate beyond this support.
            * **Single Macroeconomic Regime:** The dataset spans 2022 to 2024. Macroeconomic shifts, inflation regimes, or structural retail shocks 
              may alter consumer price responsiveness.
            """
        )

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #888; font-size: 0.8rem; padding: 12px 0;">
        EconoCausal Decision-Support Dashboard • Day 19 Final Project Deliverable • Infotact Solutions Internship • 2026
    </div>
    """,
    unsafe_allow_html=True,
)
