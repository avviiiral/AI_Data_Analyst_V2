import streamlit as st

from core.query_engine import process_query
from core.chart_engine import generate_chart
from core.insight_engine import generate_insight


def render_copilot(df):

    st.header("🤖 AI Copilot")

    # =====================================================
    # SESSION STATE
    # =====================================================

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # =====================================================
    # SUGGESTED QUESTIONS
    # =====================================================

    st.subheader("Suggested Questions")

    suggestions = [

        "Average Sales",

        "Top 10 Records",

        "Maximum Revenue",

        "Distribution of Sales",

        "Show Trend",

        "Detect Anomalies",

        "Driver Analysis",

        "Root Cause",

        "Forecast next 3 months"

    ]

    cols = st.columns(3)

    for i, question in enumerate(suggestions):

        if cols[i % 3].button(
            question,
            use_container_width=True
        ):
            st.session_state.selected_question = question

    st.divider()

    # =====================================================
    # QUERY INPUT
    # =====================================================

    default_value = st.session_state.get(
        "selected_question",
        ""
    )

    query = st.text_input(
        "Ask anything about your dataset",
        value=default_value,
        placeholder="Example: Which department has the highest sales?"
    )

    analyze = st.button(
        "Analyze",
        type="primary",
        use_container_width=True
    )

    if analyze and query:

        result = process_query(
            df,
            query
        )

        st.session_state.chat_history.append({

            "query": query,

            "result": result

        })

        st.session_state.selected_question = ""

    st.divider()

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    st.subheader("Conversation")

    if len(st.session_state.chat_history) == 0:

        st.info(
            "Start by asking a question about your data."
        )

        return

    for chat in reversed(
        st.session_state.chat_history
    ):

        st.markdown(
            f"### 👤 {chat['query']}"
        )

        result = chat["result"]

        if "title" in result:

            st.markdown(
                f"**{result['title']}**"
            )
        # =====================================================
        # METRIC
        # =====================================================

        if result["type"] == "metric":

            st.metric(
                result["title"],
                result["data"]
            )

        # =====================================================
        # TABLE
        # =====================================================

        elif result["type"] == "table":

            st.dataframe(
                result["data"],
                use_container_width=True
            )

        # =====================================================
        # GROUP BY
        # =====================================================

        elif result["type"] == "groupby":

            st.dataframe(
                result["data"],
                use_container_width=True
            )

        # =====================================================
        # TREND
        # =====================================================

        elif result["type"] == "trend":

            st.dataframe(
                result["data"],
                use_container_width=True
            )

        # =====================================================
        # FORECAST
        # =====================================================

        elif result["type"] == "forecast":

            st.metric(
                "Forecast",
                result["forecast"]
            )

            st.dataframe(
                result["data"],
                use_container_width=True
            )

        # =====================================================
        # DRIVER ANALYSIS
        # =====================================================

        elif result["type"] == "drivers":

            st.dataframe(
                result["data"],
                use_container_width=True
            )

        # =====================================================
        # ROOT CAUSE
        # =====================================================

        elif result["type"] == "rootcause":

            st.dataframe(
                result["data"],
                use_container_width=True
            )

        # =====================================================
        # ANOMALIES
        # =====================================================

        elif result["type"] == "anomaly":

            st.dataframe(
                result["data"],
                use_container_width=True
            )

        # =====================================================
        # DISTRIBUTION
        # =====================================================

        elif result["type"] == "distribution":

            pass

        # =====================================================
        # CORRELATION
        # =====================================================

        elif result["type"] == "correlation":

            st.metric(
                "Correlation",
                result["data"]
            )

        # =====================================================
        # TEXT
        # =====================================================

        elif result["type"] == "text":

            st.warning(
                result["data"]
            )

        # =====================================================
        # AUTO CHART
        # =====================================================

        fig = generate_chart(result)

        if fig:

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # =====================================================
        # AI INSIGHT
        # =====================================================

        st.success(
            generate_insight(result)
        )

        st.divider()

    # =====================================================
    # CHAT MANAGEMENT
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🗑 Clear Conversation",
            use_container_width=True
        ):

            st.session_state.chat_history = []

            st.rerun()

    with col2:

        st.metric(
            "Questions Asked",
            len(st.session_state.chat_history)
        )

    st.divider()

    # =====================================================
    # QUERY HISTORY
    # =====================================================

    st.subheader("Recent Questions")

    if st.session_state.chat_history:

        history = [
            item["query"]
            for item in st.session_state.chat_history
        ]

        st.dataframe(
            history,
            use_container_width=True
        )