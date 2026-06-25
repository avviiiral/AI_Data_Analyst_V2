import pandas as pd

from core.query_parser import detect_intent
from core.column_matcher import find_best_columns
from core.schema_detector import detect_schema
from core.trend_engine import generate_trend
from core.anomaly_detector import detect_anomalies
from core.analytics_engine import driver_analysis
from core.root_cause_engine import root_cause_analysis
from core.forecasting_engine import forecast_metric

def process_query(df, query):

    intent = detect_intent(query)

    numeric_cols = list(
        df.select_dtypes(
            include="number"
        ).columns
    )

    query_lower = query.lower()

    matched_cols = find_best_columns(
        df,
        query
    )

    # ===================================
    # AVERAGE
    # ===================================

    if intent == "average":

        for col in matched_cols:

            if col in numeric_cols:

                return {
                    "type": "metric",
                    "title": f"Average {col}",
                    "data": round(
                        df[col].mean(),
                        2
                    ),
                    "column": col
                }

    # ===================================
    # TOP
    # ===================================

    if intent == "top":

        for col in matched_cols:

            if col in numeric_cols:

                result = (
                    df.sort_values(
                        col,
                        ascending=False
                    )
                    .head(10)
                )

                return {
                    "type": "table",
                    "title": f"Top 10 by {col}",
                    "data": result,
                    "column": col
                }

    # ===================================
    # CORRELATION
    # ===================================

    if (
        intent == "correlation"
        and len(matched_cols) >= 2
    ):

        col1 = matched_cols[0]
        col2 = matched_cols[1]

        try:

            corr = round(
                df[col1].corr(df[col2]),
                3
            )

        except Exception:

            corr = 0

        return {
            "type": "correlation",
            "title": f"{col1} vs {col2}",
            "data": corr,
            "df": df,
            "col1": col1,
            "col2": col2
        }
    if intent == "maximum":
    
        for col in matched_cols:

            if col in numeric_cols:

                return {
                    "type": "metric",
                    "title": f"Maximum {col}",
                    "data": round(df[col].max(), 2),
                    "column": col
                }
    
    if intent == "minimum":
    
        for col in matched_cols:

            if col in numeric_cols:

                return {
                    "type": "metric",
                    "title": f"Minimum {col}",
                    "data": round(df[col].min(), 2),
                    "column": col
                }    
    
    if intent == "sum":
    
        for col in matched_cols:

            if col in numeric_cols:

                return {
                    "type": "metric",
                    "title": f"Total {col}",
                    "data": round(df[col].sum(), 2),
                    "column": col
                }
    
    if intent == "count":
    
        return {
            "type": "metric",
            "title": "Total Records",
            "data": len(df)
        }
    
    if intent == "distribution":
    
        for col in matched_cols:

            if col in numeric_cols:

                return {
                    "type": "distribution",
                    "title": f"Distribution of {col}",
                    "data": df,
                    "column": col
                }    
    
    # ===================================
    # GROUP BY ANALYSIS
    # ===================================

    if intent == "groupby":

        schema = detect_schema(df)

        metrics = schema[
            schema["Detected Type"] == "Metric"
        ]["Column"].tolist()

        categories = schema[
            schema["Detected Type"] == "Category"
        ]["Column"].tolist()

        metric_col = None
        category_col = None

        # Match columns from query

        for col in matched_cols:

            if col in metrics and metric_col is None:
                metric_col = col

            if col in categories and category_col is None:
                category_col = col

        # Fallback

        if metric_col is None and metrics:
            metric_col = metrics[0]

        if category_col is None and categories:
            category_col = categories[0]

        if metric_col and category_col:

            result_df = (
                df.groupby(category_col)[metric_col]
                .sum()
                .reset_index()
                .sort_values(
                    metric_col,
                    ascending=False
                )
            )

            return {
                "type": "groupby",
                "title": f"{metric_col} by {category_col}",
                "data": result_df,
                "metric": metric_col,
                "category": category_col
            }
    
    # ===================================
    # TREND
    # ===================================

    if intent == "trend":

        result = generate_trend(
            df,
            query
        )

        if result:
            return result


    # ===================================
    # ANOMALY
    # ===================================

    if intent == "anomaly":

        result = detect_anomalies(df)

        if result:
            return result


    # ===================================
    # DRIVER ANALYSIS
    # ===================================

    if intent == "drivers":

        result = driver_analysis(
            df,
            query
        )

        if result:
            return result
    
    # ===================================
    # ROOT CAUSE
    # ===================================

    if intent == "rootcause":

        result = root_cause_analysis(
            df,
            query
        )

        if result:
            return result        
    
    # ===================================
    # FORECAST
    # ===================================

    if intent == "forecast":

        result = forecast_metric(
            df,
            query
        )

        if result:
            return result
    
    return {
        "type": "text",
        "title": "Query Result",
        "data": "Could not understand query."
    }