import streamlit as st

from core.agent.agent import DataAnalystAgent


# ==========================================================
# PAGE
# ==========================================================

def render_agent(df):

    st.header("🤖 AI Data Analyst Agent")

    st.caption(
        "An intelligent multi-tool AI agent for business analytics."
    )

    # ======================================================
    # SESSION
    # ======================================================

    if "agent" not in st.session_state:

        st.session_state.agent = DataAnalystAgent()

    agent = st.session_state.agent

    # ======================================================
    # SUGGESTED QUESTIONS
    # ======================================================

    st.subheader("Suggested Questions")

    suggestions = [

        "Average Sales",

        "Show Sales Trend",

        "Forecast Revenue",

        "Driver Analysis",

        "Root Cause Analysis",

        "Detect Anomalies",

        "Analyze Dataset Quality",

        "Create Dashboard"

    ]

    cols = st.columns(4)

    for i, question in enumerate(suggestions):

        if cols[i % 4].button(

            question,

            use_container_width=True

        ):

            st.session_state.agent_query = question

    st.divider()

    # ======================================================
    # QUERY
    # ======================================================

    default = st.session_state.get(

        "agent_query",

        ""

    )

    query = st.text_input(

        "Ask your business question",

        value=default,

        placeholder="Example: Why are sales decreasing?"

    )

    analyze = st.button(

        "🚀 Analyze",

        type="primary",

        use_container_width=True

    )

    if analyze and query:

        with st.spinner("Planning analysis..."):

            response = agent.ask(

                df,

                query

            )

        st.session_state.agent_response = response

        st.session_state.agent_query = ""

    st.divider()

    # ======================================================
    # EXECUTION PLAN
    # ======================================================

    if "agent_response" in st.session_state:

        st.subheader("🧠 Execution Summary")

        response = st.session_state.agent_response

        for item in response["summary"]:

            st.success(item)

        st.divider()

    # ======================================================
    # TOOL OUTPUTS
    # ======================================================

    if "agent_response" not in st.session_state:

        return

    response = st.session_state.agent_response

    st.subheader("⚙ Tool Outputs")

    details = response.get("details", {})

    if not details:

        st.info("No tool outputs available.")

    for tool_name, data in details.items():

        with st.expander(
            f"📌 {tool_name.replace('_',' ').title()}",
            expanded=False
        ):

            # ---------------------------------------------
            # DATAFRAME
            # ---------------------------------------------

            if hasattr(data, "head"):

                st.dataframe(
                    data,
                    use_container_width=True
                )

            # ---------------------------------------------
            # DICTIONARY
            # ---------------------------------------------

            elif isinstance(data, dict):

                st.json(data)

            # ---------------------------------------------
            # LIST
            # ---------------------------------------------

            elif isinstance(data, list):

                st.write(data)

            # ---------------------------------------------
            # PLOTLY FIGURE
            # ---------------------------------------------

            elif hasattr(data, "to_plotly_json"):

                st.plotly_chart(
                    data,
                    use_container_width=True
                )

            # ---------------------------------------------
            # EVERYTHING ELSE
            # ---------------------------------------------

            else:

                st.write(data)

    st.divider()

    # ======================================================
    # RECOMMENDATIONS
    # ======================================================

    st.subheader("💡 Business Recommendations")

    recommendations = response.get(
        "recommendations",
        []
    )

    if recommendations:

        for rec in recommendations:

            st.info(rec)

    else:

        st.success(
            "No recommendations generated."
        )

    st.divider()

    # ======================================================
    # AGENT MEMORY
    # ======================================================

    st.subheader("🧠 Agent Memory")

    history = agent.history()

    if history:

        for item in history:

            if item["role"] == "user":

                st.markdown(
                    f"**👤 User:** {item['message']}"
                )

            else:

                st.markdown(
                    "**🤖 Agent:** Response Generated"
                )

    else:

        st.info("No conversation history.")

    st.divider()

    # ======================================================
    # AGENT STATISTICS
    # ======================================================

    st.subheader("📊 Agent Statistics")

    history = agent.history()

    total_messages = len(history)
    user_messages = sum(
        1 for item in history
        if item["role"] == "user"
    )

    agent_messages = total_messages - user_messages

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Messages",
        total_messages
    )

    c2.metric(
        "Questions Asked",
        user_messages
    )

    c3.metric(
        "Responses Generated",
        agent_messages
    )

    st.divider()

    # ======================================================
    # EXPORT REPORT
    # ======================================================

    report = ""

    report += "# AI Data Analyst Agent Report\n\n"

    report += "## Summary\n\n"

    for item in response["summary"]:

        report += f"- {item}\n"

    report += "\n"

    report += "## Recommendations\n\n"

    for item in response["recommendations"]:

        report += f"- {item}\n"

    st.download_button(

        "📥 Export AI Report",

        report,

        file_name="AI_Report.md",

        mime="text/markdown",

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # RESET MEMORY
    # ======================================================

    if st.button(

        "🗑 Clear Agent Memory",

        use_container_width=True

    ):

        agent.clear()

        if "agent_response" in st.session_state:

            del st.session_state.agent_response

        st.success(
            "Agent memory cleared."
        )

        st.rerun()