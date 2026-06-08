import joblib

burnout_model = joblib.load(
    "models/burnout_model.pkl"
)

sprint_model = joblib.load(
    "models/sprint_model.pkl"
)