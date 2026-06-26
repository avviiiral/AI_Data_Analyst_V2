import pandas as pd
import numpy as np


# ==========================================================
# DUPLICATES
# ==========================================================

def remove_duplicates(df):

    cleaned = df.drop_duplicates()

    removed = len(df) - len(cleaned)

    return cleaned, removed


# ==========================================================
# EMPTY COLUMNS
# ==========================================================

def remove_empty_columns(df):

    before = len(df.columns)

    cleaned = df.dropna(axis=1, how="all")

    removed = before - len(cleaned.columns)

    return cleaned, removed


# ==========================================================
# CONSTANT COLUMNS
# ==========================================================

def remove_constant_columns(df):

    constant_cols = [

        col

        for col in df.columns

        if df[col].nunique(dropna=False) <= 1

    ]

    cleaned = df.drop(columns=constant_cols)

    return cleaned, constant_cols


# ==========================================================
# NUMERIC MISSING
# ==========================================================

def fill_numeric_missing(df):

    cleaned = df.copy()

    filled = 0

    numeric = cleaned.select_dtypes(
        include=np.number
    ).columns

    for col in numeric:

        count = cleaned[col].isna().sum()

        if count:

            cleaned[col] = cleaned[col].fillna(
                cleaned[col].median()
            )

            filled += count

    return cleaned, filled


# ==========================================================
# CATEGORICAL MISSING
# ==========================================================

def fill_categorical_missing(df):

    cleaned = df.copy()

    filled = 0

    categorical = cleaned.select_dtypes(
        exclude=np.number
    ).columns

    for col in categorical:

        count = cleaned[col].isna().sum()

        if count:

            if not cleaned[col].mode().empty:

                cleaned[col] = cleaned[col].fillna(
                    cleaned[col].mode()[0]
                )

                filled += count

    return cleaned, filled


# ==========================================================
# DATE CONVERSION
# ==========================================================

def convert_dates(df):

    cleaned = df.copy()

    converted = []

    for col in cleaned.columns:

        if "date" in col.lower():

            try:

                cleaned[col] = pd.to_datetime(

                    cleaned[col],

                    errors="coerce"

                )

                converted.append(col)

            except:

                pass

    return cleaned, converted


# ==========================================================
# OUTLIER REMOVAL
# ==========================================================

def remove_outliers(df):

    cleaned = df.copy()

    removed = 0

    numeric = cleaned.select_dtypes(
        include=np.number
    ).columns

    for col in numeric:

        q1 = cleaned[col].quantile(0.25)

        q3 = cleaned[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        before = len(cleaned)

        cleaned = cleaned[
            (cleaned[col] >= lower)
            &
            (cleaned[col] <= upper)
        ]

        removed += before - len(cleaned)

    return cleaned, removed


# ==========================================================
# RESET
# ==========================================================

def reset_dataset(original_df):

    return original_df.copy()


# ==========================================================
# SUMMARY
# ==========================================================

def cleaning_summary(original_df, cleaned_df):

    return {

        "Rows Before": len(original_df),

        "Rows After": len(cleaned_df),

        "Rows Removed":
            len(original_df) - len(cleaned_df),

        "Columns Before":
            len(original_df.columns),

        "Columns After":
            len(cleaned_df.columns)

    }