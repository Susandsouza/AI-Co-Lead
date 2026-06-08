# 🚀 AI Co-Lead: Intelligent Team Lead Assistant

AI Co-Lead is an AI-powered leadership intelligence platform designed to help team leads monitor team performance, identify risks, optimize workload distribution, and make data-driven decisions.

The platform combines Machine Learning, Predictive Analytics, Risk Assessment, and Interactive Dashboards to provide real-time insights into team health and project execution.

---

## 📌 Features

### 🏠 Executive Dashboard

* Team Health Monitoring
* Organization Risk Score
* Key Performance Indicators (KPIs)
* Real-time Insights

### 📊 Work Analytics

* Department-wise Workload Analysis
* Task Assignment Tracking
* Completion Rate Monitoring
* Productivity Visualization

### ⚠️ Risk Center

* Burnout Risk Detection
* Sprint Risk Prediction
* Disengagement Analysis
* High-Risk Employee Identification

### 📅 Deadline Management

* Upcoming Deadlines
* Overdue Tasks
* Critical Task Alerts
* Priority Monitoring

### 📞 Meetings Intelligence

* Meeting Load Analysis
* Department-wise Meeting Distribution
* Collaboration Insights

### 👥 Team Insights

* Employee Performance Analysis
* Workload Balancing
* Team Health Indicators
* Productivity Assessment

### 🤖 AI Assistant

* Interactive Leadership Chatbot
* Decision Support Recommendations
* Team Performance Analysis
* Risk Explanation and Mitigation Suggestions

### 📄 Reports Center

* Executive Summary Reports
* Team Performance Reports
* Risk Reports
* Analytics Export

---

## 🧠 Machine Learning Components

AI Co-Lead uses machine learning models to predict and identify organizational risks.

### Burnout Prediction Model

Predicts employee burnout risk based on:

* Working Hours
* Task Assignments
* Meeting Hours
* Overdue Tasks
* Stress Indicators

Model File:

```text
models/burnout_model.pkl
```

### Sprint Risk Prediction Model

Predicts sprint delays and project risks using:

* Task Progress
* Overdue Work
* Team Capacity
* Meeting Load

Model File:

```text
models/sprint_model.pkl
```

---

## 📂 Project Structure

```text
AI-Co-Lead/
│
├── app.py
│
├── pages/
│   ├── home.py
│   ├── analytics.py
│   ├── risks.py
│   ├── meetings.py
│   ├── deadlines.py
│   ├── employees.py
│   ├── chatbot.py
│   └── reports.py
│
├── services/
│   ├── recommendation_engine.py
│   ├── risk_engine.py
│   └── __init__.py
│
├── models/
│   ├── burnout_model.pkl
│   └── sprint_model.pkl
│
├── AI_CoLead_5000_Dataset.csv
│
├── requirements.txt
│
└── README.md
```

---

## 📊 Dataset

The project uses a synthetic enterprise workforce dataset containing:

* 5000 Employees
* Multiple Departments
* Task Assignment Records
* Task Completion Metrics
* Sprint Data
* Risk Indicators
* Meeting Statistics
* Workload Information

Dataset Size:

```text
5000+ Employee Records
```

---

## 🛠️ Technologies Used

### Frontend

* Streamlit
* Plotly
* HTML/CSS

### Backend

* Python

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* Joblib

### Visualization

* Plotly Express
* Streamlit Charts

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/AI-Co-Lead.git
cd AI-Co-Lead
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open your browser:

```text
http://localhost:8501
```

---

## 🎯 Use Cases

### Team Leads

* Monitor team health
* Track project progress
* Balance workloads
* Reduce burnout

### Project Managers

* Predict sprint delays
* Improve delivery timelines
* Identify risks early

### Engineering Managers

* Analyze team performance
* Optimize resource allocation
* Improve productivity

### Organizations

* Enhance employee well-being
* Improve operational efficiency
* Enable data-driven leadership

---

## 🔮 Future Enhancements

* Integration with Jira
* Integration with Monday.com
* Integration with Microsoft Teams
* LLM-powered AI Assistant
* Real-time Notifications
* Predictive Workforce Analytics
* Automated Meeting Summaries
* Team Sentiment Analysis

---

## 👩‍💻 Author

**Susan Riona D'Souza**

B.Tech – Information Science Engineering (final year major project 2026-27)

Major Project:
**AI Co-Lead: Intelligent Team Lead Assistant**

---

## 📜 License

This project is developed for academic and research purposes.

