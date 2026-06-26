"""
AI Data Analyst Agent
Tool Router

Maps planner tasks to backend functions.
"""

from core.statistics_engine import dataset_statistics
from core.trend_engine import analyze_trend
from core.forecasting_engine import forecast_metric
from core.dashboard_builder import build_dashboard
from core.cleaning_engine import analyze_cleaning
from core.root_cause_engine import root_cause_analysis
from core.analytics_engine import driver_analysis
from core.anomaly_detector import detect_anomalies
from core.insight_engine import generate_insight


class ToolRouter:

    def __init__(self):

        self.tools = {

            "statistics": dataset_statistics,

            "trend": analyze_trend,

            "forecast": forecast_metric,

            "dashboard": build_dashboard,

            "cleaning": analyze_cleaning,

            "root_cause": root_cause_analysis,

            "driver_analysis": driver_analysis,

            "anomaly": detect_anomalies,

            "insight": generate_insight

        }

    # ============================================
    # GET TOOL
    # ============================================

    def get_tool(self, task):

        return self.tools.get(task)

    # ============================================
    # LIST TOOLS
    # ============================================

    def available_tools(self):

        return list(self.tools.keys())