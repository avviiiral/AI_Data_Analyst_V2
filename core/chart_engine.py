import plotly.express as px


def generate_chart(result):

    if result["type"] == "table":

        df = result["data"]

        numeric_cols = list(
            df.select_dtypes(
                include="number"
            ).columns
        )

        if numeric_cols:

            return px.bar(
                df,
                y=numeric_cols[0]
            )

    if result["type"] == "correlation":

        df = result["df"]

        return px.scatter(
            df,
            x=result["col1"],
            y=result["col2"],
            trendline="ols"
        )
    
    if result["type"] == "distribution":
    
        return px.histogram(
            result["data"],
            x=result["column"],
            title=result["title"]
        )
    
    if result["type"] == "groupby":
        return px.bar(
            result["data"],
            x=result["category"],
            y=result["metric"],
            title=result["title"]
        )   
    
    
    if result["type"] == "trend":
    
        return px.line(
            result["data"],
            x="Month",
            y=result["metric"],
            title=result["title"],
            markers=True
        )
        
    if result["type"] == "drivers":
    
        return px.bar(
            result["data"],
            x="Feature",
            y="Importance",
            title=result["title"]
        )

    if result["type"] == "forecast":
    
        return px.line(
            result["data"],
            x="Month",
            y=["Value", "Forecast"],
            title=result["title"],
            markers=True
        )
    
    if result["type"] == "rootcause":
        return px.bar(
            result["data"],
            x="Feature",
            y="Correlation",
            title=result["title"]
        )
    return None
    