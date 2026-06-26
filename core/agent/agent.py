"""
AI Data Analyst Agent

Main Agent Orchestrator
"""

import streamlit as st

from core.agent.planner import Planner
from core.agent.executor import Executor
from core.agent.memory import Memory
from core.agent.response_builder import ResponseBuilder


class DataAnalystAgent:

    def __init__(self):

        self.planner = Planner()

        self.executor = Executor()

        self.builder = ResponseBuilder()

        # -----------------------------------------
        # Persist memory across Streamlit reruns
        # -----------------------------------------

        if "agent_memory" not in st.session_state:

            st.session_state.agent_memory = Memory()

        self.memory = st.session_state.agent_memory

    # =====================================================
    # ASK
    # =====================================================

    def ask(self, df, query):

        # -----------------------------------------
        # Store user message
        # -----------------------------------------

        self.memory.add(

            "user",

            query

        )

        # -----------------------------------------
        # Create execution plan
        # -----------------------------------------

        plan = self.planner.create_plan(query)

        # -----------------------------------------
        # Execute tools
        # -----------------------------------------

        results = self.executor.execute(

            df,

            query,

            plan

        )

        # -----------------------------------------
        # Save tool outputs
        # -----------------------------------------

        for tool, output in results.items():

            if output["status"] == "success":

                self.memory.add_tool_result(

                    tool,

                    output["data"]

                )

        # -----------------------------------------
        # Build response
        # -----------------------------------------

        response = self.builder.build(

            query,

            results

        )

        # -----------------------------------------
        # Save assistant response
        # -----------------------------------------

        self.memory.add(

            "assistant",

            response

        )

        return response

    # =====================================================
    # HISTORY
    # =====================================================

    def history(self):

        return self.memory.get_history()

    # =====================================================
    # CONTEXT
    # =====================================================

    def context(self):

        return self.memory.get_context()

    # =====================================================
    # RESET
    # =====================================================

    def clear(self):

        self.memory.clear()