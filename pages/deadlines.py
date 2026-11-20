# pages/deadlines.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta


def render_deadlines(df):

    st.header("📅 Deadline Intelligence Center")

    st.markdown("""
    Monitor approaching deadlines, overdue work,
    critical delivery risks, and AI-generated action plans.
    """)

    # ==================================================
    # DATE VALIDATION
    # ==================================================

    if "Deadline" not in df.columns:

        st.warning(
            "Deadline column not found in dataset."
        )

        return

    today = pd.Timestamp.today().normalize()

    df["Deadline"] = pd.to_datetime(
        df["Deadline"]
    )

    # ==================================================
    # DEADLINE STATUS
    # ==================================================

    df["Days_Left"] = (
        df["Deadline"] - today
    ).dt.days

    overdue = df[
        df["Days_Left"] < 0
    ]

    critical = df[
        (df["Days_Left"] >= 0)
        &
        (df["Days_Left"] <= 2)
    ]

    warning = df[
        (df["Days_Left"] >= 3)
        &
        (df["Days_Left"] <= 7)
    ]

    healthy = df[
        df["Days_Left"] > 7
    ]

    # ==================================================
    # KPI CARDS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🚨 Overdue",
        len(overdue)
    )

    col2.metric(
        "🔥 Critical (0-2 Days)",
        len(critical)
    )

    col3.metric(
        "⚠️ Warning (3-7 Days)",
        len(warning)
    )

    col4.metric(
        "✅ Healthy",
        len(healthy)
    )

    st.divider()

    # ==================================================
    # DEADLINE DISTRIBUTION
    # ==================================================

    st.subheader("📊 Deadline Distribution")

    distribution = pd.DataFrame({
        "Status": [
            "Overdue",
            "Critical",
            "Warning",
            "Healthy"
        ],
        "Count": [
            len(overdue),
            len(critical),
            len(warning),
            len(healthy)
        ]
    })

    fig = px.bar(
        distribution,
        x="Status",
        y="Count",
        color="Status",
        title="Deadline Status Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # OVERDUE TASKS
    # ==================================================

    st.subheader("🚨 Overdue Tasks")

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Tasks_Assigned",
            "Deadline",
            "Days_Left"
        ]
        if c in overdue.columns
    ]

    st.dataframe(
        overdue[cols]
        .sort_values("Days_Left")
        .head(25),
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # CRITICAL TASKS
    # ==================================================

    st.subheader("🔥 Tasks Near Deadline")

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Tasks_Assigned",
            "Deadline",
            "Days_Left"
        ]
        if c in critical.columns
    ]

    st.dataframe(
        critical[cols]
        .sort_values("Days_Left")
        .head(25),
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # DEPARTMENT DEADLINE RISK
    # ==================================================

    st.subheader("🏢 Department Deadline Risk")

    dept_risk = (
        df.groupby("Department")
        ["Overdue_Tasks"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        dept_risk,
        x="Department",
        y="Overdue_Tasks",
        color="Overdue_Tasks",
        title="Department Overdue Tasks"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # DEADLINE HEATMAP
    # ==================================================

    st.subheader("🔥 Department Deadline Heatmap")

    heatmap_df = (
        df.groupby("Department")
        [
            [
                "Tasks_Assigned",
                "Tasks_Completed",
                "Overdue_Tasks"
            ]
        ]
        .sum()
        .reset_index()
    )

    heatmap = px.imshow(
        heatmap_df.set_index("Department"),
        text_auto=True,
        aspect="auto",
        title="Department Deadline Heatmap"
    )

    st.plotly_chart(
        heatmap,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # HIGH RISK EMPLOYEES
    # ==================================================

    st.subheader("⚠️ Employees Requiring Attention")

    high_risk = df[
        (df["Overdue_Tasks"] > 0)
        |
        (df["Sprint_Risk"] == 1)
    ]

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Overdue_Tasks",
            "Tasks_Assigned",
            "Completion_Rate"
        ]
        if c in high_risk.columns
    ]

    st.dataframe(
        high_risk[cols]
        .head(25),
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # AI RECOMMENDATIONS
    # ==================================================

    st.subheader("🤖 AI Recommendations")

    recommendations = []

    if len(overdue) > 25:
        recommendations.append(
            "Prioritize overdue tasks immediately."
        )

    if len(critical) > 50:
        recommendations.append(
            "Review upcoming deadlines this week."
        )

    if df["Overdue_Tasks"].sum() > 100:
        recommendations.append(
            "Consider workload redistribution."
        )

    if not recommendations:
        recommendations.append(
            "Deadline performance is healthy."
        )

    for rec in recommendations:
        st.info(rec)

    st.divider()

    # ==================================================
    # EXECUTIVE SUMMARY
    # ==================================================

    st.subheader("📋 Executive Summary")

    st.success(f"""
    Overdue Tasks: {len(overdue)}

    Critical Tasks: {len(critical)}

    Warning Tasks: {len(warning)}

    Healthy Tasks: {len(healthy)}

    AI recommends focusing on overdue and
    critical tasks to maintain sprint commitments.
    """)