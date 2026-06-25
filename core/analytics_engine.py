import pandas as pd

from core.column_matcher import find_best_columns


def driver_analysis(df, query):

    numeric_cols = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    if len(numeric_cols) < 2:
        return None

    matched_cols = find_best_columns(
        df,
        query
    )

    target_col = None

    for col in matched_cols:

        if col in numeric_cols:
            target_col = col
            break

    if target_col is None:
        target_col = numeric_cols[0]

    correlations = {}

    for col in numeric_cols:

        if col != target_col:

            try:

                corr = abs(
                    df[target_col].corr(
                        df[col]
                    )
                )

                correlations[col] = round(
                    corr,
                    3
                )

            except:
                pass

    result_df = (
        pd.DataFrame(
            correlations.items(),
            columns=[
                "Feature",
                "Importance"
            ]
        )
        .sort_values(
            "Importance",
            ascending=False
        )
    )

    return {
        "type": "drivers",
        "title": f"Drivers of {target_col}",
        "data": result_df,
        "target": target_col
    }