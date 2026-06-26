import pandas as pd
import numpy as np


def detect_outliers(series):
    """
    Detect outliers using IQR.
    """

    series = pd.to_numeric(series, errors="coerce").dropna()

    if len(series) == 0:
        return 0

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return ((series < lower) | (series > upper)).sum()


def analyze_numeric_column(series):
    """
    Statistical analysis for a single numeric column.
    """

    s = pd.to_numeric(series, errors="coerce").dropna()

    if len(s) == 0:
        return None

    q1 = s.quantile(0.25)
    median = s.quantile(0.50)
    q3 = s.quantile(0.75)

    iqr = q3 - q1

    stats = {
        "Count": int(s.count()),
        "Missing": int(series.isna().sum()),
        "Mean": round(s.mean(), 3),
        "Median": round(s.median(), 3),
        "Mode": round(s.mode().iloc[0], 3) if not s.mode().empty else None,
        "Std Dev": round(s.std(), 3),
        "Variance": round(s.var(), 3),
        "Minimum": round(s.min(), 3),
        "Maximum": round(s.max(), 3),
        "Range": round(s.max() - s.min(), 3),
        "Q1": round(q1, 3),
        "Q2": round(median, 3),
        "Q3": round(q3, 3),
        "IQR": round(iqr, 3),
        "Skewness": round(s.skew(), 3),
        "Kurtosis": round(s.kurt(), 3),
        "Outliers": int(detect_outliers(s))
    }

    return stats


def analyze_categorical_column(series):
    """
    Analysis for categorical columns.
    """

    value_counts = series.value_counts(dropna=False)

    top_value = None
    top_count = 0

    if len(value_counts):

        top_value = str(value_counts.index[0])
        top_count = int(value_counts.iloc[0])

    return {
        "Count": int(series.count()),
        "Missing": int(series.isna().sum()),
        "Unique Values": int(series.nunique(dropna=True)),
        "Top Category": top_value,
        "Top Frequency": top_count
    }


def correlation_summary(df):
    """
    Correlation matrix.
    """

    numeric = df.select_dtypes(include=np.number)

    if numeric.shape[1] < 2:
        return None

    return numeric.corr().round(3)


def missing_summary(df):
    """
    Missing values.
    """

    return pd.DataFrame({
        "Column": df.columns,
        "Missing": df.isna().sum().values,
        "Missing %": (
            df.isna().mean() * 100
        ).round(2).values
    })


def dataset_statistics(df):
    """
    Complete dataset statistics.
    """

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    numeric_stats = {}

    for col in numeric_cols:
        numeric_stats[col] = analyze_numeric_column(df[col])

    categorical_stats = {}

    for col in categorical_cols:
        categorical_stats[col] = analyze_categorical_column(df[col])

    return {

        "rows": len(df),

        "columns": len(df.columns),

        "numeric_columns": numeric_cols,

        "categorical_columns": categorical_cols,

        "numeric_stats": numeric_stats,

        "categorical_stats": categorical_stats,

        "correlation": correlation_summary(df),

        "missing": missing_summary(df)
    }