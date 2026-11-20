# services/risk_engine.py

import pandas as pd
import numpy as np


# =====================================================
# EMPLOYEE HEALTH SCORE
# =====================================================

def calculate_employee_health_score(employee):

    score = 100

    score -= employee["Stress_Level"] * 5

    score -= max(
        employee["Working_Hours"] - 40,
        0
    ) * 1.5

    score -= employee["Overdue_Tasks"] * 2

    score += employee["Engagement_Score"] * 0.3

    score = max(
        min(score, 100),
        0
    )

    return round(score, 2)


# =====================================================
# BURNOUT PROBABILITY
# =====================================================

def calculate_burnout_probability(employee):

    score = 0

    score += employee["Stress_Level"] * 10

    score += max(
        employee["Working_Hours"] - 40,
        0
    ) * 2

    score += employee["Tasks_Assigned"] * 1

    score -= employee["Engagement_Score"] * 0.5

    probability = min(score, 100)

    return round(probability, 2)


# =====================================================
# SPRINT FAILURE PROBABILITY
# =====================================================

def calculate_sprint_risk(employee):

    score = 0

    score += employee["Blocker_Count"] * 15

    score += employee["Overdue_Tasks"] * 10

    score -= employee["Sprint_Velocity"] * 5

    score -= employee["Completion_Rate"] * 0.5

    score = max(score, 0)

    return round(
        min(score, 100),
        2
    )


# =====================================================
# ENGAGEMENT RISK
# =====================================================

def calculate_engagement_risk(employee):

    score = 100

    score -= employee["Engagement_Score"]

    score -= employee["Communication_Count"] * 2

    score += employee["Stress_Level"] * 3

    score = max(score, 0)

    return round(
        min(score, 100),
        2
    )


# =====================================================
# DEPARTMENT RISK SCORE
# =====================================================

def calculate_department_risk(df):

    dept_scores = []

    grouped = df.groupby("Department")

    for dept, group in grouped:

        burnout = group[
            "Burnout_Risk"
        ].sum()

        disengagement = group[
            "Disengagement_Risk"
        ].sum()

        sprint = group[
            "Sprint_Risk"
        ].sum()

        employees = len(group)

        risk_score = (
            burnout +
            disengagement +
            sprint
        ) / max(employees, 1)

        dept_scores.append({

            "Department":
            dept,

            "Risk_Score":
            round(
                risk_score * 100,
                2
            )
        })

    return pd.DataFrame(
        dept_scores
    )


# =====================================================
# TEAM HEALTH INDEX
# =====================================================

def calculate_team_health_index(df):

    health_scores = []

    for _, row in df.iterrows():

        health_scores.append(
            calculate_employee_health_score(
                row
            )
        )

    return round(
        np.mean(health_scores),
        2
    )


# =====================================================
# HIGH RISK EMPLOYEES
# =====================================================

def identify_high_risk_employees(df):

    results = []

    for _, emp in df.iterrows():

        burnout_prob = (
            calculate_burnout_probability(
                emp
            )
        )

        sprint_prob = (
            calculate_sprint_risk(
                emp
            )
        )

        engagement_risk = (
            calculate_engagement_risk(
                emp
            )
        )

        if (
            burnout_prob > 70
            or sprint_prob > 70
            or engagement_risk > 70
        ):

            results.append({

                "Employee_ID":
                emp["Employee_ID"],

                "Department":
                emp["Department"],

                "Burnout_Probability":
                burnout_prob,

                "Sprint_Risk":
                sprint_prob,

                "Engagement_Risk":
                engagement_risk
            })

    return pd.DataFrame(
        results
    )


# =====================================================
# ORGANIZATIONAL RISK
# =====================================================

def calculate_organization_risk(df):

    burnout = int(
        df["Burnout_Risk"].sum()
    )

    sprint = int(
        df["Sprint_Risk"].sum()
    )

    disengagement = int(
        df["Disengagement_Risk"].sum()
    )

    total = len(df)

    risk = (
        burnout +
        sprint +
        disengagement
    ) / max(total, 1)

    return round(
        risk * 100,
        2
    )


# =====================================================
# COMPLETE RISK DASHBOARD DATA
# =====================================================

def generate_risk_summary(df):

    return {

        "team_health":
        calculate_team_health_index(df),

        "organization_risk":
        calculate_organization_risk(df),

        "department_risk":
        calculate_department_risk(df),

        "high_risk_employees":
        identify_high_risk_employees(df)
    }