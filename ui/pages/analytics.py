import streamlit as st
import pandas as pd

from core.health_engine import dataset_health_score
from core.statistics_engine import dataset_statistics


def render_analytics(df):
    """
    Analytics Page
    """

    st.header("📊 Analytics")

    # ==========================================
    # DATASET HEALTH
    # ==========================================

    health = dataset_health_score(df)

    st.subheader("Dataset Health")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Health Score",
        f"{health['score']}/100"
    )

    c2.metric(
        "Missing Values",
        health["missing_count"]
    )

    c3.metric(
        "Duplicate Rows",
        health["duplicate_count"]
    )

    with st.expander("Health Details", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Missing %",
                health["missing_pct"]
            )

            st.metric(
                "Duplicates %",
                health["duplicate_pct"]
            )

        with col2:

            st.markdown("### Recommendations")

            for rec in health["recommendations"]:
                st.success(rec)

    st.divider()

    # ==========================================
    # DATASET STATISTICS
    # ==========================================

    stats = dataset_statistics(df)

    st.subheader("Dataset Statistics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows",
        stats["rows"]
    )

    c2.metric(
        "Columns",
        stats["columns"]
    )

    c3.metric(
        "Numeric",
        len(stats["numeric_columns"])
    )

    c4.metric(
        "Categorical",
        len(stats["categorical_columns"])
    )

    st.divider()

    # ==========================================
    # NUMERIC STATISTICS
    # ==========================================

    st.subheader("Numeric Statistics")

    if stats["numeric_stats"]:

        selected_column = st.selectbox(
            "Select Numeric Column",
            stats["numeric_columns"]
        )

        column_stats = stats["numeric_stats"][selected_column]

        left, right = st.columns(2)

        with left:

            st.metric(
                "Mean",
                column_stats["Mean"]
            )

            st.metric(
                "Median",
                column_stats["Median"]
            )

            st.metric(
                "Mode",
                column_stats["Mode"]
            )

            st.metric(
                "Std Dev",
                column_stats["Std Dev"]
            )

            st.metric(
                "Variance",
                column_stats["Variance"]
            )

            st.metric(
                "Range",
                column_stats["Range"]
            )

        with right:

            st.metric(
                "Minimum",
                column_stats["Minimum"]
            )

            st.metric(
                "Maximum",
                column_stats["Maximum"]
            )

            st.metric(
                "Q1",
                column_stats["Q1"]
            )

            st.metric(
                "Q2",
                column_stats["Q2"]
            )

            st.metric(
                "Q3",
                column_stats["Q3"]
            )

            st.metric(
                "IQR",
                column_stats["IQR"]
            )

        st.divider()

        st.subheader("Distribution Statistics")

        d1, d2, d3 = st.columns(3)

        d1.metric(
            "Skewness",
            column_stats["Skewness"]
        )

        d2.metric(
            "Kurtosis",
            column_stats["Kurtosis"]
        )

        d3.metric(
            "Outliers",
            column_stats["Outliers"]
        )

    else:

        st.info("No numeric columns detected.")

    st.divider()
    
    # ==========================================
    # CATEGORICAL STATISTICS
    # ==========================================

    st.subheader("Categorical Statistics")

    if stats["categorical_stats"]:

        category = st.selectbox(
            "Select Categorical Column",
            list(stats["categorical_stats"].keys())
        )

        cat = stats["categorical_stats"][category]

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Unique Values",
                cat["Unique Values"]
            )

            st.metric(
                "Top Category",
                cat["Top Category"]
            )

        with c2:

            st.metric(
                "Top Frequency",
                cat["Top Frequency"]
            )

            st.metric(
                "Missing",
                cat["Missing"]
            )

    else:

        st.info("No categorical columns found.")

    st.divider()

    # ==========================================
    # MISSING VALUE SUMMARY
    # ==========================================

    st.subheader("Missing Value Summary")

    missing_df = stats["missing"]

    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================
    # CORRELATION MATRIX
    # ==========================================

    st.subheader("Correlation Matrix")

    if stats["correlation"] is not None:

        st.dataframe(
            stats["correlation"],
            use_container_width=True
        )

    else:

        st.info(
            "Correlation requires at least two numeric columns."
        )

    st.divider()

    # ==========================================
    # DATASET COMPOSITION
    # ==========================================

    st.subheader("Dataset Composition")

    composition = pd.DataFrame(
        {
            "Type": [
                "Numeric Columns",
                "Categorical Columns"
            ],
            "Count": [
                len(stats["numeric_columns"]),
                len(stats["categorical_columns"])
            ]
        }
    )

    st.dataframe(
        composition,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================
    # ANALYTICS SUMMARY
    # ==========================================

    st.subheader("Analytics Summary")

    total_missing = int(
        missing_df["Missing"].sum()
    )

    total_outliers = 0

    for column in stats["numeric_stats"].values():

        total_outliers += column["Outliers"]

    insights = []

    if total_missing == 0:
        insights.append(
            "✅ No missing values detected."
        )
    else:
        insights.append(
            f"⚠ {total_missing} missing values detected."
        )

    if total_outliers == 0:
        insights.append(
            "✅ No outliers detected."
        )
    else:
        insights.append(
            f"⚠ {total_outliers} potential outliers detected."
        )

    if stats["correlation"] is not None:

        corr = stats["correlation"].abs()

        strong = []

        cols = corr.columns

        for i in range(len(cols)):

            for j in range(i + 1, len(cols)):

                value = corr.iloc[i, j]

                if value >= 0.70:

                    strong.append(
                        (
                            cols[i],
                            cols[j],
                            round(value, 3)
                        )
                    )

        if strong:

            insights.append(
                f"📈 {len(strong)} strong correlations found."
            )

        else:

            insights.append(
                "No strong correlations detected."
            )

    for item in insights:

        st.success(item)

    st.divider()

    # ==========================================
    # AI RECOMMENDATIONS
    # ==========================================

    st.subheader("Recommendations")

    recommendations = []

    if total_missing > 0:

        recommendations.append(
            "Handle missing values before modeling."
        )

    if total_outliers > 0:

        recommendations.append(
            "Investigate detected outliers."
        )

    if len(stats["numeric_columns"]) < 2:

        recommendations.append(
            "Add more numeric columns for richer statistical analysis."
        )

    if not recommendations:

        recommendations.append(
            "Dataset is statistically healthy and ready for advanced analytics."
        )

    for rec in recommendations:

        st.info(rec)