import re
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression

from core.column_matcher import find_best_columns


def forecast_metric(df, query):

    # ----------------------------------
    # Find Date Column
    # ----------------------------------

    date_col = None

    for col in df.columns:

        col_lower = col.lower()

        if (
            "date" in col_lower
            or "created" in col_lower
            or "timestamp" in col_lower
        ):
            date_col = col
            break

    if date_col is None:
        return None

    temp_df = df.copy()

    temp_df[date_col] = pd.to_datetime(
        temp_df[date_col],
        errors="coerce"
    )

    temp_df = temp_df.dropna(
        subset=[date_col]
    )

    temp_df["Month"] = (
        temp_df[date_col]
        .dt.to_period("M")
    )

    # ----------------------------------
    # Detect Metric
    # ----------------------------------

    numeric_cols = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    matched_cols = find_best_columns(
        df,
        query
    )

    metric_col = None

    for col in matched_cols:

        if col in numeric_cols:
            metric_col = col
            break

    # ----------------------------------
    # Monthly Aggregation
    # ----------------------------------

    if metric_col is None:

        trend_df = (
            temp_df.groupby("Month")
            .size()
            .reset_index(name="Value")
        )

        metric_name = "Incident Count"

    else:

        trend_df = (
            temp_df.groupby("Month")[metric_col]
            .mean()
            .reset_index(name="Value")
        )

        metric_name = metric_col

    trend_df["Month"] = trend_df["Month"].astype(str)

    # ----------------------------------
    # Train Model
    # ----------------------------------

    X = np.arange(len(trend_df)).reshape(-1, 1)

    y = trend_df["Value"].values

    model = LinearRegression()

    model.fit(X, y)

    # ----------------------------------
    # Months Ahead
    # ----------------------------------

    months_ahead = 1

    match = re.search(
        r"(\d+)\s*month",
        query.lower()
    )

    if match:
        months_ahead = int(match.group(1))

    # ----------------------------------
    # Forecast
    # ----------------------------------

    trend_df["Forecast"] = np.nan

    last_period = pd.Period(
        trend_df.iloc[-1]["Month"],
        freq="M"
    )

    forecast = None

    for i in range(months_ahead):

        future_index = len(trend_df) + i

        prediction = round(
            float(
                model.predict(
                    [[future_index]]
                )[0]
            ),
            2
        )

        forecast = prediction

        future_month = (
            last_period + (i + 1)
        ).strftime("%Y-%m")

        trend_df.loc[len(trend_df)] = {
            "Month": future_month,
            "Value": np.nan,
            "Forecast": prediction
        }

    # ----------------------------------
    # Return
    # ----------------------------------

    return {
        "type": "forecast",
        "title": f"Forecast for {metric_name}",
        "data": trend_df,
        "forecast": forecast,
        "metric": metric_name
    }