import streamlit as st
import pandas as pd

from core.data_loader import load_data
from core.schema_detector import detect_schema
from core.profiler import profile_dataset
from core.question_generator import generate_questions
from core.health_engine import dataset_health_score
from core.query_engine import process_query
from core.chart_engine import generate_chart
from core.insight_engine import generate_insight
from core.executive_summary import generate_executive_summary
from core.dashboard_builder import build_dashboard
from ui.hero import render_hero
from ui.feature_cards import render_feature_cards

def load_css():
    
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

st.set_page_config(
    page_title="AI Data Analyst V2",
    layout="wide"
)

load_css()
from ui.sidebar import render_sidebar

render_sidebar()

render_hero()

render_feature_cards()
# ==========================================
# FILE UPLOAD
# ==========================================

from ui.upload import upload_section

uploaded_file = upload_section()

# ==========================================
# MAIN APP
# ==========================================

if uploaded_file:

    df = load_data(uploaded_file)

    st.success("Dataset Loaded Successfully")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
        [
            "Overview",
            "Schema",
            "Questions",
            "Dataset Health",
            "Executive Summary",
            "Smart Dashboard",
            "AI Analyst"
        ]
    )

    # ==========================================
    # OVERVIEW
    # ==========================================

    with tab1:

        profile = profile_dataset(df)

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Rows", profile["Rows"])
        col2.metric("Columns", profile["Columns"])
        col3.metric("Missing", profile["Missing Values"])
        col4.metric("Duplicates", profile["Duplicate Rows"])
        col5.metric("Memory (MB)", profile["Memory Usage MB"])

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(),
            use_container_width=True
        )

    # ==========================================
    # SCHEMA
    # ==========================================

    with tab2:

        schema = detect_schema(df)

        st.subheader("Detected Schema")

        st.dataframe(
            schema,
            use_container_width=True
        )

    # ==========================================
    # QUESTIONS
    # ==========================================

    with tab3:

        st.subheader("Suggested Questions")

        questions = generate_questions(df)

        for q in questions:
            st.info(q)

    # ==========================================
    # DATASET HEALTH
    # ==========================================

    with tab4:

        health = dataset_health_score(df)

        st.subheader("Dataset Quality Score")

        st.metric(
            "Health Score",
            f"{health['score']}/100"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Missing Values",
                health["missing_count"]
            )

            st.metric(
                "Missing %",
                health["missing_pct"]
            )

        with col2:

            st.metric(
                "Duplicates",
                health["duplicate_count"]
            )

            st.metric(
                "Duplicate %",
                health["duplicate_pct"]
            )

        st.subheader("Recommendations")

        for rec in health["recommendations"]:
            st.success(rec)

    # ==========================================
    # AI ANALYST
    # ==========================================

    with tab7:

        st.subheader("AI Analyst")

        query = st.text_input(
            "Ask your data anything"
        )

        if query:

            result = process_query(
                df,
                query
            )

            if "title" in result:
                st.write(f"### {result['title']}")

            # ------------------------------
            # METRIC
            # ------------------------------

            if result["type"] == "metric":

                st.metric(
                    result["title"],
                    result["data"]
                )

            # ------------------------------
            # TABLE
            # ------------------------------

            elif result["type"] == "table":

                st.dataframe(
                    result["data"],
                    use_container_width=True
                )

                fig = generate_chart(result)

                if fig:
                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # ------------------------------
            # CORRELATION
            # ------------------------------

            elif result["type"] == "correlation":

                st.metric(
                    "Correlation",
                    result["data"]
                )

                fig = generate_chart(result)

                if fig:
                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # ------------------------------
            # DISTRIBUTION
            # ------------------------------

            elif result["type"] == "distribution":

                fig = generate_chart(result)

                if fig:
                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # ------------------------------
            # GROUP BY
            # ------------------------------

            elif result["type"] == "groupby":

                st.dataframe(
                    result["data"],
                    use_container_width=True
                )

                fig = generate_chart(result)

                if fig:
                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # ------------------------------
            # TREND
            # ------------------------------

            elif result["type"] == "trend":

                st.dataframe(
                    result["data"],
                    use_container_width=True
                )

                fig = generate_chart(result)

                if fig:
                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # ------------------------------
            # ANOMALY
            # ------------------------------

            elif result["type"] == "anomaly":

                st.dataframe(
                    result["data"],
                    use_container_width=True
                )

            # ------------------------------
            # DRIVERS
            # ------------------------------

            elif result["type"] == "drivers":

                st.dataframe(
                    result["data"],
                    use_container_width=True
                )

                fig = generate_chart(result)

                if fig:
                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )
            elif result["type"] == "rootcause":
                
                st.dataframe(
                    result["data"],
                    use_container_width=True
                )

                fig = generate_chart(result)

                if fig:
                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )
            elif result["type"] == "forecast":
                
                st.metric(
                    "Forecast",
                    result["forecast"]
                )

                st.dataframe(
                    result["data"],
                    use_container_width=True
                )

                fig = generate_chart(result)

                if fig:
                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

            # ------------------------------
            # TEXT
            # ------------------------------

            elif result["type"] == "text":

                st.warning(
                    result["data"]
                )

            # ------------------------------
            # INSIGHTS
            # ------------------------------

            st.success(
                generate_insight(result)
            )
    
    with tab5:

        st.header("Executive Summary")

        summary = generate_executive_summary(df)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Rows",
            summary["rows"]
        )

        col2.metric(
            "Columns",
            summary["columns"]
        )

        col3.metric(
            "Missing",
            summary["missing"]
        )

        col4.metric(
            "Duplicates",
            summary["duplicates"]
        )

        st.subheader("Top KPIs")

        st.dataframe(
            summary["kpis"],
            use_container_width=True
        )

        st.subheader("Business Highlights")

        for item in summary["highlights"]:
            st.success(item)

        st.subheader("Potential Risks")

        for item in summary["risks"]:
            st.warning(item)

        st.subheader("Recommendations")

        for item in summary["recommendations"]:
            st.info(item)
            
    with tab6:

        st.header("Smart Dashboard")

        dashboard = build_dashboard(df)

        col1, col2 = st.columns(2)

        col1.metric(
            "Rows",
            dashboard["rows"]
        )

        col2.metric(
            "Columns",
            dashboard["columns"]
        )

        st.subheader("KPI Summary")

        st.dataframe(
            dashboard["kpis"],
            use_container_width=True
        )

        st.subheader("Category Summary")

        st.dataframe(
            dashboard["category_summary"],
            use_container_width=True
        )

        st.subheader("Detected Columns")

        st.write(
            "Numeric Columns:",
            dashboard["numeric_columns"]
        )

        st.write(
            "Category Columns:",
            dashboard["category_columns"]
        )

        st.write(
            "Detected Date Column:",
            dashboard["date_column"]
        )