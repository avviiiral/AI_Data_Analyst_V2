import pandas as pd
import numpy as np


def build_dashboard(df):
    """
    Build a dynamic dashboard for ANY dataset.
    """

    dashboard = {}

    # ==========================================================
    # BASIC INFORMATION
    # ==========================================================

    dashboard["rows"] = len(df)
    dashboard["columns"] = len(df.columns)

    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    category_cols = df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    dashboard["numeric_columns"] = numeric_cols
    dashboard["category_columns"] = category_cols

    # ==========================================================
    # DATE COLUMN DETECTION
    # ==========================================================

    date_column = None

    for col in df.columns:

        name = col.lower()

        if (
            "date" in name
            or "time" in name
            or "created" in name
            or "timestamp" in name
        ):

            date_column = col
            break

    dashboard["date_column"] = date_column

    # ==========================================================
    # KPI SUMMARY
    # ==========================================================

    kpis = []

    for col in numeric_cols:

        s = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        kpis.append({

            "Metric": col,

            "Total": round(s.sum(), 2),

            "Average": round(s.mean(), 2),

            "Median": round(s.median(), 2),

            "Minimum": round(s.min(), 2),

            "Maximum": round(s.max(), 2),

            "Std Dev": round(s.std(), 2)

        })

    dashboard["kpis"] = pd.DataFrame(kpis)

    # ==========================================================
    # CATEGORY SUMMARY
    # ==========================================================

    category_summary = []

    for col in category_cols:

        try:

            vc = df[col].value_counts()

            category_summary.append({

                "Column": col,

                "Unique Values": int(df[col].nunique()),

                "Top Value": vc.index[0],

                "Frequency": int(vc.iloc[0])

            })

        except:

            pass

    dashboard["category_summary"] = pd.DataFrame(
        category_summary
    )

    # ==========================================================
    # MISSING VALUES
    # ==========================================================

    missing = pd.DataFrame({

        "Column": df.columns,

        "Missing": df.isna().sum().values,

        "Missing %": (
            df.isna().mean()*100
        ).round(2).values

    })

    dashboard["missing"] = missing

    # ==========================================================
    # CORRELATION
    # ==========================================================

    if len(numeric_cols) >= 2:

        dashboard["correlation"] = (
            df[numeric_cols]
            .corr()
            .round(3)
        )

    else:

        dashboard["correlation"] = None

    # ==========================================================
    # TOP NUMERIC COLUMNS
    # ==========================================================

    top_numeric = []

    for col in numeric_cols:

        top_numeric.append({

            "Metric": col,

            "Total": df[col].sum()

        })

    dashboard["top_numeric"] = (
        pd.DataFrame(top_numeric)
        .sort_values(
            "Total",
            ascending=False
        )
    )

    # ==========================================================
    # TOP CATEGORIES
    # ==========================================================

    top_categories = {}

    for col in category_cols:

        try:

            top_categories[col] = (

                df[col]

                .value_counts()

                .head(10)

                .reset_index()

            )

            top_categories[col].columns = [

                col,

                "Count"

            ]

        except:

            pass

    dashboard["top_categories"] = top_categories

    # ==========================================================
    # DATASET COMPOSITION
    # ==========================================================

    dashboard["composition"] = {

        "numeric": len(numeric_cols),

        "categorical": len(category_cols)

    }

    return dashboard