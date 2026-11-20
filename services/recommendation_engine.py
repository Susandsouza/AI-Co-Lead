# services/recommendation_engine.py

import pandas as pd


# =====================================================
# WORKLOAD REDISTRIBUTION
# =====================================================

def workload_recommendations(df):

    recommendations = []

    overloaded = df[
        df["Overload_Flag"] == 1
    ].copy()

    underutilized = df[
        (df["Tasks_Assigned"] <
         df["Tasks_Assigned"].mean())
        &
        (df["Working_Hours"] <
         df["Working_Hours"].mean())
    ].copy()

    if overloaded.empty or underutilized.empty:
        return [
            "Workload distribution appears balanced."
        ]

    overloaded = overloaded.sort_values(
        "Tasks_Assigned",
        ascending=False
    )

    underutilized = underutilized.sort_values(
        "Tasks_Assigned",
        ascending=True
    )

    limit = min(
        len(overloaded),
        len(underutilized),
        10
    )

    for i in range(limit):

        sender = overloaded.iloc[i]
        receiver = underutilized.iloc[i]

        recommendations.append(
            {
                "action":
                "Redistribute Tasks",

                "from":
                sender["Employee_ID"],

                "to":
                receiver["Employee_ID"],

                "reason":
                f"{sender['Employee_ID']} has "
                f"{sender['Tasks_Assigned']} tasks while "
                f"{receiver['Employee_ID']} has "
                f"{receiver['Tasks_Assigned']} tasks."
            }
        )

    return recommendations


# =====================================================
# BURNOUT PREVENTION
# =====================================================

def burnout_recommendations(df):

    burnout = df[
        df["Burnout_Risk"] == 1
    ]

    recommendations = []

    for _, emp in burnout.head(20).iterrows():

        recommendations.append(
            {
                "employee":
                emp["Employee_ID"],

                "department":
                emp["Department"],

                "action":
                "Manager Check-In",

                "reason":
                f"Stress={emp['Stress_Level']}, "
                f"Hours={emp['Working_Hours']}"
            }
        )

    return recommendations


# =====================================================
# DISENGAGEMENT
# =====================================================

def engagement_recommendations(df):

    disengaged = df[
        df["Disengagement_Risk"] == 1
    ]

    recommendations = []

    for _, emp in disengaged.head(20).iterrows():

        recommendations.append(
            {
                "employee":
                emp["Employee_ID"],

                "action":
                "1:1 Meeting",

                "reason":
                f"Engagement Score="
                f"{emp['Engagement_Score']}"
            }
        )

    return recommendations


# =====================================================
# SPRINT RECOVERY
# =====================================================

def sprint_recommendations(df):

    sprint_risk = df[
        df["Sprint_Risk"] == 1
    ]

    recommendations = []

    for _, emp in sprint_risk.head(20).iterrows():

        recommendations.append(
            {
                "employee":
                emp["Employee_ID"],

                "action":
                "Review Sprint Blockers",

                "reason":
                f"Blockers="
                f"{emp['Blocker_Count']}"
            }
        )

    return recommendations


# =====================================================
# TOP PRIORITIES
# =====================================================

def get_top_priorities(df):

    priorities = []

    burnout_count = int(
        df["Burnout_Risk"].sum()
    )

    sprint_count = int(
        df["Sprint_Risk"].sum()
    )

    disengagement_count = int(
        df["Disengagement_Risk"].sum()
    )

    overdue_tasks = int(
        df["Overdue_Tasks"].sum()
    )

    if burnout_count > 50:
        priorities.append(
            "🔥 High burnout risk detected."
        )

    if sprint_count > 20:
        priorities.append(
            "🚨 Sprint delivery risk detected."
        )

    if disengagement_count > 30:
        priorities.append(
            "📉 Employee engagement declining."
        )

    if overdue_tasks > 100:
        priorities.append(
            "📅 Overdue tasks require attention."
        )

    if not priorities:
        priorities.append(
            "✅ No critical priorities detected."
        )

    return priorities


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def executive_summary(df):

    summary = {

        "employees":
        len(df),

        "tasks_assigned":
        int(df["Tasks_Assigned"].sum()),

        "tasks_completed":
        int(df["Tasks_Completed"].sum()),

        "burnout_risk":
        int(df["Burnout_Risk"].sum()),

        "sprint_risk":
        int(df["Sprint_Risk"].sum()),

        "disengagement_risk":
        int(df["Disengagement_Risk"].sum()),

        "overdue_tasks":
        int(df["Overdue_Tasks"].sum())
    }

    return summary


# =====================================================
# MASTER AI ENGINE
# =====================================================

def generate_ai_recommendations(df):

    return {

        "priorities":
        get_top_priorities(df),

        "workload":
        workload_recommendations(df),

        "burnout":
        burnout_recommendations(df),

        "engagement":
        engagement_recommendations(df),

        "sprint":
        sprint_recommendations(df),

        "summary":
        executive_summary(df)
    }