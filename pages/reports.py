# pages/reports.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime


def render_reports(df):

    st.header("📄 Reports & Executive Insights")

    st.markdown("""
    Generate leadership reports, executive summaries,
    performance reviews, and risk assessment reports.
    """)

    # ==================================================
    # REPORT TYPE
    # ==================================================

    report_type = st.selectbox(
        "Select Report Type",
        [
            "Executive Summary",
            "Team Performance",
            "Risk Assessment",
            "Sprint Report",
            "Employee Report"
        ]
    )

    st.divider()

    # ==================================================
    # EXECUTIVE SUMMARY
    # ==================================================

    if report_type == "Executive Summary":

        st.subheader("📊 Executive Summary")

        total_employees = len(df)

        total_tasks = int(
            df["Tasks_Assigned"].sum()
        )

        completed_tasks = int(
            df["Tasks_Completed"].sum()
        )

        overdue_tasks = int(
            df["Overdue_Tasks"].sum()
        )

        burnout = int(
            df["Burnout_Risk"].sum()
        )

        disengagement = int(
            df["Disengagement_Risk"].sum()
        )

        sprint = int(
            df["Sprint_Risk"].sum()
        )

        report = f"""
EXECUTIVE SUMMARY REPORT
Generated On: {datetime.now()}

--------------------------------------------------

Total Employees: {total_employees}

Tasks Assigned: {total_tasks}

Tasks Completed: {completed_tasks}

Overdue Tasks: {overdue_tasks}

Burnout Risks: {burnout}

Disengagement Risks: {disengagement}

Sprint Risks: {sprint}

--------------------------------------------------

AI Recommendations:

1. Review high-risk employees.

2. Address sprint blockers.

3. Improve workload distribution.

4. Monitor engagement trends.
"""

        st.text_area(
            "Generated Report",
            report,
            height=400
        )

        st.download_button(
            "⬇ Download Report",
            report,
            file_name="executive_summary.txt"
        )

    # ==================================================
    # TEAM PERFORMANCE
    # ==================================================

    elif report_type == "Team Performance":

        st.subheader("👥 Team Performance Report")

        dept = (
            df.groupby("Department")
            [
                [
                    "Tasks_Assigned",
                    "Tasks_Completed",
                    "Completion_Rate"
                ]
            ]
            .mean()
            .reset_index()
        )

        st.dataframe(
            dept,
            use_container_width=True
        )

        fig = px.bar(
            dept,
            x="Department",
            y="Completion_Rate",
            color="Completion_Rate",
            title="Department Performance"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # RISK REPORT
    # ==================================================

    elif report_type == "Risk Assessment":

        st.subheader("⚠️ Risk Assessment Report")

        risk_df = pd.DataFrame({
            "Risk": [
                "Burnout",
                "Disengagement",
                "Sprint"
            ],
            "Count": [
                df["Burnout_Risk"].sum(),
                df["Disengagement_Risk"].sum(),
                df["Sprint_Risk"].sum()
            ]
        })

        st.dataframe(
            risk_df,
            use_container_width=True
        )

        fig = px.pie(
            risk_df,
            values="Count",
            names="Risk",
            title="Risk Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # SPRINT REPORT
    # ==================================================

    elif report_type == "Sprint Report":

        st.subheader("🚀 Sprint Report")

        sprint_data = df[
            [
                "Sprint_Velocity",
                "Blocker_Count",
                "Completion_Rate"
            ]
        ]

        st.dataframe(
            sprint_data.head(20),
            use_container_width=True
        )

        fig = px.scatter(
            df,
            x="Sprint_Velocity",
            y="Completion_Rate",
            color="Department",
            title="Sprint Velocity vs Completion"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # EMPLOYEE REPORT
    # ==================================================

    elif report_type == "Employee Report":

        st.subheader("👤 Employee Report")

        employee = st.selectbox(
            "Select Employee",
            sorted(
                df["Employee_ID"].unique()
            )
        )

        emp = df[
            df["Employee_ID"] == employee
        ].iloc[0]

        report = pd.DataFrame({
            "Metric": [
                "Tasks Assigned",
                "Tasks Completed",
                "Completion Rate",
                "Stress Level",
                "Engagement Score",
                "Working Hours"
            ],
            "Value": [
                emp["Tasks_Assigned"],
                emp["Tasks_Completed"],
                emp["Completion_Rate"],
                emp["Stress_Level"],
                emp["Engagement_Score"],
                emp["Working_Hours"]
            ]
        })

        st.dataframe(
            report,
            use_container_width=True
        )

        fig = px.bar(
            report,
            x="Metric",
            y="Value",
            title=f"{employee} Performance Report"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # AI REPORT SUMMARY
    # ==================================================

    st.divider()

    st.subheader("🤖 AI Report Insights")

    insights = []

    if df["Burnout_Risk"].sum() > 50:
        insights.append(
            "Burnout levels require management attention."
        )

    if df["Sprint_Risk"].sum() > 20:
        insights.append(
            "Sprint risks could affect delivery timelines."
        )

    if df["Engagement_Score"].mean() < 70:
        insights.append(
            "Employee engagement is below optimal levels."
        )

    if not insights:
        insights.append(
            "Overall organizational performance is healthy."
        )

    for insight in insights:
        st.info(insight)