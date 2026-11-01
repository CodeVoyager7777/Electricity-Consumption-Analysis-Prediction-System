# Electricity Consumption Analysis & Prediction System

A university mini-project developed for the Predictive Analytics course to analyze historical monthly electricity demand in India and predict future demand using Multiple Linear Regression.

---

## 1. Introduction

Electricity is essential for economic growth, industrial production, and daily life. Understanding historical electricity demand trends helps in understanding how consumption changes over the years and across different months of the year. This project focuses on national-level monthly electricity demand in India from 2012 to 2026.

---

## 2. Problem Statement

Electricity demand fluctuates across seasons due to weather changes and grows year over year as infrastructure expands. Planning power generation and grid supply requires reliable estimates of future demand. The objective of this project is to build an understandable machine learning model using historical data to predict monthly electricity demand based on the year, month, and previous month's demand.

---

## 3. Project Objectives

- Explore and visualize historical electricity demand in India.
- Examine yearly growth trends and monthly seasonal patterns.
- Implement Multiple Linear Regression using Scikit-learn.
- Evaluate the model using standard metrics (R² Score, MAE, RMSE).
- Provide a simple interactive Streamlit dashboard for users to explore trends and make predictions.

---

## 4. Dataset Information and Source

- **Dataset File:** `data/India_monthly_data.csv`
- **Scope:** National-level Indian monthly energy statistics.
- **Target Variable:** `ELY.DEM.POS.TOT.India` (Total electricity demand met across India).
- **Unit of Measurement:** Million Units (MU), where $1\text{ MU} = 1\text{ GWh} = 1,000,000\text{ kWh}$.
- **Observations:** 174 recorded monthly values between April 2012 and September 2026.
- **Lag Feature:** Using a 1-month lag (`prev_demand`), 173 complete observations are used for modeling.

*Note: This dataset represents national grid-level electricity demand and does not contain household, commercial, or state-level breakdowns.*

---

## 5. Technologies Used

- **Python 3.10+** - Programming language
- **Pandas** - Data manipulation and cleaning
- **NumPy** - Numerical operations
- **Scikit-learn** - Multiple Linear Regression modeling and evaluation
- **Matplotlib** - Data visualization
- **Streamlit** - Interactive web interface
- **Joblib** - Model saving and loading

---

## 6. Machine Learning Approach

### Input Features:
1. `year` (Calendar year)
2. `month` (Calendar month from 1 to 12)
3. `prev_demand` (Electricity demand of the immediately preceding month in MU)

### Target:
- `demand` (Electricity demand of the current month in MU)

### Train-Test Split:
A **chronological split** is used (80% training, 20% testing):
- **Training Set:** 138 monthly observations (May 2012 to October 2023)
- **Testing Set:** 35 monthly observations (November 2023 to September 2026)

Using a chronological split ensures that older data is used to predict newer data, reflecting realistic forecasting without data leakage.

---

## 7. How the Model Works

The Multiple Linear Regression model learns the relationship between the target variable and the input features using Ordinary Least Squares:

$$\text{Demand} = \beta_0 + (\beta_1 \times \text{Year}) + (\beta_2 \times \text{Month}) + (\beta_3 \times \text{Previous Demand})$$

### Learned Parameters:
- **Year Coefficient:** $+1891.64$ (Captures the national annual growth in electricity consumption)
- **Month Coefficient:** $-76.68$
- **Previous Month Demand Coefficient:** $+0.61$ (Reflects month-to-month demand continuity)
- **Intercept:** $-3,775,476.49$

---

## 8. Model Evaluation Results

| Metric | Training Set (2012–2023) | Testing Set (2023–2026) |
| :--- | :--- | :--- |
| **R² Score** | **0.8848** | **0.5851** |
| **Mean Absolute Error (MAE)** | **4,505.04 MU** | **7,234.99 MU** |
| **Root Mean Squared Error (RMSE)** | **5,897.25 MU** | **8,545.25 MU** |

With average national demand hovering around 110,000 MU, an MAE of ~4,500 to 7,200 MU represents an average prediction deviation of roughly 4% to 6%.

---

## 9. Project Structure

```text
Electricity-Consumption-Analysis-Prediction-System/
├── data/
│   └── India_monthly_data.csv       # Original dataset
├── src/
│   ├── data_preprocessing.py        # Cleans data and creates lag feature
│   ├── data_analysis.py             # Summary metrics and plotting functions
│   ├── model_training.py            # Chronological split and MLR training
│   └── prediction.py                # Prediction helper function
├── models/
│   └── electricity_model.pkl        # Saved trained model
├── app/
│   └── app.py                       # Streamlit web application
├── requirements.txt                 # Dependencies
├── .gitignore
└── README.md                        # Documentation
```

---

## 10. Installation Instructions

1. Clone or download the repository:
   ```bash
   git clone https://github.com/CodeVoyager7777/Electricity-Consumption-Analysis-Prediction-System.git
   cd Electricity-Consumption-Analysis-Prediction-System
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## 11. How to Run the Application

### 1. Train the Model (already trained and saved):
```bash
python src/model_training.py
```

### 2. Launch the Streamlit App:
```bash
streamlit run app/app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 12. Screenshots

### 1. Overview Dashboard
Displays summary cards (Total Demand, Average Monthly Demand, Highest and Lowest Recorded Demand) alongside the full 2012–2026 historical demand trendline.

### 2. Data Analysis
Provides year-wise average demand comparisons, monthly seasonality patterns across all years, and a scatter plot of current month demand versus previous month demand.

### 3. Demand Prediction
Allows the user to input a Year, select a Month, and provide the previous month's demand to generate an instant prediction in Million Units (MU) with a visual historical comparison chart.

---

## 13. Limitations

1. **National-Level Aggregation:** The model predicts total electricity demand for India as a whole. It cannot forecast demand for individual states, cities, or households.
2. **Linear Assumptions:** Multiple Linear Regression assumes linear relationships and may not capture sudden non-linear economic disruptions or extreme weather events.
3. **Excluded External Factors:** Variables such as fuel prices, industrial tariffs, and extreme weather events are not included in this simple model.
4. **Academic Disclaimer:** Predictions are model-based statistical estimates intended for academic coursework and are not official government or grid dispatch forecasts.
