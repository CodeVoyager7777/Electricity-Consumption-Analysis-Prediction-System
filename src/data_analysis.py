import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def get_summary_metrics(df):
    total_demand = df["demand"].sum()
    avg_demand = df["demand"].mean()
    max_row = df.loc[df["demand"].idxmax()]
    min_row = df.loc[df["demand"].idxmin()]

    return {
        "total_demand": round(total_demand, 2),
        "avg_demand": round(avg_demand, 2),
        "max_demand": round(max_row["demand"], 2),
        "max_date": max_row["date"].strftime("%B %Y"),
        "min_demand": round(min_row["demand"], 2),
        "min_date": min_row["date"].strftime("%B %Y")
    }


def plot_historical_trend(df):
    fig, ax = plt.subplots(figsize=(10, 4.5), facecolor="white")
    ax.set_facecolor("white")
    ax.plot(df["date"], df["demand"], color="#1f77b4", linewidth=2, label="Monthly Demand")
    ax.set_title("India Monthly Electricity Demand (2012 - 2026)", fontsize=12, pad=10)
    ax.set_xlabel("Date", fontsize=10)
    ax.set_ylabel("Electricity Demand (MU)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    fig.tight_layout()
    return fig


def plot_yearly_comparison(df):
    yearly = df.groupby("year")["demand"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor="white")
    ax.set_facecolor("white")
    ax.bar(yearly["year"], yearly["demand"], color="#2ca02c", edgecolor="black", alpha=0.8)
    ax.set_title("Average Monthly Electricity Demand by Year", fontsize=12, pad=10)
    ax.set_xlabel("Year", fontsize=10)
    ax.set_ylabel("Average Demand (MU)", fontsize=10)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig


def plot_monthly_seasonality(df):
    monthly = df.groupby("month")["demand"].mean().reset_index()
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly["month_name"] = [month_names[m - 1] for m in monthly["month"]]

    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor="white")
    ax.set_facecolor("white")
    ax.plot(monthly["month_name"], monthly["demand"], marker="o", color="#ff7f0e", linewidth=2)
    ax.set_title("Seasonal Monthly Demand Pattern across All Years", fontsize=12, pad=10)
    ax.set_xlabel("Month", fontsize=10)
    ax.set_ylabel("Average Demand (MU)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig


def plot_actual_vs_lag(df):
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor="white")
    ax.set_facecolor("white")
    ax.scatter(df["prev_demand"], df["demand"], color="#9467bd", alpha=0.6, edgecolors="none")
    ax.set_title("Current Month Demand vs Previous Month Demand", fontsize=12, pad=10)
    ax.set_xlabel("Previous Month Demand (MU)", fontsize=10)
    ax.set_ylabel("Current Month Demand (MU)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    fig.tight_layout()
    return fig
