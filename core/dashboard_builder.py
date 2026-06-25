import pandas as pd


def build_dashboard(df):

    dashboard = {}

    # =====================================
    # BASIC INFO
    # =====================================

    dashboard["rows"] = len(df)
    dashboard["columns"] = len(df.columns)

    # =====================================
    # NUMERIC COLUMNS
    # =====================================

    numeric_cols = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    dashboard["numeric_columns"] = numeric_cols

    # =====================================
    # CATEGORY COLUMNS
    # =====================================

    category_cols = list(
        df.select_dtypes(
            exclude="number"
        ).columns
    )

    dashboard["category_columns"] = category_cols

    # =====================================
    # DATE COLUMN
    # =====================================

    date_col = None

    for col in df.columns:

        name = col.lower()

        if (
            "date" in name
            or "time" in name
            or "created" in name
            or "timestamp" in name
        ):

            date_col = col
            break

    dashboard["date_column"] = date_col

    # =====================================
    # KPI CARDS
    # =====================================

    kpis = []

    for col in numeric_cols:

        try:

            kpis.append({

                "Metric": col,

                "Total": round(
                    df[col].sum(),
                    2
                ),

                "Average": round(
                    df[col].mean(),
                    2
                ),

                "Maximum": round(
                    df[col].max(),
                    2
                )

            })

        except:
            pass

    dashboard["kpis"] = pd.DataFrame(kpis)

    # =====================================
    # TOP CATEGORIES
    # =====================================

    summaries = []

    for col in category_cols:

        try:

            value = (
                df[col]
                .value_counts()
                .idxmax()
            )

            count = (
                df[col]
                .value_counts()
                .max()
            )

            summaries.append({

                "Column": col,

                "Top Value": value,

                "Count": count

            })

        except:
            pass

    dashboard["category_summary"] = pd.DataFrame(
        summaries
    )

    return dashboard