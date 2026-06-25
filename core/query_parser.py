import re


def detect_intent(query):

    query = query.lower()

    # Average

    if any(word in query for word in [
        "average",
        "mean",
        "avg"
    ]):
        return "average"

    # Maximum

    if any(word in query for word in [
        "maximum",
        "max"
    ]):
        return "maximum"

    # Minimum

    if any(word in query for word in [
        "minimum",
        "min",
        "lowest",
        "smallest"
    ]):
        return "minimum"

    # Sum

    if any(word in query for word in [
        "sum",
        "total"
    ]):
        return "sum"

    # Top

    if "top" in query:
        return "top"

    # Compare

    if any(word in query for word in [
        "compare",
        "versus",
        "vs"
    ]):
        return "compare"

    # Correlation

    if any(word in query for word in [
        "relate",
        "related",
        "relationship",
        "correlation",
        "impact",
        "affect"
    ]):
        return "correlation"

    # Count

    if any(word in query for word in [
        "count",
        "how many",
        "number of"
    ]):
        return "count"

    # Distribution

    if any(word in query for word in [
        "distribution",
        "spread",
        "histogram"
    ]):
        return "distribution"

    
    if any(word in query for word in [
        "which",
        "best",
        "highest",
        "largest",
        "most",
        "top performing",
        "performs best"
    ]):
        return "groupby"
    if any(word in query for word in [
        "trend",
        "monthly trend",
        "over time"
    ]):
        return "trend"

    if any(word in query for word in [
        "anomaly",
        "anomalies",
        "outlier",
        "outliers",
        "abnormal"
    ]):
        return "anomaly"

    if any(word in query for word in [
        "influence",
        "factors",
        "driver",
        "drivers",
        "drives",
        "driver analysis"
    ]):
        return "drivers"
    
    if any(word in query for word in [
        "why",
        "reason",
        "cause",
        "causes",
        "causing",
        "increase",
        "increasing",
        "rise",
        "rising",
        "root cause"
    ]):
        return "rootcause"
    
    if any(word in query for word in [
        "forecast",
        "predict",
        "prediction",
        "future"
    ]):
        return "forecast"
    
    return "unknown"