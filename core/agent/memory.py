"""
AI Data Analyst Agent

Memory Manager

Stores conversation history,
tool executions and context.
"""

from collections import deque


class Memory:

    def __init__(self, max_history=20):

        self.max_history = max_history

        self.history = deque(maxlen=max_history)

        self.context = {}

    # ==========================================================
    # ADD MESSAGE
    # ==========================================================

    def add(self, role, message):

        self.history.append({

            "role": role,

            "message": message

        })

    # ==========================================================
    # ADD TOOL RESULT
    # ==========================================================

    def add_tool_result(self, tool, result):

        self.context[tool] = result

    # ==========================================================
    # GET HISTORY
    # ==========================================================

    def get_history(self):

        return list(self.history)

    # ==========================================================
    # GET LAST USER QUERY
    # ==========================================================

    def last_user_query(self):

        for item in reversed(self.history):

            if item["role"] == "user":

                return item["message"]

        return None

    # ==========================================================
    # GET CONTEXT
    # ==========================================================

    def get_context(self):

        return self.context

    # ==========================================================
    # GET TOOL RESULT
    # ==========================================================

    def get_tool_result(self, tool):

        return self.context.get(tool)

    # ==========================================================
    # CLEAR MEMORY
    # ==========================================================

    def clear(self):

        self.history.clear()

        self.context.clear()

    # ==========================================================
    # HAS CONTEXT
    # ==========================================================

    def has_tool(self, tool):

        return tool in self.context

    # ==========================================================
    # SUMMARY
    # ==========================================================

    def summary(self):

        return {

            "messages": len(self.history),

            "tools_used": list(self.context.keys())

        }