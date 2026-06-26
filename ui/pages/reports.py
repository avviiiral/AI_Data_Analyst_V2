import streamlit as st
import pandas as pd

from core.executive_summary import generate_executive_summary


def render_reports(df):

    st.header("📄 Executive Report")

    summary = generate_executive_summary(df)

    # ======================================================
    # DATASET OVERVIEW
    # ======================================================

    st.subheader("Dataset Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Rows",
        summary["rows"]
    )

    c2.metric(
        "Columns",
        summary["columns"]
    )

    c3.metric(
        "Missing",
        summary["missing"]
    )

    c4.metric(
        "Duplicates",
        summary["duplicates"]
    )

    st.divider()

    # ======================================================
    # DATASET READINESS
    # ======================================================

    score = 100

    score -= min(summary["missing"], 30)
    score -= min(summary["duplicates"], 20)

    score = max(score, 0)

    st.subheader("Dataset Readiness")

    st.progress(score / 100)

    st.metric(
        "Readiness Score",
        f"{score}/100"
    )

    st.divider()

    # ======================================================
    # KPI SUMMARY
    # ======================================================

    st.subheader("Business KPIs")

    if not summary["kpis"].empty:

        st.dataframe(
            summary["kpis"],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No KPI information available.")

    st.divider()

    # ======================================================
    # BUSINESS HIGHLIGHTS
    # ======================================================

    st.subheader("Business Highlights")

    if summary["highlights"]:

        for item in summary["highlights"]:

            st.success(item)

    else:

        st.info("No highlights generated.")

    st.divider()

    # ======================================================
    # RISKS
    # ======================================================

    st.subheader("Risk Assessment")

    if summary["risks"]:

        for item in summary["risks"]:

            st.warning(item)

    else:

        st.success("No significant risks detected.")

    st.divider()

    # ======================================================
    # RECOMMENDATIONS
    # ======================================================

    st.subheader("Recommendations")

    if summary["recommendations"]:

        for item in summary["recommendations"]:

            st.info(item)

    else:

        st.success("No recommendations available.")

    st.divider()

    # ======================================================
    # REPORT STATUS
    # ======================================================

    st.subheader("Report Status")

    st.success(
        "Executive report generated successfully."
    )

    st.caption(
        "Future versions will support PDF, PPTX and DOCX export."
    )