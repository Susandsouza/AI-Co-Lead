# pages/employees.py

import streamlit as st
import pandas as pd
import plotly.express as px


def render_employees(df):

    st.header("👥 Employee Intelligence Center")

    st.markdown("""
    Gain deep insights into employee performance,
    wellbeing, engagement, workload, and risks.
    """)

    # ==================================================
    # EMPLOYEE SELECTOR
    # ==================================================

    employee_ids = sorted(
        df["Employee_ID"].unique()
    )

    selected_employee = st.selectbox(
        "Select Employee",
        employee_ids
    )

    emp = df[
        df["Employee_ID"] == selected_employee
    ].iloc[0]

    # ==================================================
    # PROFILE SECTION
    # ==================================================

    st.subheader("🪪 Employee Profile")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Employee ID",
        emp["Employee_ID"]
    )

    c2.metric(
        "Department",
        emp["Department"]
    )

    c3.metric(
        "Role",
        emp["Role"]
    )

    st.divider()

    # ==================================================
    # PERFORMANCE KPIs
    # ==================================================

    st.subheader("📊 Performance Metrics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Tasks Assigned",
        int(emp["Tasks_Assigned"])
    )

    c2.metric(
        "Tasks Completed",
        int(emp["Tasks_Completed"])
    )

    c3.metric(
        "Completion %",
        round(
            emp["Completion_Rate"],
            2
        )
    )

    c4.metric(
        "Sprint Velocity",
        round(
            emp["Sprint_Velocity"],
            2
        )
    )

    st.divider()

    # ==================================================
    # WELLBEING SECTION
    # ==================================================

    st.subheader("💚 Wellbeing Metrics")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Stress Level",
        round(
            emp["Stress_Level"],
            2
        )
    )

    c2.metric(
        "Engagement Score",
        round(
            emp["Engagement_Score"],
            2
        )
    )

    c3.metric(
        "Working Hours",
        round(
            emp["Working_Hours"],
            2
        )
    )

    st.divider()

    # ==================================================
    # RISK STATUS
    # ==================================================

    st.subheader("⚠️ Risk Status")

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Burnout Risk",
        "Yes" if emp["Burnout_Risk"] == 1 else "No"
    )

    r2.metric(
        "Disengagement Risk",
        "Yes" if emp["Disengagement_Risk"] == 1 else "No"
    )

    r3.metric(
        "Sprint Risk",
        "Yes" if emp["Sprint_Risk"] == 1 else "No"
    )

    st.divider()

    # ==================================================
    # WORKLOAD ANALYSIS
    # ==================================================

    st.subheader("⚖️ Workload Analysis")

    workload_data = pd.DataFrame({
        "Metric": [
            "Tasks Assigned",
            "Tasks Completed",
            "Overdue Tasks",
            "Blockers"
        ],
        "Value": [
            emp["Tasks_Assigned"],
            emp["Tasks_Completed"],
            emp["Overdue_Tasks"],
            emp["Blocker_Count"]
        ]
    })

    fig = px.bar(
        workload_data,
        x="Metric",
        y="Value",
        color="Metric",
        title="Employee Workload"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # EMPLOYEE BENCHMARK
    # ==================================================

    st.subheader("📈 Employee vs Team Average")

    team_avg_completion = round(
        df["Completion_Rate"].mean(),
        2
    )

    team_avg_engagement = round(
        df["Engagement_Score"].mean(),
        2
    )

    comparison = pd.DataFrame({
        "Metric": [
            "Completion Rate",
            "Engagement Score"
        ],
        "Employee": [
            emp["Completion_Rate"],
            emp["Engagement_Score"]
        ],
        "Team Average": [
            team_avg_completion,
            team_avg_engagement
        ]
    })

    fig = px.bar(
        comparison,
        x="Metric",
        y=[
            "Employee",
            "Team Average"
        ],
        barmode="group",
        title="Employee Benchmark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # AI INSIGHTS
    # ==================================================

    st.subheader("🤖 AI Insights")

    insights = []

    if emp["Burnout_Risk"] == 1:
        insights.append(
            "Employee shows signs of burnout."
        )

    if emp["Disengagement_Risk"] == 1:
        insights.append(
            "Employee engagement requires attention."
        )

    if emp["Overload_Flag"] == 1:
        insights.append(
            "Workload exceeds recommended levels."
        )

    if emp["Completion_Rate"] < 60:
        insights.append(
            "Performance support may be required."
        )

    if not insights:
        insights.append(
            "Employee performance appears healthy."
        )

    for insight in insights:
        st.info(insight)

    st.divider()

    # ==================================================
    # RECOMMENDED ACTIONS
    # ==================================================

    st.subheader("🎯 Recommended Actions")

    actions = []

    if emp["Burnout_Risk"] == 1:
        actions.append(
            "Schedule a wellbeing check-in."
        )

    if emp["Overload_Flag"] == 1:
        actions.append(
            "Redistribute workload."
        )

    if emp["Disengagement_Risk"] == 1:
        actions.append(
            "Conduct a 1:1 discussion."
        )

    if emp["Completion_Rate"] < 60:
        actions.append(
            "Review blockers and priorities."
        )

    if not actions:
        actions.append(
            "Continue regular monitoring."
        )

    for action in actions:
        st.success(action)

    st.divider()

    # ==================================================
    # TOP PERFORMERS
    # ==================================================

    st.subheader("🏆 Top Performers")

    top = (
        df.sort_values(
            "Completion_Rate",
            ascending=False
        )
        .head(10)
    )

    cols = [
        "Employee_ID",
        "Department",
        "Completion_Rate",
        "Engagement_Score"
    ]

    st.dataframe(
        top[cols],
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # EMPLOYEES NEEDING ATTENTION
    # ==================================================

    st.subheader("🚨 Employees Needing Attention")

    at_risk = df[
        (df["Burnout_Risk"] == 1)
        |
        (df["Disengagement_Risk"] == 1)
        |
        (df["Sprint_Risk"] == 1)
    ]

    cols = [
        "Employee_ID",
        "Department",
        "Stress_Level",
        "Engagement_Score",
        "Completion_Rate"
    ]

    st.dataframe(
        at_risk[cols].head(20),
        use_container_width=True
    )