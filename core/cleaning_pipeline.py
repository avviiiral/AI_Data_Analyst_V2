from core.cleaning_actions import (
    remove_duplicates,
    remove_empty_columns,
    remove_constant_columns,
    fill_numeric_missing,
    fill_categorical_missing,
    convert_dates,
    remove_outliers
)

from core.session_manager import (
    get_cleaned_df,
    update_dataset
)


# ==========================================================
# DUPLICATES
# ==========================================================

def run_remove_duplicates():

    df = get_cleaned_df()

    cleaned, removed = remove_duplicates(df)

    update_dataset(
        cleaned,
        f"Removed {removed} duplicate rows"
    )

    return removed


# ==========================================================
# EMPTY COLUMNS
# ==========================================================

def run_remove_empty_columns():

    df = get_cleaned_df()

    cleaned, removed = remove_empty_columns(df)

    update_dataset(
        cleaned,
        f"Removed {removed} empty columns"
    )

    return removed


# ==========================================================
# CONSTANT COLUMNS
# ==========================================================

def run_remove_constant_columns():

    df = get_cleaned_df()

    cleaned, cols = remove_constant_columns(df)

    update_dataset(
        cleaned,
        f"Removed {len(cols)} constant columns"
    )

    return cols


# ==========================================================
# NUMERIC MISSING
# ==========================================================

def run_fill_numeric():

    df = get_cleaned_df()

    cleaned, filled = fill_numeric_missing(df)

    update_dataset(
        cleaned,
        f"Filled {filled} numeric missing values"
    )

    return filled


# ==========================================================
# CATEGORICAL MISSING
# ==========================================================

def run_fill_categorical():

    df = get_cleaned_df()

    cleaned, filled = fill_categorical_missing(df)

    update_dataset(
        cleaned,
        f"Filled {filled} categorical missing values"
    )

    return filled


# ==========================================================
# DATE CONVERSION
# ==========================================================

def run_convert_dates():

    df = get_cleaned_df()

    cleaned, cols = convert_dates(df)

    update_dataset(
        cleaned,
        f"Converted {len(cols)} date columns"
    )

    return cols


# ==========================================================
# OUTLIERS
# ==========================================================

def run_remove_outliers():

    df = get_cleaned_df()

    cleaned, removed = remove_outliers(df)

    update_dataset(
        cleaned,
        f"Removed {removed} outlier rows"
    )

    return removed


# ==========================================================
# AUTO CLEAN
# ==========================================================

def run_auto_clean():

    summary = {}

    summary["duplicates"] = run_remove_duplicates()

    summary["empty_columns"] = run_remove_empty_columns()

    summary["constant_columns"] = run_remove_constant_columns()

    summary["numeric_missing"] = run_fill_numeric()

    summary["categorical_missing"] = run_fill_categorical()

    summary["dates"] = run_convert_dates()

    summary["outliers"] = run_remove_outliers()

    return summary