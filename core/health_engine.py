import pandas as pd


def dataset_health_score(df):

    rows, cols = df.shape

    total_cells = rows * cols

    missing_count = df.isnull().sum().sum()

    duplicate_count = df.duplicated().sum()

    missing_pct = (
        missing_count / total_cells * 100
        if total_cells > 0
        else 0
    )

    duplicate_pct = (
        duplicate_count / rows * 100
        if rows > 0
        else 0
    )

    score = 100

    score -= min(missing_pct * 2, 40)

    score -= min(duplicate_pct * 2, 20)

    score = max(round(score), 0)

    recommendations = []

    if missing_pct > 0:
        recommendations.append(
            f"Fill or handle {missing_count} missing values."
        )

    if duplicate_count > 0:
        recommendations.append(
            f"Remove {duplicate_count} duplicate rows."
        )

    date_columns = []

    for col in df.columns:

        if (
            "date" in col.lower()
            or "time" in col.lower()
        ):
            date_columns.append(col)

    if date_columns:
        recommendations.append(
            "Validate and standardize date columns."
        )

    if len(recommendations) == 0:
        recommendations.append(
            "Dataset quality looks excellent."
        )

    return {
        "score": score,
        "missing_count": int(missing_count),
        "missing_pct": round(missing_pct, 2),
        "duplicate_count": int(duplicate_count),
        "duplicate_pct": round(duplicate_pct, 2),
        "recommendations": recommendations,
    }