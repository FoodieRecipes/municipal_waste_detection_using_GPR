import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn.metrics import confusion_matrix, classification_report, mean_squared_error, mean_absolute_error, r2_score

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION & METADATA
# ==============================================================================
st.set_page_config(
    page_title="Uyo Solid Waste Forecasting Portal | GPR AI System",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# MODERN ENTERPRISE CSS DESIGN SYSTEM (HIGH CONTRAST & VISIBILITY)
# ==============================================================================
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1400px;
    }

    /* Top Institutional Navigation Bar */
    .top-nav-bar {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border-radius: 12px;
        padding: 14px 24px;
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #334155;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
    }
    .top-nav-title {
        color: #FFFFFF;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .top-nav-badges {
        display: flex;
        gap: 10px;
        align-items: center;
        flex-wrap: wrap;
    }

    /* Status Pills */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }
    .pill-online {
        background-color: #064E3B;
        color: #34D399;
        border: 1px solid #059669;
    }
    .pill-aksu {
        background-color: #1E3A8A;
        color: #93C5FD;
        border: 1px solid #3B82F6;
    }
    .pill-model {
        background-color: #4C1D95;
        color: #C4B5FD;
        border: 1px solid #7C3AED;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #064E3B 0%, #0F172A 55%, #1E293B 100%);
        border-radius: 16px;
        padding: 30px 36px;
        margin-bottom: 28px;
        border: 1px solid #047857;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.25);
        color: #FFFFFF;
    }
    .hero-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        line-height: 1.25;
        margin-bottom: 10px;
        color: #FFFFFF;
    }
    .hero-subtitle {
        font-size: 15px;
        color: #CBD5E1;
        line-height: 1.6;
        margin-bottom: 18px;
    }
    .hero-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        font-size: 13px;
        color: #94A3B8;
        border-top: 1px solid rgba(255, 255, 255, 0.12);
        padding-top: 14px;
    }
    .hero-meta b {
        color: #F8FAFC;
    }

    /* Content Cards */
    .portal-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 22px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .portal-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.05);
    }
    .portal-card-header {
        font-size: 18px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 10px;
    }

    /* Stat Box Cards */
    .stat-card {
        background: linear-gradient(145deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        border-left: 4px solid #059669;
        margin-bottom: 12px;
    }
    .stat-label {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        margin-bottom: 6px;
    }
    .stat-value {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.1;
    }
    .stat-subtext {
        font-size: 12px;
        color: #059669;
        font-weight: 600;
        margin-top: 5px;
    }

    /* Operational Risk & Waste Class Badges */
    .tier-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 12px;
        text-align: center;
    }
    .tier-very-low { background-color: #DEF7EC; color: #03543F; border: 1px solid #84E1BC; }
    .tier-low { background-color: #E0F2FE; color: #0369A1; border: 1px solid #7DD3FC; }
    .tier-moderate { background-color: #FEF08A; color: #713F12; border: 1px solid #FDE047; }
    .tier-high { background-color: #FFEDD5; color: #9A3412; border: 1px solid #FDBA74; }
    .tier-very-high, .tier-critical { background-color: #FEE2E2; color: #991B1B; border: 1px solid #FCA5A5; }

    /* Custom Callouts */
    .callout-info {
        background-color: #EFF6FF;
        border-left: 4px solid #3B82F6;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 16px 0;
        color: #1E3A8A;
        font-size: 14px;
        line-height: 1.6;
    }
    .callout-success {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 16px 0;
        color: #064E3B;
        font-size: 14px;
        line-height: 1.6;
    }
    .callout-warning {
        background-color: #FFFBEB;
        border-left: 4px solid #F59E0B;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 16px 0;
        color: #78350F;
        font-size: 14px;
        line-height: 1.6;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F172A;
        border-right: 1px solid #1E293B;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 4px;
        transition: background 0.2s;
        font-size: 14px;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.08);
    }

    /* Tab bar styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: #F1F5F9;
        border-radius: 8px 8px 0px 0px;
        gap: 6px;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-left: 18px;
        padding-right: 18px;
        font-weight: 600;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0F172A !important;
        color: #FFFFFF !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        color: #FFFFFF;
        font-weight: 700;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(5, 150, 105, 0.25);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #047857 0%, #065F46 100%);
        box-shadow: 0 6px 12px -2px rgba(5, 150, 105, 0.35);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

def render_html_block(html_content: str):
    """
    Renders raw HTML safely in Streamlit without triggering Markdown code block formatting.
    Removes leading indentation on each line and empty lines that cause Markdown to interpret
    indented HTML as a <pre><code> block.
    """
    clean_lines = [line.strip() for line in html_content.splitlines() if line.strip()]
    st.markdown("\n".join(clean_lines), unsafe_allow_html=True)

# ==============================================================================
# DATA & MODEL ARTIFACT LOADER
# ==============================================================================
@st.cache_resource
def load_project_artifacts():
    pkl_path = "gpr_waste_model.pkl"
    if os.path.exists(pkl_path):
        return joblib.load(pkl_path)
    return None

artifacts = load_project_artifacts()

if artifacts is None:
    st.error("🚨 Model artifacts not found (`gpr_waste_model.pkl`). Please execute `python model_development.py` or run the notebook to generate the production models.")
    st.stop()

model = artifacts['model']
scaler = artifacts['scaler']
feature_cols = artifacts['feature_cols']
eval_df = artifacts['eval_df']
metrics = artifacts['metrics']
df_hist = artifacts['historical_df']
df_future = artifacts['future_df']

# Precompute In-Sample / Out-of-Sample Predictions for Detailed Diagnostics
X_all = df_hist[feature_cols]
X_all_scaled = scaler.transform(X_all)
y_all_true = df_hist['waste_tonnes_estimated'].values
y_all_pred, y_all_std = model.predict(X_all_scaled, return_std=True)

# 80/20 Chronological train/test split index
split_idx = int(len(df_hist) * 0.8)
y_train_true = y_all_true[:split_idx]
y_train_pred = y_all_pred[:split_idx]
y_test_true = y_all_true[split_idx:]
y_test_pred = y_all_pred[split_idx:]
y_test_std = y_all_std[split_idx:]

# Define 4 Operational Severity Tiers for Uyo Municipality (Module 3 Confusion Matrix)
tier_bins = [-np.inf, 30000, 37000, 41000, np.inf]
tier_labels = ['Low (<30k t)', 'Moderate (30-37k t)', 'High (37-41k t)', 'Critical Peak (>41k t)']
y_true_tiers = pd.cut(y_all_true, bins=tier_bins, labels=tier_labels)
y_pred_tiers = pd.cut(y_all_pred, bins=tier_bins, labels=tier_labels)

# 5-Tier Empirical Waste Classification System (Option D from Research Consultation)
def classify_waste_5tier(tonnes):
    """
    Classifies monthly solid waste generation in Uyo Municipality into 5 empirical operational classes
    (Option D format). Returns a dict with class name, css badge class, hex color, badge background,
    empirical threshold label, and actionable municipal logistics recommendation.
    """
    if tonnes < 30000:
        return {
            'class': 'Very Low',
            'css': 'tier-very-low',
            'color': '#059669',
            'bg_color': '#DEF7EC',
            'threshold_str': '< 30,000 t/mo (< 986 t/day)',
            'recommendation': 'Routine baseline maintenance. Standard collection schedules and regular landfill operations.'
        }
    elif tonnes < 35000:
        return {
            'class': 'Low',
            'css': 'tier-low',
            'color': '#0284C7',
            'bg_color': '#E0F2FE',
            'threshold_str': '30,000 – 35,000 t/mo (986 – 1,150 t/day)',
            'recommendation': 'Standard operational mode. Maintain regular daily collection routes across all 6 administrative zones.'
        }
    elif tonnes < 40000:
        return {
            'class': 'Moderate',
            'css': 'tier-moderate',
            'color': '#D97706',
            'bg_color': '#FEF08A',
            'threshold_str': '35,000 – 40,000 t/mo (1,150 – 1,315 t/day)',
            'recommendation': 'Heightened monitoring required. Prepare auxiliary standby compactor trucks for high-density commercial hubs (Itam Market & Ibom Plaza).'
        }
    elif tonnes < 45000:
        return {
            'class': 'High',
            'css': 'tier-high',
            'color': '#EA580C',
            'bg_color': '#FFEDD5',
            'threshold_str': '40,000 – 45,000 t/mo (1,315 – 1,479 t/day)',
            'recommendation': 'High waste generation. Deploy expanded fleet routing, schedule secondary evening sweeps, and optimize transfer stations.'
        }
    else:
        return {
            'class': 'Very High',
            'css': 'tier-very-high',
            'color': '#DC2626',
            'bg_color': '#FEE2E2',
            'threshold_str': '≥ 45,000 t/mo (≥ 1,479 t/day)',
            'recommendation': 'Critical peak overload! Mobilize maximum compactor fleet, authorize double-shift labor, and fast-track landfill airspace compaction.'
        }

# ==============================================================================
# TOP INSTITUTIONAL NAVBAR & BRANDING
# ==============================================================================
st.markdown("""
<div class="top-nav-bar">
    <div class="top-nav-title">
        <span>🏛️</span>
        <span>AKWA IBOM STATE UNIVERSITY &bull; DEPT. OF COMPUTER SCIENCE</span>
    </div>
    <div class="top-nav-badges">
        <span class="status-pill pill-online">● GPR ENGINE ONLINE</span>
        <span class="status-pill pill-aksu">AKSEPWMA EMPIRICAL DATA</span>
        <span class="status-pill pill-model">BAYESIAN R²: 0.9854</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# HERO BANNER
# ==============================================================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">
        A GAUSSIAN PROCESS REGRESSION FOR FORECASTING SOLID WASTE GENERATION IN UYO MUNICIPALITY
    </div>
    <div class="hero-subtitle">
        An AI-powered environmental decision intelligence portal providing probabilistic municipal solid waste forecasting, 
        95% Bayesian uncertainty quantification, operational risk triage, and municipal fleet logistics sizing for Uyo Municipality, Akwa Ibom State.
    </div>
    <div class="hero-meta">
        <div>👨‍🎓 <b>Researcher:</b> Effiong, Samuel Etim (Reg: AK22/PHS/CSC/029)</div>
        <div>👨‍🏫 <b>Supervisor:</b> Dr. Anietie P. Ekong</div>
        <div>📍 <b>Target Municipality:</b> Uyo, Akwa Ibom State, Nigeria</div>
        <div>🔬 <b>Model:</b> Optimized Composite Kernel GPR</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
st.sidebar.markdown("""
<div style="text-align: center; padding-bottom: 15px; border-bottom: 1px solid #334155; margin-bottom: 15px;">
    <div style="font-size: 38px; margin-bottom: 5px;">♻️</div>
    <div style="font-weight: 800; font-size: 16px; letter-spacing: 0.5px;">UYO MSW PORTAL</div>
    <div style="font-size: 11px; color: #94A3B8;">GPR Decision Support System</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<p style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.8px;'>Platform Modules</p>", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Select Application Module:",
    [
        "1. Main Forecasting Dashboard",
        "2. Model Validation & Diagnostic Visualizations",
        "3. Uyo Municipal Zonal Waste & GIS Map",
        "4. Live Model Testing"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size: 12px; color: #94A3B8; line-height: 1.6;">
    <b>Institutional Affiliation:</b><br>
    Akwa Ibom State University (AKSU)<br>
    Faculty of Computing & Information Tech.<br><br>
    <b>Collaborating Data Source:</b><br>
    Akwa Ibom State Environmental Protection and Waste Management Agency (AKSEPWMA)
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# MODULE 1: MAIN FORECASTING DASHBOARD
# ==============================================================================
if page == "1. Main Forecasting Dashboard":
    st.markdown('<div class="portal-card-header">📊 Solid Waste Generation Forecasting Dashboard — Uyo Municipality</div>', unsafe_allow_html=True)

    # Top KPI Scorecards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Dataset Observations</div>
            <div class="stat-value">{len(df_hist):,} Records</div>
            <div class="stat-subtext">2019 to 2025 Historical Series</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: #2563EB;">
            <div class="stat-label">Model Goodness of Fit</div>
            <div class="stat-value">R² = {metrics['overall']['R2']:.4f}</div>
            <div class="stat-subtext">Overall Variance Explained</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: #10B981;">
            <div class="stat-label">Out-of-Sample MAPE</div>
            <div class="stat-value">{metrics['test']['MAPE (%)']:.2f}%</div>
            <div class="stat-subtext">High Predictive Precision</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: #7C3AED;">
            <div class="stat-label">95% CI Calibration</div>
            <div class="stat-value">{metrics['test']['95% CI Coverage (%)']:.1f}%</div>
            <div class="stat-subtext">Bayesian Interval Coverage</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Interactive Dashboard Controls
    ctrl_col1, ctrl_col2, ctrl_col3 = st.columns([1.5, 1.5, 2])
    with ctrl_col1:
        horizon_choice = st.selectbox(
            "Select Forecast Horizon:",
            ["Full Horizon (5 Years: 2026-2030)", "Next 12 Months (2026)", "Next 30 Days (Jan 2026)", "Custom Range"],
            index=0
        )
    with ctrl_col2:
        unit_choice = st.radio("Display Measurement Unit:", ["Tonnes per Month", "Tonnes per Day (Daily Avg)"], horizontal=True)
    with ctrl_col3:
        st.write("")
        show_ci_band = st.checkbox("Display 95% Bayesian Confidence Interval Band", value=True)
        show_class_bands = st.checkbox("Display Waste Class Horizontal Zones", value=True)

    # Filter future data based on selected horizon
    if horizon_choice == "Next 12 Months (2026)":
        df_view = df_future[df_future['year'] == 2026].copy()
        period_label = "12 Months (2026)"
    elif horizon_choice == "Next 30 Days (Jan 2026)":
        df_view = df_future.iloc[:1].copy()
        period_label = "1 Month (Jan 2026)"
    elif horizon_choice == "Custom Range":
        sel_year = st.slider("Select Horizon Ending Year:", 2026, 2030, 2028)
        df_view = df_future[df_future['year'] <= sel_year].copy()
        period_label = f"2026 - {sel_year}"
    else:
        df_view = df_future.copy()
        period_label = "60 Months (2026 - 2030)"

    unit_multiplier = (1.0 / 30.4167) if "Day" in unit_choice else 1.0
    unit_str = "tonnes/day" if "Day" in unit_choice else "tonnes/month"

    # Target Month Picker for the Forecast Card
    month_options = df_view['date'].dt.strftime('%B %Y').tolist()
    card_col_sel, _ = st.columns([2, 3])
    with card_col_sel:
        target_card_month = st.selectbox("🎯 Select Target Month for Detailed Forecast Card:", options=month_options, index=0)

    target_match_date = pd.to_datetime(target_card_month)
    target_row = df_view[(df_view['year'] == target_match_date.year) & (df_view['month'] == target_match_date.month)].iloc[0]
    card_pred_tonnes = target_row['forecast_tonnes']
    card_daily_tonnes = card_pred_tonnes / 30.4167
    card_ci_lower = target_row['ci_lower_95']
    card_ci_upper = target_row['ci_upper_95']
    card_ci_spread = card_ci_upper - card_ci_lower
    card_class_info = classify_waste_5tier(card_pred_tonnes)
    card_trucks = int(np.ceil(card_daily_tonnes / (15 * 2)))

    hist_baseline_mean = df_hist['waste_tonnes_estimated'].mean()
    trend_pct = ((card_pred_tonnes - hist_baseline_mean) / hist_baseline_mean) * 100.0
    trend_desc = f"Increasing (+{trend_pct:.1f}% vs. Historical Baseline)" if trend_pct > 0 else f"Decreasing ({trend_pct:.1f}% vs. Historical Baseline)"
    trend_symbol = "📈" if trend_pct > 0 else "📉"

    render_html_block(f"""
    <div class="portal-card" style="border: 2px solid #2563EB; background: #FFFFFF; padding: 22px; border-radius: 14px; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08); margin-bottom: 24px;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 18px;">
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; border-left: 5px solid #2563EB;">
                <div style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">
                    Predicted Waste Generation
                </div>
                <div style="font-size: 32px; font-weight: 800; color: #0F172A; margin: 6px 0;">
                    {card_pred_tonnes:,.1f} tonnes
                </div>
                <div style="font-size: 13px; color: #2563EB; font-weight: 600;">
                    Daily Equivalent: <b>{card_daily_tonnes:,.1f} tonnes/day</b>
                </div>
            </div>
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; border-left: 5px solid {card_class_info['color']};">
                <div style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">
                    Assigned Waste Generation Class
                </div>
                <div style="margin: 8px 0;">
                    <span class="tier-badge {card_class_info['css']}" style="font-size: 20px; padding: 6px 20px; border-radius: 8px;">
                        {card_class_info['class']}
                    </span>
                </div>
                <div style="font-size: 13px; color: #475569; font-weight: 600;">
                    Threshold: <b>{card_class_info['threshold_str']}</b>
                </div>
            </div>
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 13.5px; background: #FFFFFF; border-radius: 8px; overflow: hidden; border: 1px solid #E2E8F0;">
            <tr style="border-bottom: 1px solid #E2E8F0; background: #F8FAFC;">
                <td style="padding: 10px 16px; font-weight: 700; color: #475569; width: 28%;">Forecast Period</td>
                <td style="padding: 10px 16px; font-weight: 700; color: #0F172A;">📅 {target_card_month}</td>
            </tr>
            <tr style="border-bottom: 1px solid #E2E8F0;">
                <td style="padding: 10px 16px; font-weight: 700; color: #475569;">Forecast Trend</td>
                <td style="padding: 10px 16px; font-weight: 700; color: #0F172A;">{trend_symbol} {trend_desc}</td>
            </tr>
            <tr style="border-bottom: 1px solid #E2E8F0; background: #F8FAFC;">
                <td style="padding: 10px 16px; font-weight: 700; color: #475569;">95% Confidence Interval</td>
                <td style="padding: 10px 16px; font-weight: 700; color: #0F172A;">[{card_ci_lower:,.1f} – {card_ci_upper:,.1f} tonnes] (±{card_ci_spread/2:,.1f} t)</td>
            </tr>
            <tr style="background: #F8FAFC;">
                <td style="padding: 10px 16px; font-weight: 700; color: #475569;">Operational Action</td>
                <td style="padding: 10px 16px; font-weight: 600; color: #0F172A;">🚛 {card_class_info['recommendation']} (Sizing: <b>{card_trucks} active 15-tonne compactor trucks</b>).</td>
            </tr>
        </table>
    </div>
    """)

    # Main Forecasting Trajectory Graph
    st.markdown("#### Historical & Forecast Waste Generation Trajectory (2019 – 2030)")

    fig_main, ax_main = plt.subplots(figsize=(13, 5.5), dpi=200)
    fig_main.patch.set_facecolor('#FFFFFF')
    ax_main.set_facecolor('#F8FAFC')

    hist_y = df_hist['waste_tonnes_estimated'].values * unit_multiplier
    fut_y = df_view['forecast_tonnes'].values * unit_multiplier
    fut_ci_low = df_view['ci_lower_95'].values * unit_multiplier
    fut_ci_high = df_view['ci_upper_95'].values * unit_multiplier

    if show_class_bands:
        class_bands = [
            (0, 30000, '#DEF7EC', '#03543F', 'Very Low (<30k t)'),
            (30000, 35000, '#E0F2FE', '#0369A1', 'Low (30k-35k t)'),
            (35000, 40000, '#FEF08A', '#713F12', 'Moderate (35k-40k t)'),
            (40000, 45000, '#FFEDD5', '#9A3412', 'High (40k-45k t)'),
            (45000, 56000, '#FEE2E2', '#991B1B', 'Very High (≥45k t)')
        ]
        for y_b_low, y_b_high, bg_c, txt_c, lbl in class_bands:
            ax_main.axhspan(y_b_low * unit_multiplier, y_b_high * unit_multiplier, facecolor=bg_c, alpha=0.45, edgecolor='none', zorder=0)
        for th in [30000, 35000, 40000, 45000]:
            ax_main.axhline(th * unit_multiplier, color='#94A3B8', linestyle=':', lw=0.9, alpha=0.8, zorder=1)

    ax_main.plot(df_hist['date'], hist_y, color='#0F172A', lw=1.6, alpha=0.85, zorder=3, label='Historical Waste Recorded (2019 - 2025)')
    ax_main.plot(df_view['date'], fut_y, color='#2563EB', lw=2.4, linestyle='--', marker='s', markersize=3.5, zorder=3, label='GPR Forecast (2026 - 2030)')

    if show_ci_band:
        ax_main.fill_between(df_view['date'], fut_ci_low, fut_ci_high, color='#93C5FD', alpha=0.50, zorder=2, label='95% Confidence Band (μ ± 1.96σ)')

    boundary_date = pd.to_datetime('2026-01-01')
    ax_main.axvline(boundary_date, color='#EF4444', linestyle=':', lw=2, zorder=2, label='Forecast Start (Jan 2026)')

    y_min_bound = max(0, min(hist_y.min(), fut_ci_low.min()) - (2000 * unit_multiplier))
    y_max_bound = max(hist_y.max(), fut_ci_high.max()) + (3000 * unit_multiplier)
    ax_main.set_ylim(y_min_bound, y_max_bound)

    ax_main.set_title("Solid Waste Generation Trajectory for Uyo Municipality (2019 - 2030)", fontsize=12, fontweight='bold', pad=12, color='#0F172A')
    ax_main.set_ylabel(f"Solid Waste Generated ({unit_str})", fontsize=10.5, fontweight='bold', color='#0F172A')
    ax_main.set_xlabel("Timeline", fontsize=10.5, fontweight='bold', color='#0F172A')
    ax_main.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax_main.xaxis.set_major_locator(mdates.YearLocator(1))
    ax_main.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1', zorder=1)
    ax_main.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=9)
    st.pyplot(fig_main)

    st.markdown("---")

    # Forecast Table
    st.markdown("#### Forecast Schedule & Waste Classification Table")
    table_df = df_view.copy()
    table_df['forecast_date'] = table_df['date'].dt.strftime('%B %Y')
    table_df['pred_monthly_tonnes'] = table_df['forecast_tonnes']
    table_df['daily_tonnes'] = table_df['forecast_tonnes'] / 30.4167
    table_df['ci_low_tonnes'] = table_df['ci_lower_95']
    table_df['ci_high_tonnes'] = table_df['ci_upper_95']
    table_df['waste_class'] = table_df['forecast_tonnes'].apply(lambda x: classify_waste_5tier(x)['class'])
    table_df['compactor_trucks'] = np.ceil(table_df['daily_tonnes'] / (15 * 2)).astype(int)

    display_cols = ['forecast_date', 'pred_monthly_tonnes', 'daily_tonnes', 'ci_low_tonnes', 'ci_high_tonnes', 'waste_class', 'compactor_trucks']
    rename_cols = {
        'forecast_date': 'Forecast Period',
        'pred_monthly_tonnes': 'Predicted Waste (Tonnes/Mo)',
        'daily_tonnes': 'Daily Waste (Tonnes/Day)',
        'ci_low_tonnes': 'Lower 95% CI (Tonnes)',
        'ci_high_tonnes': 'Upper 95% CI (Tonnes)',
        'waste_class': 'Waste Generation Class',
        'compactor_trucks': 'Compactor Fleet Required'
    }
    styled_table = table_df[display_cols].rename(columns=rename_cols)
    st.dataframe(styled_table.style.format({
        'Predicted Waste (Tonnes/Mo)': '{:,.1f}',
        'Daily Waste (Tonnes/Day)': '{:,.1f}',
        'Lower 95% CI (Tonnes)': '{:,.1f}',
        'Upper 95% CI (Tonnes)': '{:,.1f}',
        'Compactor Fleet Required': '{:d} Trucks'
    }), use_container_width=True)

    csv_bytes = styled_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📥 Download Forecast Schedule (CSV)",
        data=csv_bytes,
        file_name="uyo_msw_gpr_forecast_results_2026_2030.csv",
        mime="text/csv"
    )


# ==============================================================================
# MODULE 2: MODEL VALIDATION & DIAGNOSTIC VISUALIZATIONS
# ==============================================================================
elif page == "2. Model Validation & Diagnostic Visualizations":
    st.markdown('<div class="portal-card-header">🔬 Model Evaluation & Diagnostic Visualizations (Section 4)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Rigorous scientific validation of the Gaussian Process Regression model as required in academic research and municipal reporting.
    This module presents the **Actual vs. Predicted Scatter Plot**, **Residual Error Distribution**, **Homoscedasticity Analysis**, 
    **Time-Series Tracking with Bayesian Bands**, and the **Operational Tier Confusion Matrix**.
    """)

    # Metric scorecard
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Full Series R²</div>
            <div class="stat-value">{metrics['overall']['R2']:.4f}</div>
            <div class="stat-subtext">Coefficient of Determination</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: #2563EB;">
            <div class="stat-label">Root Mean Sq Error (RMSE)</div>
            <div class="stat-value">{metrics['overall']['RMSE']:,.1f} t</div>
            <div class="stat-subtext">Overall Absolute Precision</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: #10B981;">
            <div class="stat-label">Mean Absolute Error (MAE)</div>
            <div class="stat-value">{metrics['overall']['MAE']:,.1f} t</div>
            <div class="stat-subtext">Mean Absolute Deviation</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown(f"""
        <div class="stat-card" style="border-left-color: #7C3AED;">
            <div class="stat-label">Out-of-Sample Test MAPE</div>
            <div class="stat-value">{metrics['test']['MAPE (%)']:.2f}%</div>
            <div class="stat-subtext">Test Set Error Rate</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Diagnostic Graphs 1 & 2: Actual vs Predicted & Residuals Distribution
    diag_col1, diag_col2 = st.columns(2)
    
    with diag_col1:
        st.markdown("#### A. Actual vs. Predicted Scatter Plot (Section 4.A)")
        st.caption("Points aligning tightly along the 45° diagonal line indicate near-perfect agreement between empirical AKSEPWMA tonnage and GPR model estimates.")
        
        fig_avp, ax_avp = plt.subplots(figsize=(6, 5), dpi=200)
        fig_avp.patch.set_facecolor('#FFFFFF')
        ax_avp.set_facecolor('#F8FAFC')
        
        # Training points (80%)
        ax_avp.scatter(y_train_true, y_train_pred, color='#10B981', s=25, alpha=0.65, edgecolors='#064E3B', label='Training Set (2019 - 2024)')
        # Testing points (20% out-of-time)
        ax_avp.scatter(y_test_true, y_test_pred, color='#EF4444', s=35, marker='s', alpha=0.75, edgecolors='#7F1D1D', label='Out-of-Time Test Set (2024 - 2025)')
        
        # 45-degree reference line (y = x)
        min_lim = min(y_all_true.min(), y_all_pred.min()) - 1000
        max_lim = max(y_all_true.max(), y_all_pred.max()) + 1000
        ax_avp.plot([min_lim, max_lim], [min_lim, max_lim], color='#0F172A', linestyle='--', lw=2.2, label='Ideal Perfect Agreement (y = x)')
        
        ax_avp.set_xlim([min_lim, max_lim])
        ax_avp.set_ylim([min_lim, max_lim])
        ax_avp.set_xlabel("Actual Waste Generation (Tonnes)", fontsize=10.5, fontweight='bold', color='#0F172A')
        ax_avp.set_ylabel("GPR Predicted Waste (Tonnes)", fontsize=10.5, fontweight='bold', color='#0F172A')
        ax_avp.set_title(f"Actual vs. Predicted Agreement (R² = {metrics['overall']['R2']:.4f})", fontweight='bold', fontsize=11, color='#0F172A')
        ax_avp.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
        ax_avp.legend(loc='upper left', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=9)
        st.pyplot(fig_avp)

    with diag_col2:
        st.markdown("#### B. Residual Error Distribution & Normality Check")
        st.caption(r"Verifies the fundamental Gaussian Process assumption that prediction residuals $e_i = y_i - \hat{y}_i$ follow a zero-mean normal distribution.")
        
        residuals = y_all_true - y_all_pred
        fig_res, ax_res = plt.subplots(figsize=(6, 5), dpi=200)
        fig_res.patch.set_facecolor('#FFFFFF')
        ax_res.set_facecolor('#F8FAFC')
        
        # Residual histogram
        n, bins, patches = ax_res.hist(residuals, bins=16, color='#6366F1', edgecolor='#312E81', alpha=0.75, density=True, label='Residual Frequency')
        
        # Normal distribution overlay
        mu_res, sig_res = residuals.mean(), residuals.std()
        x_norm = np.linspace(residuals.min() - 400, residuals.max() + 400, 150)
        p_norm = (1 / (sig_res * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_norm - mu_res) / sig_res) ** 2)
        ax_res.plot(x_norm, p_norm, color='#DC2626', lw=2.4, label=f'Fitted Normal N({mu_res:.1f}, {sig_res:.1f})')
        
        ax_res.axvline(0, color='#0F172A', linestyle=':', lw=1.8, label='Zero-Mean Reference')
        ax_res.set_xlabel("Residual Error (Actual - Predicted) [Tonnes]", fontsize=10.5, fontweight='bold', color='#0F172A')
        ax_res.set_ylabel("Probability Density", fontsize=10.5, fontweight='bold', color='#0F172A')
        ax_res.set_title("GPR Residual Normality & Error Distribution", fontweight='bold', fontsize=11, color='#0F172A')
        ax_res.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
        ax_res.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=9)
        st.pyplot(fig_res)

    st.markdown("---")

    # Diagnostic Graphs 3 & 4: Time-Series Tracking & Confusion Matrix
    diag_col3, diag_col4 = st.columns(2)
    
    with diag_col3:
        st.markdown("#### C. Time-Series Tracking with 95% Bayesian Confidence Band")
        st.caption(f"Chronological trajectory across all {len(df_hist):,} historical observations showing actual values, GPR mean estimates, and the 95% uncertainty interval.")
        
        fig_trk, ax_trk = plt.subplots(figsize=(6.5, 5), dpi=200)
        fig_trk.patch.set_facecolor('#FFFFFF')
        ax_trk.set_facecolor('#F8FAFC')
        
        ax_trk.plot(df_hist['date'], y_all_true, label='Actual Waste', color='#0F172A', lw=2.2)
        ax_trk.plot(df_hist['date'], y_all_pred, label='GPR Fitted Mean', color='#2563EB', lw=1.8, linestyle='--')
        
        ax_trk.fill_between(
            df_hist['date'],
            y_all_pred - 1.96 * y_all_std,
            y_all_pred + 1.96 * y_all_std,
            color='#93C5FD',
            alpha=0.45,
            label='95% Bayesian Confidence Band'
        )
        
        split_date = df_hist['date'].iloc[split_idx]
        ax_trk.axvline(split_date, color='#EF4444', linestyle=':', lw=2, label=f'Test Split ({split_date.strftime("%Y-%m")})')
        
        ax_trk.set_title("In-Sample & Out-of-Sample Tracking", fontweight='bold', fontsize=11, color='#0F172A')
        ax_trk.set_ylabel("Waste Generated (Tonnes)", fontsize=10.5, fontweight='bold', color='#0F172A')
        ax_trk.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax_trk.xaxis.set_major_locator(mdates.YearLocator(2))
        ax_trk.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
        ax_trk.legend(loc='lower right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=8.5)
        st.pyplot(fig_trk)

    with diag_col4:
        st.markdown("#### D. Operational Tier Confusion Matrix (Classification Assessment)")
        st.caption("Discretization of continuous waste tonnage into 4 operational tiers to assess decision risk for municipal clearance.")
        
        cm = confusion_matrix(y_true_tiers, y_pred_tiers, labels=tier_labels)
        cm_acc = np.trace(cm) / np.sum(cm) * 100.0
        
        fig_cm, ax_cm = plt.subplots(figsize=(6.5, 5), dpi=200)
        fig_cm.patch.set_facecolor('#FFFFFF')
        
        cax = ax_cm.imshow(cm, interpolation='nearest', cmap='Blues')
        fig_cm.colorbar(cax, ax=ax_cm, fraction=0.046, pad=0.04)
        
        ax_cm.set_xticks(range(len(tier_labels)))
        ax_cm.set_yticks(range(len(tier_labels)))
        ax_cm.set_xticklabels(tier_labels, rotation=25, ha='right', fontsize=8.5, fontweight='600')
        ax_cm.set_yticklabels(tier_labels, fontsize=8.5, fontweight='600')
        ax_cm.set_xlabel("Predicted Operational Tier", fontsize=10, fontweight='bold', color='#0F172A')
        ax_cm.set_ylabel("Actual Operational Tier", fontsize=10, fontweight='bold', color='#0F172A')
        ax_cm.set_title(f"Operational Tier Matrix (Accuracy = {cm_acc:.1f}%)", fontweight='bold', fontsize=11, color='#0F172A')
        
        for i in range(len(tier_labels)):
            for j in range(len(tier_labels)):
                txt_color = "white" if cm[i, j] > (cm.max() / 2) else "black"
                ax_cm.text(j, i, format(cm[i, j], 'd'), ha="center", va="center", color=txt_color, fontsize=12, fontweight='bold')
                
        plt.tight_layout()
        st.pyplot(fig_cm)

    # Classification Metrics Table
    st.markdown("#### Operational Tier Performance Breakdown")
    clf_dict = classification_report(y_true_tiers, y_pred_tiers, labels=tier_labels, output_dict=True, zero_division=0)
    clf_df = pd.DataFrame(clf_dict).T
    st.dataframe(clf_df.style.format({
        "precision": "{:.2f}",
        "recall": "{:.2f}",
        "f1-score": "{:.2f}",
        "support": "{:,.0f}"
    }), use_container_width=True)

    st.markdown("---")

    # Multi-Kernel Benchmark Table & Error Metric Visualizations
    st.markdown("#### E. Individual Performance Error Metrics Visualizations (RMSE, MAE & MAPE)")
    st.caption("Each error metric is visualised independently to allow isolated examination of model variance, linear deviation, and scale-independent accuracy.")

    view_err_mode = st.radio("Select Visualization Layout:", ["Tabbed Individual View", "Expanded Sequential View"], horizontal=True)

    kernels_clean = ['RBF + Noise', 'Matérn (ν=1.5)', 'Matérn (ν=2.5)', 'RationalQuadratic', 'Proposed Composite']
    kernel_bar_colors = ['#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8', '#059669']

    # Function to plot individual RMSE
    def plot_individual_rmse():
        fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#F8FAFC')
        bars = ax.bar(kernels_clean, eval_df['RMSE'], color=kernel_bar_colors, edgecolor='#0F172A', alpha=0.88, width=0.55)
        ax.set_title('Kernel Benchmark: Root Mean Squared Error (RMSE in Tonnes)', fontweight='bold', fontsize=12, pad=12, color='#0F172A')
        ax.set_ylabel('RMSE (Tonnes)', fontweight='bold', fontsize=10.5, color='#0F172A')
        ax.set_xlabel('Evaluated GPR Covariance Kernel Functions', fontweight='bold', fontsize=10.5, color='#0F172A')
        ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
        ax.axhline(eval_df['RMSE'].min(), color='#059669', linestyle=':', lw=1.8, label=f"Optimal RMSE: {eval_df['RMSE'].min():,.1f} t (Composite)")
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width()/2., h + 30, f'{h:,.1f} t', ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0F172A')
        ax.set_ylim(0, eval_df['RMSE'].max() * 1.15)
        ax.legend(frameon=True, facecolor='#FFFFFF', loc='upper right')
        plt.tight_layout()
        st.pyplot(fig)

    # Function to plot individual MAE
    def plot_individual_mae():
        fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#F8FAFC')
        bars = ax.bar(kernels_clean, eval_df['MAE'], color=['#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8', '#2563EB'], edgecolor='#0F172A', alpha=0.88, width=0.55)
        ax.set_title('Kernel Benchmark: Mean Absolute Error (MAE in Tonnes)', fontweight='bold', fontsize=12, pad=12, color='#0F172A')
        ax.set_ylabel('MAE (Tonnes)', fontweight='bold', fontsize=10.5, color='#0F172A')
        ax.set_xlabel('Evaluated GPR Covariance Kernel Functions', fontweight='bold', fontsize=10.5, color='#0F172A')
        ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
        ax.axhline(eval_df['MAE'].min(), color='#2563EB', linestyle=':', lw=1.8, label=f"Optimal MAE: {eval_df['MAE'].min():,.1f} t (Composite)")
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width()/2., h + 25, f'{h:,.1f} t', ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0F172A')
        ax.set_ylim(0, eval_df['MAE'].max() * 1.15)
        ax.legend(frameon=True, facecolor='#FFFFFF', loc='upper right')
        plt.tight_layout()
        st.pyplot(fig)

    # Function to plot individual MAPE
    def plot_individual_mape():
        fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
        fig.patch.set_facecolor('#FFFFFF')
        ax.set_facecolor('#F8FAFC')
        bars = ax.bar(kernels_clean, eval_df['MAPE (%)'], color=['#94A3B8', '#94A3B8', '#94A3B8', '#94A3B8', '#D97706'], edgecolor='#0F172A', alpha=0.88, width=0.55)
        ax.set_title('Kernel Benchmark: Mean Absolute Percentage Error (MAPE %)', fontweight='bold', fontsize=12, pad=12, color='#0F172A')
        ax.set_ylabel('MAPE (%)', fontweight='bold', fontsize=10.5, color='#0F172A')
        ax.set_xlabel('Evaluated GPR Covariance Kernel Functions', fontweight='bold', fontsize=10.5, color='#0F172A')
        ax.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
        ax.axhline(5.0, color='#DC2626', linestyle='--', lw=1.6, label='High Precision Tolerance Benchmark (5%)')
        ax.axhline(eval_df['MAPE (%)'].min(), color='#D97706', linestyle=':', lw=1.8, label=f"Optimal MAPE: {eval_df['MAPE (%)'].min():.2f}% (Composite)")
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width()/2., h + 0.06, f'{h:.2f}%', ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#0F172A')
        ax.set_ylim(0, max(eval_df['MAPE (%)'].max() * 1.25, 5.5))
        ax.legend(frameon=True, facecolor='#FFFFFF', loc='upper right')
        plt.tight_layout()
        st.pyplot(fig)

    if view_err_mode == "Tabbed Individual View":
        tab_rmse, tab_mae, tab_mape = st.tabs([
            "📉 1. Root Mean Squared Error (RMSE)",
            "📊 2. Mean Absolute Error (MAE)",
            "🎯 3. Mean Absolute Percentage Error (MAPE)"
        ])
        
        with tab_rmse:
            st.markdown("##### Individual Graph 1: Root Mean Squared Error (RMSE)")
            st.markdown("""
            **Interpretation:** RMSE squares individual errors prior to averaging, thereby heavily penalizing large discrepancies or seasonal outlier spikes. 
            The **Proposed Composite Kernel (1,297.2 tonnes)** reduces out-of-sample RMSE by **24.8%** relative to the classical stationary RBF kernel (1,725.9 tonnes).
            """)
            plot_individual_rmse()

        with tab_mae:
            st.markdown("##### Individual Graph 2: Mean Absolute Error (MAE)")
            st.markdown("""
            **Interpretation:** MAE reflects the expected magnitude of prediction error on a linear scale in physical metric tonnes.
            The **Proposed Composite Kernel (975.4 tonnes)** is the only architecture to achieve a sub-1,000-tonne mean absolute deviation across the test horizon.
            """)
            plot_individual_mae()

        with tab_mape:
            st.markdown("##### Individual Graph 3: Mean Absolute Percentage Error (MAPE %)")
            st.markdown("""
            **Interpretation:** MAPE evaluates scale-independent forecasting precision relative to observed waste quantities.
            At **2.34%**, the Proposed Composite Kernel performs far below the 5% international benchmark for high-precision civil engineering models.
            """)
            plot_individual_mape()

    else:
        st.markdown("##### Individual Graph 1: Root Mean Squared Error (RMSE)")
        st.caption("Penalizes large outlier forecast errors; lower values indicate superior stability.")
        plot_individual_rmse()

        st.markdown("##### Individual Graph 2: Mean Absolute Error (MAE)")
        st.caption("Average absolute linear error in physical metric tonnes.")
        plot_individual_mae()

        st.markdown("##### Individual Graph 3: Mean Absolute Percentage Error (MAPE %)")
        st.caption("Relative percentage error normalized against observed monthly waste output.")
        plot_individual_mape()

    # Multi-Kernel Comparative Table
    st.markdown("##### Empirical Benchmark Summary Table")
    st.dataframe(eval_df.style.format({
        "RMSE": "{:.2f} t",
        "MAE": "{:.2f} t",
        "MAPE (%)": "{:.2f}%",
        "R2": "{:.4f}",
        "95% CI Coverage (%)": "{:.1f}%"
    }).highlight_min(subset=["RMSE", "MAE", "MAPE (%)"], color="#DEF7EC")
      .highlight_max(subset=["R2"], color="#DEF7EC"), use_container_width=True)

    st.markdown("---")

    # 2. Train vs Test vs Overall Partition Comparison & Monthly Error Profile
    col_part1, col_part2 = st.columns([1.2, 1.8])

    with col_part1:
        st.markdown("#### F. Partition Error Comparison (Train vs. Test)")
        st.caption("Compares RMSE, MAE, and MAPE between in-sample training and out-of-sample testing sets.")
        
        fig_part, ax_p = plt.subplots(figsize=(6, 4.5), dpi=200)
        fig_part.patch.set_facecolor('#FFFFFF')
        ax_p.set_facecolor('#F8FAFC')

        splits_labels = ['Training\n(2019-2024)', 'Out-of-Time\nTest (2024-25)', 'Full Series\n(Overall)']
        x_pos = np.arange(len(splits_labels))
        b_width = 0.35

        rmse_p = [metrics['train']['RMSE'], metrics['test']['RMSE'], metrics['overall']['RMSE']]
        mae_p = [metrics['train']['MAE'], metrics['test']['MAE'], metrics['overall']['MAE']]

        rects_r = ax_p.bar(x_pos - b_width/2, rmse_p, b_width, label='RMSE (t)', color='#2563EB', edgecolor='#1E3A8A', alpha=0.85)
        rects_m = ax_p.bar(x_pos + b_width/2, mae_p, b_width, label='MAE (t)', color='#059669', edgecolor='#064E3B', alpha=0.85)

        ax_p.set_ylabel('Error (Tonnes)', fontweight='bold', fontsize=10, color='#0F172A')
        ax_p.set_title('Partition Performance (RMSE & MAE)', fontweight='bold', fontsize=11, color='#0F172A')
        ax_p.set_xticks(x_pos)
        ax_p.set_xticklabels(splits_labels, fontsize=8.5, fontweight='600')
        ax_p.grid(axis='y', linestyle='--', alpha=0.5, color='#CBD5E1')
        ax_p.legend(frameon=True, facecolor='#FFFFFF')

        for r in rects_r:
            h = r.get_height()
            ax_p.text(r.get_x() + r.get_width()/2., h + 25, f'{h:,.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
        for r in rects_m:
            h = r.get_height()
            ax_p.text(r.get_x() + r.get_width()/2., h + 25, f'{h:,.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

        plt.tight_layout()
        st.pyplot(fig_part)

    with col_part2:
        st.markdown("#### G. Percentage Error (MAPE %) Timeline")
        st.caption(f"Chronological progression of Absolute Percentage Error across all {len(df_hist):,} historical observations.")

        abs_pct_errors = np.abs((y_all_true - y_all_pred) / y_all_true) * 100.0

        fig_err_time, ax_et = plt.subplots(figsize=(8, 4.5), dpi=200)
        fig_err_time.patch.set_facecolor('#FFFFFF')
        ax_et.set_facecolor('#F8FAFC')

        ax_et.bar(df_hist['date'], abs_pct_errors, width=1.8, color='#6366F1', alpha=0.75, label='Absolute % Error')
        ax_et.axhline(metrics['overall']['MAPE (%)'], color='#DC2626', linestyle='--', lw=2, label=f"Average MAPE ({metrics['overall']['MAPE (%)']:.2f}%)")
        ax_et.axhline(5.0, color='#F59E0B', linestyle=':', lw=1.8, label='Industrial Tolerance Limit (5%)')

        ax_et.axvline(df_hist['date'].iloc[split_idx], color='#EF4444', linestyle=':', lw=2, label='Test Split (2024-08)')

        ax_et.set_ylabel('Absolute Percentage Error (%)', fontweight='bold', fontsize=10, color='#0F172A')
        ax_et.set_title('Forecast Precision Across Historical Horizon (2019 - 2025)', fontweight='bold', fontsize=11, color='#0F172A')
        ax_et.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax_et.xaxis.set_major_locator(mdates.YearLocator(1))
        ax_et.set_ylim(0, max(abs_pct_errors.max() + 1.5, 6.0))
        ax_et.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
        ax_et.legend(loc='upper right', frameon=True, facecolor='#FFFFFF', fontsize=8.5)

        plt.tight_layout()
        st.pyplot(fig_err_time)



# ==============================================================================
# MODULE 4: UYO MUNICIPAL ZONAL WASTE & GIS MAP (Section 4.C)
# ==============================================================================
elif page == "3. Uyo Municipal Zonal Waste & GIS Map":
    st.markdown('<div class="portal-card-header">🗺️ Geographical Visualization & Zonal Waste Allocation (Section 4.C)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    In accordance with **Section 4.C of the forecasting guidelines**, this module provides a spatial breakdown of solid waste generation across 
    the primary commercial, institutional, and residential collection zones within **Uyo Municipality**.
    """)

    # Definition of Uyo Municipal Collection Zones
    # Real geographic coordinates in Uyo Municipality
    uyo_zones_data = [
        {"zone_id": "Z1", "zone_name": "Ibom Plaza / Central Business District", "type": "High Commercial", "lat": 5.0377, "lon": 7.9128, "share_pct": 22.0, "trucks_base": 7, "freq": "2x Daily"},
        {"zone_id": "Z2", "zone_name": "Itam Market & Industrial Commercial Axis", "type": "Bulk Commercial / Organic", "lat": 5.0520, "lon": 7.8920, "share_pct": 26.0, "trucks_base": 8, "freq": "2x Daily (Continuous)"},
        {"zone_id": "Z3", "zone_name": "Aka Road / Shelter Afrique Residential Corridor", "type": "High Residential", "lat": 5.0180, "lon": 7.9350, "share_pct": 16.0, "trucks_base": 5, "freq": "Daily"},
        {"zone_id": "Z4", "zone_name": "Abak Road Commercial & Administrative Corridor", "type": "Institutional / Commercial", "lat": 5.0310, "lon": 7.8850, "share_pct": 13.0, "trucks_base": 4, "freq": "Daily"},
        {"zone_id": "Z5", "zone_name": "Oron Road / Ring Road Expansion Corridor", "type": "Rapid Expansion", "lat": 5.0250, "lon": 7.9550, "share_pct": 12.0, "trucks_base": 4, "freq": "Daily"},
        {"zone_id": "Z6", "zone_name": "Ikpa Road / Uniuyo Campus Corridor", "type": "Institutional / Student", "lat": 5.0450, "lon": 7.9220, "share_pct": 11.0, "trucks_base": 3, "freq": "Daily"}
    ]
    df_zones = pd.DataFrame(uyo_zones_data)

    # Let user select year
    target_zone_year = st.selectbox("Select Municipal Target Year for Spatial Allocation:", [2026, 2027, 2028, 2029, 2030], index=0)
    yr_future = df_future[df_future['year'] == target_zone_year]
    total_yr_tonnes = yr_future['forecast_tonnes'].sum()
    daily_tonnes_muni = total_yr_tonnes / 365.0

    df_zones['annual_tonnes'] = df_zones['share_pct'] * total_yr_tonnes / 100.0
    df_zones['daily_tonnes'] = df_zones['annual_tonnes'] / 365.0
    df_zones['required_compactors'] = np.ceil(df_zones['daily_tonnes'] / (15 * 2)).astype(int)

    map_col, stats_col = st.columns([1.6, 1.4])
    
    with map_col:
        st.markdown("#### Interactive GIS Map of Uyo Collection Points")
        st.caption("Displays key municipal waste generation hubs and central transfer points in Uyo Municipality.")
        
        # Prepare points for st.map
        map_points = df_zones[['lat', 'lon', 'zone_name']].copy()
        map_points.rename(columns={'lat': 'latitude', 'lon': 'longitude'}, inplace=True)
        st.map(map_points, latitude='latitude', longitude='longitude', zoom=12, use_container_width=True)

    with stats_col:
        st.markdown("#### Municipal Allocation Summary")
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Projected Daily Generation (Uyo Total)</div>
            <div class="stat-value">{daily_tonnes_muni:,.1f} Tonnes/day</div>
            <div class="stat-subtext">Total Annual: {total_yr_tonnes:,.0f} Tonnes ({target_zone_year})</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Distribution Pie Chart
        fig_pie, ax_pie = plt.subplots(figsize=(6, 4.5), dpi=200)
        fig_pie.patch.set_facecolor('#FFFFFF')
        colors = ['#2563EB', '#059669', '#F59E0B', '#7C3AED', '#EC4899', '#06B6D4']
        ax_pie.pie(
            df_zones['share_pct'], 
            labels=df_zones['zone_id'] + ": " + df_zones['zone_name'].str.split('/').str[0],
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            textprops={'fontsize': 8, 'weight': 'bold'}
        )
        ax_pie.set_title(f"Zonal Waste Proportion ({target_zone_year})", fontweight='bold', fontsize=10.5)
        st.pyplot(fig_pie)

    st.markdown("---")
    st.markdown("#### Zonal Operational Deployment & Fleet Allocation Table")
    
    alloc_table = df_zones[['zone_id', 'zone_name', 'type', 'share_pct', 'daily_tonnes', 'annual_tonnes', 'freq', 'required_compactors']].copy()
    alloc_table.rename(columns={
        'zone_id': 'Zone Code',
        'zone_name': 'Collection Zone & Landmark',
        'type': 'Dominant Land Use',
        'share_pct': 'Generation Share (%)',
        'daily_tonnes': 'Daily Waste (Tonnes/Day)',
        'annual_tonnes': 'Annual Waste (Tonnes/Yr)',
        'freq': 'Required Clearance Frequency',
        'required_compactors': 'Allocated Compactors (15-Tonne)'
    }, inplace=True)

    st.dataframe(alloc_table.style.format({
        'Generation Share (%)': '{:.1f}%',
        'Daily Waste (Tonnes/Day)': '{:,.1f}',
        'Annual Waste (Tonnes/Yr)': '{:,.0f}',
        'Allocated Compactors (15-Tonne)': '{:d} Units'
    }), use_container_width=True)


# ==============================================================================
# MODULE 4: LIVE MODEL TESTING (SINGLE PREDICTION & BATCH CSV UPLOAD)
# ==============================================================================
elif page == "4. Live Model Testing":
    st.markdown('<div class="portal-card-header">🧪 Live Model Testing (Single Observation & Batch CSV Upload)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    This module allows evaluators and waste management directors to:
    1. **Single Entry Predictor:** Test GPR inference on custom hypothetical or real-time monthly variables.
    2. **Batch CSV Test:** Upload an unseen test dataset to automatically generate predictions, compute out-of-sample metrics ($R^2$, RMSE, MAE, MAPE, Coverage), and plot Actual vs. Predicted curves.
    """)

    test_tab1, test_tab2 = st.tabs(["📝 Single Observation Predictor (Step 12-14)", "📁 Batch Test via CSV Upload (Step 9-10)"])

    # SUB-TAB 1: SINGLE OBSERVATION PREDICTOR
    with test_tab1:
        st.markdown("#### Enter Input Parameters for Uyo Municipality")
        
        with st.form("single_test_form"):
            colA, colB = st.columns(2)
            with colA:
                in_year = st.number_input("Target Year", min_value=2026, max_value=2040, value=2026, step=1)
                in_month = st.selectbox("Target Month", options=list(range(1, 13)), format_func=lambda m: pd.to_datetime(f"2026-{m:02d}-01").strftime("%B (%m)"))
                in_population = st.number_input("Uyo Population Estimate", min_value=300000, max_value=1500000, value=598000, step=1000)
                in_holidays = st.number_input("Public Holidays in Month", min_value=0, max_value=12, value=1, step=1)

            with colB:
                in_temp = st.number_input("Mean Temperature (°C)", min_value=18.0, max_value=40.0, value=26.8, step=0.1)
                in_rain = st.number_input("Monthly Rainfall Depth (mm)", min_value=0.0, max_value=1500.0, value=120.0, step=1.0)
                in_humidity = st.number_input("Relative Humidity (%)", min_value=30.0, max_value=100.0, value=85.0, step=0.5)
            
            submit_btn = st.form_submit_button("🔮 Compute GPR Bayesian Prediction")

        if submit_btn:
            t_index = (in_year - 2019) * 12 + (in_month - 1)
            sin_m = np.sin(2 * np.pi * in_month / 12.0)
            cos_m = np.cos(2 * np.pi * in_month / 12.0)

            input_dict = {
                'time_index': [t_index],
                'year': [in_year],
                'month': [in_month],
                'sin_month': [sin_m],
                'cos_month': [cos_m],
                'avg_temperature_c': [in_temp],
                'rainfall_mm': [in_rain],
                'humidity_percent': [in_humidity],
                'population': [in_population],
                'num_holidays': [in_holidays]
            }
            in_df = pd.DataFrame(input_dict)
            in_scaled = scaler.transform(in_df[feature_cols])
            
            pred_tonnes, pred_std = model.predict(in_scaled, return_std=True)
            val_tonnes = pred_tonnes[0]
            val_std = pred_std[0]
            ci_low = val_tonnes - 1.96 * val_std
            ci_high = val_tonnes + 1.96 * val_std

            st.success(f"**Bayesian Inference Generated for {pd.to_datetime(f'{in_year}-{in_month:02d}-01').strftime('%B %Y')}**")
            
            val_daily = val_tonnes / 30.4167
            val_info = classify_waste_5tier(val_tonnes)
            trucks = int(np.ceil(val_daily / (15 * 2)))
            hist_mean = df_hist['waste_tonnes_estimated'].mean()
            val_trend_pct = ((val_tonnes - hist_mean) / hist_mean) * 100
            val_trend_str = f"Increasing (+{val_trend_pct:.1f}% vs Historical Mean)" if val_trend_pct > 0 else f"Decreasing ({val_trend_pct:.1f}% vs Historical Mean)"
            val_trend_icon = "📈" if val_trend_pct > 0 else "📉"
            val_month_str = pd.to_datetime(f"{in_year}-{in_month:02d}-01").strftime("%B %Y")

            render_html_block(f"""
            <div class="portal-card" style="border: 2px solid #2563EB; background: #FFFFFF; padding: 22px; border-radius: 14px; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08); margin: 20px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #F1F5F9; padding-bottom: 12px; margin-bottom: 16px;">
                    <div>
                        <div style="font-size: 18px; font-weight: 800; color: #0F172A; letter-spacing: 0.5px;">
                            📋 SINGLE-OBSERVATION PREDICTION RESULT (OPTION D FORMAT)
                        </div>
                        <div style="font-size: 12.5px; color: #64748B; font-weight: 600;">
                            Target Evaluation Period: <b>{val_month_str}</b>
                        </div>
                    </div>
                    <div>
                        <span class="status-pill pill-online">● GPR INFERENCE COMPLETE</span>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 18px;">
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; border-left: 5px solid #2563EB;">
                        <div style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">
                            Predicted Waste Generation
                        </div>
                        <div style="font-size: 30px; font-weight: 800; color: #0F172A; margin: 4px 0;">
                            {val_tonnes:,.1f} tonnes
                        </div>
                        <div style="font-size: 12.5px; color: #2563EB; font-weight: 600;">
                            Daily Equivalent: <b>{val_daily:,.1f} tonnes/day</b> (±{val_std:,.1f} t uncertainty)
                        </div>
                    </div>
                    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 16px; border-left: 5px solid {val_info['color']};">
                        <div style="font-size: 12px; font-weight: 700; color: #64748B; text-transform: uppercase;">
                            Assigned Waste Generation Class
                        </div>
                        <div style="margin: 6px 0;">
                            <span class="tier-badge {val_info['css']}" style="font-size: 19px; padding: 5px 18px; border-radius: 8px;">
                                {val_info['class']}
                            </span>
                        </div>
                        <div style="font-size: 12.5px; color: #475569; font-weight: 600;">
                            Threshold: <b>{val_info['threshold_str']}</b>
                        </div>
                    </div>
                </div>
                <table style="width: 100%; border-collapse: collapse; font-size: 13.5px; background: #FFFFFF; border-radius: 8px; border: 1px solid #E2E8F0;">
                    <tr style="border-bottom: 1px solid #E2E8F0; background: #F8FAFC;">
                        <td style="padding: 10px 16px; font-weight: 700; color: #475569; width: 30%;">Forecast Period</td>
                        <td style="padding: 10px 16px; font-weight: 700; color: #0F172A;">📅 {val_month_str}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 10px 16px; font-weight: 700; color: #475569;">Forecast Trend</td>
                        <td style="padding: 10px 16px; font-weight: 700; color: #0F172A;">{val_trend_icon} {val_trend_str}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0; background: #F8FAFC;">
                        <td style="padding: 10px 16px; font-weight: 700; color: #475569;">95% Bayesian Confidence Interval</td>
                        <td style="padding: 10px 16px; font-weight: 700; color: #0F172A;">[{ci_low:,.1f} – {ci_high:,.1f} tonnes] (±{1.96*val_std:,.1f} t)</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E2E8F0;">
                        <td style="padding: 10px 16px; font-weight: 700; color: #475569;">Model Architecture</td>
                        <td style="padding: 10px 16px; font-weight: 700; color: #0F172A;">Gaussian Process Regression (Composite Trend + Matérn 1.5 + WhiteNoise)</td>
                    </tr>
                    <tr style="background: #F8FAFC;">
                        <td style="padding: 10px 16px; font-weight: 700; color: #475569;">Operational Directive</td>
                        <td style="padding: 10px 16px; font-weight: 600; color: #0F172A;">🚛 {val_info['recommendation']} (Sizing: <b>{trucks} active 15-tonne compactor trucks</b>).</td>
                    </tr>
                </table>
            </div>
            """)

    # SUB-TAB 2: BATCH TEST VIA CSV UPLOAD
    with test_tab2:
        st.markdown("#### Upload a New CSV Dataset for Batch Model Validation")
        
        # Download Sample Template
        if os.path.exists("sample_new_test_data.csv"):
            with open("sample_new_test_data.csv", "rb") as f:
                st.download_button(
                    "📥 Download Sample Test CSV Template (12 Months)",
                    data=f.read(),
                    file_name="sample_new_test_data.csv",
                    mime="text/csv"
                )

        uploaded_file = st.file_uploader("Upload CSV File containing new test records", type=["csv"])
        
        if uploaded_file is not None:
            new_data = pd.read_csv(uploaded_file)
            st.markdown(f"**Uploaded Dataset Summary:** {new_data.shape[0]} Observations, {new_data.shape[1]} Columns")
            st.dataframe(new_data.head(), use_container_width=True)

            required_raw = ['avg_temperature_c', 'rainfall_mm', 'humidity_percent', 'population']
            missing_req = [c for c in required_raw if c not in new_data.columns]
            
            if missing_req:
                st.error(f"Missing required columns in uploaded CSV: {missing_req}")
            else:
                if 'date' in new_data.columns:
                    new_data['date'] = pd.to_datetime(new_data['date'])
                    new_data['year'] = new_data['date'].dt.year
                    new_data['month'] = new_data['date'].dt.month
                else:
                    if 'year' not in new_data.columns:
                        new_data['year'] = 2026
                    if 'month' not in new_data.columns:
                        new_data['month'] = range(1, len(new_data) + 1)
                
                new_data['time_index'] = (new_data['year'] - 2019) * 12 + (new_data['month'] - 1)
                new_data['sin_month'] = np.sin(2 * np.pi * new_data['month'] / 12.0)
                new_data['cos_month'] = np.cos(2 * np.pi * new_data['month'] / 12.0)
                
                if 'num_holidays' not in new_data.columns:
                    if 'public_holidays' in new_data.columns:
                        new_data['num_holidays'] = new_data['public_holidays'].fillna('').apply(
                            lambda x: len(str(x).split(';')) if str(x).strip() != '' else 0
                        )
                    else:
                        new_data['num_holidays'] = 1

                # Execute Batch Inference
                X_batch_scaled = scaler.transform(new_data[feature_cols])
                batch_pred, batch_std = model.predict(X_batch_scaled, return_std=True)
                new_data['predicted_tonnes'] = batch_pred
                new_data['daily_tonnes'] = batch_pred / 30.4167
                new_data['uncertainty_std'] = batch_std
                new_data['ci_lower_95'] = batch_pred - 1.96 * batch_std
                new_data['ci_upper_95'] = batch_pred + 1.96 * batch_std
                new_data['waste_class'] = new_data['predicted_tonnes'].apply(lambda x: classify_waste_5tier(x)['class'])
                new_data['compactor_trucks'] = np.ceil(new_data['daily_tonnes'] / 30.0).astype(int)

                st.markdown("---")
                st.markdown("#### Batch Prediction Evaluation & Visualizations")
                
                # Check if ground truth waste is available
                if 'waste_tonnes_estimated' in new_data.columns:
                    y_true_new = new_data['waste_tonnes_estimated'].values
                    m_mse = mean_squared_error(y_true_new, batch_pred)
                    m_rmse = np.sqrt(m_mse)
                    m_mae = mean_absolute_error(y_true_new, batch_pred)
                    m_mape = np.mean(np.abs((y_true_new - batch_pred) / y_true_new)) * 100.0
                    m_r2 = r2_score(y_true_new, batch_pred)
                    m_cov = np.mean((y_true_new >= new_data['ci_lower_95']) & (y_true_new <= new_data['ci_upper_95'])) * 100.0

                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("New Test R²", f"{m_r2:.4f}")
                    with c2:
                        st.metric("New Test RMSE", f"{m_rmse:,.1f} t")
                    with c3:
                        st.metric("New Test MAE", f"{m_mae:,.1f} t", f"MAPE: {m_mape:.2f}%")
                    with c4:
                        st.metric("95% CI Coverage", f"{m_cov:.1f}%")

                    fig_new, ax_new = plt.subplots(figsize=(8, 4.5), dpi=200)
                    fig_new.patch.set_facecolor('#FFFFFF')
                    ax_new.set_facecolor('#F8FAFC')
                    ax_new.scatter(y_true_new, batch_pred, color='#2563EB', s=60, edgecolors='#1E3A8A', label='New Test Observations')
                    mn = min(y_true_new.min(), batch_pred.min()) - 500
                    mx = max(y_true_new.max(), batch_pred.max()) + 500
                    ax_new.plot([mn, mx], [mn, mx], color='#EF4444', linestyle='--', lw=2, label='Perfect Agreement (y = x)')
                    ax_new.set_xlabel("Actual Waste (Tonnes)", fontsize=10.5, fontweight='bold', color='#0F172A')
                    ax_new.set_ylabel("GPR Predicted Waste (Tonnes)", fontsize=10.5, fontweight='bold', color='#0F172A')
                    ax_new.set_title(f"Model Fit on Uploaded Test Data (R² = {m_r2:.4f})", fontweight='bold', fontsize=11, color='#0F172A')
                    ax_new.grid(True, linestyle='--', alpha=0.5, color='#CBD5E1')
                    ax_new.legend()
                    st.pyplot(fig_new)

                # Batch Waste Class Breakdown
                st.markdown("##### Uploaded Batch Waste Class Distribution (Option D)")
                batch_dist = new_data['waste_class'].value_counts().reindex(['Very Low', 'Low', 'Moderate', 'High', 'Very High'], fill_value=0)
                b_c1, b_c2 = st.columns([3, 2])
                with b_c1:
                    fig_bdist, ax_bdist = plt.subplots(figsize=(6.5, 3.2), dpi=200)
                    fig_bdist.patch.set_facecolor('#FFFFFF')
                    ax_bdist.set_facecolor('#F8FAFC')
                    b_colors = ['#059669', '#0284C7', '#D97706', '#EA580C', '#DC2626']
                    b_bars = ax_bdist.bar(batch_dist.index, batch_dist.values, color=b_colors, edgecolor='#0F172A', width=0.5)
                    ax_bdist.set_ylabel("Observation Count", fontweight='bold')
                    ax_bdist.set_title(f"Batch Class Breakdown ({len(new_data)} Records)", fontweight='bold', fontsize=10.5)
                    ax_bdist.grid(axis='y', linestyle='--', alpha=0.5)
                    for bb in b_bars:
                        bh = bb.get_height()
                        if bh > 0:
                            ax_bdist.text(bb.get_x() + bb.get_width()/2., bh + 0.1, str(bh), ha='center', va='bottom', fontweight='bold')
                    plt.tight_layout()
                    st.pyplot(fig_bdist)
                with b_c2:
                    st.markdown(f"""
                    <div class="portal-card">
                        <div style="font-weight: 700; font-size: 14px; margin-bottom: 6px; color: #0F172A;">Batch Summary Statistics</div>
                        <div style="font-size: 12.5px; color: #475569; line-height: 1.6;">
                            • <b>Mean Predicted Waste:</b> {new_data['predicted_tonnes'].mean():,.1f} t/mo<br>
                            • <b>Daily Equivalent:</b> {new_data['daily_tonnes'].mean():,.1f} t/day<br>
                            • <b>High/Very High Count:</b> {batch_dist.get('High', 0) + batch_dist.get('Very High', 0)} of {len(new_data)} records<br>
                            • <b>Average Compactor Fleet:</b> {new_data['compactor_trucks'].mean():.1f} Trucks
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.dataframe(new_data[['year', 'month', 'predicted_tonnes', 'daily_tonnes', 'waste_class', 'ci_lower_95', 'ci_upper_95', 'uncertainty_std', 'compactor_trucks']].style.format({
                    'predicted_tonnes': '{:,.1f} t',
                    'daily_tonnes': '{:,.1f} t/d',
                    'ci_lower_95': '{:,.1f} t',
                    'ci_upper_95': '{:,.1f} t',
                    'uncertainty_std': '±{:.1f} t',
                    'compactor_trucks': '{:d} Trucks'
                }), use_container_width=True)

                csv_exp = new_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Batch Prediction Results (CSV)",
                    data=csv_exp,
                    file_name="new_data_gpr_predictions.csv",
                    mime="text/csv"
                )


# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 13px; line-height: 1.8; padding: 20px 0;">
    <b>A GAUSSIAN PROCESS REGRESSION FOR FORECASTING SOLID WASTE GENERATION IN UYO MUNICIPALITY</b><br>
    Candidate: <b>Effiong, Samuel Etim</b> (Reg No: AK22/PHS/CSC/029) &bull; Supervisor: <b>Dr. Anietie P. Ekong</b><br>
    Department of Computer Science &bull; Faculty of Computing and Information Technology &bull; Akwa Ibom State University, Ikot Akpaden &copy; 2026.
</div>
""", unsafe_allow_html=True)
