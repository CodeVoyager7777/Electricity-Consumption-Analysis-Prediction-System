import os
import joblib
import pandas as pd


def load_model(model_path="models/electricity_model.pkl"):
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file not found. Please train the model first.")
    return joblib.load(model_path)


def predict_demand(year, month, prev_demand, model_payload=None):
    if model_payload is None:
        model_payload = load_model()

    model = model_payload["model"]
    features = model_payload["features"]

    input_data = pd.DataFrame([{
        "year": int(year),
        "month": int(month),
        "prev_demand": float(prev_demand)
    }])[features]

    pred_value = model.predict(input_data)[0]
    return round(float(pred_value), 2)


if __name__ == "__main__":
    result = predict_demand(2026, 10, 162191.11)
    print("Predicted Demand:", result, "MU")
