import pandas as pd

from core.column_matcher import find_best_columns


def root_cause_analysis(df, query):

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

    drivers = []

    for col in numeric_cols:

        if col == target_col:
            continue

        try:

            corr = abs(
                df[target_col].corr(df[col])
            )

            drivers.append(
                {
                    "Feature": col,
                    "Correlation": round(corr, 3)
                }
            )

        except:
            pass

    result_df = (
        pd.DataFrame(drivers)
        .sort_values(
            "Correlation",
            ascending=False
        )
    )

    return {
        "type": "rootcause",
        "title": f"Why Analysis for {target_col}",
        "data": result_df,
        "target": target_col
    }