"""
AI Data Analyst Agent
Tool Registry V2
"""

from core.statistics_engine import dataset_statistics
from core.trend_engine import generate_trend
from core.forecasting_engine import forecast_metric
from core.dashboard_builder import build_dashboard
from core.cleaning_engine import analyze_cleaning
from core.root_cause_engine import root_cause_analysis
from core.analytics_engine import driver_analysis
from core.anomaly_detector import detect_anomalies
from core.insight_engine import generate_insight


TOOLS = {

    "statistics": {

        "function": dataset_statistics,

        "inputs": ["df"],

        "description": "Generate descriptive statistics"

    },

    "trend": {

        "function": generate_trend,

        "inputs": ["df"],

        "description": "Analyze trends"

    },

    "forecast": {

        "function": forecast_metric,

        "inputs": ["df", "query"],

        "description": "Forecast future values"

    },

    "dashboard": {

        "function": build_dashboard,

        "inputs": ["df"],

        "description": "Generate dashboard"

    },

    "cleaning": {

        "function": analyze_cleaning,

        "inputs": ["df"],

        "description": "Analyze data quality"

    },

    "root_cause": {

        "function": root_cause_analysis,

        "inputs": ["df"],

        "description": "Root cause analysis"

    },

    "driver_analysis": {

        "function": driver_analysis,

        "inputs": ["df"],

        "description": "Driver analysis"

    },

    "anomaly": {

        "function": detect_anomalies,

        "inputs": ["df"],

        "description": "Detect anomalies"

    },

    "insight": {

        "function": generate_insight,

        "inputs": ["last_result"],

        "description": "Generate business insight"

    }

}