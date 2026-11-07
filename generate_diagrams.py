import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('presentation_assets', exist_ok=True)

PRIMARY_GREEN = '#1E7F43'
SECONDARY_GREEN = '#27AE60'
DARK_TEXT = '#1A2530'
LIGHT_GREY = '#F4F6F7'
BORDER_COLOR = '#BDC3C7'

# -------------------------------------------------------------
# Diagram 1: Slide 6 - 10-Step Project Methodology Workflow
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 6), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.axis('off')

# 10 steps split into 2 rows of 5 steps
steps = [
    ("1. Data Collection", "73,100 store logs\n(2022-2024, 5 stores)", "#E8F8F5", PRIMARY_GREEN),
    ("2. Data Cleaning", "0 nulls, 0 duplicates\nType validation", "#E8F8F5", PRIMARY_GREEN),
    ("3. EDA & Auditing", "Price/demand stats\nTemporal patterns", "#E8F8F5", PRIMARY_GREEN),
    ("4. Baseline Modeling", "Random Forest\nMAE 69.51, R2 0.318", "#EBF5FB", "#2980B9"),
    ("5. Causal DAG", "Confounder isolation\nCollider screening", "#FEF9E7", "#D4AC0D"),
    ("6. DML Preparation", "Feature matrix W\nRobinson residualization", "#FEF9E7", "#D4AC0D"),
    ("7. DML Estimation", "3-fold cross-fitting\nExtraTrees nuisance", "#E8F8F5", PRIMARY_GREEN),
    ("8. Validation", "HC3 robust SE\n18-spec robustness", "#E8F8F5", PRIMARY_GREEN),
    ("9. Pricing Scenarios", "What-if simulation\n-10% to +10% prices", "#FDEDEC", "#C0392B"),
    ("10. Business Matrix", "Status-quo policy\nPhased micro-pilots", "#EAFAF1", SECONDARY_GREEN),
]

# Row 1: steps 0 to 4 (left to right)
y1 = 0.65
# Row 2: steps 5 to 9 (left to right)
y2 = 0.20
box_w = 0.165
box_h = 0.26

for idx, (title, desc, fill_col, border_col) in enumerate(steps[:5]):
    x = 0.02 + idx * 0.198
    rect = patches.FancyBboxPatch((x, y1), box_w, box_h, boxstyle="round,pad=0.015,rounding_size=0.02",
                                  facecolor=fill_col, edgecolor=border_col, linewidth=2.2)
    ax.add_patch(rect)
    ax.text(x + box_w/2, y1 + box_h - 0.055, title, ha='center', va='center', fontsize=11, fontweight='bold', color=DARK_TEXT)
    ax.text(x + box_w/2, y1 + 0.09, desc, ha='center', va='center', fontsize=9, color='#34495E', linespacing=1.2)
    
    # Arrow to next if not last in row
    if idx < 4:
        ax.annotate('', xy=(x + box_w + 0.03, y1 + box_h/2), xytext=(x + box_w + 0.003, y1 + box_h/2),
                    arrowprops=dict(arrowstyle="->", color=border_col, lw=2.5, mutation_scale=15))

# Connect Row 1 to Row 2 (Step 4 to Step 5)
ax.annotate('', xy=(0.02 + 0.165/2, y2 + box_h + 0.02), xytext=(0.02 + 4*0.198 + 0.165/2, y1 - 0.02),
            arrowprops=dict(arrowstyle="->", color='#7F8C8D', lw=2, linestyle='--', connectionstyle="arc3,rad=-0.15"))

for idx, (title, desc, fill_col, border_col) in enumerate(steps[5:]):
    x = 0.02 + idx * 0.198
    rect = patches.FancyBboxPatch((x, y2), box_w, box_h, boxstyle="round,pad=0.015,rounding_size=0.02",
                                  facecolor=fill_col, edgecolor=border_col, linewidth=2.2)
    ax.add_patch(rect)
    ax.text(x + box_w/2, y2 + box_h - 0.055, title, ha='center', va='center', fontsize=11, fontweight='bold', color=DARK_TEXT)
    ax.text(x + box_w/2, y2 + 0.09, desc, ha='center', va='center', fontsize=9, color='#34495E', linespacing=1.2)
    
    if idx < 4:
        ax.annotate('', xy=(x + box_w + 0.03, y2 + box_h/2), xytext=(x + box_w + 0.003, y2 + box_h/2),
                    arrowprops=dict(arrowstyle="->", color=border_col, lw=2.5, mutation_scale=15))

# Header / Legend
plt.title('EconoCausal End-to-End Methodological Architecture (Days 1 - 19)', fontsize=14, fontweight='bold', pad=15, color=DARK_TEXT)
plt.savefig('presentation_assets/slide6_workflow_diagram.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created slide6_workflow_diagram.png")

# -------------------------------------------------------------
# Diagram 2: Slide 8 - Double Machine Learning (DML) Architecture
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(15, 6.2), dpi=300)
fig.patch.set_facecolor('#FFFFFF')
ax.set_facecolor('#FFFFFF')
ax.axis('off')

# Section 1: Observational Inputs
rect1 = patches.FancyBboxPatch((0.02, 0.15), 0.22, 0.70, boxstyle="round,pad=0.02,rounding_size=0.03",
                               facecolor='#F4F6F7', edgecolor='#7F8C8D', linewidth=2)
ax.add_patch(rect1)
ax.text(0.13, 0.78, "Observed Variables", ha='center', fontsize=13, fontweight='bold', color=DARK_TEXT)
ax.text(0.13, 0.63, "Treatment (T):\nRetail Price ($)", ha='center', fontsize=11, fontweight='bold', color=PRIMARY_GREEN,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#E8F8F5', edgecolor=PRIMARY_GREEN))
ax.text(0.13, 0.43, "Outcome (Y):\nDaily Units Sold", ha='center', fontsize=11, fontweight='bold', color='#2980B9',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#EBF5FB', edgecolor='#2980B9'))
ax.text(0.13, 0.23, "Controls (W):\nProduct, Store, Category,\nRegion, Year, Month, DOW", ha='center', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFFFF', edgecolor='#BDC3C7'))

# Arrow to Stage 1
ax.annotate('', xy=(0.28, 0.50), xytext=(0.24, 0.50), arrowprops=dict(arrowstyle="->", color=DARK_TEXT, lw=2.5))

# Section 2: Stage 1 Nuisance & Cross-Fitting
rect2 = patches.FancyBboxPatch((0.29, 0.15), 0.26, 0.70, boxstyle="round,pad=0.02,rounding_size=0.03",
                               facecolor='#FEFDE8', edgecolor='#F1C40F', linewidth=2)
ax.add_patch(rect2)
ax.text(0.42, 0.78, "Stage 1: Nuisance Models\n& 3-Fold Cross-Fitting", ha='center', fontsize=12, fontweight='bold', color='#7D6608')
ax.text(0.42, 0.58, "Model 1: E[Y | W]\nExtraTreesRegressor (n=60)\nPredicts Units Sold from W", ha='center', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFFFF', edgecolor='#F1C40F'))
ax.text(0.42, 0.35, "Model 2: E[T | W]\nExtraTreesRegressor (n=60)\nPredicts Price from W", ha='center', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFFFF', edgecolor='#F1C40F'))
ax.text(0.42, 0.19, "Out-of-fold predictions prevent\nregularization & overfitting bias", ha='center', fontsize=9, color='#7D6608', style='italic')

# Arrow to Stage 2
ax.annotate('', xy=(0.59, 0.50), xytext=(0.55, 0.50), arrowprops=dict(arrowstyle="->", color=DARK_TEXT, lw=2.5))

# Section 3: Residualization (Robinson 1988)
rect3 = patches.FancyBboxPatch((0.60, 0.15), 0.18, 0.70, boxstyle="round,pad=0.02,rounding_size=0.03",
                               facecolor='#E8F8F5', edgecolor=PRIMARY_GREEN, linewidth=2)
ax.add_patch(rect3)
ax.text(0.69, 0.78, "Stage 2:\nResidualization", ha='center', fontsize=12, fontweight='bold', color=PRIMARY_GREEN)
ax.text(0.69, 0.58, "Demand Residual:\nỸ = Y - E[Y|W]\n(Unconfounded Demand)", ha='center', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFFFF', edgecolor=PRIMARY_GREEN))
ax.text(0.69, 0.35, "Price Residual:\nT̃ = T - E[T|W]\n(Orthogonal Price Shock)", ha='center', fontsize=10,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFFFF', edgecolor=PRIMARY_GREEN))
ax.text(0.69, 0.20, "Removes confounding\ninfluence of W", ha='center', fontsize=9, color=PRIMARY_GREEN, style='italic')

# Arrow to Stage 3
ax.annotate('', xy=(0.82, 0.50), xytext=(0.78, 0.50), arrowprops=dict(arrowstyle="->", color=DARK_TEXT, lw=2.5))

# Section 4: Stage 3 Causal Parameter
rect4 = patches.FancyBboxPatch((0.83, 0.15), 0.15, 0.70, boxstyle="round,pad=0.02,rounding_size=0.03",
                               facecolor='#EAFAF1', edgecolor=PRIMARY_GREEN, linewidth=2.5)
ax.add_patch(rect4)
ax.text(0.905, 0.78, "Stage 3:\nCausal Parameter", ha='center', fontsize=12, fontweight='bold', color=PRIMARY_GREEN)
ax.text(0.905, 0.55, "OLS Regression:\nỸ = θ · T̃ + ε\nwith HC3 Robust SE", ha='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFFFF', edgecolor=PRIMARY_GREEN))
ax.text(0.905, 0.35, "Result:\nθ = +0.0107\n95% CI: [-0.02, +0.04]\np = 0.490 (Inelastic)", ha='center', fontsize=9.5, fontweight='bold', color=DARK_TEXT,
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#FEF9E7', edgecolor='#F1C40F'))
ax.text(0.905, 0.19, "Root-N consistent\n& asymptotically normal", ha='center', fontsize=8.5, color='#27AE60', style='italic')

plt.title("Robinson's Partially Linear Double Machine Learning (DML) Architecture", fontsize=14, fontweight='bold', pad=15, color=DARK_TEXT)
plt.savefig('presentation_assets/slide8_dml_architecture.png', dpi=300, bbox_inches='tight')
plt.close()
print("Created slide8_dml_architecture.png")
