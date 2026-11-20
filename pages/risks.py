
# pages/risks.py

import streamlit as st
import pandas as pd
import plotly.express as px

from services.risk_engine import generate_risk_summary


def render_risks(df):

    # ==========================================
    # DATA PREPARATION
    # ==========================================

    st.header("⚠️ Risk Intelligence Center")

    risk_summary = generate_risk_summary(df)

    st.markdown("""
    AI Co-Lead continuously analyzes employee behavior,
    workload patterns, sprint performance, and engagement
    indicators to identify potential risks before they
    impact project delivery.
    """)

    # Safely retrieve numeric columns
    def get_numeric(column):
        if column in df.columns:
            return pd.to_numeric(
                df[column], errors="coerce"
            ).fillna(0)
        return pd.Series(0, index=df.index, dtype=float)

    # Risk classification columns
    burnout_flags = get_numeric("Burnout_Risk")
    disengagement_flags = get_numeric("Disengagement_Risk")
    sprint_flags = get_numeric("Sprint_Risk")

    burnout_count = int((burnout_flags == 1).sum())
    disengagement_count = int((disengagement_flags == 1).sum())
    sprint_risk_count = int((sprint_flags == 1).sum())

    # ==========================================
    # RISK KPI CARDS
    # ==========================================

    col1, col2, col3 = st.columns(3)

    col1.metric("🔥 Burnout Risks", burnout_count)
    col2.metric("📉 Disengagement Risks", disengagement_count)
    col3.metric("🚨 Sprint Risks", sprint_risk_count)

    st.divider()

    # ==========================================
    # ORGANIZATIONAL RISK METRICS
    # ==========================================

    st.subheader("🧠 Organizational Risk Metrics")

    c1, c2 = st.columns(2)

    c1.metric(
        "💚 Team Health Index",
        f"{risk_summary['team_health']:.2f}%"
    )

    c2.metric(
        "⚠️ Organization Risk",
        f"{risk_summary['organization_risk']:.2f}%"
    )

    st.divider()

    # ==========================================
    # RISK DISTRIBUTION
    # ==========================================

    st.subheader("📊 Risk Distribution")

    risk_distribution = pd.DataFrame({
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
        risk_distribution,
        x="Risk Type",
        y="Count",
        color="Risk Type",
        title="Employee Risk Distribution"
    )

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==========================================
    # BURNOUT RISK EMPLOYEES
    # ==========================================

    st.subheader("🔥 Burnout Risk Employees")

    burnout_df = df.loc[burnout_flags == 1].copy()

    display_columns = [
        c for c in [
            "Employee_ID",
            "Department",
            "Working_Hours",
            "Stress_Level",
            "Tasks_Assigned"
        ]
        if c in burnout_df.columns
    ]

    if not burnout_df.empty and display_columns:
        st.dataframe(
            burnout_df[display_columns].head(25),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No burnout-risk employee records available.")

    st.info("""
    AI Insight:

    Employees with high working hours, elevated stress
    levels, and excessive task assignments may be at
    greater risk of burnout.
    """)

    st.divider()

    # ==========================================
    # DISENGAGEMENT DETECTION
    # ==========================================

    st.subheader("📉 Silent Disengagement Detection")

    disengaged_df = df.loc[
        disengagement_flags == 1
    ].copy()

    display_columns = [
        c for c in [
            "Employee_ID",
            "Department",
            "Communication_Count",
            "Engagement_Score"
        ]
        if c in disengaged_df.columns
    ]

    if not disengaged_df.empty and display_columns:
        st.dataframe(
            disengaged_df[display_columns].head(25),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No disengagement-risk records available.")

    st.warning("""
    AI Insight:

    Reduced participation, communication, or engagement
    may indicate potential silent disengagement.
    """)

    st.divider()

    # ==========================================
    # SPRINT RISK ANALYSIS
    # ==========================================

    st.subheader("🚨 Sprint Risk Analysis")

    sprint_df = df.loc[sprint_flags == 1].copy()

    display_columns = [
        c for c in [
            "Employee_ID",
            "Department",
            "Blocker_Count",
            "Sprint_Velocity",
            "Overdue_Tasks"
        ]
        if c in sprint_df.columns
    ]

    if not sprint_df.empty and display_columns:
        st.dataframe(
            sprint_df[display_columns].head(25),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No sprint-risk records available.")

    st.error("""
    AI Insight:

    Blockers, delayed tasks, low velocity, and workload
    imbalance can contribute to sprint delivery risks.
    """)

    st.divider()

    # ==========================================
    # DEPARTMENT RISK HEATMAP
    # ==========================================

    st.subheader("🔥 Department Risk Heatmap")

    if "Department" in df.columns:

        dept_risks = df[["Department"]].copy()

        dept_risks["Burnout Risk"] = burnout_flags
        dept_risks["Disengagement Risk"] = disengagement_flags
        dept_risks["Sprint Risk"] = sprint_flags

        dept_risks = dept_risks.groupby(
            "Department"
        )[
            [
                "Burnout Risk",
                "Disengagement Risk",
                "Sprint Risk"
            ]
        ].sum()

        heatmap = px.imshow(
            dept_risks,
            text_auto=True,
            aspect="auto",
            title="Department-wise Risk Distribution",
            color_continuous_scale="Reds"
        )

        heatmap.update_layout(template="plotly_dark")

        st.plotly_chart(
            heatmap,
            use_container_width=True
        )

    else:
        st.info("Department information is unavailable.")

    st.divider()

    # ==========================================
    # ORGANIZATIONAL RISK SCORE
    # ==========================================

    st.subheader("🧠 Organizational Risk Score")

    total_employees = len(df)

    total_risk_flags = (
        burnout_count +
        disengagement_count +
        sprint_risk_count
    )

    risk_score = (
        total_risk_flags / max(total_employees, 1)
    ) * 100

    st.progress(
        min(int(risk_score), 100)
    )

    st.write(
        f"Current Risk Incidence Score: "
        f"**{risk_score:.2f}%**"
    )

    if risk_score < 20:
        st.success("🟢 Risk levels are under control.")

    elif risk_score < 40:
        st.warning("🟡 Risk levels require monitoring.")

    else:
        st.error("🔴 High organizational risk detected.")

    st.caption(
        "Risk incidence score counts risk flags; "
        "an employee may contribute to more than one category."
    )

    st.divider()

    # ==========================================
    # AI RECOMMENDATIONS
    # ==========================================

    st.subheader("🤖 AI Recommendations")

    recommendations = []

    if burnout_count > 50:
        recommendations.append(
            "🔥 Redistribute workload across teams."
        )

    if disengagement_count > 30:
        recommendations.append(
            "👥 Conduct employee engagement reviews."
        )

    if sprint_risk_count > 20:
        recommendations.append(
            "🚨 Review blockers and sprint commitments."
        )

    if not recommendations:
        recommendations.append(
            "✅ No major risk thresholds triggered."
        )

    for recommendation in recommendations:
        st.info(recommendation)

    st.divider()

    