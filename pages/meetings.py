# pages/meetings.py

import streamlit as st
import pandas as pd
import plotly.express as px


def render_meetings(df):

    st.header("📞 Meeting Intelligence Center")

    st.markdown("""
    Analyze meeting patterns, employee meeting load,
    and the impact of meetings on productivity.
    """)

    # ==================================================
    # KPI SECTION
    # ==================================================

    total_meeting_hours = round(
        df["Meeting_Hours"].sum(),
        2
    )

    avg_meeting_hours = round(
        df["Meeting_Hours"].mean(),
        2
    )

    max_meeting_hours = round(
        df["Meeting_Hours"].max(),
        2
    )

    overloaded_meeting_count = len(
        df[df["Meeting_Hours"] > avg_meeting_hours]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "📞 Total Meeting Hours",
        total_meeting_hours
    )

    col2.metric(
        "⏱ Avg Meeting Hours",
        avg_meeting_hours
    )

    col3.metric(
        "🔥 Highest Meeting Load",
        max_meeting_hours
    )

    col4.metric(
        "⚠ High Meeting Employees",
        overloaded_meeting_count
    )

    st.divider()

    # ==================================================
    # DEPARTMENT MEETING LOAD
    # ==================================================

    st.subheader("🏢 Department Meeting Load")

    dept_meetings = (
        df.groupby("Department")
        [
            "Meeting_Hours"
        ]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        dept_meetings,
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
    # MEETING DISTRIBUTION
    # ==================================================

    st.subheader("📊 Meeting Hour Distribution")

    fig = px.histogram(
        df,
        x="Meeting_Hours",
        nbins=20,
        title="Distribution of Meeting Hours"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # PRODUCTIVITY VS MEETINGS
    # ==================================================

    st.subheader("📈 Productivity vs Meetings")

    fig = px.scatter(
        df,
        x="Meeting_Hours",
        y="Completion_Rate",
        color="Department",
        hover_data=["Employee_ID"],
        title="Meeting Hours vs Completion Rate"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info("""
    AI Insight:

    This graph helps determine whether increased
    meeting participation improves or negatively
    impacts employee productivity.
    """)

    st.divider()

    # ==================================================
    # ENGAGEMENT VS MEETINGS
    # ==================================================

    st.subheader("😊 Engagement vs Meetings")

    fig = px.scatter(
        df,
        x="Meeting_Hours",
        y="Engagement_Score",
        color="Department",
        hover_data=["Employee_ID"],
        title="Meeting Hours vs Engagement"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # HIGH MEETING LOAD EMPLOYEES
    # ==================================================

    st.subheader("🔥 Employees with High Meeting Load")

    high_meeting = (
        df.sort_values(
            "Meeting_Hours",
            ascending=False
        )
        .head(20)
    )

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Meeting_Hours",
            "Tasks_Assigned",
            "Completion_Rate"
        ]
        if c in df.columns
    ]

    st.dataframe(
        high_meeting[cols],
        use_container_width=True
    )

    st.warning("""
    AI Insight:

    Employees with excessive meeting load may
    have reduced time for focused work.
    """)

    st.divider()

    # ==================================================
    # LOW MEETING PARTICIPATION
    # ==================================================

    st.subheader("📉 Low Meeting Participation")

    low_meeting = (
        df.sort_values(
            "Meeting_Hours",
            ascending=True
        )
        .head(20)
    )

    st.dataframe(
        low_meeting[cols],
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # DEPARTMENT MEETING HEATMAP
    # ==================================================

    st.subheader("🔥 Meeting Load Heatmap")

    heatmap_df = (
        df.groupby("Department")
        [
            [
                "Meeting_Hours",
                "Completion_Rate",
                "Engagement_Score"
            ]
        ]
        .mean()
        .reset_index()
    )

    heatmap = px.imshow(
        heatmap_df.set_index("Department"),
        text_auto=True,
        aspect="auto",
        title="Department Meeting Heatmap"
    )

    st.plotly_chart(
        heatmap,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # MEETING EFFICIENCY SCORE
    # ==================================================

    st.subheader("🧠 Meeting Efficiency Score")

    efficiency_score = (
        df["Completion_Rate"].mean()
        /
        max(df["Meeting_Hours"].mean(), 1)
    ) * 10

    efficiency_score = min(
        round(efficiency_score, 2),
        100
    )

    st.progress(
        int(min(efficiency_score, 100))
    )

    st.write(
        f"Meeting Efficiency Score: "
        f"**{efficiency_score}%**"
    )

    if efficiency_score >= 80:
        st.success(
            "🟢 Meetings appear efficient."
        )

    elif efficiency_score >= 50:
        st.warning(
            "🟡 Meeting efficiency can improve."
        )

    else:
        st.error(
            "🔴 Meetings may be impacting productivity."
        )

    st.divider()

    # ==================================================
    # AI RECOMMENDATIONS
    # ==================================================

    st.subheader("🤖 AI Recommendations")

    recommendations = []

    if avg_meeting_hours > 15:
        recommendations.append(
            "Reduce unnecessary meetings."
        )

    if efficiency_score < 50:
        recommendations.append(
            "Review meeting frequency and duration."
        )

    if overloaded_meeting_count > 100:
        recommendations.append(
            "Balance meeting participation across teams."
        )

    if not recommendations:
        recommendations.append(
            "Meeting patterns appear healthy."
        )

    for rec in recommendations:
        st.info(rec)

    st.divider()

    # ==================================================
    # AI EXECUTIVE SUMMARY
    # ==================================================

    st.subheader("📋 Executive Summary")

    st.success(f"""
    Total Meeting Hours: {total_meeting_hours}

    Average Meeting Hours: {avg_meeting_hours}

    High Meeting Load Employees: {overloaded_meeting_count}

    Meeting Efficiency Score: {efficiency_score}%

    AI recommends monitoring employees with
    excessive meeting hours to ensure adequate
    focus time for productive work.
    """)