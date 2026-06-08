# pages/risks.py

import streamlit as st
import pandas as pd
import plotly.express as px
from services.recommendation_engine import generate_ai_recommendations
from services.risk_engine import generate_risk_summary


def render_risks(df):

    st.header("⚠️ Risk Intelligence Center")
    risk_data = generate_risk_summary(df)

    st.markdown("""
    AI Co-Lead continuously analyzes employee behavior,
    workload patterns, sprint performance, and engagement
    indicators to identify potential risks before they impact
    project delivery.
    """)

    # ==================================================
    # RISK KPIs
    # ==================================================
    
    burnout_count = int(df["Burnout_Risk"].sum())
    disengagement_count = int(df["Disengagement_Risk"].sum())
    sprint_risk_count = int(df["Sprint_Risk"].sum())

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🔥 Burnout Risks",
        burnout_count
    )

    col2.metric(
        "📉 Disengagement Risks",
        disengagement_count
    )

    col3.metric(
        "🚨 Sprint Risks",
        sprint_risk_count
    )

    st.divider()
    st.subheader("🧠 Organizational Risk Metrics")

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
    # RISK DISTRIBUTION
    # ==================================================

    st.subheader("📊 Risk Distribution")

    risk_data = pd.DataFrame({
        "Risk Type": [
            "Burnout",
            "Disengagement",
            "Sprint"
        ],
        "Count": [
            burnout_count,
            disengagement_count,
            sprint_risk_count
        ]
    })

    fig = px.bar(
        risk_data,
        x="Risk Type",
        y="Count",
        color="Risk Type",
        title="Risk Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # BURNOUT RISK EMPLOYEES
    # ==================================================

    st.subheader("🔥 Burnout Risk Employees")

    burnout_df = df[
        df["Burnout_Risk"] == 1
    ]

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Working_Hours",
            "Stress_Level",
            "Tasks_Assigned"
        ]
        if c in burnout_df.columns
    ]

    st.dataframe(
        burnout_df[cols].head(25),
        use_container_width=True
    )

    st.info("""
    AI Insight:

    Employees with high working hours,
    elevated stress levels, and excessive task
    assignments are more likely to experience burnout.
    """)

    st.divider()


    # ==================================================
    # DISENGAGEMENT DETECTION
    # ==================================================

    st.subheader("📉 Silent Disengagement Detection")

    disengaged = df[
        df["Disengagement_Risk"] == 1
    ]

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Communication_Count",
            "Engagement_Score"
        ]
        if c in disengaged.columns
    ]

    st.dataframe(
        disengaged[cols].head(25),
        use_container_width=True
    )

    st.warning("""
    AI Insight:

    These employees show reduced participation,
    communication, or engagement levels that may
    indicate silent disengagement.
    """)

    st.divider()

    # ==================================================
    # SPRINT RISK
    # ==================================================

    st.subheader("🚨 Sprint Risk Analysis")

    sprint_df = df[
        df["Sprint_Risk"] == 1
    ]

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Blocker_Count",
            "Sprint_Velocity",
            "Overdue_Tasks"
        ]
        if c in sprint_df.columns
    ]

    st.dataframe(
        sprint_df[cols].head(25),
        use_container_width=True
    )

    st.error("""
    AI Insight:

    Sprint risks are typically caused by blockers,
    delayed tasks, low velocity, and workload imbalance.
    """)

    st.divider()

    # ==================================================
    # DEPARTMENT RISK HEATMAP
    # ==================================================

    st.subheader("🔥 Department Risk Heatmap")

    dept_risks = (
        df.groupby("Department")
        [
            [
                "Burnout_Risk",
                "Disengagement_Risk",
                "Sprint_Risk"
            ]
        ]
        .sum()
        .reset_index()
    )

    heatmap = px.imshow(
        dept_risks.set_index("Department"),
        text_auto=True,
        aspect="auto",
        title="Department Risk Heatmap"
    )

    st.plotly_chart(
        heatmap,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # RISK SCORE
    # ==================================================

    st.subheader("🧠 Organizational Risk Score")

    total_employees = len(df)

    total_risks = (
        burnout_count +
        disengagement_count +
        sprint_risk_count
    )

    risk_score = (
        total_risks /
        max(total_employees, 1)
    ) * 100

    st.progress(
        min(int(risk_score), 100)
    )

    st.write(
        f"Current Organizational Risk Score: "
        f"**{risk_score:.2f}%**"
    )

    if risk_score < 20:
        st.success(
            "🟢 Risk levels are under control."
        )

    elif risk_score < 40:
        st.warning(
            "🟡 Risk levels require monitoring."
        )

    else:
        st.error(
            "🔴 High organizational risk detected."
        )

    st.divider()

    # ==================================================
    # AI RECOMMENDATIONS
    # ==================================================

    st.subheader("🤖 AI Recommendations")

    recommendations = []

    if burnout_count > 50:
        recommendations.append(
            "Redistribute workload across teams."
        )

    if disengagement_count > 30:
        recommendations.append(
            "Conduct employee engagement reviews."
        )

    if sprint_risk_count > 20:
        recommendations.append(
            "Review blockers and sprint commitments."
        )

    if not recommendations:
        recommendations.append(
            "No major risks detected."
        )

    for rec in recommendations:
        st.info(rec)

    st.divider()

    # ==================================================
    # TOP HIGH-RISK EMPLOYEES
    # ==================================================

    st.subheader("🚨 Employees Requiring Immediate Attention")

    high_risk = df[
        (df["Burnout_Risk"] == 1)
        |
        (df["Disengagement_Risk"] == 1)
        |
        (df["Sprint_Risk"] == 1)
    ]

    cols = [
        c for c in [
            "Employee_ID",
            "Department",
            "Tasks_Assigned",
            "Stress_Level",
            "Engagement_Score",
            "Blocker_Count"
        ]
        if c in high_risk.columns
    ]

    st.dataframe(
        high_risk[cols].head(30),
        use_container_width=True
    )


    st.subheader("🚨 AI-Detected High Risk Employees")

    st.dataframe(
        risk_data["high_risk_employees"],
        use_container_width=True
    )