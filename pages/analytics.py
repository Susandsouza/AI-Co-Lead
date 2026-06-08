# pages/analytics.py

import streamlit as st
import pandas as pd
import plotly.express as px


def render_analytics(df):

    st.header("📊 Work Analytics Center")

    st.markdown("""
    Analyze productivity, workload, performance trends,
    employee engagement, and team efficiency across departments.
    """)

    # ==================================================
    # KPI SECTION
    # ==================================================

    total_tasks = int(df["Tasks_Assigned"].sum())
    completed_tasks = int(df["Tasks_Completed"].sum())

    avg_completion = round(
        df["Completion_Rate"].mean(),
        2
    )

    avg_engagement = round(
        df["Engagement_Score"].mean(),
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📌 Tasks Assigned",
        total_tasks
    )

    col2.metric(
        "✅ Tasks Completed",
        completed_tasks
    )

    col3.metric(
        "📈 Avg Completion %",
        f"{avg_completion}%"
    )

    col4.metric(
        "😊 Avg Engagement",
        avg_engagement
    )

    st.divider()

    # ==================================================
    # DEPARTMENT PERFORMANCE
    # ==================================================

    st.subheader("🏢 Department Performance")

    dept_perf = (
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
        dept_perf,
        x="Department",
        y=[
            "Tasks_Assigned",
            "Tasks_Completed"
        ],
        barmode="group",
        title="Department Productivity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # COMPLETION RATE
    # ==================================================

    st.subheader("📈 Completion Rate by Department")

    completion = (
        df.groupby("Department")
        [
            "Completion_Rate"
        ]
        .mean()
        .reset_index()
    )

    fig = px.line(
        completion,
        x="Department",
        y="Completion_Rate",
        markers=True,
        title="Average Completion Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # WORKLOAD DISTRIBUTION
    # ==================================================

    st.subheader("⚖️ Workload Distribution")

    fig = px.histogram(
        df,
        x="Tasks_Assigned",
        nbins=20,
        title="Tasks Assigned Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # WORKING HOURS
    # ==================================================

    st.subheader("⏱️ Working Hours Analysis")

    fig = px.box(
        df,
        y="Working_Hours",
        color="Department",
        title="Working Hours by Department"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # MEETING ANALYTICS
    # ==================================================

    st.subheader("📞 Meeting Load")

    meeting_df = (
        df.groupby("Department")
        [
            "Meeting_Hours"
        ]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        meeting_df,
        x="Department",
        y="Meeting_Hours",
        color="Meeting_Hours",
        title="Meeting Hours by Department"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # ENGAGEMENT ANALYTICS
    # ==================================================

    st.subheader("😊 Engagement Analysis")

    engagement = (
        df.groupby("Department")
        [
            "Engagement_Score"
        ]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        engagement,
        x="Department",
        y="Engagement_Score",
        color="Engagement_Score",
        title="Average Engagement Score"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # TOP PERFORMERS
    # ==================================================

    st.subheader("🏆 Top Performers")

    top_performers = (
        df.sort_values(
            "Completion_Rate",
            ascending=False
        )
        .head(15)
    )

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Completion_Rate",
            "Tasks_Completed"
        ]
        if c in df.columns
    ]

    st.dataframe(
        top_performers[cols],
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # LOW PERFORMERS
    # ==================================================

    st.subheader("📉 Employees Needing Support")

    low_performers = (
        df.sort_values(
            "Completion_Rate",
            ascending=True
        )
        .head(15)
    )

    st.dataframe(
        low_performers[cols],
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # PRODUCTIVITY VS STRESS
    # ==================================================

    st.subheader("🧠 Productivity vs Stress")

    fig = px.scatter(
        df,
        x="Stress_Level",
        y="Completion_Rate",
        color="Department",
        title="Stress vs Productivity"
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

    if avg_completion < 70:
        insights.append(
            "Completion rates are below target."
        )

    if avg_engagement < 70:
        insights.append(
            "Employee engagement needs improvement."
        )

    if df["Meeting_Hours"].mean() > 15:
        insights.append(
            "Meeting load is high and may impact productivity."
        )

    if not insights:
        insights.append(
            "Performance indicators are healthy."
        )

    for insight in insights:
        st.info(insight)

def render_home(df):

    ai = generate_ai_recommendations(df)

    st.subheader("🤖 AI Priorities")

    for priority in ai["priorities"]:
        st.warning(priority)