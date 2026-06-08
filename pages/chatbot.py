# pages/chatbot.py

import streamlit as st
import pandas as pd
from services.risk_engine import generate_risk_summary


def generate_response(query, df):
    risk_data = generate_risk_summary(df)

    
    query = query.lower()

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    if "summary" in query or "status" in query:

        return f"""
## 📊 Executive Summary

👥 Total Employees: {len(df)}

📌 Tasks Assigned: {int(df['Tasks_Assigned'].sum())}

✅ Tasks Completed: {int(df['Tasks_Completed'].sum())}

⏰ Overdue Tasks: {int(df['Overdue_Tasks'].sum())}

🔥 Burnout Risks: {int(df['Burnout_Risk'].sum())}

📉 Disengagement Risks: {int(df['Disengagement_Risk'].sum())}

🚨 Sprint Risks: {int(df['Sprint_Risk'].sum())}
"""
    elif "health" in query:

        return f"""
## 💚 Team Health

Team Health Index:
{risk_data['team_health']}%

Organization Risk:
{risk_data['organization_risk']}%
"""

    # =====================================
    # BURNOUT
    # =====================================

    elif "burnout" in query:

        count = int(df["Burnout_Risk"].sum())

        return f"""
## 🔥 Burnout Analysis

Employees at Risk: {count}

Possible Causes:

• High workload

• Long working hours

• Elevated stress levels

### Recommended Actions

✔ Reduce workload

✔ Schedule manager check-ins

✔ Encourage work-life balance
"""

    # =====================================
    # ENGAGEMENT
    # =====================================

    elif "engagement" in query:

        count = int(df["Disengagement_Risk"].sum())

        return f"""
## 📉 Engagement Analysis

Employees at Risk: {count}

Possible Causes:

• Reduced communication

• Low participation

• Low engagement score

### Recommended Actions

✔ Conduct 1:1 discussions

✔ Improve team involvement

✔ Recognize achievements
"""

    # =====================================
    # SPRINT RISK
    # =====================================

    elif "sprint" in query:

        count = int(df["Sprint_Risk"].sum())

        return f"""
## 🚨 Sprint Risk Analysis

Sprint Risks Detected: {count}

Potential Causes:

• Blockers

• Delayed tasks

• Low velocity

### Recommended Actions

✔ Remove blockers

✔ Reprioritize tasks

✔ Review sprint scope
"""

    # =====================================
    # OVERLOADED EMPLOYEES
    # =====================================

    elif "overload" in query or "workload" in query:

        overloaded = df[
            df["Overload_Flag"] == 1
        ]

        return f"""
## ⚖️ Workload Analysis

Overloaded Employees: {len(overloaded)}

Recommendation:

✔ Redistribute workload

✔ Balance assignments

✔ Monitor weekly workload trends
"""

    # =====================================
    # WHO NEEDS ATTENTION
    # =====================================

    elif "attention" in query:

        high_risk = df[
            (df["Burnout_Risk"] == 1)
            |
            (df["Disengagement_Risk"] == 1)
            |
            (df["Sprint_Risk"] == 1)
        ]

        return f"""
## 🚨 Attention Required

Employees Requiring Attention:

{len(high_risk)}

Recommended:

✔ Schedule reviews

✔ Address blockers

✔ Rebalance workload
"""

    # =====================================
    # PRODUCTIVITY
    # =====================================

    elif "productivity" in query:

        avg_completion = round(
            df["Completion_Rate"].mean(),
            2
        )

        return f"""
## 📈 Productivity Analysis

Average Completion Rate:

{avg_completion}%

Recommendations:

✔ Reduce meeting overload

✔ Prioritize high-value tasks

✔ Improve sprint planning
"""

    # =====================================
    # DEFAULT
    # =====================================

    return """
## 🤖 AI Co-Lead Assistant

I can help with:

• Team Summary

• Burnout Risk

• Employee Engagement

• Sprint Risks

• Productivity

• Workload Analysis

Try asking:

- Give me a summary

- Show burnout risk

- Analyze engagement

- Show sprint risk

- Which employees need attention?

- How is productivity?
"""


# =====================================================
# MAIN CHATBOT PAGE
# =====================================================

def render_chatbot(df):

    st.header("🤖 AI Co-Lead Assistant")

    st.markdown("""
    Ask questions about:

    • Team Health

    • Burnout Risks

    • Sprint Performance

    • Productivity

    • Employee Engagement
    """)

    # =====================================
    # QUICK ACTIONS
    # =====================================

    st.subheader("⚡ Quick Questions")

    c1, c2, c3, c4 = st.columns(4)

    quick_question = None

    if c1.button("📊 Summary"):
        quick_question = "summary"

    if c2.button("🔥 Burnout"):
        quick_question = "burnout"

    if c3.button("🚨 Sprint Risk"):
        quick_question = "sprint"

    if c4.button("📉 Engagement"):
        quick_question = "engagement"

    # =====================================
    # CHAT HISTORY
    # =====================================

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:

        with st.chat_message(
            msg["role"]
        ):
            st.markdown(
                msg["content"]
            )

    user_input = st.chat_input(
        "Ask AI Co-Lead..."
    )

    prompt = user_input

    if quick_question:
        prompt = quick_question

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):
            st.markdown(prompt)

        response = generate_response(
            prompt,
            df
        )

        with st.chat_message(
            "assistant"
        ):
            st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    st.divider()

    st.success(
        "AI Assistant is actively monitoring team health and project risks."
    )