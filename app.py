# app.py
from pathlib import Path
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pages.risks import render_risks
from pages.analytics import render_analytics
from pages.meetings import render_meetings
from pages.deadlines import render_deadlines
from pages.employees import render_employees
from pages.chatbot import render_chatbot
from pages.reports import render_reports
from services.recommendation_engine import generate_ai_recommendations
from services.risk_engine import generate_risk_summary
# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="AI Co-Lead",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ---------------- LOGO CONFIG ----------------
BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "co_lead_logo.png"

st.markdown("""
<style>
[data-testid="stSidebarNav"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    
    df = pd.read_csv("AI_CoLead_5000_Dataset.csv")

    # Generate dates if missing
    if "Task_Date" not in df.columns:
        today = datetime.today()

        df["Task_Date"] = [
            today - timedelta(days=np.random.randint(0, 30))
            for _ in range(len(df))
        ]

        df["Deadline"] = (
            df["Task_Date"]
            + pd.to_timedelta(
                np.random.randint(1, 15, size=len(df)),
                unit="D"
            )
        )

    return df


df = load_data()

risk_data = generate_risk_summary(df)
# Store globally
st.session_state["df"] = df

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #020617,
        #0f172a
    );
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    color: white;
}

.hero {
    padding: 20px;
    border-radius: 15px;
    background: linear-gradient(
        90deg,
        #1e3a8a,
        #0f172a
    );
    margin-bottom: 20px;
}

.hero-text {
    color: white;
    margin: 0;
}

.hero h2 {
    font-size: 42px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 18px;
    opacity: 0.9;
}

            section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Sidebar Buttons */

section[data-testid="stSidebar"] button {
    width: 100% !important;
    height: 50px !important;

    border-radius: 12px !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    background: rgba(255,255,255,0.03) !important;

    color: white !important;

    text-align: left !important;

    font-size: 15px !important;

    font-weight: 500 !important;

    margin-bottom: 8px !important;

    transition: all 0.3s ease !important;
}

section[data-testid="stSidebar"] button:hover {
    background: rgba(37,99,235,0.25) !important;

    border: 1px solid #3b82f6 !important;

    transform: translateX(4px);
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

col_logo, col_title = st.columns([1, 10])

with col_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=100)
    else:
        st.markdown("## 🚀")

with col_title:
    st.markdown(
        """
        <div class="main-title">
            AI Co-Lead: Intelligent Team Lead Assistant
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("""
<div class='hero'>
    <h2 class='hero-text'>
        Smart insights for modern team leaders
    </h2>
    <p class='hero-text'>
            Monitor risks • Optimize workload • Improve performance
    </p>
</div>
""", unsafe_allow_html=True)



# ==========================================
# SIDEBAR - AI CO-LEAD BRANDING & NAVIGATION
# ==========================================

with st.sidebar:

    # BRAND LOGO
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=180)

    # BRAND CARD
    with st.container(border=True):

        st.markdown(
            "<h3 style='text-align:center;'>AI Co-Lead</h3>",
            unsafe_allow_html=True
        )

        st.caption("Intelligent Team Lead Assistant")

        st.divider()

        st.metric(
            "💚 Team Health",
            f"{risk_data['team_health']:.2f}%"
        )

        st.metric(
            "⚠️ Organization Risk",
            f"{risk_data['organization_risk']:.2f}%"
        )

    # TEAM STATUS
    if risk_data["team_health"] > 80:
        st.success("🟢 Team Performing Well")

    elif risk_data["team_health"] > 60:
        st.warning("🟡 Monitor Team Closely")

    else:
        st.error("🔴 Immediate Attention Needed")

    st.divider()

    # NAVIGATION
    st.markdown("### 📍 Navigation")

    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"

    st.info(f"Current Page: {st.session_state.page}")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "🏠 Home"

    if st.button("📊 Work Analytics", use_container_width=True):
        st.session_state.page = "📊 Work Analytics"

    if st.button("⚠️ Risk Center", use_container_width=True):
        st.session_state.page = "⚠️ Risk Center"

    if st.button("📞 Meetings", use_container_width=True):
        st.session_state.page = "📞 Meetings"

    if st.button("📅 Deadlines", use_container_width=True):
        st.session_state.page = "📅 Deadlines"

    if st.button("👥 Team Insights", use_container_width=True):
        st.session_state.page = "👥 Team Insights"

    if st.button("🤖 AI Assistant", use_container_width=True):
        st.session_state.page = "🤖 AI Assistant"

    if st.button("📄 Reports", use_container_width=True):
        st.session_state.page = "📄 Reports"

page = st.session_state.page

# ---------------- ROUTING ----------------

from pages.home import render_home

if page == "🏠 Home":
    render_home(df)

elif page == "📊 Work Analytics":
    render_analytics(df)

elif page == "⚠️ Risk Center":
    render_risks(df)

elif page == "📞 Meetings":
    render_meetings(df)

elif page == "📅 Deadlines":
    render_deadlines(df)

elif page == "👥 Team Insights":
    render_employees(df)

elif page == "🤖 AI Assistant":
    render_chatbot(df)

elif page == "📄 Reports":
    render_reports(df)