# Electricity Consumption Analysis & Prediction System

A data analytics and machine learning application to analyze monthly national electricity demand in India and forecast future demand using Multiple Linear Regression.

---

## Overview

Electricity demand in India shows strong seasonal variations as well as long-term annual growth driven by industrial expansion, electrification, and rising seasonal cooling needs. This project analyzes historical monthly electricity consumption data from 2012 to 2026, evaluates seasonal and yearly demand patterns, and provides an interactive Streamlit interface to forecast monthly electricity demand.

## Features

- **Interactive Dashboard:** View key metrics such as total electricity consumed, monthly average, and all-time high/low demand months alongside the complete historical trend.
- **Trend & Seasonality Analysis:** Break down consumption year-by-year and explore monthly seasonality cycles across the entire 14-year period.
- **Demand Forecasting:** Predict national electricity demand for any given year, month, and prior month's demand using a trained Multiple Linear Regression model.
- **Visual Comparisons:** Instantly compare predictions against historical benchmarks (minimum, average, and peak demand).

---

## Dataset

- **File:** `data/India_monthly_data.csv`
- **Target Variable:** `ELY.DEM.POS.TOT.India` (Total electricity demand met in India)
- **Unit:** Million Units (MU), where $1\text{ MU} = 1\text{ GWh} = 1,000,000\text{ kWh}$
- **Timeline:** Monthly records from April 2012 to September 2026 (174 observations)

A 1-month lag feature (`prev_demand`) is constructed to capture month-to-month persistence without introducing future data leakage, resulting in 173 complete observations.

---

## Methodology

### Features Used
1. `year` - Captures long-term annual growth and electrification trends.
2. `month` - Captures seasonal cyclicality across the year.
3. `prev_demand` - Electricity demand of the preceding month (MU).

### Train / Test Split
To simulate realistic forward-looking forecasting, a **chronological split** (80% train, 20% test) was used:
- **Training Set:** May 2012 – October 2023 (138 months)
- **Testing Set:** November 2023 – September 2026 (35 months)

### Model Performance

| Metric | Training Set | Testing Set |
| :--- | :--- | :--- |
| **R² Score** | **0.8848** | **0.5851** |
| **Mean Absolute Error (MAE)** | **4,505 MU** | **7,235 MU** |
| **Root Mean Squared Error (RMSE)** | **5,897 MU** | **8,545 MU** |

Given that average monthly demand is approximately 110,000 MU, an MAE of ~4,500 to 7,200 MU corresponds to an average prediction error of roughly 4% to 6%.

---

## Project Structure

```text
├── data/
│   └── India_monthly_data.csv       # Historical dataset
├── src/
│   ├── data_preprocessing.py        # Data cleaning and lag feature creation
│   ├── data_analysis.py             # Plotting and summary functions
│   ├── model_training.py            # Train-test split and regression training
│   └── prediction.py                # Model inference function
├── models/
│   └── electricity_model.pkl        # Serialized regression model
├── app/
│   └── app.py                       # Streamlit application
├── requirements.txt                 # Python dependencies
├── .gitignore
└── README.md
```

---

## Setup & Running

### 1. Clone the repository
```bash
git clone https://github.com/CodeVoyager7777/Electricity-Consumption-Analysis-Prediction-System.git
cd Electricity-Consumption-Analysis-Prediction-System
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Retrain the model
```bash
python src/model_training.py
```

### 4. Run the Streamlit web app
```bash
streamlit run app/app.py
```

Once running, navigate to `http://localhost:8501` in your browser.
