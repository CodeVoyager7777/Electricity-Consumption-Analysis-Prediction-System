import pandas as pd


def load_and_preprocess_data(filepath="data/India_monthly_data.csv"):
    df = pd.read_csv(filepath)
    target_col = "ELY.DEM.POS.TOT.India"

    data = df[df[target_col].notnull()][["yyyymm", target_col]].copy()
    data = data.sort_values("yyyymm").reset_index(drop=True)

    data["date"] = pd.to_datetime(data["yyyymm"].astype(str), format="%Y%m")
    data["year"] = data["date"].dt.year
    data["month"] = data["date"].dt.month
    data["demand"] = data[target_col]
    data["prev_demand"] = data["demand"].shift(1)

    clean_data = data.dropna(subset=["prev_demand"]).reset_index(drop=True)
    return clean_data[["date", "year", "month", "prev_demand", "demand"]]


if __name__ == "__main__":
    df = load_and_preprocess_data()
    print("Preprocessed rows:", len(df))
    print(df.head())
