# AI Co-Lead Professional Dashboard (Final + Interactive)

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="AI Co-Lead Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("AI_CoLead_5000_Dataset.csv")

    # Add simulated fields if missing
    if "Task_Date" not in df.columns:
        today = datetime.today()
        df["Task_Date"] = [today - timedelta(days=np.random.randint(0, 30)) for _ in range(len(df))]
        df["Deadline"] = df["Task_Date"] + pd.to_timedelta(np.random.randint(1, 10, size=len(df)), unit='d')
        df["Meeting_Count"] = np.random.randint(0, 6, size=len(df))

    return df

df = load_data()

# ---------------- UI STYLE ----------------
st.markdown("""
    <style>
    .main {background-color: #0e1117; color: white;}
    .stMetric {background-color: #1c1f26; padding: 10px; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 AI Co-Lead: Intelligent Team Dashboard")

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio("Navigation", [
    "📊 Overview",
    "📈 Work Analytics",
    "⚠️ Risk Analysis",
    "📅 Deadlines & Risks",
    "🆕 New Tasks",
    "📊 Progress Tracking",
    "📞 Meetings Summary",
    "👥 Team Insights",
    "🤖 AI Assistant"
])

# ---------------- OVERVIEW ----------------
if page == "📊 Overview":
    st.header("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Employees", len(df))
    col2.metric("Active Work", int(df["Tasks_Assigned"].sum()))
    col3.metric("Completed", int(df["Tasks_Completed"].sum()))
    col4.metric("Overdue", int(df["Overdue_Tasks"].sum()))

    st.subheader("📌 Work Summary (KPI View)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Tasks Assigned", int(df["Tasks_Assigned"].sum()))
    col2.metric("Tasks Completed", int(df["Tasks_Completed"].sum()))
    col3.metric("Overdue Tasks", int(df["Overdue_Tasks"].sum()))

    st.subheader("📊 Work Distribution Graph")
    st.caption("X-axis: Work Type | Y-axis: Number of Tasks")

    work_data = pd.DataFrame({
        "Work Type": ["Assigned", "Completed", "Overdue"],
        "Count": [
            df["Tasks_Assigned"].sum(),
            df["Tasks_Completed"].sum(),
            df["Overdue_Tasks"].sum()
        ],
        "Description": [
            "Total tasks assigned to employees",
            "Tasks successfully completed",
            "Tasks delayed beyond deadline"
        ]
    })

    fig = px.bar(
        work_data,
        x="Work Type",
        y="Count",
        color="Work Type",
        hover_data=["Description"],
        title="Work Summary"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- WORK ANALYTICS ----------------
elif page == "📈 Work Analytics":
    st.header("📈 Work Analytics")

    st.subheader("Department-wise Workload")
    st.caption("X-axis: Department | Y-axis: Tasks")

    dept_data = df.groupby("Department")[["Tasks_Assigned", "Tasks_Completed"]].sum().reset_index()

    fig = px.bar(
        dept_data,
        x="Department",
        y=["Tasks_Assigned", "Tasks_Completed"],
        barmode="group",
        title="Department-wise Workload",
        hover_data={
            "Tasks_Assigned": True,
            "Tasks_Completed": True
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top Performing Employees")
    top = df.sort_values(by="Completion_Rate", ascending=False).head(10)
    st.dataframe(top[["Employee_ID", "Department", "Completion_Rate"]])

# ---------------- RISK ----------------
elif page == "⚠️ Risk Analysis":
    st.header("⚠️ Risk Analysis")

    col1, col2, col3 = st.columns(3)
    col1.metric("Burnout Risk", int(df["Burnout_Risk"].sum()))
    col2.metric("Disengagement Risk", int(df["Disengagement_Risk"].sum()))
    col3.metric("Sprint Risk", int(df["Sprint_Risk"].sum()))

    st.subheader("📊 Risk Distribution Graph")
    st.caption("X-axis: Risk Type | Y-axis: Count")

    risk_data = pd.DataFrame({
        "Risk Type": ["Burnout", "Disengagement", "Sprint"],
        "Count": [
            df["Burnout_Risk"].sum(),
            df["Disengagement_Risk"].sum(),
            df["Sprint_Risk"].sum()
        ],
        "Description": [
            "High workload + stress",
            "Low communication + engagement",
            "High blockers / delays"
        ]
    })

    fig = px.bar(
        risk_data,
        x="Risk Type",
        y="Count",
        color="Risk Type",
        hover_data=["Description"],
        title="Risk Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- DEADLINES ----------------
elif page == "📅 Deadlines & Risks":
    st.header("📅 Deadlines & Risks")

    st.subheader("⏳ Tasks Near Deadline")
    st.caption("Tasks due in next 2 days")
    near_deadline = df[df["Deadline"] <= datetime.today() + timedelta(days=2)]
    st.dataframe(near_deadline[["Employee_ID", "Deadline", "Overdue_Tasks"]].head(30))

    st.subheader("⚠️ High Risk Tasks")
    st.dataframe(df[df["Sprint_Risk"] == 1].head(30))

# ---------------- NEW TASKS ----------------
elif page == "🆕 New Tasks":
    st.header("🆕 New Tasks")

    st.caption("Recently assigned tasks")
    recent = df.sort_values(by="Task_Date", ascending=False).head(30)
    st.dataframe(recent[["Employee_ID", "Department", "Task_Date"]])

# ---------------- PROGRESS ----------------
elif page == "📊 Progress Tracking":
    st.header("📊 Progress Tracking")

    df["Progress_%"] = (df["Tasks_Completed"] / df["Tasks_Assigned"]) * 100

    st.subheader("Progress Table")
    st.dataframe(df[["Employee_ID", "Progress_%"]].head(30))

    st.subheader("📈 Progress Trend")
    st.caption("X-axis: Employees | Y-axis: Completion %")
    st.line_chart(df["Progress_%"].head(100))

# ---------------- MEETINGS ----------------
elif page == "📞 Meetings Summary":
    st.header("📞 Meetings Summary")

    st.subheader("Meeting Load by Department")
    st.caption("X-axis: Department | Y-axis: Meeting Hours")

    meeting_data = df.groupby("Department")["Meeting_Hours"].sum().reset_index()

    fig = px.bar(
        meeting_data,
        x="Department",
        y="Meeting_Hours",
        color="Meeting_Hours",
        title="Meeting Load",
        hover_data={"Meeting_Hours": True}
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- TEAM ----------------
elif page == "👥 Team Insights":
    st.header("👥 Team Insights")

    st.subheader("🔥 Overloaded Employees")
    st.dataframe(df[df["Overload_Flag"] == 1].head(20))

    st.subheader("😐 Low Engagement Employees")
    st.dataframe(df[df["Disengagement_Risk"] == 1].head(20))

# ---------------- AI ----------------
elif page == "🤖 AI Assistant":
    st.header("🤖 AI Assistant")

    user_input = st.text_input("Ask about team performance...")

    if user_input:
        if "burnout" in user_input.lower():
            st.write("⚠️ Suggest reducing workload for high-risk employees.")
        elif "engagement" in user_input.lower():
            st.write("📉 Suggest conducting 1:1 meetings.")
        elif "sprint" in user_input.lower():
            st.write("🚨 Check blockers affecting sprint.")
        else:
            st.write("🤖 Monitor workload, communication, and risks regularly.")

    st.success("AI Assistant supports decision-making.")