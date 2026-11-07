import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# -----------------------------------------------------------------------------
# Color Palette & Typography
# -----------------------------------------------------------------------------
C_PRIMARY = RGBColor(27, 94, 32)       # Dark Emerald Green (#1B5E20)
C_SECONDARY = RGBColor(46, 125, 50)    # Forest Green (#2E7D32)
C_ACCENT = RGBColor(76, 175, 80)       # Vibrant Green (#4CAF50)
C_LIGHT_BG = RGBColor(248, 250, 252)   # Very light grey-blue (#F8FAFC)
C_CARD_BG = RGBColor(255, 255, 255)    # Pure White
C_CARD_BORDER = RGBColor(226, 232, 240)# Light border (#E2E8F0)
C_DARK_TEXT = RGBColor(26, 37, 48)     # Navy/Charcoal (#1A2530)
C_BODY_TEXT = RGBColor(51, 65, 85)     # Slate text (#334155)
C_MUTED = RGBColor(100, 116, 139)      # Muted slate (#64748B)
C_PILL_BG = RGBColor(232, 245, 233)    # Pale green pill background
C_RED = RGBColor(192, 57, 43)          # Warning/destruction red
C_GOLD = RGBColor(212, 172, 13)        # Highlight gold
C_BLUE = RGBColor(41, 128, 185)        # Alternative blue

FONT_TITLE = 'Helvetica'
FONT_BODY = 'Arial'

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # completely blank layout

    def set_slide_background(slide):
        # Add background fill
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = C_LIGHT_BG
        bg.line.fill.background() # no border

        # Top green accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, Inches(0.08))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_PRIMARY
        bar.line.fill.background()

    def add_header(slide, category_text, title_text, subtitle_text=None):
        # Category pill
        pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.35), Inches(2.8), Inches(0.32))
        pill.fill.solid()
        pill.fill.fore_color.rgb = C_PILL_BG
        pill.line.color.rgb = C_ACCENT
        pill.line.width = Pt(1)
        tf_pill = pill.text_frame
        tf_pill.word_wrap = True
        tf_pill.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_pill = tf_pill.paragraphs[0]
        p_pill.text = category_text.upper()
        p_pill.font.name = FONT_BODY
        p_pill.font.size = Pt(9.5)
        p_pill.font.bold = True
        p_pill.font.color.rgb = C_PRIMARY
        p_pill.alignment = PP_ALIGN.CENTER

        # Slide Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_TITLE
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = C_DARK_TEXT

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.name = FONT_BODY
            p2.font.size = Pt(11)
            p2.font.color.rgb = C_MUTED
            p2.space_before = Pt(3)

    def add_card(slide, left, top, width, height, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.2)
        return card

    def add_bullet(tf, bold_prefix, text, size=11, space_after=8, color=C_BODY_TEXT):
        p = tf.add_paragraph()
        p.font.name = FONT_BODY
        p.font.size = Pt(size)
        p.space_after = Pt(space_after)
        
        run_bold = p.add_run()
        run_bold.text = bold_prefix + " "
        run_bold.font.bold = True
        run_bold.font.color.rgb = C_DARK_TEXT
        
        run_text = p.add_run()
        run_text.text = text
        run_text.font.bold = False
        run_text.font.color.rgb = color

    def add_speaker_note(slide, note_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = note_text

    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)

    # Decorative header banner card
    hero = add_card(slide1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(4.2), bg_color=C_CARD_BG, border_color=C_CARD_BORDER)
    
    # Left accent bar on card
    l_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(0.18), Inches(4.2))
    l_bar.fill.solid()
    l_bar.fill.fore_color.rgb = C_PRIMARY
    l_bar.line.fill.background()

    # Title text box inside hero
    tb_hero = slide1.shapes.add_textbox(Inches(1.25), Inches(1.1), Inches(10.8), Inches(3.6))
    tf_hero = tb_hero.text_frame
    tf_hero.word_wrap = True

    p0 = tf_hero.paragraphs[0]
    p0.text = "INTERNSHIP MID-REVIEW PRESENTATION"
    p0.font.name = FONT_BODY
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = C_PRIMARY

    p1 = tf_hero.add_paragraph()
    p1.text = "EconoCausal"
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(40)
    p1.font.bold = True
    p1.font.color.rgb = C_DARK_TEXT
    p1.space_before = Pt(8)

    p2 = tf_hero.add_paragraph()
    p2.text = "AI-Integrated Causal Demand Estimation & Dynamic Pricing Decision-Support System"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = C_SECONDARY
    p2.space_before = Pt(6)

    p3 = tf_hero.add_paragraph()
    p3.text = "A semiparametric econometric framework leveraging Double Machine Learning (DML) to isolate structural price elasticity, evaluate retail scenarios under inventory constraints, and enforce business governance."
    p3.font.name = FONT_BODY
    p3.font.size = Pt(12)
    p3.font.color.rgb = C_MUTED
    p3.space_before = Pt(14)

    # Metadata Grid (3 cards along the bottom)
    card_w = Inches(3.75)
    gap = Inches(0.24)
    y_cards = Inches(5.25)
    h_cards = Inches(1.7)

    # Student Card
    c_stu = add_card(slide1, Inches(0.8), y_cards, card_w, h_cards)
    tb_stu = slide1.shapes.add_textbox(Inches(0.95), y_cards + Inches(0.12), card_w - Inches(0.3), h_cards - Inches(0.24))
    tf_stu = tb_stu.text_frame
    tf_stu.word_wrap = True
    p = tf_stu.paragraphs[0]
    p.text = "CANDIDATE DETAILS"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    add_bullet(tf_stu, "Student:", "Ippili Hasika", size=11, space_after=2)
    add_bullet(tf_stu, "Role:", "Data Analyst Intern", size=10.5, space_after=0)

    # Academic Card
    c_acad = add_card(slide1, Inches(0.8) + card_w + gap, y_cards, card_w, h_cards)
    tb_acad = slide1.shapes.add_textbox(Inches(0.8) + card_w + gap + Inches(0.15), y_cards + Inches(0.12), card_w - Inches(0.3), h_cards - Inches(0.24))
    tf_acad = tb_acad.text_frame
    tf_acad.word_wrap = True
    p = tf_acad.paragraphs[0]
    p.text = "ACADEMIC AFFILIATION"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    add_bullet(tf_acad, "College:", "ANITS (Anil Neerukonda Inst. of Tech. & Sci.)", size=10.5, space_after=2)
    add_bullet(tf_acad, "Department:", "Information Technology", size=10.5, space_after=0)

    # Organization Card
    c_org = add_card(slide1, Inches(0.8) + 2*(card_w + gap), y_cards, card_w, h_cards)
    tb_org = slide1.shapes.add_textbox(Inches(0.8) + 2*(card_w + gap) + Inches(0.15), y_cards + Inches(0.12), card_w - Inches(0.3), h_cards - Inches(0.24))
    tf_org = tb_org.text_frame
    tf_org.word_wrap = True
    p = tf_org.paragraphs[0]
    p.text = "INTERNSHIP HOST"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    add_bullet(tf_org, "Organization:", "Infotact Solutions", size=11, space_after=2)
    add_bullet(tf_org, "Review Stage:", "Mid-Review Progress Defense (Days 1–19)", size=10.5, space_after=0)

    add_speaker_note(slide1, 
        "Good morning/afternoon, esteemed reviewers and mentors. My name is Hasika Ippili, currently pursuing Information Technology at ANITS, and working as a Data Analyst Intern at Infotact Solutions. Today, I am excited to present my internship mid-review on 'EconoCausal: AI-Integrated Causal Demand Estimation and Dynamic Pricing'. In this project, we address the critical retail challenge of setting optimal prices by bridging modern machine learning with rigorous econometrics through Double Machine Learning.")

    # =========================================================================
    # SLIDE 2: Problem Statement
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Context & Motivation", "Problem Statement: The Retail Pricing Challenge",
               "Why standard predictive machine learning leads to flawed pricing decisions and revenue destruction.")

    # Left text card
    c_left2 = add_card(slide2, Inches(0.8), Inches(1.5), Inches(4.5), Inches(5.4))
    tb_left2 = slide2.shapes.add_textbox(Inches(0.95), Inches(1.65), Inches(4.2), Inches(5.1))
    tf_l2 = tb_left2.text_frame
    tf_l2.word_wrap = True

    p = tf_l2.paragraphs[0]
    p.text = "CORE BUSINESS CHALLENGES"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.space_after = Pt(10)

    add_bullet(tf_l2, "Price vs. Demand Trade-off:", "Price changes directly drive consumer purchasing. Raising prices may suppress unit sales, while deep discounting sacrifices unit margin.", size=10.5, space_after=10)
    add_bullet(tf_l2, "The Discounting Fallacy:", "Lowering prices increases sales volume, but if demand is price-inelastic, total revenue (P × Q) drops significantly.", size=10.5, space_after=10)
    add_bullet(tf_l2, "Endogeneity & Confounding:", "Prices are not randomized. Retailers set prices based on store location, seasonality, inventory, and promotions, creating severe confounding.", size=10.5, space_after=10)
    add_bullet(tf_l2, "Predictive vs. Causal Gap:", "Standard supervised models forecast demand under existing policies, but cannot answer counterfactual 'what-if' pricing interventions.", size=10.5, space_after=10)
    add_bullet(tf_l2, "Need for Governance:", "Retailers require data-driven pricing engines bounded by inventory limits, cost realities, and statistical uncertainty.", size=10.5, space_after=0)

    # Right Image container
    c_img2 = add_card(slide2, Inches(5.5), Inches(1.5), Inches(7.033), Inches(5.4))
    slide2.shapes.add_picture('presentation_assets/slide2_demand_concept.png', Inches(5.6), Inches(1.8), width=Inches(6.833))

    add_speaker_note(slide2,
        "Slide 2 outlines the retail pricing dilemma. In retail, every pricing decision involves a trade-off. While basic economics suggests that price hikes lower demand and discounts boost sales, the critical business metric is total revenue and gross profit. In observational retail data, price is endogenous—confounded by store prestige, seasons, and stock levels. As shown in the illustration on the right, classical theory assumes high elasticity where discounts pay off, but our empirical retail data reveals near-zero elasticity. Discounting in this environment causes immediate revenue destruction without boosting volume.")

    # =========================================================================
    # SLIDE 3: Project Objectives
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Project Scope", "Project Objectives: Bridging Prediction and Causality",
               "Six structured objectives designed to transition from historical observation to decision intelligence.")

    # 6 Objective Cards in a 2x3 grid
    obj_data = [
        ("1. Data Engineering & Auditing", "Analyze 73,100 store-level retail records across 20 products, 5 stores, and 4 regions over 2 full years (2022–2024). Verify zero missingness and schema integrity.", C_PRIMARY),
        ("2. Exploratory & Temporal Analysis", "Investigate bivariate distributions, price support variation across all 100 product-store pairs, and seasonal demand trajectories to isolate macroeconomic trends.", C_PRIMARY),
        ("3. Baseline Demand Modeling", "Build supervised predictive models (Random Forest, Gradient Boosting, RidgeCV) on chronological holdout data to establish forecasting baselines and identify feature bias.", C_BLUE),
        ("4. Double Machine Learning (DML)", "Implement Robinson's partially linear semiparametric DML with 3-fold cross-fitting and HC3 standard errors to isolate true structural price elasticity from non-linear confounders.", C_PRIMARY),
        ("5. What-If Scenario Simulation", "Develop a constrained pricing simulation engine evaluating candidate price changes (-10% to +10%) bounded by physical inventory caps and 95% confidence intervals.", C_RED),
        ("6. Decision-Support & Governance", "Formulate an evidence-based pricing governance matrix, distinguish top-line revenue from bottom-line profit, and deliver an interactive Streamlit dashboard.", C_SECONDARY)
    ]

    card_w3 = Inches(3.75)
    card_h3 = Inches(2.55)
    x_coords3 = [Inches(0.8), Inches(4.79), Inches(8.78)]
    y_coords3 = [Inches(1.5), Inches(4.3)]

    for i, (title, desc, color) in enumerate(obj_data):
        row = i // 3
        col = i % 3
        x = x_coords3[col]
        y = y_coords3[row]
        
        card = add_card(slide3, x, y, card_w3, card_h3)
        
        # Color bar top of card
        top_bar = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, card_w3, Inches(0.08))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = color
        top_bar.line.fill.background()

        tb = slide3.shapes.add_textbox(x + Inches(0.15), y + Inches(0.15), card_w3 - Inches(0.3), card_h3 - Inches(0.25))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_TITLE
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = C_DARK_TEXT
        p.space_after = Pt(8)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = C_BODY_TEXT

    add_speaker_note(slide3,
        "On Slide 3, we outline the six foundational objectives of EconoCausal. First, we clean and audit two years of daily store transactions. Second, we examine pricing and demand structures across all 100 product-store pairs. Third, we establish a predictive baseline using Random Forest and Ridge regression. Fourth, we implement Double Machine Learning to isolate true price elasticity from high-dimensional confounding. Fifth, we evaluate counterfactual pricing scenarios under real-world inventory constraints. Finally, we establish a managerial decision framework and deliver an interactive dashboard for merchant decision-makers.")

    # =========================================================================
    # SLIDE 4: Dataset Description
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Data Architecture", "Dataset Description & Verified Quality Audit",
               "Daily store-level inventory and sales transactions across two consecutive calendar years (73,100 records).")

    # Left: Table of Columns & Properties
    c_table4 = add_card(slide4, Inches(0.8), Inches(1.5), Inches(7.5), Inches(5.4))
    tb_t4 = slide4.shapes.add_textbox(Inches(0.95), Inches(1.65), Inches(7.2), Inches(5.1))
    tf_t4 = tb_t4.text_frame
    tf_t4.word_wrap = True

    p = tf_t4.paragraphs[0]
    p.text = "CORE TRANSACTION SCHEMA & DESCRIPTIVE STATISTICS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.space_after = Pt(8)

    add_bullet(tf_t4, "Date (731 days):", "Daily timeline from 2022-01-01 to 2024-01-01. Transformed to Year, Month, DayOfWeek.", size=10, space_after=5)
    add_bullet(tf_t4, "Product ID (20 items):", "Identifiers P0001 to P0020 representing 5 distinct merchandise categories.", size=10, space_after=5)
    add_bullet(tf_t4, "Store ID (5 stores):", "Retail locations S001 to S005 spanning 4 geographical regions (East, North, South, West).", size=10, space_after=5)
    add_bullet(tf_t4, "Category (5 departments):", "Clothing (14,626), Electronics (14,521), Furniture (14,699), Groceries (14,611), Toys (14,643).", size=10, space_after=5)
    add_bullet(tf_t4, "Price (Treatment T):", "Unit retail price. Mean = $55.03, Median = $55.01, Range: [$10.04, $99.97].", size=10, space_after=5)
    add_bullet(tf_t4, "Units Sold (Outcome Y):", "Daily sales volume. Mean = 140.2 units, Median = 107.0 units, Range: [0, 499 units].", size=10, space_after=5)
    add_bullet(tf_t4, "Inventory Level:", "Daily on-hand stock. Mean = 273.2 units, Median = 273.0 units, Range: [50, 500 units].", size=10, space_after=5)
    add_bullet(tf_t4, "Units Ordered & Demand Forecast:", "Replenishment orders (mean 110 units) and upstream baseline forecasts (flagged -9.99 anomaly).", size=10, space_after=5)
    add_bullet(tf_t4, "Gross Revenue (Derived):", "Calculated as Price × Units Sold. Mean = $7,717/day, Total Cumulative = $564.1 Million.", size=10, space_after=0)

    # Right: Verified Data Quality Badges
    c_qual4 = add_card(slide4, Inches(8.5), Inches(1.5), Inches(4.033), Inches(5.4))
    tb_q4 = slide4.shapes.add_textbox(Inches(8.65), Inches(1.65), Inches(3.733), Inches(5.1))
    tf_q4 = tb_q4.text_frame
    tf_q4.word_wrap = True

    p = tf_q4.paragraphs[0]
    p.text = "VERIFIED QUALITY AUDIT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.space_after = Pt(8)

    # Metric badge 1
    add_bullet(tf_q4, "Total Rows:", "73,100 verified records across 100 product-store pairs (20 products × 5 stores × 731 days).", size=10, space_after=8)
    add_bullet(tf_q4, "Missing Values:", "0 null values (100% complete across all attributes in raw and cleaned files).", size=10, space_after=8)
    add_bullet(tf_q4, "Duplicate Records:", "0 duplicate rows identified during automated deduplication checks.", size=10, space_after=8)
    add_bullet(tf_q4, "Intra-SKU Price Variation:", "100% of product-store pairs exhibit temporal price changes (62 to 94 distinct price points per pair).", size=10, space_after=8)
    add_bullet(tf_q4, "Forecast Data Anomaly:", "Audit identified negative Demand Forecasts (-9.99). Flagged and isolated from causal estimation.", size=10, space_after=8)
    add_bullet(tf_q4, "Critical Limitation:", "Wholesale Unit Cost (COGS) is absent. The data only tracks retail selling price and sales volume.", size=10, space_after=0, color=C_RED)

    add_speaker_note(slide4,
        "Turning to Slide 4, here is our audited dataset. We analyzed 73,100 store-level records covering 731 consecutive days from January 2022 to January 2024. The dataset covers 20 products across 5 retail stores and 5 categories: Clothing, Electronics, Furniture, Groceries, and Toys. As shown in the quality audit panel, there are zero missing values and zero duplicate records. Crucially, all 100 product-store pairs exhibit substantial temporal price variation, providing sufficient support for causal residualization. We also document that wholesale unit costs are absent, which means all downstream optimizations must target revenue rather than profit.")

    # =========================================================================
    # SLIDE 5: Data Preprocessing and EDA
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Data Engineering & EDA", "Data Preprocessing & Exploratory Data Analysis",
               "Systematic data sanitization, feature engineering, and empirical distributional diagnostics.")

    # Top summary cards (3 pills)
    card_w5 = Inches(3.75)
    c_p1 = add_card(slide5, Inches(0.8), Inches(1.4), card_w5, Inches(0.8))
    tb_p1 = slide5.shapes.add_textbox(Inches(0.9), Inches(1.45), card_w5 - Inches(0.2), Inches(0.7))
    tf_p1 = tb_p1.text_frame
    p = tf_p1.paragraphs[0]
    p.text = "1. Data Sanitization"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p_b = tf_p1.add_paragraph()
    p_b.text = "ISO datetime parsing; verified non-negative prices & sales; schema validation."
    p_b.font.size = Pt(9)
    p_b.font.color.rgb = C_MUTED

    c_p2 = add_card(slide5, Inches(0.8) + card_w5 + Inches(0.24), Inches(1.4), card_w5, Inches(0.8))
    tb_p2 = slide5.shapes.add_textbox(Inches(0.8) + card_w5 + Inches(0.34), Inches(1.45), card_w5 - Inches(0.2), Inches(0.7))
    tf_p2 = tb_p2.text_frame
    p = tf_p2.paragraphs[0]
    p.text = "2. Feature Engineering"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p_b = tf_p2.add_paragraph()
    p_b.text = "Extracted Year (2022-2024), Month (1-12), DOW (0-6), and Gross Revenue."
    p_b.font.size = Pt(9)
    p_b.font.color.rgb = C_MUTED

    c_p3 = add_card(slide5, Inches(0.8) + 2*(card_w5 + Inches(0.24)), Inches(1.4), card_w5, Inches(0.8))
    tb_p3 = slide5.shapes.add_textbox(Inches(0.8) + 2*(card_w5 + Inches(0.24)) + Inches(0.1), Inches(1.45), card_w5 - Inches(0.2), Inches(0.7))
    tf_p3 = tb_p3.text_frame
    p = tf_p3.paragraphs[0]
    p.text = "3. Bivariate Finding"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p_b = tf_p3.add_paragraph()
    p_b.text = "Uncontrolled Price vs Demand correlation r ≈ 0.00; OLS slope = +0.0045 (p=0.77)."
    p_b.font.size = Pt(9)
    p_b.font.color.rgb = C_MUTED

    # Bottom Image Container (Actual Project Charts)
    c_img5 = add_card(slide5, Inches(0.8), Inches(2.35), Inches(11.733), Inches(4.7))
    slide5.shapes.add_picture('presentation_assets/slide5_eda_combined.png', Inches(0.9), Inches(2.45), width=Inches(11.533))

    add_speaker_note(slide5,
        "Slide 5 presents our preprocessing and exploratory findings. We validated schemas, converted dates into cyclic features, and calculated derived revenue. As you can see in the five empirical charts directly from our codebase: Panel 1 shows prices uniformly distributed between $10 and $100. Panel 2 shows daily units sold centered around 140 units with rightward skew. Panel 3 shows that bivariate correlation between price and demand is effectively zero—the OLS regression slope is flat at plus 0.0045. Panels 4 and 5 confirm stable multi-year macro demand and consistent velocity across categories, setting the stage for econometric modeling.")

    # =========================================================================
    # SLIDE 6: Project Methodology and Workflow
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Methodological Pipeline", "End-to-End Project Methodology and Workflow",
               "A structured 10-stage architecture bridging data engineering, predictive modeling, DML, and pricing governance.")

    # Methodology Diagram (Custom 10-step architecture)
    c_img6 = add_card(slide6, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    slide6.shapes.add_picture('presentation_assets/slide6_workflow_diagram.png', Inches(0.95), Inches(1.7), width=Inches(11.433))

    add_speaker_note(slide6,
        "Slide 6 illustrates our 10-stage project pipeline. We start with raw transactional data cleaning and EDA. In Stage 4, we train a predictive demand benchmark. In Stage 5, we formalize our Causal Directed Acyclic Graph (DAG) to isolate true confounders and flag post-treatment colliders like inventory. In Stages 6, 7, and 8, we prepare orthogonal feature matrices, execute Double Machine Learning with 3-fold cross-fitting, and run extensive HC3 validation. Finally, in Stages 9 and 10, we simulate pricing scenarios under inventory constraints and formulate business governance rules.")

    # =========================================================================
    # SLIDE 7: Baseline Demand Modeling
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Predictive Benchmarking", "Baseline Demand Modeling: Predictive vs. Causal",
               "Evaluating supervised forecasting performance and uncovering the post-treatment inventory trap.")

    # Left: Explanation Card
    c_left7 = add_card(slide7, Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.4))
    tb_l7 = slide7.shapes.add_textbox(Inches(0.95), Inches(1.65), Inches(4.0), Inches(5.1))
    tf_l7 = tb_l7.text_frame
    tf_l7.word_wrap = True

    p = tf_l7.paragraphs[0]
    p.text = "PREDICTIVE MODELING AUDIT"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.space_after = Pt(8)

    add_bullet(tf_l7, "Chronological Split:", "80% Train (58,480 rows: Jan 2022–Aug 2023) | 20% Test (14,620 rows: Aug 2023–Jan 2024). Strictly prevents temporal data leakage.", size=10, space_after=6)
    add_bullet(tf_l7, "Core Model Tested:", "RandomForestRegressor (100 trees, default depth) combined with ColumnTransformer (One-Hot Encoding for categorical features).", size=10, space_after=6)
    add_bullet(tf_l7, "Verified Holdout Performance:", "• Random Forest: MAE = 69.51, RMSE = 89.36, R² = 0.3184\n• HistGradBoost: MAE = 68.68, RMSE = 87.81, R² = 0.3419\n• RidgeCV (L2): MAE = 68.65, RMSE = 87.65, R² = 0.3443\n• Dummy Baseline: MAE = 88.81, R² = 0.0000", size=9.5, space_after=6)
    add_bullet(tf_l7, "The Predictive vs. Causal Trap:", "Supervised models learn E[Y | Price, Inventory]. They capture associative patterns for replenishment forecasting, but fail completely at counterfactual pricing questions (∂Y/∂Price).", size=10, space_after=6)
    add_bullet(tf_l7, "The Collider Finding:", "Inventory Level drives 0.7118 test R² drop in permutation importance, while Price accounts for only 0.0029. Inventory is an operational stock cap, not organic demand!", size=10, space_after=0, color=C_RED)

    # Right: Benchmark Chart & Feature Importance
    c_img7 = add_card(slide7, Inches(5.3), Inches(1.5), Inches(7.233), Inches(5.4))
    slide7.shapes.add_picture('presentation_assets/slide7_model_benchmarks.png', Inches(5.45), Inches(1.75), width=Inches(6.933))

    add_speaker_note(slide7,
        "Slide 7 covers our baseline predictive demand modeling. We trained Random Forest, Gradient Boosting, and Ridge models using a strict 80-20 chronological split to avoid data leakage. The Random Forest achieved an R-squared of 0.3184 and an MAE of 69.5 units, outperforming the mean baseline. However, as the right-hand chart shows, permutation importance reveals a massive trap: Inventory Level accounts for over 71% of test R-squared drop, while Price accounts for less than 0.3%. In retail, inventory is a post-treatment stocking proxy—a collider! This proves why standard supervised regression cannot be used for price optimization.")

    # =========================================================================
    # SLIDE 8: Double Machine Learning (DML)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Econometric Foundation", "Double Machine Learning (DML): Causal Identification",
               "Robinson's partially linear model with Neyman orthogonality and 3-fold cross-fitting.")

    # Technical DML Workflow Diagram
    c_img8 = add_card(slide8, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4))
    slide8.shapes.add_picture('presentation_assets/slide8_dml_architecture.png', Inches(0.95), Inches(1.7), width=Inches(11.433))

    add_speaker_note(slide8,
        "Slide 8 is our core technical econometric slide. In retail pricing, correlation does not imply causation because confounding factors—like product quality, store tier, and seasonality—influence both price and demand. Double Machine Learning, pioneered by Chernozhukov and based on Robinson's 1988 partially linear model, solves this. In Stage 1, we use ExtraTrees regressors to predict Units Sold from controls, and Price from controls, using 3-fold cross-fitting to eliminate overfitting bias. In Stage 2, we subtract these predictions to obtain orthogonal residuals. In Stage 3, we regress the demand residuals on price residuals using HC3 robust standard errors to isolate the unconfounded causal price elasticity.")

    # =========================================================================
    # SLIDE 9: Pricing Scenario Analysis
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Scenario Simulation", "Pricing Scenario Analysis: Constrained What-If Simulation",
               "Evaluating candidate price changes (-10% to +10%) under physical inventory caps and uncertainty.")

    # Left: Explanation Card
    c_left9 = add_card(slide9, Inches(0.8), Inches(1.5), Inches(4.5), Inches(5.4))
    tb_l9 = slide9.shapes.add_textbox(Inches(0.95), Inches(1.65), Inches(4.2), Inches(5.1))
    tf_l9 = tb_l9.text_frame
    tf_l9.word_wrap = True

    p = tf_l9.paragraphs[0]
    p.text = "SIMULATION ENGINE SPECIFICATION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.space_after = Pt(8)

    add_bullet(tf_l9, "Local Demand Equation:", "Q_hat(P) = min(InventoryCap, max(0, Q_0 + θ·ΔP)). Evaluates discrete price steps: -10%, -5%, Base, +5%, +10%.", size=10, space_after=6)
    add_bullet(tf_l9, "Benchmark Case (P0001 at S001):", "• Base Price: $55.13 | Base Demand: 173.0 units\n• Base Daily Revenue: $9,537.49 | Stock Cap: 195 units", size=10, space_after=6)
    add_bullet(tf_l9, "Discounting Disaster (-10%):", "Candidate Price = $49.62. Estimated Demand = 172.94 units. Realized Revenue = $8,580.81 (an immediate -$956.68 or -10.03% collapse).", size=10, space_after=6, color=C_RED)
    add_bullet(tf_l9, "Simulated Price Increase (+10%):", "Candidate Price = $60.64. Estimated Demand = 173.06 units. Revenue = $10,494.82 (+10.04%).", size=10, space_after=6, color=C_SECONDARY)
    add_bullet(tf_l9, "Revenue ≠ Profit Warning:", "Revenue is P × Q. Profit is (P - c) × Q - F. Because wholesale procurement cost (c) is missing, claiming +10% price hikes are 'optimal' is invalid. Governance mandates micro-pilots (±2%).", size=10, space_after=0, color=C_RED)

    # Right: Scenario Bar Chart
    c_img9 = add_card(slide9, Inches(5.5), Inches(1.5), Inches(7.033), Inches(5.4))
    slide9.shapes.add_picture('presentation_assets/slide9_pricing_scenarios.png', Inches(5.65), Inches(1.75), width=Inches(6.733))

    add_speaker_note(slide9,
        "Slide 9 demonstrates our constrained pricing simulator for Product P0001 at Store S001. Using our DML estimate, we test 5 pricing scenarios from minus 10% to plus 10%. Look at the results: because demand volume is flat at approximately 173 units, a 10% discount reduces daily revenue by $956—a 10% loss with zero volume compensation! Conversely, a 10% price hike simulates a 10% revenue gain. However, we explicitly highlight that Revenue is NOT Profit. Without Cost of Goods Sold data, aggressive price hikes could damage customer retention. We therefore recommend maintaining baseline prices and testing small plus 2% adjustments in phased micro-pilots.")

    # =========================================================================
    # SLIDE 10: Results and Key Learnings
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Empirical Findings", "Results & Key Learnings: 18-Specification Robustness",
               "Verified econometric parameters, confidence bounds, and multi-model stress testing.")

    # Left: Findings Cards (Summary table / text)
    c_left10 = add_card(slide10, Inches(0.8), Inches(1.5), Inches(4.3), Inches(5.4))
    tb_l10 = slide10.shapes.add_textbox(Inches(0.95), Inches(1.65), Inches(4.0), Inches(5.1))
    tf_l10 = tb_l10.text_frame
    tf_l10.word_wrap = True

    p = tf_l10.paragraphs[0]
    p.text = "VERIFIED PROJECT RESULTS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.space_after = Pt(8)

    add_bullet(tf_l10, "Primary DML Estimate (Spec 1):", "θ = +0.0107 units per $1 price change\n• 95% CI: [-0.0197, +0.0411]\n• HC3 Std Error: 0.0155 | p-value: 0.4899\n• Structurally price-inelastic (fails to reject θ=0).", size=9.5, space_after=6)
    add_bullet(tf_l10, "Collider Sensitivity (Spec 2):", "Adding Inventory Level yields θ = -0.0195 (p=0.119). Confirms severe collider shift when conditioning on post-treatment stock.", size=9.5, space_after=6)
    add_bullet(tf_l10, "18/18 Specifications Span Zero:", "Zero out of 18 model specifications (different nuisance models, categories, regions, years) achieve significance at α=0.05.", size=9.5, space_after=6)
    add_bullet(tf_l10, "Category Elasticities:", "Clothing (θ = -0.022), Electronics (θ = -0.0005), Furniture (θ = -0.015), Groceries (θ = +0.043), Toys (θ = +0.002). All cross zero.", size=9.5, space_after=6)
    add_bullet(tf_l10, "Operational Governance:", "Strictly reject automated discounting. Demand elasticity does not justify price cuts.", size=9.5, space_after=0, color=C_PRIMARY)

    # Right: Robustness Forest Plot
    c_img10 = add_card(slide10, Inches(5.3), Inches(1.5), Inches(7.233), Inches(5.4))
    slide10.shapes.add_picture('presentation_assets/slide10_dml_forest_plot.png', Inches(5.45), Inches(1.75), width=Inches(6.933))

    add_speaker_note(slide10,
        "Slide 10 presents our verified econometric results and key learnings. In our primary DML specification, the estimated price coefficient is plus 0.0107 with a p-value of 0.4899 and a 95% confidence interval of minus 0.0197 to plus 0.0411. Because this confidence interval spans zero, demand is structurally price-inelastic. To prove this was not an artifact of model choice, we conducted an 18-specification robustness analysis across alternative nuisance models, controls, years, and categories. As shown in the forest plot on the right, all 18 specifications cross the red null line. This is a profound finding: discounting in this retail catalog destroys revenue.")

    # =========================================================================
    # SLIDE 11: Challenges, Limitations and Future Scope
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11)
    add_header(slide11, "Critical Appraisal", "Project Challenges, Limitations & Future Scope",
               "Honest evaluation of data constraints, econometric trade-offs, and future research roadmap.")

    # Left Card: Challenges & Limitations
    c_left11 = add_card(slide11, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.4))
    tb_l11 = slide11.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.3), Inches(5.1))
    tf_l11 = tb_l11.text_frame
    tf_l11.word_wrap = True

    p = tf_l11.paragraphs[0]
    p.text = "CHALLENGES & DATA LIMITATIONS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p.space_after = Pt(10)

    add_bullet(tf_l11, "Unobserved Confounding:", "Observational retail data lacks marketing campaigns, promotional discounts, foot traffic, and competitor pricing actions.", size=10, space_after=8)
    add_bullet(tf_l11, "Missing Unit Cost Data (COGS):", "The database contains no wholesale cost information. Maximizing gross revenue is not equivalent to maximizing net profit.", size=10, space_after=8)
    add_bullet(tf_l11, "Inventory Timestamp Ambiguity:", "If inventory is logged at end-of-day, conditioning on it introduces post-treatment collider bias, distorting treatment effects.", size=10, space_after=8)
    add_bullet(tf_l11, "Linear Treatment Assumption:", "Partially linear DML assumes constant marginal price sensitivity, which may not hold for extreme price shocks beyond ±15%.", size=10, space_after=8)
    add_bullet(tf_l11, "Statistical Non-Significance:", "With p=0.4899, pricing outputs serve as decision-support heuristics rather than autonomous production algorithms.", size=10, space_after=0)

    # Right Card: Completed Progress & Future Scope
    c_right11 = add_card(slide11, Inches(6.8), Inches(1.5), Inches(5.733), Inches(5.4))
    tb_r11 = slide11.shapes.add_textbox(Inches(7.0), Inches(1.65), Inches(5.333), Inches(5.1))
    tf_r11 = tb_r11.text_frame
    tf_r11.word_wrap = True

    p = tf_r11.paragraphs[0]
    p.text = "FUTURE RESEARCH & EXTENSIONS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY
    p.space_after = Pt(10)

    add_bullet(tf_r11, "Heterogeneous Treatment Effects (HTE):", "Deploy Causal Forests and generalized DML to explore whether specific luxury or perishable SKUs exhibit significant price sensitivity.", size=10, space_after=8)
    add_bullet(tf_r11, "Cost Modeling & Profit Optimization:", "Acquire or simulate wholesale margin structures to enable true constrained profit maximization: Π = (P - c)·Q - F.", size=10, space_after=8)
    add_bullet(tf_r11, "Completed Streamlit Dashboard:", "Production dashboard in app.py with 8 interactive modules, real-time what-if sliders, and governance matrices already built!", size=10, space_after=8, color=C_SECONDARY)
    add_bullet(tf_r11, "A/B Micro-Pilot Testing:", "Design a randomized store-level pricing pilot (±2% price changes) across select retail clusters to establish ground-truth causal elasticity.", size=10, space_after=8)
    add_bullet(tf_r11, "Cross-SKU Cannibalization:", "Model cross-price elasticities to capture substitution effects across competing products within the same merchandise department.", size=10, space_after=0)

    add_speaker_note(slide11,
        "Slide 11 addresses our project limitations and future roadmap. Academic and practical honesty is essential: our sales data lacks marketing promotions, competitor prices, and wholesale procurement costs. Furthermore, inventory timing must be audited to prevent collider bias. In terms of future work, we plan to implement Causal Forests for heterogeneous subgroup treatment effects, acquire cost structures to optimize profit rather than just revenue, and formulate an A/B micro-pilot proposal. I am also proud to report that our interactive Streamlit dashboard is already fully implemented in app.py!")

    # =========================================================================
    # SLIDE 12: Conclusion & Q&A
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12)

    # Hero Banner Card
    c_hero12 = add_card(slide12, Inches(0.8), Inches(0.8), Inches(11.733), Inches(4.3), bg_color=C_CARD_BG, border_color=C_CARD_BORDER)
    l_bar12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(0.18), Inches(4.3))
    l_bar12.fill.solid()
    l_bar12.fill.fore_color.rgb = C_PRIMARY
    l_bar12.line.fill.background()

    tb_h12 = slide12.shapes.add_textbox(Inches(1.25), Inches(1.05), Inches(10.8), Inches(3.8))
    tf_h12 = tb_h12.text_frame
    tf_h12.word_wrap = True

    p = tf_h12.paragraphs[0]
    p.text = "MID-REVIEW PROJECT SUMMARY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_PRIMARY

    p_t = tf_h12.add_paragraph()
    p_t.text = "Conclusion: EconoCausal Impact & Deliverables"
    p_t.font.name = FONT_TITLE
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = C_DARK_TEXT
    p_t.space_before = Pt(6)

    add_bullet(tf_h12, "Problem Solved:", "Addressed the flaw of using naive predictive regression for retail pricing, which mistakes correlation for causation and overlooks inventory colliders.", size=10.5, space_after=6)
    add_bullet(tf_h12, "Rigorous Methodology:", "Integrated Double Machine Learning (Robinson 1988) with 3-fold cross-fitting, ExtraTrees nuisance models, and HC3 robust standard errors.", size=10.5, space_after=6)
    add_bullet(tf_h12, "Verified Finding:", "Demonstrated that demand is structurally inelastic (θ = +0.0107, p = 0.49), proving that discounting destroys revenue across all 18 specifications.", size=10.5, space_after=6)
    add_bullet(tf_h12, "Delivered Assets:", "19 engineering daily logs, 13 verified Jupyter notebooks, comprehensive validation modules, and a fully interactive Streamlit application.", size=10.5, space_after=0)

    # Q&A Footer Banner Card
    c_qa = add_card(slide12, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.5), bg_color=C_PILL_BG, border_color=C_ACCENT)
    tb_qa = slide12.shapes.add_textbox(Inches(1.2), Inches(5.5), Inches(11.0), Inches(1.2))
    tf_qa = tb_qa.text_frame
    tf_qa.word_wrap = True

    p_qa1 = tf_qa.paragraphs[0]
    p_qa1.text = "Thank You — Questions & Answers"
    p_qa1.font.name = FONT_TITLE
    p_qa1.font.size = Pt(22)
    p_qa1.font.bold = True
    p_qa1.font.color.rgb = C_PRIMARY
    p_qa1.alignment = PP_ALIGN.CENTER

    p_qa2 = tf_qa.add_paragraph()
    p_qa2.text = "Ippili Hasika  •  Data Analyst Intern  •  Infotact Solutions  •  ANITS Information Technology"
    p_qa2.font.name = FONT_BODY
    p_qa2.font.size = Pt(11)
    p_qa2.font.color.rgb = C_DARK_TEXT
    p_qa2.alignment = PP_ALIGN.CENTER
    p_qa2.space_before = Pt(4)

    add_speaker_note(slide12,
        "In conclusion, EconoCausal demonstrates the critical importance of causal inference in business decision-making. By applying Double Machine Learning rather than relying on associative predictions, we uncovered that demand is structurally inelastic, preventing disastrous discounting policies. Over the past 19 days, we have delivered clean data pipelines, predictive benchmarks, verified econometric models, 18 robustness checks, and an interactive decision-support application. Thank you so much for your time and guidance. I would be delighted to take any questions.")

    # Save presentation
    output_path = 'EconoCausal_Internship_Mid_Review_Presentation.pptx'
    prs.save(output_path)
    print(f"Successfully created presentation: {output_path}")

if __name__ == '__main__':
    create_presentation()
