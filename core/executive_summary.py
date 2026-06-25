import pandas as pd


def generate_executive_summary(df):

    summary = {}

    # =========================================
    # Dataset Overview
    # =========================================

    summary["rows"] = len(df)
    summary["columns"] = len(df.columns)
    summary["missing"] = int(df.isna().sum().sum())
    summary["duplicates"] = int(df.duplicated().sum())

    # =========================================
    # Numeric KPIs
    # =========================================

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    kpis = []

    for col in numeric_cols[:5]:

        kpis.append({
            "Metric": col,
            "Average": round(df[col].mean(), 2),
            "Maximum": round(df[col].max(), 2),
            "Minimum": round(df[col].min(), 2),
            "Total": round(df[col].sum(), 2)
        })

    summary["kpis"] = pd.DataFrame(kpis)

    # =========================================
    # Category Highlights
    # =========================================

    highlights = []

    category_cols = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    for col in category_cols[:3]:

        try:

            top = df[col].mode()[0]

            count = df[col].value_counts().iloc[0]

            highlights.append(
                f"{top} appears most frequently in '{col}' ({count} records)."
            )

        except:
            pass

    summary["highlights"] = highlights

    # =========================================
    # Risks
    # =========================================

    risks = []

    if summary["missing"] > 0:
        risks.append(
            f"{summary['missing']} missing values detected."
        )

    if summary["duplicates"] > 0:
        risks.append(
            f"{summary['duplicates']} duplicate rows detected."
        )

    if not risks:
        risks.append(
            "No major data quality issues detected."
        )

    summary["risks"] = risks

    # =========================================
    # Recommendations
    # =========================================

    recommendations = []

    if summary["missing"] > 0:
        recommendations.append(
            "Handle missing values before modeling."
        )

    if summary["duplicates"] > 0:
        recommendations.append(
            "Remove duplicate records."
        )

    if not recommendations:
        recommendations.append(
            "Dataset appears ready for analysis."
        )

    summary["recommendations"] = recommendations

    return summary