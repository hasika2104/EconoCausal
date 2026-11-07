import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

# Ensure output directory exists
os.makedirs('presentation_assets', exist_ok=True)

# Styling defaults
PRIMARY_GREEN = '#1E7F43'   # Emerald / Forest Green
SECONDARY_GREEN = '#27AE60' # Mint green
LIGHT_BG = '#F8FAFC'
DARK_TEXT = '#1A2530'
ACCENT_RED = '#C0392B'
ACCENT_BLUE = '#2980B9'
ACCENT_GREY = '#7F8C8D'
CARD_BG = '#FFFFFF'

plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['text.color'] = DARK_TEXT
plt.rcParams['axes.labelcolor'] = DARK_TEXT
plt.rcParams['xtick.color'] = DARK_TEXT
plt.rcParams['ytick.color'] = DARK_TEXT
plt.rcParams['font.size'] = 11

print("Loading cleaned dataset...")
df = pd.read_csv('data/processed/retail_inventory_cleaned.csv')
print(f"Dataset shape: {df.shape}")

# -------------------------------------------------------------
# Chart 1: Slide 2 - Problem Statement: Price vs Demand Concept
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')

# Panel A: Classical Economic Demand (Elastic)
p = np.linspace(20, 90, 100)
d_elastic = 250 - 2.0 * p
axes[0].plot(p, d_elastic, color=ACCENT_BLUE, lw=3, label='Theoretical Elastic Demand')
axes[0].set_title('A. Textbook Assumption\n(Negative Elasticity: Price ↑ ⇒ Demand ↓)', fontsize=12, fontweight='bold', pad=12, color=DARK_TEXT)
axes[0].set_xlabel('Product Price ($)', fontweight='bold')
axes[0].set_ylabel('Demand / Units Sold', fontweight='bold')
axes[0].grid(True, linestyle='--', alpha=0.4)
axes[0].annotate('Price Cut (-10%)\nVolume Gains Offset Price', xy=(40, 170), xytext=(22, 190),
                 arrowprops=dict(arrowstyle="->", color=ACCENT_BLUE, lw=1.5), fontsize=9, fontweight='semibold')

# Panel B: Observational Reality in EconoCausal
axes[1].scatter(df['Price'].sample(1500, random_state=42), df['Units Sold'].sample(1500, random_state=42), 
                alpha=0.15, color=ACCENT_GREY, s=15, label='Actual Data (Subsample)')
# Fit line
p_eval = np.linspace(10, 100, 100)
axes[1].plot(p_eval, [140.2]*100, color=PRIMARY_GREEN, lw=3.5, label='Causal Estimate (θ ≈ +0.0107, p=0.49)')
axes[1].set_title('B. EconoCausal Reality\n(Inelastic Demand: Flat Relationship)', fontsize=12, fontweight='bold', pad=12, color=PRIMARY_GREEN)
axes[1].set_xlabel('Product Price ($)', fontweight='bold')
axes[1].set_ylabel('Units Sold', fontweight='bold')
axes[1].set_ylim(0, 500)
axes[1].grid(True, linestyle='--', alpha=0.4)
axes[1].legend(loc='upper right', frameon=True, fontsize=9)

# Panel C: The Revenue Consequence
p_scen = np.array([49.62, 52.37, 55.13, 57.89, 60.64])
rev_scen = np.array([8580.81, 9059.07, 9537.49, 10016.07, 10494.82])
colors_rev = [ACCENT_RED, '#E67E22', '#7F8C8D', SECONDARY_GREEN, PRIMARY_GREEN]
bars = axes[2].bar(['-10%', '-5%', 'Base (0%)', '+5%', '+10%'], rev_scen, color=colors_rev, width=0.55, edgecolor='none')
axes[2].set_title('C. Revenue Impact Under Inelasticity\n(Price Cuts Destroy Revenue)', fontsize=12, fontweight='bold', pad=12, color=DARK_TEXT)
axes[2].set_ylabel('Simulated Revenue ($)', fontweight='bold')
axes[2].set_ylim(7000, 11500)
axes[2].grid(axis='y', linestyle='--', alpha=0.4)
for bar in bars:
    height = bar.get_height()
    axes[2].annotate(f'${height:,.0f}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('presentation_assets/slide2_demand_concept.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created slide2_demand_concept.png")

# -------------------------------------------------------------
# Chart 2: Slide 5 - Comprehensive EDA Visualizations (5 panels)
# -------------------------------------------------------------
fig = plt.figure(figsize=(16, 7.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.25)

# 1. Price Distribution
ax1 = fig.add_subplot(gs[0, 0])
sns.histplot(df['Price'], bins=30, kde=True, color=PRIMARY_GREEN, ax=ax1, edgecolor='white', alpha=0.7)
ax1.set_title('Price Distribution ($10.04 - $99.97)', fontsize=11, fontweight='bold', color=DARK_TEXT)
ax1.set_xlabel('Price ($)', fontweight='semibold')
ax1.set_ylabel('Frequency', fontweight='semibold')
ax1.axvline(df['Price'].mean(), color=ACCENT_RED, linestyle='--', lw=2, label=f'Mean: ${df["Price"].mean():.2f}')
ax1.legend(frameon=True, fontsize=9)
ax1.grid(True, linestyle='--', alpha=0.3)

# 2. Units Sold Distribution
ax2 = fig.add_subplot(gs[0, 1])
sns.histplot(df['Units Sold'], bins=30, kde=True, color=SECONDARY_GREEN, ax=ax2, edgecolor='white', alpha=0.7)
ax2.set_title('Units Sold Distribution (0 - 499 units)', fontsize=11, fontweight='bold', color=DARK_TEXT)
ax2.set_xlabel('Units Sold', fontweight='semibold')
ax2.set_ylabel('Frequency', fontweight='semibold')
ax2.axvline(df['Units Sold'].mean(), color=ACCENT_RED, linestyle='--', lw=2, label=f'Mean: {df["Units Sold"].mean():.1f}')
ax2.legend(frameon=True, fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.3)

# 3. Price vs Units Sold (Bivariate Correlation)
ax3 = fig.add_subplot(gs[0, 2])
sample_df = df.sample(3000, random_state=42)
ax3.scatter(sample_df['Price'], sample_df['Units Sold'], alpha=0.2, color='#2C3E50', s=12)
m, b = np.polyfit(df['Price'], df['Units Sold'], 1)
ax3.plot(p_eval, m*p_eval + b, color=ACCENT_RED, lw=2.5, label=f'OLS slope = +{m:.4f} (r ≈ 0.00)')
ax3.set_title('Price vs Units Sold (No Raw Correlation)', fontsize=11, fontweight='bold', color=DARK_TEXT)
ax3.set_xlabel('Price ($)', fontweight='semibold')
ax3.set_ylabel('Units Sold', fontweight='semibold')
ax3.legend(frameon=True, fontsize=9)
ax3.grid(True, linestyle='--', alpha=0.3)

# 4. Monthly Demand Patterns (2022-2023)
ax4 = fig.add_subplot(gs[1, 0:2])
df['YearMonth'] = df['Year'].astype(str) + '-' + df['Month'].astype(str).str.zfill(2)
monthly_summary = df.groupby('YearMonth')['Units Sold'].agg(['mean', 'median']).reset_index()
# Take the 24 full months
monthly_summary = monthly_summary.iloc[:24]
ax4.plot(monthly_summary['YearMonth'], monthly_summary['mean'], marker='o', lw=2.5, color=PRIMARY_GREEN, label='Mean Daily Units Sold')
ax4.plot(monthly_summary['YearMonth'], monthly_summary['median'], marker='s', lw=2, linestyle=':', color=ACCENT_BLUE, label='Median Daily Units Sold')
ax4.set_title('Monthly Demand Patterns Across 24 Months (Stable Macro Trend)', fontsize=11, fontweight='bold', color=DARK_TEXT)
ax4.set_xlabel('Year-Month', fontweight='semibold')
ax4.set_ylabel('Daily Units Sold per Product-Store', fontweight='semibold')
ax4.tick_params(axis='x', rotation=45)
ax4.grid(True, linestyle='--', alpha=0.3)
ax4.legend(frameon=True, fontsize=9)

# 5. Category-wise Demand
ax5 = fig.add_subplot(gs[1, 2])
cat_summary = df.groupby('Category')['Units Sold'].mean().sort_values(ascending=False)
bars = ax5.bar(cat_summary.index, cat_summary.values, color=['#1E7F43', '#27AE60', '#52BE80', '#7DCEA0', '#A9DFBF'], width=0.6)
ax5.set_title('Category-Wise Mean Daily Demand', fontsize=11, fontweight='bold', color=DARK_TEXT)
ax5.set_xlabel('Merchandise Category', fontweight='semibold')
ax5.set_ylabel('Mean Units Sold', fontweight='semibold')
ax5.tick_params(axis='x', rotation=25)
ax5.grid(axis='y', linestyle='--', alpha=0.3)
for bar in bars:
    height = bar.get_height()
    ax5.annotate(f'{height:.1f}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points",
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('presentation_assets/slide5_eda_combined.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created slide5_eda_combined.png")

# -------------------------------------------------------------
# Chart 3: Slide 7 - Predictive Model Benchmarks & Feature Importance
# -------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')

# Left: Model R2 and MAE
models = ['Mean Baseline\n(Dummy)', 'Random Forest\n(Baseline)', 'HistGradBoost\n(Alternative 1)', 'RidgeCV\n(Alternative 2)']
r2_scores = [0.00, 0.3184, 0.3419, 0.3443]
mae_scores = [88.81, 69.51, 68.68, 68.65]

x = np.arange(len(models))
width = 0.35

rects1 = axes[0].bar(x - width/2, [r*100 for r in r2_scores], width, label='Variance Explained ($R^2$ %)', color=PRIMARY_GREEN)
rects2 = axes[0].bar(x + width/2, mae_scores, width, label='Test Error (MAE units)', color=ACCENT_BLUE)

axes[0].set_title('Predictive Demand Models: Holdout Evaluation (N=14,620)', fontsize=12, fontweight='bold', pad=12)
axes[0].set_xticks(x)
axes[0].set_xticklabels(models, fontweight='semibold')
axes[0].legend(frameon=True, fontsize=9)
axes[0].grid(axis='y', linestyle='--', alpha=0.3)

for r in rects1:
    h = r.get_height()
    axes[0].annotate(f'{h:.1f}%', xy=(r.get_x() + r.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')
for r in rects2:
    h = r.get_height()
    axes[0].annotate(f'{h:.1f}', xy=(r.get_x() + r.get_width() / 2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8.5, fontweight='bold')

# Right: Feature Permutation Importance
features = ['Inventory Level', 'Price (Treatment)', 'Category', 'Month', 'Product ID', 'DayOfWeek']
perm_drop = [0.7118, 0.0029, 0.0019, 0.0015, 0.0007, 0.0006]
colors_imp = [ACCENT_RED if f == 'Inventory Level' else (PRIMARY_GREEN if f.startswith('Price') else ACCENT_GREY) for f in features]

y_pos = np.arange(len(features))
bars_imp = axes[1].barh(y_pos, perm_drop, color=colors_imp, height=0.6)
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(features, fontweight='semibold')
axes[1].invert_yaxis()
axes[1].set_xlabel('Holdout Test $R^2$ Drop When Shuffled', fontweight='bold')
axes[1].set_title('Feature Permutation Importance: Inventory Dominates', fontsize=12, fontweight='bold', pad=12)
axes[1].grid(axis='x', linestyle='--', alpha=0.3)

for bar in bars_imp:
    w = bar.get_width()
    axes[1].annotate(f'{w:.4f}', xy=(w, bar.get_y() + bar.get_height() / 2),
                     xytext=(4, 0), textcoords="offset points", ha='left', va='center', fontsize=8.5, fontweight='bold')

# Annotation callout
axes[1].text(0.25, 3.5, "Inventory is a post-treatment\nstocking proxy, NOT organic demand.\nPrice has negligible predictive weight!", 
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF9E7', edgecolor='#F1C40F', alpha=0.9),
             fontsize=9, fontweight='semibold', color='#7D6608')

plt.tight_layout()
plt.savefig('presentation_assets/slide7_model_benchmarks.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created slide7_model_benchmarks.png")

# -------------------------------------------------------------
# Chart 4: Slide 10 - Robustness & DML Forest Plot
# -------------------------------------------------------------
robust_df = pd.read_csv('reports/day15_robustness_results.csv')
key_specs = robust_df[robust_df['specification_id'].isin([
    'SPEC_01_BASELINE', 'SPEC_02_INVENTORY', 'SPEC_04_RIDGE', 'SPEC_05_HISTGB',
    'SUB_CAT_CLOTHING', 'SUB_CAT_ELECTRONICS', 'SUB_CAT_FURNITURE', 'SUB_CAT_GROCERIES', 'SUB_CAT_TOYS'
])].copy()

fig, ax = plt.subplots(figsize=(12, 5.5), dpi=300)
fig.patch.set_facecolor('#FFFFFF')

y_coords = np.arange(len(key_specs))
labels = [
    'Spec 1 (Core Baseline DML)',
    'Spec 2 (+ Inventory Level Collider)',
    'Spec 4 (RidgeCV Linear Nuisance)',
    'Spec 5 (HistGradientBoost Nuisance)',
    'Subgroup: Clothing Category',
    'Subgroup: Electronics Category',
    'Subgroup: Furniture Category',
    'Subgroup: Groceries Category',
    'Subgroup: Toys Category'
]

thetas = key_specs['theta_estimate'].values
ci_lows = key_specs['ci_lower_95'].values
ci_highs = key_specs['ci_upper_95'].values

# Zero line
ax.axvline(0, color=ACCENT_RED, linestyle='--', lw=2, label='Null Effect (θ = 0)')

# Errorbars
for i in range(len(key_specs)):
    color = PRIMARY_GREEN if i == 0 else (ACCENT_BLUE if i < 4 else '#8E44AD')
    ax.errorbar(thetas[i], y_coords[i], xerr=[[thetas[i] - ci_lows[i]], [ci_highs[i] - thetas[i]]],
                fmt='o', color=color, ecolor=color, elinewidth=2.5, capsize=5, capthick=2, markersize=8)
    ax.annotate(f"θ = {thetas[i]:+.4f} (95% CI: [{ci_lows[i]:.3f}, {ci_highs[i]:.3f}])",
                xy=(ci_highs[i], y_coords[i]), xytext=(8, -3), textcoords="offset points",
                fontsize=8.5, fontweight='semibold', color=DARK_TEXT)

ax.set_yticks(y_coords)
ax.set_yticklabels(labels, fontweight='semibold')
ax.invert_yaxis()
ax.set_xlabel('Estimated Treatment Effect θ (Δ Demand per $1 Price Increase)', fontweight='bold')
ax.set_title('Double Machine Learning: Robustness Across Specifications & Categories\n(All 95% Confidence Intervals Cross Zero ⇒ Inelastic Demand)', 
             fontsize=12, fontweight='bold', pad=12, color=DARK_TEXT)
ax.grid(axis='x', linestyle='--', alpha=0.3)
ax.set_xlim(-0.12, 0.18)
ax.legend(loc='lower right', frameon=True, fontsize=9.5)

plt.tight_layout()
plt.savefig('presentation_assets/slide10_dml_forest_plot.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created slide10_dml_forest_plot.png")

# -------------------------------------------------------------
# Chart 5: Slide 9 - Pricing Scenarios Bar Chart (Benchmark P0001 at S001)
# -------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(11, 4.8), dpi=300)
fig.patch.set_facecolor('#FFFFFF')

scenarios = ['-10% Discount\n($49.62)', '-5% Discount\n($52.37)', 'Baseline (0%)\n($55.13)', '+5% Increase\n($57.89)', '+10% Increase\n($60.64)']
rev = [8580.81, 9059.07, 9537.49, 10016.07, 10494.82]
units = [172.94, 172.97, 173.00, 173.03, 173.06]
bar_colors = [ACCENT_RED, '#E67E22', '#7F8C8D', SECONDARY_GREEN, PRIMARY_GREEN]

bars = ax1.bar(scenarios, rev, color=bar_colors, width=0.52, label='Projected Gross Revenue ($)')
ax1.set_ylabel('Projected Daily Revenue ($)', fontweight='bold', color=DARK_TEXT)
ax1.set_ylim(7000, 11800)
ax1.grid(axis='y', linestyle='--', alpha=0.3)

for bar in bars:
    h = bar.get_height()
    diff = ((h - 9537.49) / 9537.49) * 100
    diff_str = f"{diff:+.1f}%" if diff != 0 else "0.0%"
    ax1.annotate(f"${h:,.2f}\n({diff_str})", xy=(bar.get_x() + bar.get_width() / 2, h),
                 xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold')

# Secondary line for units sold
ax2 = ax1.twinx()
ax2.plot(scenarios, units, color='#2C3E50', marker='s', markersize=8, lw=2.5, linestyle='--', label='Estimated Units Sold (Q)')
ax2.set_ylabel('Estimated Daily Units Sold', fontweight='bold', color='#2C3E50')
ax2.set_ylim(160, 185)

# Callout banner
plt.title('Benchmark Pricing Simulation: Product P0001 at Store S001\n(Demand Volume Flat at ~173 Units; Revenue Tracks Price Linearly)', 
          fontsize=12, fontweight='bold', pad=14, color=DARK_TEXT)

fig.legend(loc='upper left', bbox_to_anchor=(0.14, 0.88), frameon=True, fontsize=8.5)
plt.tight_layout()
plt.savefig('presentation_assets/slide9_pricing_scenarios.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created slide9_pricing_scenarios.png")

print("All charts successfully generated!")
