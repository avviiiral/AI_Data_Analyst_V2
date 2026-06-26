import streamlit as st
import plotly.express as px
import pandas as pd

from core.dashboard_builder import build_dashboard


def render_dashboard(df):
    """
    Dashboard Page
    """

    st.header("📈 Smart Dashboard")

    dashboard = build_dashboard(df)

    # ==========================================================
    # OVERVIEW
    # ==========================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", dashboard["rows"])
    c2.metric("Columns", dashboard["columns"])
    c3.metric(
        "Numeric",
        dashboard["composition"]["numeric"]
    )
    c4.metric(
        "Categorical",
        dashboard["composition"]["categorical"]
    )

    st.divider()

    # ==========================================================
    # KPI SUMMARY
    # ==========================================================

    st.subheader("📊 KPI Summary")

    st.dataframe(
        dashboard["kpis"],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================================
    # INTERACTIVE CHART BUILDER
    # ==========================================================

    st.subheader("📈 Interactive Chart Builder")

    numeric_cols = dashboard["numeric_columns"]
    category_cols = dashboard["category_columns"]

    if len(numeric_cols) == 0:

        st.warning("No numeric columns available.")

        return

    metric = st.selectbox(
        "Metric",
        numeric_cols
    )

    category = None

    if len(category_cols):

        category = st.selectbox(
            "Category",
            category_cols
        )

    chart_type = st.selectbox(

        "Chart Type",

        [

            "Bar",

            "Line",

            "Pie",

            "Box",

            "Histogram",

            "Scatter"

        ]

    )

    fig = None

    # ----------------------------------------------------------
    # BAR
    # ----------------------------------------------------------

    if chart_type == "Bar":

        if category:

            temp = (

                df

                .groupby(category)[metric]

                .sum()

                .reset_index()

            )

            fig = px.bar(

                temp,

                x=category,

                y=metric,

                title=f"{metric} by {category}"

            )

    # ----------------------------------------------------------
    # LINE
    # ----------------------------------------------------------

    elif chart_type == "Line":

        if category:

            temp = (

                df

                .groupby(category)[metric]

                .sum()

                .reset_index()

            )

            fig = px.line(

                temp,

                x=category,

                y=metric,

                markers=True

            )

    # ----------------------------------------------------------
    # PIE
    # ----------------------------------------------------------

    elif chart_type == "Pie":

        if category:

            temp = (

                df

                .groupby(category)[metric]

                .sum()

                .reset_index()

            )

            fig = px.pie(

                temp,

                names=category,

                values=metric

            )

    # ----------------------------------------------------------
    # BOX
    # ----------------------------------------------------------

    elif chart_type == "Box":

        fig = px.box(

            df,

            y=metric,

            points="outliers"

        )

    # ----------------------------------------------------------
    # HISTOGRAM
    # ----------------------------------------------------------

    elif chart_type == "Histogram":

        fig = px.histogram(

            df,

            x=metric

        )

    # ----------------------------------------------------------
    # SCATTER
    # ----------------------------------------------------------

    elif chart_type == "Scatter":

        if len(numeric_cols) >= 2:

            x = st.selectbox(

                "X Axis",

                numeric_cols,

                key="scatter_x"

            )

            y = st.selectbox(

                "Y Axis",

                numeric_cols,

                index=1,

                key="scatter_y"

            )

            fig = px.scatter(

                df,

                x=x,

                y=y,

                color=category if category else None,

                trendline="ols"

            )

    if fig:

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()
    
    # ==========================================================
    # CORRELATION MATRIX
    # ==========================================================

    st.subheader("📌 Correlation Matrix")

    if dashboard["correlation"] is not None:

        fig = px.imshow(
            dashboard["correlation"],
            text_auto=True,
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title="Correlation Heatmap"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info(
            "At least two numeric columns are required."
        )

    st.divider()

    # ==========================================================
    # TOP NUMERIC METRICS
    # ==========================================================

    st.subheader("🏆 Top Metrics")

    st.dataframe(
        dashboard["top_numeric"],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================================
    # CATEGORY ANALYSIS
    # ==========================================================

    st.subheader("📂 Category Analysis")

    if dashboard["top_categories"]:

        category_name = st.selectbox(
            "Choose Category",
            list(dashboard["top_categories"].keys()),
            key="category_summary"
        )

        category_df = dashboard["top_categories"][category_name]

        col1, col2 = st.columns([1, 2])

        with col1:

            st.dataframe(
                category_df,
                use_container_width=True,
                hide_index=True
            )

        with col2:

            fig = px.bar(
                category_df,
                x=category_name,
                y="Count",
                title=f"Top Values in {category_name}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    else:

        st.info("No categorical columns available.")

    st.divider()

    # ==========================================================
    # MISSING VALUE DASHBOARD
    # ==========================================================

    st.subheader("⚠ Missing Values")

    st.dataframe(
        dashboard["missing"],
        use_container_width=True,
        hide_index=True
    )

    if dashboard["missing"]["Missing"].sum() > 0:

        fig = px.bar(
            dashboard["missing"],
            x="Column",
            y="Missing",
            title="Missing Values by Column"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.success("No missing values detected.")

    st.divider()

    # ==========================================================
    # AUTOMATIC TREND
    # ==========================================================

    st.subheader("📅 Trend Analysis")

    if dashboard["date_column"] is not None:

        if len(numeric_cols):

            metric = numeric_cols[0]

            temp = df.copy()

            temp[dashboard["date_column"]] = pd.to_datetime(
                temp[dashboard["date_column"]],
                errors="coerce"
            )

            temp = temp.dropna(
                subset=[dashboard["date_column"]]
            )

            temp["Month"] = (
                temp[dashboard["date_column"]]
                .dt.to_period("M")
                .astype(str)
            )

            trend = (
                temp.groupby("Month")[metric]
                .mean()
                .reset_index()
            )

            fig = px.line(
                trend,
                x="Month",
                y=metric,
                markers=True,
                title=f"Monthly Trend of {metric}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("No numeric metric available.")

    else:

        st.info(
            "No date column detected."
        )

    st.divider()

    # ==========================================================
    # BUSINESS INSIGHTS
    # ==========================================================

    st.subheader("💡 Dashboard Insights")

    insights = []

    insights.append(
        f"Dataset contains **{dashboard['rows']}** records."
    )

    insights.append(
        f"Detected **{dashboard['composition']['numeric']}** numeric columns."
    )

    insights.append(
        f"Detected **{dashboard['composition']['categorical']}** categorical columns."
    )

    if dashboard["missing"]["Missing"].sum() == 0:

        insights.append(
            "Dataset contains no missing values."
        )

    else:

        insights.append(
            f"{dashboard['missing']['Missing'].sum()} missing values detected."
        )

    if dashboard["correlation"] is not None:

        insights.append(
            "Correlation analysis is available."
        )

    for item in insights:

        st.success(item)