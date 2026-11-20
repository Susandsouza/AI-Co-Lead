import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("AI_CoLead_5000_Dataset.csv")

# Features
X = df[
    [
        "Tasks_Assigned",
        "Working_Hours",
        "Meeting_Hours",
        "Stress_Level",
        "Overdue_Tasks"
    ]
]

# Target
y = df["Burnout_Risk"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Save model
joblib.dump(
    model,
    "models/burnout_model.pkl"
)

print("Burnout model saved successfully.")