from sklearn.ensemble import IsolationForest


def detect_anomalies(df):

    numeric_cols = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    if len(numeric_cols) == 0:
        return None

    target_col = numeric_cols[0]

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    temp_df = df.copy()

    temp_df["Anomaly"] = model.fit_predict(
        temp_df[[target_col]]
    )

    anomalies = temp_df[
        temp_df["Anomaly"] == -1
    ]

    return {
        "type": "anomaly",
        "title": f"Anomalies in {target_col}",
        "data": anomalies,
        "column": target_col
    }