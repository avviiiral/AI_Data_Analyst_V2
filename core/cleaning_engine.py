import pandas as pd
import numpy as np


# ==========================================================
# OUTLIER DETECTION
# ==========================================================

def detect_outliers(series):

    series = pd.to_numeric(
        series,
        errors="coerce"
    ).dropna()

    if len(series) == 0:
        return 0

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return int(
        ((series < lower) | (series > upper)).sum()
    )


# ==========================================================
# DATA TYPE DETECTION
# ==========================================================

def detect_wrong_types(df):

    issues = []

    for col in df.columns:

        if df[col].dtype == object:

            try:

                pd.to_datetime(df[col])

                issues.append({

                    "Column": col,

                    "Issue": "Date stored as Text",

                    "Suggestion": "Convert to Datetime"

                })

            except:

                pass

    return pd.DataFrame(issues)


# ==========================================================
# HIGH CORRELATION
# ==========================================================

def detect_high_correlation(df):

    numeric = df.select_dtypes(
        include=np.number
    )

    if numeric.shape[1] < 2:

        return pd.DataFrame()

    corr = numeric.corr().abs()

    pairs = []

    cols = corr.columns

    for i in range(len(cols)):

        for j in range(i + 1, len(cols)):

            value = corr.iloc[i, j]

            if value >= 0.90:

                pairs.append({

                    "Column 1": cols[i],

                    "Column 2": cols[j],

                    "Correlation": round(value, 3)

                })

    return pd.DataFrame(pairs)


# ==========================================================
# MAIN ENGINE
# ==========================================================

def analyze_cleaning(df):

    report = {}

    # ------------------------------------------------------

    report["rows"] = len(df)

    report["columns"] = len(df.columns)

    report["duplicates"] = int(
        df.duplicated().sum()
    )

    # ------------------------------------------------------

    missing = pd.DataFrame({

        "Column": df.columns,

        "Missing": df.isna().sum().values,

        "Missing %": (
            df.isna().mean() * 100
        ).round(2).values

    })

    report["missing"] = missing

    # ------------------------------------------------------

    empty_columns = [

        col

        for col in df.columns

        if df[col].isna().all()

    ]

    report["empty_columns"] = empty_columns

    # ------------------------------------------------------

    constant_columns = [

        col

        for col in df.columns

        if df[col].nunique(dropna=False) == 1

    ]

    report["constant_columns"] = constant_columns

    # ------------------------------------------------------

    numeric = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    report["numeric_columns"] = numeric

    categorical = df.select_dtypes(
        exclude=np.number
    ).columns.tolist()

    report["categorical_columns"] = categorical

    # ------------------------------------------------------

    outliers = []

    for col in numeric:

        count = detect_outliers(df[col])

        outliers.append({

            "Column": col,

            "Outliers": count

        })

    report["outliers"] = pd.DataFrame(outliers)

    # ------------------------------------------------------

    report["type_issues"] = detect_wrong_types(df)

    report["high_correlation"] = detect_high_correlation(df)

    return report