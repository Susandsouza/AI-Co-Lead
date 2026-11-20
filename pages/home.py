
# pages/home.py

import streamlit as st
import pandas as pd
import plotly.express as px

from services.recommendation_engine import generate_ai_recommendations
from services.risk_engine import generate_risk_summary


def render_home(df):

    # ==========================================
    # DATA PROCESSING
    # ==========================================

    risk_data = generate_risk_summary(df)
    ai_data = generate_ai_recommendations(df)

    st.header("🏠 AI Co-Lead Command Center")

    # Safely retrieve numeric columns
    def get_numeric(column):
        if column in df.columns:
            return pd.to_numeric(
                df[column], errors="coerce"
            ).fillna(0)
        return pd.Series(0, index=df.index, dtype=float)

    total_employees = len(df)
    total_tasks = int(get_numeric("Tasks_Assigned").sum())
    completed_tasks = int(get_numeric("Tasks_Completed").sum())
    overdue_tasks = int(get_numeric("Overdue_Tasks").sum())

    # ==========================================
    # MAIN KPI CARDS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Employees", f"{total_employees:,}")
    col2.metric("📌 Tasks Assigned", f"{total_tasks:,}")
    col3.metric("✅ Tasks Completed", f"{completed_tasks:,}")
    col4.metric("⏰ Overdue Tasks", f"{overdue_tasks:,}")

    st.divider()

    # ==========================================
    # AI HEALTH OVERVIEW
    # ==========================================

    st.subheader("🧠 AI Health Overview")

    col1, col2 = st.columns(2)

    team_health = float(risk_data["team_health"])
    organization_risk = float(risk_data["organization_risk"])

    col1.metric("💚 Team Health Index", f"{team_health:.2f}%")
    col2.metric("⚠️ Organization Risk", f"{organization_risk:.2f}%")

    # ==========================================
    # TEAM HEALTH SCORE
    # ==========================================

    st.subheader("💚 Team Health Score")

    health_score = max(0, min(100, team_health))

    st.progress(int(health_score))

    st.write(
        f"Overall Team Health: **{health_score:.1f}%**"
    )

    # ==========================================
    # RISK COUNTS
    # ==========================================

    burnout_count = int(get_numeric("Burnout_Risk").sum())
    sprint_risk_count = int(get_numeric("Sprint_Risk").sum())
    engagement_risk_count = int(
        get_numeric("Disengagement_Risk").sum()
    )

    # ==========================================
    # TEAM MOOD
    # ==========================================

    st.subheader("😊 Team Mood Indicator")

    if "Engagement_Score" in df.columns:

        avg_engagement = get_numeric("Engagement_Score").mean()

        if avg_engagement >= 80:
            st.success("😊 Team Sentiment: Positive")

        elif avg_engagement >= 60:
            st.warning("😐 Team Sentiment: Neutral")

        else:
            st.error("😟 Team Sentiment: At Risk")

        st.caption(f"Average Engagement Score: {avg_engagement:.1f}")

    else:
        st.info("Engagement data is unavailable.")

    # ==========================================
    # AI RECOMMENDATIONS
    # ==========================================

    st.subheader("🤖 AI Priorities")

    for priority in ai_data.get("priorities", []):
        st.warning(priority)

    # ==========================================
    # CRITICAL ALERTS
    # ==========================================

    st.subheader("🚨 Critical Alerts")

    alert_col1, alert_col2, alert_col3 = st.columns(3)

    alert_col1.metric("🔥 Burnout Risks", f"{burnout_count:,}")
    alert_col2.metric("⚠️ Sprint Risks", f"{sprint_risk_count:,}")
    alert_col3.metric("👥 Disengagement Risks", f"{engagement_risk_count:,}")

    # ==========================================
    # DEPARTMENT WORKLOAD
    # ==========================================

    st.subheader("📊 Department Workload")

    if "Department" in df.columns:

        workload = df.groupby("Department").agg(
            Tasks_Assigned=("Tasks_Assigned", "sum"),
            Tasks_Completed=("Tasks_Completed", "sum")
        ).reset_index()

        fig = px.bar(
            workload,
            x="Department",
            y=["Tasks_Assigned", "Tasks_Completed"],
            barmode="group",
            title="Department Workload"
        )

        fig.update_layout(
            xaxis_title="Department",
            yaxis_title="Tasks",
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ==========================================
    # DEPARTMENT RISK HEATMAP
    # ==========================================

    st.subheader("🔥 Department Risk Heatmap")

    risk_columns = [
        "Burnout_Risk",
        "Sprint_Risk",
        "Disengagement_Risk"
    ]

    available_risk_columns = [
        col for col in risk_columns if col in df.columns
    ]

    if "Department" in df.columns and available_risk_columns:

        risk_df = df.groupby("Department")[
            available_risk_columns
        ].sum()

        heatmap = px.imshow(
            risk_df,
            text_auto=True,
            aspect="auto",
            title="Department Risk Heatmap",
            color_continuous_scale="Reds"
        )

        st.plotly_chart(heatmap, use_container_width=True)

    else:
        st.info("Department risk data is unavailable.")

    # ==========================================
    # HIGH-RISK EMPLOYEES
    # ==========================================

    st.subheader("⚠️ Employees Requiring Attention")

    available_risk_columns = [
        col for col in risk_columns if col in df.columns
    ]

    if available_risk_columns:

        high_risk_mask = pd.Series(False, index=df.index)

        for col in available_risk_columns:
            high_risk_mask |= get_numeric(col) == 1

        high_risk = df[high_risk_mask]

        display_columns = [
            col for col in [
                "Employee_ID",
                "Department",
                "Tasks_Assigned",
                "Stress_Level",
                "Engagement_Score"
            ]
            if col in high_risk.columns
        ]

        if not high_risk.empty:
            st.dataframe(
                high_risk[display_columns].head(20),
                use_container_width=True
            )
        else:
            st.success("No high-risk employees identified.")

    # ==========================================
    # QUICK ACTIONS
    # ==========================================

    st.subheader("⚡ Quick Actions")

    c1, c2, c3 = st.columns(3)

    c1.button("📄 Generate Report", key="home_report")
    c2.button("📅 Review Deadlines", key="home_deadlines")
    c3.button("🤖 Open AI Assistant", key="home_assistant")