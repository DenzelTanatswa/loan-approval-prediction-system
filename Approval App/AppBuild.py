import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

st.set_page_config(page_title="Loan Approval System", page_icon="🏦", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f5f7fa; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2942 0%, #1a4a7a 100%);
        padding-top: 1rem;
    }
    [data-testid="stSidebar"] * { color: #000000 !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stSlider label {
        color: #a8c8f0 !important; font-size: 0.82rem; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.05em;
    }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }

    .navbar {
        background: linear-gradient(135deg, #0f2942 0%, #1a4a7a 60%, #2563a8 100%);
        padding: 1.8rem 2.5rem; border-radius: 16px; margin-bottom: 1.8rem;
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 4px 20px rgba(15,41,66,0.25);
    }
    .navbar-left h1 { color: white; font-size: 1.9rem; font-weight: 700; margin: 0; }
    .navbar-left p  { color: #a8c8f0; font-size: 0.92rem; margin: 0.3rem 0 0; }
    .navbar-badge {
        background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3);
        color: white !important; padding: 0.4rem 1rem; border-radius: 20px;
        font-size: 0.82rem; font-weight: 600;
    }

    .card {
        background: white; border-radius: 14px; padding: 1.5rem 1.8rem;
        margin-bottom: 1.4rem; box-shadow: 0 2px 14px rgba(0,0,0,0.06);
        border: 1px solid #e8edf5;
    }
    .card-title {
        font-size: 0.78rem; font-weight: 700; color: #1a4a7a;
        text-transform: uppercase; letter-spacing: 0.08em;
        margin-bottom: 1.1rem; padding-bottom: 0.6rem; border-bottom: 2px solid #e8f0fe;
    }

    .tile { background: linear-gradient(135deg, #f0f6ff, #e8f0fe); border-radius: 12px;
        padding: 1rem 1.2rem; text-align: center; border: 1px solid #d0e4ff; }
    .tile .val { font-size: 1.35rem; font-weight: 700; color: #0f2942; }
    .tile .lbl { font-size: 0.72rem; color: #5a7a9a; margin-top: 0.25rem; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.04em; }

    .stat-card { border-radius: 14px; padding: 1.3rem 1.5rem; text-align: center; border: 1px solid #e0e8f5; }
    .stat-card.green { background: linear-gradient(135deg, #e8f8f0, #c8eedd); border-color: #a8ddc0; }
    .stat-card.red   { background: linear-gradient(135deg, #fde8e8, #f9c0c0); border-color: #f0a0a0; }
    .stat-card.blue  { background: linear-gradient(135deg, #e8f0fe, #d0e4ff); border-color: #a8c8f0; }
    .stat-card.gold  { background: linear-gradient(135deg, #fef9e7, #fdebd0); border-color: #f0d080; }
    .stat-val { font-size: 1.6rem; font-weight: 700; color: #0f2942; }
    .stat-lbl { font-size: 0.75rem; color: #5a7a9a; margin-top: 0.3rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.05em; }

    .risk-badge { display: inline-block; padding: 0.35rem 1rem; border-radius: 20px; font-size: 0.82rem; font-weight: 700; margin-left: 0.6rem; }
    .risk-poor  { background: #fde8e8; color: #c0392b; }
    .risk-fair  { background: #fef3e2; color: #d68910; }
    .risk-good  { background: #e8f8f0; color: #1e8449; }
    .risk-excel { background: #e8f0fe; color: #1a4a7a; }

    .result-approved { background: linear-gradient(135deg, #e8f8f0, #c8eedd); border-left: 6px solid #1e8449; border-radius: 14px; padding: 1.8rem 2rem; }
    .result-rejected { background: linear-gradient(135deg, #fde8e8, #f9c0c0); border-left: 6px solid #c0392b; border-radius: 14px; padding: 1.8rem 2rem; }
    .result-title { font-size: 1.7rem; font-weight: 700; margin: 0; }
    .result-sub   { font-size: 0.95rem; margin-top: 0.4rem; opacity: 0.75; }

    div.stButton > button {
        background: linear-gradient(135deg, #0f2942, #2563a8); color: white !important;
        border: none; border-radius: 10px; padding: 0.8rem 2rem; font-size: 1rem;
        font-weight: 600; width: 100%; letter-spacing: 0.03em; transition: all 0.2s;
        box-shadow: 0 4px 14px rgba(15,41,66,0.3);
    }
    div.stButton > button:hover { opacity: 0.88; transform: translateY(-1px); }

    .stTabs [data-baseweb="tab-list"] { gap: 0.5rem; background: transparent; }
    .stTabs [data-baseweb="tab"] {
        background: white; border-radius: 8px 8px 0 0; padding: 0.6rem 1.4rem;
        font-weight: 600; color: #5a7a9a; border: 1px solid #e0e8f5; border-bottom: none;
    }
    .stTabs [aria-selected="true"] { background: #0f2942 !important; color: white !important; }

    .sidebar-section { color: #a8c8f0 !important; font-size: 0.78rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.08em; margin: 1rem 0 0.4rem; }

    /* Download button */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #1e8449, #27ae60) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
        padding: 0.7rem 1.8rem !important; font-weight: 600 !important; width: 100% !important;
        box-shadow: 0 4px 14px rgba(30,132,73,0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

model   = joblib.load("../Models/loan_approval_model.pkl")
encoder = joblib.load("../Models/label_encoder.pkl")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 Loan Advisor")
    st.markdown("---")
    st.markdown('<div class="sidebar-section">👤 Applicant Info</div>', unsafe_allow_html=True)
    dependents    = st.number_input("Dependents", min_value=0, max_value=10, value=0)
    education     = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Employment", ["No", "Yes"],
                                 format_func=lambda x: "Self-Employed" if x == "Yes" else "Salaried")
    st.markdown('<div class="sidebar-section">💳 Credit Profile</div>', unsafe_allow_html=True)
    cibil_score = st.slider("CIBIL Score", 300, 900, 700)
    st.markdown('<div class="sidebar-section">💰 Loan Details</div>', unsafe_allow_html=True)
    income      = st.number_input("Annual Income (€)", min_value=0, value=5000000, step=100000)
    loan_amount = st.number_input("Loan Amount (€)",   min_value=0, value=10000000, step=100000)
    loan_term   = st.number_input("Loan Term (Years)", min_value=1, max_value=30, value=15)
    st.markdown("---")
    st.markdown('<p style="font-size:0.75rem;opacity:0.5;text-align:center">Powered by Random Forest ML</p>', unsafe_allow_html=True)

# ── Navbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="navbar-left">
        <h1>🏦 Loan Approval Prediction System</h1>
        <p>AI-powered credit risk assessment using Random Forest classification</p>
    </div>
    <div class="navbar-badge">ML Model v1.0</div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📋  Application Form", "📊  Dashboard & Results"])

# ── Tab 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="card"><div class="card-title">📊 Asset Portfolio</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1: residential_asset = st.number_input("Residential (€)", min_value=0, value=5000000, step=100000)
    with c2: commercial_asset  = st.number_input("Commercial (€)",  min_value=0, value=3000000, step=100000)
    with c3: luxury_asset      = st.number_input("Luxury (€)",      min_value=0, value=2000000, step=100000)
    with c4: bank_asset        = st.number_input("Bank Assets (€)", min_value=0, value=4000000, step=100000)
    st.markdown('</div>', unsafe_allow_html=True)

    total_assets = residential_asset + commercial_asset + luxury_asset + bank_asset
    debt_ratio   = round((loan_amount / income) * 100, 1) if income > 0 else 0
    net_worth    = total_assets - loan_amount

    if cibil_score >= 750:   risk_class, risk_label = "risk-excel", "Excellent"
    elif cibil_score >= 700: risk_class, risk_label = "risk-good",  "Good"
    elif cibil_score >= 650: risk_class, risk_label = "risk-fair",  "Fair"
    else:                    risk_class, risk_label = "risk-poor",  "Poor"

    st.markdown('<div class="card"><div class="card-title">📈 Financial Snapshot</div>', unsafe_allow_html=True)
    t1, t2, t3, t4, t5 = st.columns(5)
    with t1: st.markdown(f'<div class="tile"><div class="val">€{total_assets/1e6:.1f}M</div><div class="lbl">Total Assets</div></div>', unsafe_allow_html=True)
    with t2: st.markdown(f'<div class="tile"><div class="val">{debt_ratio}%</div><div class="lbl">Debt-to-Income</div></div>', unsafe_allow_html=True)
    with t3: st.markdown(f'<div class="tile"><div class="val">€{net_worth/1e6:.1f}M</div><div class="lbl">Net Worth</div></div>', unsafe_allow_html=True)
    with t4: st.markdown(f'<div class="tile"><div class="val">{loan_term} yrs</div><div class="lbl">Loan Term</div></div>', unsafe_allow_html=True)
    with t5: st.markdown(f'<div class="tile"><div class="val">{cibil_score} <span class="risk-badge {risk_class}">{risk_label}</span></div><div class="lbl">CIBIL Score</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    predict = st.button("🔍 Run Credit Assessment")

# ── Tab 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    if "prob_approve" not in st.session_state:
        st.markdown("""
        <div style="text-align:center; padding: 4rem 2rem; background: white; border-radius: 16px; border: 2px dashed #d0e4ff;">
            <div style="font-size:3rem;">📊</div>
            <div style="font-size:1.2rem; font-weight:700; color:#1a4a7a; margin-top:1rem;">No Assessment Run Yet</div>
            <div style="color:#5a7a9a; margin-top:0.5rem;">Go to the Application Form tab, fill in the details and click <strong>Run Credit Assessment</strong>.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        pred         = st.session_state.prediction
        confidence   = st.session_state.confidence
        prob_approve = st.session_state.prob_approve
        prob_reject  = st.session_state.prob_reject
        input_df     = st.session_state.input_df
        timestamp    = st.session_state.timestamp

        # Result banner
        if pred == 1:
            st.markdown(f"""
            <div class="result-approved">
                <div class="result-title">✅ Loan Approved</div>
                <div class="result-sub">Applicant meets all credit criteria &nbsp;·&nbsp; Assessed: <strong>{timestamp}</strong></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-rejected">
                <div class="result-title">❌ Loan Rejected</div>
                <div class="result-sub">Applicant does not meet credit criteria &nbsp;·&nbsp; Assessed: <strong>{timestamp}</strong></div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Summary cards ─────────────────────────────────────────────────────
        st.markdown('<div class="card"><div class="card-title">📌 Prediction Summary</div>', unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        color = "green" if pred == 1 else "red"
        with s1: st.markdown(f'<div class="stat-card {color}"><div class="stat-val">{"✅ Approved" if pred == 1 else "❌ Rejected"}</div><div class="stat-lbl">Decision</div></div>', unsafe_allow_html=True)
        with s2: st.markdown(f'<div class="stat-card blue"><div class="stat-val">{confidence:.1f}%</div><div class="stat-lbl">Model Confidence</div></div>', unsafe_allow_html=True)
        with s3: st.markdown(f'<div class="stat-card gold"><div class="stat-val">{int(input_df["cibil_score"].values[0])}</div><div class="stat-lbl">CIBIL Score</div></div>', unsafe_allow_html=True)
        with s4: st.markdown(f'<div class="stat-card blue"><div class="stat-val">€{int(input_df["loan_amount"].values[0])/1e6:.1f}M</div><div class="stat-lbl">Loan Amount</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Charts row ────────────────────────────────────────────────────────
        ch1, ch2 = st.columns([1, 1])

        with ch1:
            st.markdown('<div class="card"><div class="card-title">📊 Approval Probability</div>', unsafe_allow_html=True)
            fig_bar = go.Figure(go.Bar(
                x=["Rejected", "Approved"],
                y=[round(prob_reject * 100, 2), round(prob_approve * 100, 2)],
                marker_color=["#e74c3c", "#1e8449"],
                text=[f"{prob_reject*100:.1f}%", f"{prob_approve*100:.1f}%"],
                textposition="outside",
                width=0.45
            ))
            fig_bar.update_layout(
                yaxis=dict(range=[0, 115], title="Probability (%)", gridcolor="#f0f4f8", showgrid=True),
                xaxis=dict(title=""),
                plot_bgcolor="white", paper_bgcolor="white",
                margin=dict(t=10, b=10, l=10, r=10), height=280,
                font=dict(family="Inter", size=13)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with ch2:
            st.markdown('<div class="card"><div class="card-title">🎯 Confidence Gauge</div>', unsafe_allow_html=True)
            gauge_color = "#1e8449" if pred == 1 else "#c0392b"
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=round(confidence, 1),
                number={"suffix": "%", "font": {"size": 28, "family": "Inter"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#aaa"},
                    "bar":  {"color": gauge_color},
                    "bgcolor": "white",
                    "steps": [
                        {"range": [0,  50], "color": "#fde8e8"},
                        {"range": [50, 75], "color": "#fef3e2"},
                        {"range": [75, 100],"color": "#e8f8f0"},
                    ],
                    "threshold": {"line": {"color": gauge_color, "width": 4}, "thickness": 0.75, "value": confidence}
                }
            ))
            fig_gauge.update_layout(
                paper_bgcolor="white", margin=dict(t=20, b=10, l=30, r=30), height=280,
                font=dict(family="Inter")
            )
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Asset breakdown pie + Input summary ───────────────────────────────
        ch3, ch4 = st.columns([1, 1])

        with ch3:
            st.markdown('<div class="card"><div class="card-title">🏠 Asset Breakdown</div>', unsafe_allow_html=True)
            asset_vals = [
                int(input_df["residential_assets_value"].values[0]),
                int(input_df["commercial_assets_value"].values[0]),
                int(input_df["luxury_assets_value"].values[0]),
                int(input_df["bank_asset_value"].values[0]),
            ]
            fig_pie = px.pie(
                names=["Residential", "Commercial", "Luxury", "Bank"],
                values=asset_vals,
                color_discrete_sequence=["#2563a8", "#1e8449", "#d68910", "#c0392b"],
                hole=0.45
            )
            fig_pie.update_layout(
                paper_bgcolor="white", margin=dict(t=10, b=10, l=10, r=10), height=280,
                font=dict(family="Inter", size=13),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with ch4:
            st.markdown('<div class="card"><div class="card-title">📋 Input Summary</div>', unsafe_allow_html=True)
            display_df = input_df.T.rename(columns={0: "Value"})
            display_df.index = [
                "Dependents", "Education", "Self Employed", "Annual Income (€)",
                "Loan Amount (€)", "Loan Term (yrs)", "CIBIL Score",
                "Residential Asset (€)", "Commercial Asset (€)", "Luxury Asset (€)", "Bank Asset (€)"
            ]
            st.dataframe(display_df, use_container_width=True, height=280)
            st.markdown('</div>', unsafe_allow_html=True)

        # ── Export ────────────────────────────────────────────────────────────
        st.markdown('<div class="card"><div class="card-title">⬇️ Export Prediction Report</div>', unsafe_allow_html=True)

        export_df = display_df.copy()
        export_df.loc["─── Result ───"]    = "─────────"
        export_df.loc["Decision"]          = "Approved" if pred == 1 else "Rejected"
        export_df.loc["Model Confidence"]  = f"{confidence:.2f}%"
        export_df.loc["Approve Prob (%)"]  = f"{prob_approve * 100:.2f}%"
        export_df.loc["Reject Prob (%)"]   = f"{prob_reject  * 100:.2f}%"
        export_df.loc["Assessment Time"]   = timestamp

        buf = io.StringIO()
        export_df.to_csv(buf)

        dl1, dl2, dl3 = st.columns([1, 1, 1])
        with dl2:
            st.download_button(
                label="📥 Download Report as CSV",
                data=buf.getvalue(),
                file_name=f"loan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        st.markdown('</div>', unsafe_allow_html=True)

# ── Prediction logic ──────────────────────────────────────────────────────────
if predict:
    education_enc     = 0 if education == "Graduate" else 1
    self_employed_enc = 1 if self_employed == "Yes" else 0

    input_data = pd.DataFrame({
        "no_of_dependents":         [dependents],
        "education":                [education_enc],
        "self_employed":            [self_employed_enc],
        "income_annum":             [income],
        "loan_amount":              [loan_amount],
        "loan_term":                [loan_term],
        "cibil_score":              [cibil_score],
        "residential_assets_value": [residential_asset],
        "commercial_assets_value":  [commercial_asset],
        "luxury_assets_value":      [luxury_asset],
        "bank_asset_value":         [bank_asset]
    })

    prediction  = model.predict(input_data)
    probability = model.predict_proba(input_data)

    st.session_state.prediction_done = True
    st.session_state.prediction      = int(prediction[0])
    st.session_state.confidence      = float(max(probability[0])) * 100
    st.session_state.prob_approve    = float(probability[0][1])
    st.session_state.prob_reject     = float(probability[0][0])
    st.session_state.input_df        = input_data
    st.session_state.timestamp       = datetime.now().strftime("%d %b %Y, %H:%M:%S")

    st.rerun()
