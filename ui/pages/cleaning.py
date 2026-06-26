import streamlit as st

from core.cleaning_engine import analyze_cleaning
from core.session_manager import (
    initialize_session,
    get_cleaned_df,
    get_original_df,
    get_history,
    session_summary,
    reset_dataset
)

from core.cleaning_pipeline import (
    run_remove_duplicates,
    run_remove_empty_columns,
    run_remove_constant_columns,
    run_fill_numeric,
    run_fill_categorical,
    run_convert_dates,
    run_remove_outliers,
    run_auto_clean
)


def render_cleaning(df):

    initialize_session(df)

    st.header("🧹 AI Data Preparation Studio")

    cleaned_df = get_cleaned_df()

    report = analyze_cleaning(cleaned_df)

    # =====================================================
    # BEFORE / AFTER
    # =====================================================

    summary = session_summary()

    st.subheader("Dataset Comparison")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows",
        summary["Rows After"],
        delta=summary["Rows After"] - summary["Rows Before"]
    )

    c2.metric(
        "Columns",
        summary["Columns After"],
        delta=summary["Columns After"] - summary["Columns Before"]
    )

    c3.metric(
        "Duplicates",
        report["duplicates"]
    )

    st.divider()

    # =====================================================
    # CLEANING PIPELINE
    # =====================================================

    st.subheader("Cleaning Pipeline")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Remove Duplicates",
            use_container_width=True
        ):

            removed = run_remove_duplicates()

            st.success(
                f"Removed {removed} duplicate rows."
            )

            st.rerun()

        if st.button(
            "Fill Numeric Missing",
            use_container_width=True
        ):

            filled = run_fill_numeric()

            st.success(
                f"Filled {filled} numeric values."
            )

            st.rerun()

        if st.button(
            "Remove Empty Columns",
            use_container_width=True
        ):

            removed = run_remove_empty_columns()

            st.success(
                f"Removed {removed} empty columns."
            )

            st.rerun()

        if st.button(
            "Convert Dates",
            use_container_width=True
        ):

            cols = run_convert_dates()

            st.success(
                f"Converted {len(cols)} date columns."
            )

            st.rerun()

    with col2:

        if st.button(
            "Fill Categorical Missing",
            use_container_width=True
        ):

            filled = run_fill_categorical()

            st.success(
                f"Filled {filled} categorical values."
            )

            st.rerun()

        if st.button(
            "Remove Constant Columns",
            use_container_width=True
        ):

            cols = run_remove_constant_columns()

            st.success(
                f"Removed {len(cols)} constant columns."
            )

            st.rerun()

        if st.button(
            "Remove Outliers",
            use_container_width=True
        ):

            removed = run_remove_outliers()

            st.success(
                f"Removed {removed} outlier rows."
            )

            st.rerun()

        if st.button(
            "🚀 Auto Clean",
            type="primary",
            use_container_width=True
        ):

            run_auto_clean()

            st.success(
                "Automatic cleaning completed."
            )

            st.rerun()

    st.divider()

    # =====================================================
    # CLEANING HISTORY
    # =====================================================

    st.subheader("Cleaning History")

    history = get_history()

    if history:

        for item in history:

            st.success(item)

    else:

        st.info(
            "No cleaning actions performed."
        )

    st.divider()

    # =====================================================
    # DATA QUALITY REPORT
    # =====================================================

    st.subheader("Current Dataset Quality")

    st.dataframe(
        report["missing"],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    st.subheader("Outlier Report")

    st.dataframe(
        report["outliers"],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================================
    # PREVIEW
    # =====================================================

    st.subheader("Current Dataset")

    st.dataframe(
        cleaned_df.head(25),
        use_container_width=True,
        height=350
    )

    st.divider()

    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.download_button(
        "📥 Download Clean Dataset",
        cleaned_df.to_csv(index=False).encode("utf-8"),
        file_name="clean_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.divider()

    # =====================================================
    # RESET
    # =====================================================

    if st.button(
        "🔄 Reset Dataset",
        use_container_width=True
    ):

        reset_dataset()

        st.success(
            "Dataset restored."
        )

        st.rerun()