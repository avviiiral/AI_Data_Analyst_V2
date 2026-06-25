import pandas as pd

from core.column_matcher import find_best_columns


def generate_trend(df, query):

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
        .astype(str)
    )

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

    # -----------------------------------
    # INCIDENT COUNT TREND
    # -----------------------------------

    if metric_col is None:

        trend_df = (
            temp_df.groupby("Month")
            .size()
            .reset_index(
                name="Count"
            )
        )

        return {
            "type": "trend",
            "title": "Monthly Incident Trend",
            "data": trend_df,
            "metric": "Count"
        }

    # -----------------------------------
    # METRIC TREND
    # -----------------------------------

    trend_df = (
        temp_df.groupby("Month")[metric_col]
        .mean()
        .reset_index()
    )

    return {
        "type": "trend",
        "title": f"Monthly Trend of {metric_col}",
        "data": trend_df,
        "metric": metric_col
    }