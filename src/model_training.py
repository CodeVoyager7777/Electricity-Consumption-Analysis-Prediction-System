import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error
from src.data_preprocessing import load_and_preprocess_data


def train_and_save_model(data_path="data/India_monthly_data.csv", model_path="models/electricity_model.pkl"):
    df = load_and_preprocess_data(data_path)

    features = ["year", "month", "prev_demand"]
    target = "demand"

    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)

    train_metrics = {
        "r2": round(float(r2_score(y_train, y_pred_train)), 4),
        "mae": round(float(mean_absolute_error(y_train, y_pred_train)), 2),
        "rmse": round(float(root_mean_squared_error(y_train, y_pred_train)), 2)
    }

    test_metrics = {
        "r2": round(float(r2_score(y_test, y_pred_test)), 4),
        "mae": round(float(mean_absolute_error(y_test, y_pred_test)), 2),
        "rmse": round(float(root_mean_squared_error(y_test, y_pred_test)), 2)
    }

    test_results = test_df[["date", "demand"]].copy()
    test_results["predicted"] = y_pred_test.round(2)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model_payload = {
        "model": model,
        "features": features,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "coefficients": {f: round(float(c), 4) for f, c in zip(features, model.coef_)},
        "intercept": round(float(model.intercept_), 4),
        "test_results": test_results
    }
    joblib.dump(model_payload, model_path)

    print("Training finished.")
    print("Train Metrics:", train_metrics)
    print("Test Metrics:", test_metrics)
    return model_payload


if __name__ == "__main__":
    train_and_save_model()
