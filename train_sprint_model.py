import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df = pd.read_csv("AI_CoLead_5000_Dataset.csv")

X = df[
    [
        "Tasks_Assigned",
        "Tasks_Completed",
        "Overdue_Tasks",
        "Meeting_Hours"
    ]
]

y = df["Sprint_Risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

joblib.dump(
    model,
    "models/sprint_model.pkl"
)

print("✅ sprint_model.pkl created")