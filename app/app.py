import os
import sys
import streamlit as st
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.data_preprocessing import load_and_preprocess_data
from src.data_analysis import (
    get_summary_metrics,
    plot_historical_trend,
    plot_yearly_comparison,
    plot_monthly_seasonality,
    plot_actual_vs_lag
)
from src.prediction import load_model, predict_demand

st.set_page_config(
    page_title="Electricity Consumption Analysis & Prediction System",
    page_icon="⚡",
    layout="wide"
)


@st.cache_data
def get_data():
    return load_and_preprocess_data("data/India_monthly_data.csv")


@st.cache_resource
def get_model():
    return load_model("models/electricity_model.pkl")


def main():
    st.title("⚡ Electricity Consumption Analysis & Prediction System")
    st.write("An analysis and prediction project for monthly national electricity demand in India.")

    df = get_data()
    model_payload = get_model()
    metrics = get_summary_metrics(df)

    tab_dash, tab_analysis, tab_pred = st.tabs(["Dashboard", "Data Analysis", "Demand Prediction"])

    with tab_dash:
        st.subheader("National Electricity Demand Overview")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Demand", f"{metrics['total_demand']:,} MU")
        col2.metric("Average Monthly Demand", f"{metrics['avg_demand']:,} MU")
        col3.metric("Highest Demand Month", f"{metrics['max_demand']:,} MU", metrics['max_date'])
        col4.metric("Lowest Demand Month", f"{metrics['min_demand']:,} MU", metrics['min_date'])

        st.markdown("### Historical Demand Trend")
        fig_trend = plot_historical_trend(df)
        st.pyplot(fig_trend)

        st.info("Unit Note: Electricity demand is reported in MU (Million Units), where 1 MU = 1 GWh = 1,000,000 kWh.")

    with tab_analysis:
        st.subheader("Historical Demand Patterns")

        col_left, col_right = st.columns(2)

        with col_left:
            st.markdown("#### Year-wise Comparison")
            fig_year = plot_yearly_comparison(df)
            st.pyplot(fig_year)

        with col_right:
            st.markdown("#### Monthly Seasonal Pattern")
            fig_season = plot_monthly_seasonality(df)
            st.pyplot(fig_season)

        st.markdown("---")
        st.markdown("#### Actual Demand vs Previous Month Demand")
        fig_lag = plot_actual_vs_lag(df)
        st.pyplot(fig_lag)

    with tab_pred:
        st.subheader("Monthly Demand Prediction")
        st.write("Predict national electricity demand using Multiple Linear Regression.")

        col_in1, col_in2, col_in3 = st.columns(3)

        with col_in1:
            input_year = st.number_input("Year", min_value=2012, max_value=2035, value=2026, step=1)

        with col_in2:
            month_names = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            selected_month_name = st.selectbox("Month", options=month_names, index=9)
            input_month = month_names.index(selected_month_name) + 1

        with col_in3:
            latest_prev = float(df["demand"].iloc[-1])
            input_prev_demand = st.number_input(
                "Previous Month's Electricity Demand (MU)",
                min_value=50000.0,
                max_value=250000.0,
                value=round(latest_prev, 2),
                step=500.0
            )

        if st.button("Predict Electricity Demand", type="primary"):
            prediction = predict_demand(input_year, input_month, input_prev_demand, model_payload)

            st.success(f"### Predicted Electricity Demand: **{prediction:,.2f} MU**")

            comp_col1, comp_col2, comp_col3 = st.columns(3)
            comp_col1.metric("Predicted Demand", f"{prediction:,.2f} MU")
            comp_col2.metric("Historical Average", f"{metrics['avg_demand']:,} MU")
            diff = prediction - metrics['avg_demand']
            comp_col3.metric("Difference from Average", f"{diff:+,.2f} MU")

            fig_comp, ax_comp = plt.subplots(figsize=(8, 3.5))
            bars = ax_comp.bar(
                ["Historical Min", "Historical Average", "Predicted Demand", "Historical Max"],
                [metrics["min_demand"], metrics["avg_demand"], prediction, metrics["max_demand"]],
                color=["#7f7f7f", "#1f77b4", "#2ca02c", "#d62728"]
            )
            ax_comp.set_ylabel("Demand (MU)")
            ax_comp.set_title("Predicted Demand Compared to Historical Range")
            ax_comp.grid(axis="y", linestyle="--", alpha=0.6)
            for bar in bars:
                height = bar.get_height()
                ax_comp.annotate(f"{height:,.0f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                                 xytext=(0, 3), textcoords="offset points", ha="center", fontsize=9)
            fig_comp.tight_layout()
            st.pyplot(fig_comp)

            st.caption("Note: This is a model-based estimate using Multiple Linear Regression, not an official government electricity forecast.")


if __name__ == "__main__":
    main()
