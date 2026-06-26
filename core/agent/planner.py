"""
AI Data Analyst Agent
Planner V2

Creates an execution plan for the AI Agent.
"""


class Planner:

    def __init__(self):
        pass

    def create_plan(self, query: str):

        q = query.lower()

        plan = []

        # =====================================================
        # Helper
        # =====================================================

        def add(tool, priority):

            plan.append({

                "tool": tool,

                "priority": priority

            })

        # =====================================================
        # Statistics
        # =====================================================

        if any(word in q for word in [

            "average",
            "mean",
            "median",
            "maximum",
            "minimum",
            "sum",
            "count"

        ]):

            add("statistics", 1)

        # =====================================================
        # Trend
        # =====================================================

        if any(word in q for word in [

            "trend",
            "growth",
            "monthly",
            "daily",
            "yearly",
            "over time"

        ]):

            add("trend", 2)

        # =====================================================
        # Forecast
        # =====================================================

        if any(word in q for word in [

            "forecast",
            "predict",
            "future",
            "next month",
            "next year"

        ]):

            add("forecast", 3)

        # =====================================================
        # Dashboard
        # =====================================================

        if any(word in q for word in [

            "dashboard",
            "chart",
            "graph",
            "visualize"

        ]):

            add("dashboard", 4)

        # =====================================================
        # Cleaning
        # =====================================================

        if any(word in q for word in [

            "clean",
            "duplicate",
            "missing",
            "outlier"

        ]):

            add("cleaning", 5)

        # =====================================================
        # Root Cause
        # =====================================================

        if any(word in q for word in [

            "why",
            "reason",
            "cause"

        ]):

            add("root_cause", 6)

        # =====================================================
        # Driver Analysis
        # =====================================================

        if any(word in q for word in [

            "driver",
            "impact",
            "important",
            "influence"

        ]):

            add("driver_analysis", 7)

        # =====================================================
        # Anomaly
        # =====================================================

        if any(word in q for word in [

            "anomaly",
            "abnormal"

        ]):

            add("anomaly", 8)

        # =====================================================
        # Always finish with insight
        # =====================================================

        add("insight", 999)

        # =====================================================
        # Remove duplicates
        # =====================================================

        seen = set()

        unique = []

        for item in plan:

            if item["tool"] not in seen:

                unique.append(item)

                seen.add(item["tool"])

        unique.sort(

            key=lambda x: x["priority"]

        )

        return unique