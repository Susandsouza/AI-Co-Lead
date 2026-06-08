# pages/home.py

import streamlit as st
import pandas as pd
import plotly.express as px

from services.recommendation_engine import generate_ai_recommendations

from services.risk_engine import generate_risk_summary

def render_home(df):

    risk_data = generate_risk_summary(df)
    ai_data = generate_ai_recommendations(df)

    st.header("🏠 AI Co-Lead Command Center")

    total_employees = len(df)
    total_tasks = int(df["Tasks_Assigned"].sum())
    completed_tasks = int(df["Tasks_Completed"].sum())
    overdue_tasks = int(df["Overdue_Tasks"].sum())

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("👥 Employees", total_employees)
    col2.metric("📌 Tasks Assigned", total_tasks)
    col3.metric("✅ Tasks Completed", completed_tasks)
    col4.metric("⏰ Overdue Tasks", overdue_tasks)

    st.divider()

    st.subheader("🧠 AI Health Overview")

    c1, c2 = st.columns(2)

    c1.metric(
        "Team Health Index",
        f"{risk_data['team_health']}%"
    )

    c2.metric(
        "Organization Risk",
        f"{risk_data['organization_risk']}%"
    )
    # ==================================================
    # KPI CARDS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Employees",
        total_employees
    )

    col2.metric(
        "📌 Tasks Assigned",
        total_tasks
    )

    col3.metric(
        "✅ Tasks Completed",
        completed_tasks
    )

    col4.metric(
        "⏰ Overdue Tasks",
        overdue_tasks
    )

    st.divider()
    st.subheader("🧠 AI Health Overview")

    col1, col2 = st.columns(2)

    col1.metric(
        "💚 Team Health",
        f"{risk_data['team_health']}%"
    )

    col2.metric(
        "⚠️ Organization Risk",
        f"{risk_data['organization_risk']}%"
    )
    # ==================================================
    # TEAM HEALTH SCORE
    # ==================================================

    health_score = max(
        0,
        100
        - (burnout_count * 0.5)
        - (sprint_risk_count * 0.5)
        - (engagement_risk_count * 0.5)
    )

    st.subheader("💚 Team Health Score")

    st.progress(int(health_score))

    st.write(
        f"Overall Team Health: **{health_score:.1f}%**"
    )

    # ==================================================
    # TEAM MOOD
    # ==================================================

    st.subheader("😊 Team Mood Indicator")

    avg_engagement = df[
        "Engagement_Score"
    ].mean()

    if avg_engagement >= 80:
        st.success(
            "😊 Team Sentiment: Positive"
        )

    elif avg_engagement >= 60:
        st.warning(
            "😐 Team Sentiment: Neutral"
        )

    else:
        st.error(
            "😟 Team Sentiment: At Risk"
        )

    # ==================================================
    # AI RECOMMENDATIONS
    # ==================================================

    st.subheader("🤖 AI Priorities")

    for priority in ai_data["priorities"]:
        st.warning(priority)

    # ==================================================
    # CRITICAL ALERTS
    # ==================================================

    st.subheader("🚨 Critical Alerts")

    alert_col1, alert_col2, alert_col3 = st.columns(3)

    alert_col1.metric(
        "Burnout Risks",
        burnout_count
    )

    alert_col2.metric(
        "Sprint Risks",
        sprint_risk_count
    )

    alert_col3.metric(
        "Engagement Risks",
        engagement_risk_count
    )

    # ==================================================
    # WORKLOAD OVERVIEW
    # ==================================================

    st.subheader("📊 Department Workload")

    workload = (
        df.groupby("Department")
        [
            [
                "Tasks_Assigned",
                "Tasks_Completed"
            ]
        ]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        workload,
        x="Department",
        y=[
            "Tasks_Assigned",
            "Tasks_Completed"
        ],
        barmode="group",
        title="Department Workload"
    )

    fig.update_layout(
        xaxis_title="Department",
        yaxis_title="Tasks"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # RISK HEATMAP
    # ==================================================

    st.subheader(
        "🔥 Department Risk Heatmap"
    )

    risk_df = (
        df.groupby("Department")
        [
            [
                "Burnout_Risk",
                "Sprint_Risk",
                "Disengagement_Risk"
            ]
        ]
        .sum()
        .reset_index()
    )

    heatmap = px.imshow(
        risk_df.set_index("Department"),
        text_auto=True,
        aspect="auto",
        title="Department Risk Heatmap"
    )

    st.plotly_chart(
        heatmap,
        use_container_width=True
    )

    # ==================================================
    # HIGH RISK EMPLOYEES
    # ==================================================

    st.subheader(
        "⚠️ Employees Requiring Attention"
    )

    high_risk = df[
        (df["Burnout_Risk"] == 1)
        |
        (df["Sprint_Risk"] == 1)
        |
        (df["Disengagement_Risk"] == 1)
    ]

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Tasks_Assigned",
            "Stress_Level",
            "Engagement_Score"
        ]
        if c in high_risk.columns
    ]

    st.dataframe(
        high_risk[cols].head(20),
        use_container_width=True
    )

    # ==================================================
    # QUICK ACTIONS
    # ==================================================

    st.subheader("⚡ Quick Actions")

    c1, c2, c3 = st.columns(3)

    c1.button("📄 Generate Report")

    c2.button("📅 Review Deadlines")

    c3.button("🤖 Open AI Assistant")

