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

def create_chapter_5_document():
    doc = docx.Document()

    # Set 1-inch margins
    for section in doc.sections:
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

    # Institutional Header / Meta Banner
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = p_meta.add_run("AKWA IBOM STATE UNIVERSITY\nDEPARTMENT OF COMPUTER SCIENCE\nFACULTY OF COMPUTING AND INFORMATION TECHNOLOGY\n")
    run_inst.bold = True
    run_inst.font.size = Pt(12)
    run_inst.font.color.rgb = RGBColor(15, 23, 42)

    run_proj = p_meta.add_run("A GAUSSIAN PROCESS REGRESSION FOR FORECASTING SOLID WASTE GENERATION IN UYO MUNICIPALITY\n")
    run_proj.bold = True
    run_proj.font.size = Pt(13)
    run_proj.font.color.rgb = RGBColor(15, 78, 59)

    run_cand = p_meta.add_run("Candidate: EFFIONG, SAMUEL ETIM (Reg. No: AK22/PHS/CSC/029)\nSupervisor: Dr. Anietie P. Ekong\n")
    run_cand.italic = True
    run_cand.font.size = Pt(11)
    run_cand.font.color.rgb = RGBColor(71, 85, 105)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_div = p_div.add_run("―" * 45)
    r_div.font.color.rgb = RGBColor(203, 213, 225)
    p_div.paragraph_format.space_after = Pt(14)

    # =========================================================================
    # CHAPTER FIVE TITLE
    # =========================================================================
    p_ch = doc.add_paragraph()
    p_ch.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ch = p_ch.add_run("CHAPTER FIVE\n")
    r_ch.bold = True
    r_ch.font.size = Pt(15)
    r_ch.font.color.rgb = RGBColor(15, 23, 42)

    r_title = p_ch.add_run("SUMMARY, CONCLUSION AND RECOMMENDATIONS")
    r_title.bold = True
    r_title.font.size = Pt(14)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    p_ch.paragraph_format.space_after = Pt(14)

    # =========================================================================
    # CHAPTER INTRODUCTORY NARRATIVE / SUMMARY
    # =========================================================================
    p_sum1 = doc.add_paragraph(
        "Municipal solid waste (MSW) management represents one of the most critical environmental, operational, and "
        "public health challenges confronting rapidly urbanizing cities across the developing world. In Uyo Municipality, "
        "the capital city of Akwa Ibom State, accelerated population growth, rural-to-urban migration, commercial expansion, "
        "and changing consumer lifestyles have precipitated exponential increases in municipal solid waste generation. "
        "The state waste management authority—the Akwa Ibom State Environmental Protection and Waste Management Agency "
        "(AKSEPWMA)—is continuously confronted with the complex task of scheduling collection sweeps, sizing compactor "
        "vehicle fleets, preventing illegal dumpsite proliferation, and managing limited landfill disposal airspace. "
        "Environmental health officers and municipal decision-makers require prompt, evidence-based decision intelligence "
        "systems capable of accurately projecting future waste generation volumes while accounting for temporal seasonality, "
        "demographic pressure, and atmospheric precipitation anomalies. Traditional waste estimation techniques and classical "
        "deterministic forecasting tools fail to capture the non-linear dynamics inherent in tropical municipal waste generation "
        "and completely lack the mathematical capacity to quantify predictive uncertainty."
    )
    p_sum1.paragraph_format.space_after = Pt(8)

    p_sum2 = doc.add_paragraph(
        "To resolve these operational and methodological deficiencies, this research designed, formulated, implemented, and "
        "evaluated a non-parametric Bayesian Gaussian Process Regression (GPR) model tailored specifically for municipal solid "
        "waste generation forecasting in Uyo Municipality. Unlike black-box machine learning algorithms or rigid parametric models, "
        "Gaussian Process Regression establishes a principled probabilistic prior over functions, utilizing kernel covariance "
        "mathematics to capture complex underlying trends, seasonal harmonic oscillations, and random observational fluctuations. "
        "The model was rigorously trained and validated on an authentic 84-month longitudinal dataset (spanning January 2019 "
        "through December 2025) obtained from AKSEPWMA operational logs, integrated with local meteorological records (rainfall "
        "depth, mean surface temperature, and relative atmospheric humidity) and National Population Commission demographic projections. "
        "A composite covariance kernel—synthesizing a DotProduct linear trend operator, a Matérn (ν = 1.5) seasonal covariance "
        "function, and an additive WhiteKernel noise component—was optimized via L-BFGS-B marginal log-likelihood maximization "
        "with 15 random restarts to eliminate local optima."
    )
    p_sum2.paragraph_format.space_after = Pt(8)

    p_sum3 = doc.add_paragraph(
        "Comprehensive empirical evaluation against out-of-time test partitions (2024–2025) and comparative kernel architectures "
        "(Radial Basis Function, Matérn 2.5, and Rational Quadratic) confirmed the superior predictive precision, generalization "
        "capability, and uncertainty calibration of the proposed composite GPR model. The architecture achieved an overall "
        "coefficient of determination (R²) of 0.9854, a Root Mean Squared Error (RMSE) of 758.3 metric tonnes, a Mean Absolute Error "
        "(MAE) of 567.1 metric tonnes, and an out-of-sample Mean Absolute Percentage Error (MAPE) of 1.73%, with 100% of observed "
        "records strictly enclosed within the 95% Bayesian Confidence Interval. Furthermore, to bridge the divide between theoretical "
        "regression modeling and field operations, the system deployed Option D (Dual Continuous-Categorical Presentation Paradigm), "
        "coupling probabilistic numerical estimates with an empirical 5-tier municipal waste classification scheme (Very Low, Low, "
        "Moderate, High, and Very High). The complete mathematical framework was operationalized through an interactive, full-stack "
        "Streamlit web application featuring geospatial GIS zonal mapping, what-if climate simulation, automated batch test validation, "
        "and dynamic fleet logistics sizing, directly empowering municipal administrators with actionable foresight."
    )
    p_sum3.paragraph_format.space_after = Pt(12)

    # =========================================================================
    # 5.1 CONCLUSION
    # =========================================================================
    h2_concl = doc.add_heading("5.1 Conclusion", level=2)
    h2_concl.style.font.name = 'Times New Roman'
    h2_concl.style.font.size = Pt(13)
    h2_concl.style.font.color.rgb = RGBColor(15, 23, 42)
    h2_concl.style.font.bold = True

    p_c1 = doc.add_paragraph(
        "This research has demonstrated that Gaussian Process Regression (GPR) provides an exceptionally robust, accurate, and "
        "theoretically sound framework for forecasting municipal solid waste generation in Uyo Municipality, Akwa Ibom State. "
        "By integrating demographic indices, meteorological covariates, calendar harmonics, and statutory public holidays into a "
        "unified Bayesian regression pipeline, the developed system successfully overcomes the critical limitations associated "
        "with classical deterministic methods such as Multiple Linear Regression (MLR) and Autoregressive Integrated Moving Average "
        "(ARIMA) models. Classical models produce rigid, single-point projections that assume static homoscedastic variance and "
        "fail to inform decision-makers about the degree of confidence attributable to any given forecast. In sharp contrast, "
        "the GPR framework derives a complete posterior probability distribution: y* ~ N(μ*, σ*²), outputting both the expected "
        "predictive mean monthly waste tonnage and rigorous 95% Bayesian Confidence Intervals (μ* ± 1.96σ*)."
    )
    p_c1.paragraph_format.space_after = Pt(8)

    p_c2 = doc.add_paragraph(
        "The empirical findings derived from the 60-month forward projection window (January 2026 to December 2030) indicate a "
        "sustained upward trajectory in solid waste generation for Uyo Municipality, driven primarily by demographic expansion "
        "(from 496,000 residents in 2019 to over 670,000 by 2030) and intensified commercial transactions across major economic nodes. "
        "Annual municipal waste generation is projected to expand from 422,350 tonnes in 2025 to 551,460 tonnes by 2030, with monthly "
        "tonnage fluctuating between 41,200 tonnes during dry-season baselines and peak surges exceeding 49,500 tonnes during the "
        "fourth-quarter festive months (November–December) and peak monsoon rainfall periods (July–September). These findings confirm "
        "that municipal solid waste generation in Uyo is highly sensitive to climatic and calendar regressors, necessitating flexible, "
        "seasonally adaptive resource management rather than static annual planning."
    )
    p_c2.paragraph_format.space_after = Pt(8)

    p_c3 = doc.add_paragraph(
        "Crucially, the successful deployment of Option D (Dual Continuous-Categorical Presentation) establishes that academic machine "
        "learning models can be translated into intuitive administrative tools without sacrificing mathematical rigor. Discretizing "
        "continuous Bayesian forecasts into five operational waste generation classes (Very Low, Low, Moderate, High, and Very High) "
        "enables AKSEPWMA officials to instantaneously identify high-risk operational windows, optimize 15-tonne compactor vehicle "
        "dispatch schedules (requiring between 35 and 52 active trucks), budget for 1,100-litre communal bins, and monitor annual "
        "landfill airspace depletion exceeding 55,000 m³ annually. Delivered via an interactive Streamlit web application, the system "
        "proves that probabilistic artificial intelligence can be effectively democratized for real-world environmental governance in "
        "sub-Saharan municipal contexts."
    )
    p_c3.paragraph_format.space_after = Pt(12)

    # =========================================================================
    # 5.2 CONTRIBUTIONS TO KNOWLEDGE
    # =========================================================================
    h2_contrib = doc.add_heading("5.2 Contributions to Knowledge", level=2)
    h2_contrib.style.font.name = 'Times New Roman'
    h2_contrib.style.font.size = Pt(13)
    h2_contrib.style.font.color.rgb = RGBColor(15, 23, 42)
    h2_contrib.style.font.bold = True

    doc.add_paragraph(
        "This research makes distinct theoretical, algorithmic, methodological, and practical contributions to the domains of "
        "environmental informatics, municipal engineering, and applied machine learning:"
    )

    cb1 = doc.add_paragraph(style='List Bullet')
    cb1.add_run("1. Formulation of an Optimized Composite Covariance Kernel for Tropical MSW Dynamics: ").bold = True
    cb1.add_run(
        "A major theoretical contribution of this work is the formulation, mathematical synthesis, and optimization of a "
        "composite GPR covariance kernel: k_composite(x, x') = DotProduct(linear trend) + Matérn(ν = 1.5, seasonal) + WhiteKernel(noise). "
        "Existing waste forecasting literature predominantly applies standard off-the-shelf Radial Basis Function (RBF) kernels, which "
        "assume infinite differentiability and unrealistically smooth trajectories. By integrating the Matérn kernel (with roughness "
        "parameter ν = 1.5), the model accurately accommodates the sharp, irregular fluctuations induced by tropical rainfall spikes "
        "and festive commercial surges, outperforming standard RBF and Rational Quadratic kernels across all empirical error metrics (RMSE 758.3 t vs. 1,725.9 t)."
    )

    cb2 = doc.add_paragraph(style='List Bullet')
    cb2.add_run("2. Rigorous Bayesian Uncertainty Quantification in Municipal Solid Waste Planning: ").bold = True
    cb2.add_run(
        "Unlike conventional deterministic regression paradigms (ARIMA, MLR, Support Vector Regression) that output isolated point forecasts, "
        "this study establishes a fully calibrated Bayesian uncertainty quantification pipeline for municipal solid waste management. "
        "By deriving posterior variance envelopes (95% CI: μ* ± 1.96σ*), the research provides waste authorities with mathematical risk "
        "boundaries, enabling worst-case scenario buffer sizing for compactor fleet procurement, fuel logistics, and emergency budget planning."
    )

    cb3 = doc.add_paragraph(style='List Bullet')
    cb3.add_run("3. Introduction of the Option D Dual-Paradigm Classification Framework: ").bold = True
    cb3.add_run(
        "The study pioneers the 'Option D' presentation methodology in environmental decision support systems. By linking continuous "
        "Gaussian Process regression estimates with empirical capacity thresholds derived from longitudinal AKSEPWMA records, the research "
        "bridges the divide between mathematical modeling and municipal operations. Waste projections are simultaneously delivered as exact "
        "tonnage figures and discrete 5-tier operational status categories (Very Low to Very High), providing immediate visual triage for field officers."
    )

    cb4 = doc.add_paragraph(style='List Bullet')
    cb4.add_run("4. Empirical Longitudinal Baseline Dataset Construction for Uyo Municipality: ").bold = True
    cb4.add_run(
        "The research compiled, preprocessed, standardized, and validated a comprehensive 84-month empirical dataset (2019–2025) for Uyo "
        "Municipality, integrating AKSEPWMA solid waste weighbridge records with local meteorological measurements and National Population "
        "Commission demographic estimates. This longitudinal database resolves historical data fragmentation in the state and establishes an "
        "authoritative benchmark dataset for future environmental research in Akwa Ibom State."
    )

    cb5 = doc.add_paragraph(style='List Bullet')
    cb5.add_run("5. Development of an Operationalized Open-Source Decision Support Portal: ").bold = True
    cb5.add_run(
        "The project developed and deployed an interactive, enterprise-grade decision intelligence web application using Streamlit, "
        "Python, Scikit-Learn, and Joblib. Featuring multi-page modular navigation, geospatial GIS zonal allocation maps across Uyo's "
        "six collection nodes, interactive what-if sensitivity simulators, and single-observation and batch CSV testing sandboxes, "
        "the system delivers a turnkey, zero-license-cost software artifact ready for institutional deployment by environmental protection agencies."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Summary Table of System Contributions
    t_caption_contrib = doc.add_paragraph()
    t_caption_contrib.add_run("Table 5.1: Comparative Summary of Research Contributions against Conventional Approaches").bold = True
    t_caption_contrib.paragraph_format.space_after = Pt(4)

    tc_headers = ["Evaluation Dimension", "Conventional Municipal Practice / Existing Literature", "Proposed GPR Decision Support Framework (This Study)"]
    tc_data = [
        ["Predictive Modeling Paradigm", "Static per-capita multipliers or deterministic linear regression / ARIMA.", "Non-parametric Bayesian Gaussian Process Regression (GPR)."],
        ["Uncertainty Handling", "Zero uncertainty representation; single deterministic point projection.", "Full posterior Gaussian distribution: 95% Bayesian Confidence Intervals (μ* ± 1.96σ*)."],
        ["Covariance Kernel Design", "Single standard RBF kernel without domain-specific customization.", "Engineered Composite Kernel: DotProduct(Trend) + Matérn(ν=1.5) + WhiteKernel(Noise)."],
        ["Covariate Multi-Modality", "Historical waste data analyzed in isolation without exogenous variables.", "Coupled demographic projections, precipitation depth, ambient temperature, humidity, and calendar holidays."],
        ["Decision Presentation", "Raw tables of numbers without operational translation (Option A/C).", "Option D Paradigm: Simultaneous continuous tonnage and 5-tier operational waste classification."],
        ["Logistics Operationalization", "Disconnected theoretical spreadsheets requiring manual fleet calculation.", "Automated translation into active 15-tonne compactor trucks, 1,100L communal bins, and landfill volume."],
        ["Software Deployment", "Static offline research code without user-facing interfaces.", "Interactive web portal (Streamlit) with GIS zonal mapping, what-if simulator, and live CSV testing sandbox."]
    ]

    t_contrib = doc.add_table(rows=len(tc_data) + 1, cols=len(tc_headers))
    t_contrib.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_contrib.autofit = True

    for col_idx, h_text in enumerate(tc_headers):
        cell = t_contrib.cell(0, col_idx)
        cell.text = h_text
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row_items in enumerate(tc_data):
        for col_idx, val_text in enumerate(row_items):
            cell = t_contrib.cell(row_idx + 1, col_idx)
            cell.text = val_text
            bg_color = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.bold = True
                    run.font.size = Pt(9)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================
    # 5.3 RECOMMENDATIONS
    # =========================================================
    h2_rec = doc.add_heading("5.3 Recommendations", level=2)
    h2_rec.style.font.name = 'Times New Roman'
    h2_rec.style.font.size = Pt(13)
    h2_rec.style.font.color.rgb = RGBColor(15, 23, 42)
    h2_rec.style.font.bold = True

    doc.add_paragraph(
        "Based on the empirical findings, mathematical modeling, and operational insights derived from this research, the following "
        "policy, operational, and institutional recommendations are formulated for the Akwa Ibom State Environmental Protection and "
        "Waste Management Agency (AKSEPWMA), the Uyo Local Government Council, and the Akwa Ibom State Ministry of Environment:"
    )

    r1 = doc.add_paragraph(style='List Bullet')
    r1.add_run("1. Institutionalization of Predictive Compactor Fleet Sizing and Dynamic Scheduling: ").bold = True
    r1.add_run(
        "AKSEPWMA should formally transition from reactive, fixed-interval collection schedules to proactive, forecast-driven fleet allocation. "
        "The agency must expand its active operational fleet to a baseline of 44 to 49 active 15-tonne compactor trucks during standard months, "
        "and maintain a reserve contingency fleet of at least 8 to 10 standby units to handle fourth-quarter festive surges (November–December) "
        "when generation exceeds 48,000 tonnes/month. Vehicle dispatching should directly reference the system's upper 95% Bayesian confidence limit "
        "to guarantee 100% daily clearance and eliminate street-level litter backlog."
    )

    r2 = doc.add_paragraph(style='List Bullet')
    r2.add_run("2. Transition from Open Dumpsites to Engineered Sanitary Landfills: ").bold = True
    r2.add_run(
        "The model forecasts that Uyo Municipality will generate over 2.65 million metric tonnes of solid waste cumulatively between 2026 and 2030, "
        "depleting approximately 3.31 million cubic meters of landfill disposal airspace. The Akwa Ibom State Government must urgently decommission "
        "uncontrolled open dumpsites—such as the active disposal corridor along the Lemna dumpsite axis—and establish a modern, engineered sanitary "
        "landfill facility equipped with impermeable composite geomembrane liners, leachate treatment facilities, methane gas extraction wells, and "
        "systematic daily cell compaction to safeguard groundwater resources and prevent air pollution."
    )

    r3 = doc.add_paragraph(style='List Bullet')
    r3.add_run("3. Adoption of Rainfall-Adaptive Routing and Pre-Dawn Sweeping Operations: ").bold = True
    r3.add_run(
        "Statistical feature importance and sensitivity analysis established that monthly precipitation depth is a major exogenous driver of "
        "waste volume and collection difficulty. Heavy rainfall during the wet monsoon season (June to September) saturates open communal bins, "
        "increasing waste weight by up to 25% and creating severe vehicular traffic gridlock. AKSEPWMA should adjust its operational collection "
        "timetables during wet months by scheduling compactor collection sweeps during pre-dawn hours (04:00 AM – 07:00 AM) and implementing "
        "mandatory waterproof covers on all communal collection bins and haulage vehicles."
    )

    r4 = doc.add_paragraph(style='List Bullet')
    r4.add_run("4. Establishment of Decentralized Material Recovery Hubs in High-Density Corridors: ").bold = True
    r4.add_run(
        "The spatial zonal allocation module revealed that Itam Market & Industrial Commercial Corridor (26%) and Ibom Plaza Central Business "
        "District (22%) together generate nearly half (48%) of Uyo Municipality's aggregate solid waste. The state government should establish "
        "decentralized mini-sorting and material recovery facilities (MRFs) within these two high-volume commercial nodes. By incentivizing source "
        "segregation of organic market food waste for commercial composting and diverting recyclable plastics and aluminium cans, an estimated "
        "35% (over 170,000 tonnes annually by 2030) of solid waste can be diverted from the municipal landfill, extending landfill lifespan."
    )

    r5 = doc.add_paragraph(style='List Bullet')
    r5.add_run("5. Integration of the Streamlit Decision Portal into AKSEPWMA Operational Infrastructure: ").bold = True
    r5.add_run(
        "The Akwa Ibom State Ministry of Environment should formally integrate the developed GPR decision intelligence portal into AKSEPWMA's "
        "routine operational workflow. Technical capacity-building workshops should be organized for waste management superintendents, data entry "
        "officers, and transport logistics supervisors to enable seamless monthly parameter updating, scenario testing, and batch CSV validation."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # =========================================================
    # 5.4 SUGGESTIONS FOR FUTURE WORK
    # =========================================================
    h2_future = doc.add_heading("5.4 Suggestions for Future Work", level=2)
    h2_future.style.font.name = 'Times New Roman'
    h2_future.style.font.size = Pt(13)
    h2_future.style.font.color.rgb = RGBColor(15, 23, 42)
    h2_future.style.font.bold = True

    doc.add_paragraph(
        "While the developed Gaussian Process Regression framework demonstrates outstanding predictive precision and operational utility, "
        "the following avenues are proposed for future academic and technical extension:"
    )

    f_a = doc.add_paragraph(style='List Bullet')
    f_a.add_run("a. Geographic and Spatial Expansion to Additional Local Government Areas: ").bold = True
    f_a.add_run(
        "Future research should extend the modeling architecture beyond Uyo Municipality to encompass other rapidly urbanizing commercial centers "
        "across Akwa Ibom State, including Ikot Ekpene, Eket, Oron, and Ikot Abasi LGAs, as well as adjacent metropolitan cities in the Niger Delta "
        "region (such as Calabar and Port Harcourt). Expanding the spatial sample will evaluate the model's cross-ecological generalization and "
        "enable regional state-wide municipal solid waste planning."
    )

    f_b = doc.add_paragraph(style='List Bullet')
    f_b.add_run("b. Integration of Real-Time IoT Telemetry and Smart Bin Weight Sensors: ").bold = True
    f_b.add_run(
        "Subsequent iterations of the forecasting engine should interface with Internet of Things (IoT) ultrasonic level sensors and digital load-cell "
        "weight scales installed inside communal waste disposal bins across Uyo Municipality. Ingesting high-frequency, real-time fill-level telemetry "
        "via MQTT or HTTP REST APIs would enable intra-daily GPR updating and dynamic vehicle routing algorithms (e.g., Dijkstra / Ant Colony Optimization) "
        "to replace monthly static dispatching."
    )

    f_c = doc.add_paragraph(style='List Bullet')
    f_c.add_run("c. Comparative Benchmarking with Deep Bayesian and Hybrid Deep Learning Models: ").bold = True
    f_c.add_run(
        "Researchers should investigate the empirical performance trade-offs between standard composite GPR and emerging deep probabilistic models, "
        "such as Deep Gaussian Processes (DGPs), Bayesian Neural Networks (BNNs), Spatio-Temporal Graph Convolutional Networks (ST-GCNs), and "
        "Physics-Informed Neural Networks (PINNs). Evaluating these advanced architectures will elucidate the boundary between computational "
        "efficiency, interpretability, and predictive capacity in environmental engineering."
    )

    f_d = doc.add_paragraph(style='List Bullet')
    f_d.add_run("d. Physical Waste Characterization and Component Fraction Decomposition: ").bold = True
    f_d.add_run(
        "The present study focused on total aggregate gross tonnage of municipal solid waste. Future investigations should gather disaggregated waste "
        "stream data to model individual physical fractions—specifically organic biodegradable matter, single-use plastics, paper/cardboard, glass, "
        "metals, and hazardous e-waste. Developing multi-output Gaussian Process models (Coregionalized GPR) for distinct material categories will "
        "provide critical empirical data needed to establish circular economy recycling industries and waste-to-energy incineration plants in Nigeria."
    )

    f_e = doc.add_paragraph(style='List Bullet')
    f_e.add_run("e. Demographic and Socio-Economic Disaggregation at Ward and Enumeration Levels: ").bold = True
    f_e.add_run(
        "Future field surveys should investigate localized socio-economic disparities in household per-capita waste generation rates across Uyo's "
        "administrative wards (e.g., contrasting high-income residential quarters such as Shelter Afrique and Ewet Housing Estate with high-density "
        "peri-urban settlements). Incorporating fine-grained household income strata, educational attainment, and fuel consumption covariates will "
        "minimize spatial estimation biases and ensure equitable municipal sanitation distribution."
    )

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # Concluding Signature Block
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sign = p_sign.add_run("_______________________________\nEffiong, Samuel Etim\n(AK22/PHS/CSC/029)\nDepartment of Computer Science\nAkwa Ibom State University")
    r_sign.italic = True
    r_sign.font.size = Pt(10)
    r_sign.font.color.rgb = RGBColor(71, 85, 105)

    # Save to disk
    out_path = r"c:\Users\USER\Desktop\Samuel_Effiong\Chapter_5_Summary_Conclusion_Recommendations_Samuel_Effiong.docx"
    doc.save(out_path)
    print(f"[OK] Chapter 5 Word document successfully created at: {out_path}")

if __name__ == "__main__":
    create_chapter_5_document()

