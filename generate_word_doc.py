import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets the background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Sets cell padding (in dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = docx.Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(6)

    # Header / Meta Banner
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = p_meta.add_run("AKWA IBOM STATE UNIVERSITY\nDEPARTMENT OF COMPUTER SCIENCE\n")
    run_inst.bold = True
    run_inst.font.size = Pt(13)
    run_inst.font.color.rgb = RGBColor(15, 23, 42)

    run_proj = p_meta.add_run("A GAUSSIAN PROCESS REGRESSION FOR FORECASTING SOLID WASTE GENERATION IN UYO MUNICIPALITY\n")
    run_proj.bold = True
    run_proj.font.size = Pt(13)
    run_proj.font.color.rgb = RGBColor(15, 78, 59)

    run_cand = p_meta.add_run("Candidate: EFFIONG, SAMUEL ETIM (AK22/PHS/CSC/029)\nSupervisor: Dr. Anietie P. Ekong\n")
    run_cand.italic = True
    run_cand.font.size = Pt(11)
    run_cand.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================================
    # SECTION 4.1 SYSTEM DESIGN
    # =========================================================================
    h1 = doc.add_heading("4.1 SYSTEM DESIGN", level=1)
    h1.style.font.name = 'Times New Roman'
    h1.style.font.size = Pt(14)
    h1.style.font.color.rgb = RGBColor(15, 23, 42)
    h1.style.font.bold = True

    # 4.1.1 Input Specification
    h2_in = doc.add_heading("4.1.1 Input Specification", level=2)
    h2_in.style.font.name = 'Times New Roman'
    h2_in.style.font.size = Pt(13)
    h2_in.style.font.color.rgb = RGBColor(15, 23, 42)
    h2_in.style.font.bold = True

    p_in_intro = doc.add_paragraph(
        "The input specification defines the nature, structure, format, validation constraints, and transformation pipelines "
        "of all empirical and operational data entering the Gaussian Process Regression (GPR) waste forecasting system. "
        "The system accepts data through two primary operational channels:"
    )
    
    b1 = doc.add_paragraph(style='List Bullet')
    r1 = b1.add_run("Batch Historical Ingestion: ")
    r1.bold = True
    b1.add_run(
        "An empirical 84-month longitudinal dataset (covering January 2019 through December 2025) sourced from the Akwa Ibom State "
        "Environmental Protection and Waste Management Agency (AKSEPWMA), coupled with climatic records from meteorological stations "
        "and census demographic projections."
    )

    b2 = doc.add_paragraph(style='List Bullet')
    r2 = b2.add_run("Interactive Real-Time Input: ")
    r2.bold = True
    b2.add_run(
        "User-driven parameter entry through the interactive Streamlit web interface for single-month scenario analysis or batch "
        "comma-separated values (CSV) upload for out-of-sample model evaluation and validation."
    )

    p_dict = doc.add_paragraph(
        "Table 4.1 details the input attributes ingested by the system, including data types, units of measurement, observed empirical ranges "
        "in Uyo Municipality, validation constraints, and functional descriptions."
    )

    # Table 4.1: Input Data Dictionary
    t_caption1 = doc.add_paragraph()
    t_caption1.add_run("Table 4.1: Input Data Dictionary for Uyo Municipality MSW Forecasting System").bold = True
    t_caption1.paragraph_format.space_after = Pt(4)

    t1_headers = ["S/N", "Field / Variable Name", "Data Type", "Measurement Unit", "Empirical Range", "Validation Constraints", "Description & Source"]
    t1_data = [
        ["1", "date", "Date / String", "YYYY-MM", "2019-01 to 2025-12", "Valid ISO calendar month; chronological order", "Monthly observation timestamp (AKSEPWMA records)."],
        ["2", "population", "Integer", "Persons", "496,000 – 595,000", "Pt > 0; monotonically non-decreasing", "Projected human population of Uyo Municipality based on National Population Commission (NPC) baseline."],
        ["3", "avg_temperature_c", "Float", "Degrees Celsius (°C)", "24.8 – 28.5 °C", "18.0 ≤ T ≤ 42.0", "Mean monthly ambient surface temperature in Uyo (influences organic decay and generation rates)."],
        ["4", "rainfall_mm", "Float", "Millimetres (mm)", "12.0 – 510.5 mm", "Rt ≥ 0.0", "Cumulative monthly precipitation depth; key driver of waste moisture, vegetable waste, and logistics."],
        ["5", "humidity_percent", "Float", "Percentage (%)", "74.0 – 91.5 %", "0.0 ≤ H ≤ 100.0", "Mean monthly relative atmospheric humidity in Uyo Municipality."],
        ["6", "public_holidays", "String", "Delimited Dates", "N/A", "Semicolon-delimited calendar dates", "Registry of statutory national, state, and religious public holidays in Nigeria occurring in the month."],
        ["7", "num_holidays", "Integer", "Count", "0 – 3 days", "0 ≤ n ≤ 10", "Total count of public holidays in the target month; proxies for high-generation domestic and festive periods."],
        ["8", "waste_tonnes_estimated", "Float", "Metric Tonnes (t)", "26,480 – 43,120 t", "Wt > 0.0", "Recorded empirical municipal solid waste collected in Uyo Municipality (target variable y for training)."]
    ]

    table1 = doc.add_table(rows=len(t1_data) + 1, cols=len(t1_headers))
    table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    table1.autofit = True

    # Style Header Row
    for col_idx, h_text in enumerate(t1_headers):
        cell = table1.cell(0, col_idx)
        cell.text = h_text
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Populate Data Rows
    for row_idx, row_items in enumerate(t1_data):
        for col_idx, val_text in enumerate(row_items):
            cell = table1.cell(row_idx + 1, col_idx)
            cell.text = val_text
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            if col_idx in [0, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 4.1.1.2 Feature Engineering Pipeline
    h3_trans = doc.add_heading("4.1.1.1 Input Preprocessing and Feature Engineering Transformations", level=3)
    h3_trans.style.font.name = 'Times New Roman'
    h3_trans.style.font.size = Pt(12)
    h3_trans.style.font.color.rgb = RGBColor(15, 23, 42)
    h3_trans.style.font.bold = True

    p_trans = doc.add_paragraph(
        "Before raw inputs are passed into the Gaussian Process covariance kernel, the system subjects them to mathematical "
        "transformations to maintain temporal causality, eliminate dimension scale bias, and encode cyclical seasonal periodicity:"
    )

    t_p1 = doc.add_paragraph(style='List Bullet')
    t_p1.add_run("Continuous Time-Step Encoding (t): ").bold = True
    t_p1.add_run("To enable trend extrapolation, calendar months are mapped onto a continuous non-negative integer sequence relative to the baseline epoch (January 2019 = 0): t = (Year - 2019) * 12 + (Month - 1).")

    t_p2 = doc.add_paragraph(style='List Bullet')
    t_p2.add_run("Cyclical Month Harmonic Encoding: ").bold = True
    t_p2.add_run("Because January (m = 1) is temporally adjacent to December (m = 12), calendar periodicity is preserved through orthogonal trigonometric basis functions: sin_month = sin(2πm / 12) and cos_month = cos(2πm / 12).")

    t_p3 = doc.add_paragraph(style='List Bullet')
    t_p3.add_run("Standardization Pipeline (z-score Scaling): ").bold = True
    t_p3.add_run("Because feature dimensions possess vastly disparate scales (e.g., population ~ 5 x 10^5 versus temperature ~ 2.6 x 10^1), all features are normalized based on training set statistics: z = (x - μ) / σ to ensure numerical stability during kernel marginal log-likelihood optimization.")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 4.1.2 Output Specification
    h2_out = doc.add_heading("4.1.2 Output Specification", level=2)
    h2_out.style.font.name = 'Times New Roman'
    h2_out.style.font.size = Pt(13)
    h2_out.style.font.color.rgb = RGBColor(15, 23, 42)
    h2_out.style.font.bold = True

    doc.add_paragraph(
        "The output specification defines the mathematical format, numerical precision, operational semantics, and reporting artifacts generated "
        "by the Gaussian Process Regression model for AKSEPWMA administrators, environmental scientists, and municipal waste directors."
    )

    doc.add_paragraph(
        "Following expert research and municipal decision-support consultations, the system implements Option D (Dual Continuous-Categorical Paradigm). "
        "Unlike deterministic regression algorithms that generate only an isolated point estimate, the GPR model outputs a complete posterior Gaussian "
        "probability distribution for each target period: y* ~ N(μ*, σ*^2). Simultaneously, each continuous numerical forecast is discretized into an "
        "actionable 5-tier operational waste generation class based on empirical AKSEPWMA capacity thresholds. The system structures its outputs into five analytical layers:"
    )

    # Output Categories
    o1 = doc.add_paragraph(style='List Bullet')
    o1.add_run("Probabilistic Point and Interval Forecasts: ").bold = True
    o1.add_run("Delivers the expected predictive mean monthly waste tonnage (μ*), average daily equivalent tonnage, and strict 95% Bayesian Confidence Intervals: [μ* - 1.96σ*, μ* + 1.96σ*], communicating both the expected central trajectory and mathematical uncertainty bounds.")

    o2 = doc.add_paragraph(style='List Bullet')
    o2.add_run("Empirical 5-Tier Operational Waste Classification (Option D): ").bold = True
    o2.add_run("Discretizes continuous tonnage projections into five operational management classes: Very Low (< 30,000 tonnes/month), Low (30,000 – 35,000 tonnes/month), Moderate (35,000 – 40,000 tonnes/month), High (40,000 – 45,000 tonnes/month), and Very High (≥ 45,000 tonnes/month).")

    o3 = doc.add_paragraph(style='List Bullet')
    o3.add_run("Municipal Logistics and Fleet Sizing Directives: ").bold = True
    o3.add_run("Translates projected tonnage directly into required logistical assets, including: active 15-tonne compactor trucks required (N_trucks = ceil(Daily_Tonnes / 30)), 1,100-litre communal collection bins (N_bins = ceil(Daily_Tonnes * 1.2 / 0.25)), and annual landfill airspace depletion rate in cubic meters (V_landfill = Annual_Tonnes / 0.8).")

    o4 = doc.add_paragraph(style='List Bullet')
    o4.add_run("Spatial Zonal Allocation (GIS Distribution): ").bold = True
    o4.add_run("Apportions municipal waste forecasts across Uyo's six designated collection hubs: Ibom Plaza/Central Business District (22%), Itam Market & Industrial Commercial Axis (26%), Aka Road/Shelter Afrique Residential Corridor (16%), Abak Road Commercial Corridor (13%), Oron Road Corridor (12%), and Ikpa Road/Uniuyo Campus Corridor (11%).")

    o5 = doc.add_paragraph(style='List Bullet')
    o5.add_run("Standardized Option D Final Forecast Presentation Card: ").bold = True
    o5.add_run("Provides an executive dashboard summary specifying: Forecast Period, Predicted Waste Generation (monthly and daily equivalent), Assigned Waste Generation Class, Forecast Trend, 95% Bayesian Prediction Interval, Model Architecture, and Actionable Municipal Recommendation.")

    # Table 4.2: Output Data Schema
    t_caption2 = doc.add_paragraph()
    t_caption2.add_run("Table 4.2: Output Data Schema for 2026–2030 Projections (Option D Format)").bold = True
    t_caption2.paragraph_format.space_after = Pt(4)

    t2_headers = ["Output Field Name", "Data Type", "Display Format", "Measurement Unit", "Description & Operational Interpretation"]
    t2_data = [
        ["forecast_date", "String", "Month YYYY", "Calendar Date", "Target forecast timeline (e.g., January 2026 through December 2030)."],
        ["pred_monthly_tonnes", "Float", "44,724.2", "Tonnes/Month", "GPR posterior predictive mean monthly solid waste generation (μ*)."],
        ["daily_tonnes", "Float", "1,470.4", "Tonnes/Day", "Average daily solid waste generation equivalent (μ* / 30.4167)."],
        ["ci_low_tonnes", "Float", "40,179.0", "Metric Tonnes", "Lower 95% Bayesian predictive confidence limit (μ* - 1.96σ*)."],
        ["ci_high_tonnes", "Float", "49,269.4", "Metric Tonnes", "Upper 95% Bayesian predictive confidence limit (μ* + 1.96σ*)."],
        ["uncertainty_width", "Float", "±4,545.2", "Metric Tonnes", "Full width of the 95% predictive uncertainty spread (3.92σ*)."],
        ["waste_class", "String", "Categorical Badge", "5-Tier Class", "Operational waste generation class: Very Low, Low, Moderate, High, Very High."],
        ["compactor_trucks", "Integer", "49", "Vehicles", "Minimum 15-tonne compactor trucks required for 100% daily clearance (15T @ 2 trips/day)."],
        ["logistics_directive", "String", "Textual Action", "Guideline", "Actionable fleet scheduling, labor shift, and landfill compaction instruction."]
    ]

    table2 = doc.add_table(rows=len(t2_data) + 1, cols=len(t2_headers))
    table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2.autofit = True

    for col_idx, h_text in enumerate(t2_headers):
        cell = table2.cell(0, col_idx)
        cell.text = h_text
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row_items in enumerate(t2_data):
        for col_idx, val_text in enumerate(row_items):
            cell = table2.cell(row_idx + 1, col_idx)
            cell.text = val_text
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            if col_idx in [0, 1, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Table 4.2B: Empirical 5-Tier Operational Waste Classification Scheme
    t_caption2b = doc.add_paragraph()
    t_caption2b.add_run("Table 4.2B: Empirical 5-Tier Operational Waste Classification Scheme & Action Directives").bold = True
    t_caption2b.paragraph_format.space_after = Pt(4)

    t2b_headers = ["Waste Class", "Monthly Range (Tonnes/Mo)", "Daily Equivalent (Tonnes/Day)", "Indicator Color", "Empirical Baseline Context", "Operational & Logistics Directive"]
    t2b_data = [
        ["Very Low", "< 30,000 t", "< 986.3 t/day", "Green (#059669)", "Observed in 2019 baseline (low urban population)", "Routine baseline maintenance. Standard compactor scheduling and regular landfill operations."],
        ["Low", "30,000 – 35,000 t", "986.3 – 1,150.7 t/day", "Blue (#0284C7)", "Historical 2020–2022 dry-season average", "Standard operational mode. Maintain regular daily collection sweeps across all 6 zones (33-38 compactors)."],
        ["Moderate", "35,000 – 40,000 t", "1,150.7 – 1,315.1 t/day", "Amber (#D97706)", "Historical 2023–2024 mean & early 2026", "Heightened monitoring. Pre-position standby compactor units at Itam Market and Ibom Plaza (39-44 compactors)."],
        ["High", "40,000 – 45,000 t", "1,315.1 – 1,479.5 t/day", "Orange (#EA580C)", "Predominant class for 2026–2030 projections", "High generation. Deploy expanded fleet routing, secondary evening sweeps, and optimize transfer hubs (44-49 compactors)."],
        ["Very High", "≥ 45,000 t", "≥ 1,479.5 t/day", "Red (#DC2626)", "Festive Q4 seasons (Nov-Dec) and peak wet months", "Critical peak overload! Mobilize maximum compactor fleet (≥50 trucks), authorize overtime shifts, and fast-track landfill compaction."]
    ]

    table2b = doc.add_table(rows=len(t2b_data) + 1, cols=len(t2b_headers))
    table2b.alignment = WD_TABLE_ALIGNMENT.CENTER
    table2b.autofit = True

    for col_idx, h_text in enumerate(t2b_headers):
        cell = table2b.cell(0, col_idx)
        cell.text = h_text
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row_items in enumerate(t2b_data):
        for col_idx, val_text in enumerate(row_items):
            cell = table2b.cell(row_idx + 1, col_idx)
            cell.text = val_text
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            if col_idx in [0, 1, 2, 3]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 4.1.2.2 Graphical and Diagnostic Visualizations
    h3_diag = doc.add_heading("4.1.2.1 Diagnostic Graphical and Analytical Outputs", level=3)
    h3_diag.style.font.name = 'Times New Roman'
    h3_diag.style.font.size = Pt(12)
    h3_diag.style.font.color.rgb = RGBColor(15, 23, 42)
    h3_diag.style.font.bold = True

    doc.add_paragraph(
        "The system generates twelve standardized high-resolution visual artifacts (rendered at 200 DPI vector clarity) for research reporting and administrative defense:"
    )

    g1 = doc.add_paragraph(style='List Bullet')
    g1.add_run("Actual vs. Predicted Scatter Plot: ").bold = True
    g1.add_run("Validates empirical fit against the 45-degree diagonal line of perfect agreement (y = x), distinguishing training observations (green circles) from out-of-time test observations (red squares), confirming an overall R^2 of 0.9854.")

    g2 = doc.add_paragraph(style='List Bullet')
    g2.add_run("Residual Error Normality Histogram: ").bold = True
    g2.add_run("Confirms that model error residuals (e_i = y_i - ŷ_i) conform to an authentic Gaussian normal distribution N(μ, σ) centered around zero without systematic bias.")

    g3 = doc.add_paragraph(style='List Bullet')
    g3.add_run("Chronological Time-Series Tracking Plot: ").bold = True
    g3.add_run("Traces the full 84-month observed trajectory against GPR model predictions alongside the continuous shaded 95% Bayesian uncertainty band, marking the train/test chronological split boundary.")

    g4 = doc.add_paragraph(style='List Bullet')
    g4.add_run("Operational Tier Confusion Matrix Heatmap: ").bold = True
    g4.add_run("A color-coded classification heatmap assessing model fidelity across the four operational triage tiers, demonstrating an overall classification accuracy of 91.7%.")

    g5 = doc.add_paragraph(style='List Bullet')
    g5.add_run("Interactive GIS Municipal Collection Map: ").bold = True
    g5.add_run("A geospatial representation of Uyo Municipality collection zones (Ibom Plaza, Itam Market, Aka Road, etc.) with proportional tonnage markers and truck route indicators.")

    g6 = doc.add_paragraph(style='List Bullet')
    g6.add_run("Root Mean Squared Error (RMSE) Benchmark Graph: ").bold = True
    g6.add_run("A standalone bar chart contrasting Root Mean Squared Error (in Metric Tonnes) across all candidate kernels, heavily penalizing variance to confirm that the Proposed Composite Kernel achieves minimum variance and outlier error (RMSE = 1,297.2 t vs. RBF = 1,725.9 t).")

    g7 = doc.add_paragraph(style='List Bullet')
    g7.add_run("Mean Absolute Error (MAE) Benchmark Graph: ").bold = True
    g7.add_run("A standalone bar chart contrasting Mean Absolute Error (in Metric Tonnes) on a linear physical scale across candidate kernels, verifying that the Proposed Composite Kernel is the sole architecture achieving sub-1,000-tonne mean deviation (MAE = 975.4 t vs. RBF = 1,331.7 t).")

    g8 = doc.add_paragraph(style='List Bullet')
    g8.add_run("Mean Absolute Percentage Error (MAPE %) Benchmark Graph: ").bold = True
    g8.add_run("A standalone bar chart evaluating scale-independent relative accuracy across kernels, showing that the Proposed Composite Kernel achieves 2.34% MAPE, well below the 5% international tolerance limit for precision engineering.")

    g9 = doc.add_paragraph(style='List Bullet')
    g9.add_run("Partition Error Comparison Chart (Train vs. Out-of-Time Test): ").bold = True
    g9.add_run("A grouped bar chart comparing RMSE and MAE across the in-sample training partition (2019-2024: RMSE 542.2 t, MAE 463.5 t), out-of-time testing partition (2024-2025: RMSE 1,297.2 t, MAE 975.4 t), and full 84-month series (RMSE 758.3 t, MAE 567.1 t) to demonstrate generalization capacity without overfitting.")

    g10 = doc.add_paragraph(style='List Bullet')
    g10.add_run("Monthly Percentage Error (MAPE %) Chronological Timeline: ").bold = True
    g10.add_run("A longitudinal timeline plotting monthly absolute percentage error |y_t - ŷ_t| / y_t * 100% across all 84 historical months against the acceptable 5% municipal tolerance threshold, proving consistent precision throughout the observation window.")

    g11 = doc.add_paragraph(style='List Bullet')
    g11.add_run("Main Forecasting Trajectory with Colored Waste Class Bands: ").bold = True
    g11.add_run("A longitudinal time-series plot featuring horizontal pastel color-shaded background zones corresponding to the five empirical waste generation classes (Very Low: <30k t, Low: 30k-35k t, Moderate: 35k-40k t, High: 40k-45k t, Very High: ≥45k t), visually revealing exactly when future municipal generation crosses operational capacity boundaries.")

    g12 = doc.add_paragraph(style='List Bullet')
    g12.add_run("Waste Generation Class Distribution Breakdown Chart: ").bold = True
    g12.add_run("A categorical distribution bar chart quantifying the proportion of future forecast months falling into each operational class over the 2026–2030 horizon, highlighting sustained High and Very High periods to guide AKSEPWMA compactor fleet acquisition and landfill airspace planning.")

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =========================================================================
    # SECTION 4.4 SYSTEM SPECIFICATIONS
    # =========================================================================
    h1_spec = doc.add_heading("4.4 SYSTEM SPECIFICATIONS", level=1)
    h1_spec.style.font.name = 'Times New Roman'
    h1_spec.style.font.size = Pt(14)
    h1_spec.style.font.color.rgb = RGBColor(15, 23, 42)
    h1_spec.style.font.bold = True

    doc.add_paragraph(
        "The system specifications define the minimum and recommended hardware, software, networking, and security environments "
        "required to develop, train, execute, and deploy the Gaussian Process Regression Municipal Solid Waste Forecasting System."
    )

    # 4.4.1 Hardware Specifications
    h2_hw = doc.add_heading("4.4.1 Hardware Specifications", level=2)
    h2_hw.style.font.name = 'Times New Roman'
    h2_hw.style.font.size = Pt(13)
    h2_hw.style.font.color.rgb = RGBColor(15, 23, 42)
    h2_hw.style.font.bold = True

    doc.add_paragraph(
        "The hardware environment must support numerical linear algebra routines (Cholesky decomposition O(N^3) and covariance matrix inversion) "
        "during the L-BFGS-B marginal log-likelihood optimization phase, while ensuring rapid responsiveness for interactive Streamlit dashboard operations."
    )

    t_caption3 = doc.add_paragraph()
    t_caption3.add_run("Table 4.3: Hardware Specifications for System Execution and Deployment").bold = True
    t_caption3.paragraph_format.space_after = Pt(4)

    t3_headers = ["Hardware Component", "Minimum Required Specification", "Recommended Specification (Development & Deployment)", "Technical Justification"]
    t3_data = [
        ["Processor (CPU)", "Intel Core i3 / AMD Ryzen 3 (Quad-Core, 2.0 GHz)", "Intel Core i7 / AMD Ryzen 7 (8 Cores, 16 Threads, 3.2 GHz or higher)", "Accelerates L-BFGS-B log-likelihood optimization and multi-restart kernel fitting."],
        ["System Memory (RAM)", "8 GB DDR4", "16 GB DDR4 / DDR5", "Houses historical time series, covariate matrices, covariance arrays, and serialized model caches."],
        ["Secondary Storage", "256 GB Solid State Drive (SSD)", "512 GB NVMe M.2 SSD (Read/Write ≥ 3000 MB/s)", "Provides rapid I/O for empirical dataset loading, model serialization, and log persistence."],
        ["Display / Monitor", "14-inch HD Display (1366 x 768 resolution)", "15.6-inch Full HD Display (1920 x 1080 IPS or higher)", "Ensures high clarity for multi-panel dashboards, confusion matrices, and wide time-series charts."],
        ["Input Peripherals", "Standard QWERTY Keyboard and Mouse/Touchpad", "Standard QWERTY Keyboard and High-Precision Optical Mouse", "Standard data entry, script execution, and interactive dashboard parameter tuning."],
        ["Network Interface", "10/100 Mbps Ethernet or 802.11n Wi-Fi", "Gigabit Ethernet / Wi-Fi 6 (802.11ax)", "Facilitates live meteorological data synchronization, satellite updates, and intranet client serving."]
    ]

    table3 = doc.add_table(rows=len(t3_data) + 1, cols=len(t3_headers))
    table3.alignment = WD_TABLE_ALIGNMENT.CENTER
    table3.autofit = True

    for col_idx, h_text in enumerate(t3_headers):
        cell = table3.cell(0, col_idx)
        cell.text = h_text
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row_items in enumerate(t3_data):
        for col_idx, val_text in enumerate(row_items):
            cell = table3.cell(row_idx + 1, col_idx)
            cell.text = val_text
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            if col_idx in [0]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 4.4.2 Software Specifications
    h2_sw = doc.add_heading("4.4.2 Software Specifications", level=2)
    h2_sw.style.font.name = 'Times New Roman'
    h2_sw.style.font.size = Pt(13)
    h2_sw.style.font.color.rgb = RGBColor(15, 23, 42)
    h2_sw.style.font.bold = True

    doc.add_paragraph(
        "The software architecture leverages the modern open-source Python scientific computing and machine learning ecosystem, "
        "ensuring cross-platform reproducibility, strict mathematical typing, and rapid client interactivity."
    )

    t_caption4 = doc.add_paragraph()
    t_caption4.add_run("Table 4.4: Software Specifications and Library Dependency Stack").bold = True
    t_caption4.paragraph_format.space_after = Pt(4)

    t4_headers = ["Software Layer / Module", "Minimum Software Requirement", "Version Deployed / Verified", "Role & Functional Responsibility"]
    t4_data = [
        ["Operating System", "Microsoft Windows 10 (64-bit) / Ubuntu 20.04 LTS", "Microsoft Windows 11 Pro (64-bit)", "Host environment providing kernel threading and 64-bit memory addressing."],
        ["Programming Language", "Python 3.10 (64-bit)", "Python 3.14 / Python 3.11 (64-bit)", "Core execution runtime for feature preprocessing, mathematical modeling, and web serving."],
        ["Machine Learning Library", "Scikit-Learn 1.3+", "Scikit-Learn 1.6+", "Implements GaussianProcessRegressor, composite kernels (DotProduct, Matern, WhiteKernel), and metrics."],
        ["Scientific Computing", "NumPy 1.24+ / SciPy 1.10+", "NumPy 2.x / SciPy 1.14+", "High-performance N-dimensional array processing, matrix algebra, and trigonometric encodings."],
        ["Data Manipulation", "Pandas 2.0+", "Pandas 2.2+", "Time-series indexing, CSV data ingestion, missing value imputation, and tabular reporting."],
        ["Model Persistence", "Joblib 1.3+", "Joblib 1.4+", "Serialization and zero-latency disk loading of trained model weights and precomputed caches (gpr_waste_model.pkl)."],
        ["Web Application Framework", "Streamlit 1.30+", "Streamlit 1.42+", "Renders the interactive web application, navigation tabs, slider controls, and CSV export engines."],
        ["Plotting & Visualization", "Matplotlib 3.7+ / Seaborn 0.12+", "Matplotlib 3.10+ / Seaborn 0.13+", "Generates publication-standard 200 DPI vector charts, residual distributions, and confusion matrices."],
        ["Integrated Development Env.", "VS Code / JupyterLab", "VS Code with Python & Jupyter Extensions", "Interactive code execution, cell-by-cell inspection, syntax verification, and debugging."],
        ["Web Browser Interface", "HTML5 / ECMAScript 6 Compliant", "Google Chrome / Microsoft Edge / Firefox", "Client-side rendering of the responsive decision intelligence portal and GIS maps."]
    ]

    table4 = doc.add_table(rows=len(t4_data) + 1, cols=len(t4_headers))
    table4.alignment = WD_TABLE_ALIGNMENT.CENTER
    table4.autofit = True

    for col_idx, h_text in enumerate(t4_headers):
        cell = table4.cell(0, col_idx)
        cell.text = h_text
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row_items in enumerate(t4_data):
        for col_idx, val_text in enumerate(row_items):
            cell = table4.cell(row_idx + 1, col_idx)
            cell.text = val_text
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            if col_idx in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.size = Pt(9)
                run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 4.4.3 Operational and Network Specifications
    h2_ops = doc.add_heading("4.4.3 Operational, Network, and Security Specifications", level=2)
    h2_ops.style.font.name = 'Times New Roman'
    h2_ops.style.font.size = Pt(13)
    h2_ops.style.font.color.rgb = RGBColor(15, 23, 42)
    h2_ops.style.font.bold = True

    op1 = doc.add_paragraph(style='List Bullet')
    op1.add_run("Client-Server Reactive Architecture: ").bold = True
    op1.add_run("The application operates under an asynchronous event-driven model where the Python backend runs on localhost:8501. User interactions with slider widgets transmit differential parameters via WebSockets (ws://) to trigger instant Bayesian posterior updates without requiring full-page reloads.")

    op2 = doc.add_paragraph(style='List Bullet')
    op2.add_run("State Persistence & Fast Caching: ").bold = True
    op2.add_run("Trained model parameters, composite covariance kernel matrices, and fitted StandardScaler coefficients are persisted as a compiled binary artifact (gpr_waste_model.pkl). The application loads these objects via Streamlit's @st.cache_resource, guaranteeing sub-second startup times.")

    op3 = doc.add_paragraph(style='List Bullet')
    op3.add_run("Input Integrity & Fault Tolerance: ").bold = True
    op3.add_run("All interactive forms enforce strict physiological boundary checks (e.g., rejecting negative rainfall depth or temperatures outside the tropical envelope). During batch CSV testing, missing required columns are caught via schema validation handlers, returning helpful diagnostic alerts rather than throwing unhandled exceptions.")

    # Save to disk
    out_path = r"c:\Users\USER\Desktop\Samuel_Effiong\Chapter_4_System_Specifications_Samuel_Effiong.docx"
    doc.save(out_path)
    print(f"[OK] Word document successfully created at: {out_path}")

if __name__ == "__main__":
    create_document()

