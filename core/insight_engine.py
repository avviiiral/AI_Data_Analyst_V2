def generate_insight(result):
    
    if result["type"] == "metric":

        return (
            f"{result['title']} is "
            f"{result['data']}."
        )

    elif result["type"] == "table":

        return (
            "Top records identified successfully."
        )

    elif result["type"] == "correlation":

        corr = result["data"]

        if abs(corr) >= 0.7:
            return (
                f"Strong relationship detected "
                f"(correlation = {corr})."
            )

        elif abs(corr) >= 0.3:
            return (
                f"Moderate relationship detected "
                f"(correlation = {corr})."
            )
        
        else:
            return (
                f"Weak relationship detected "
                f"(correlation = {corr})."
            )
    elif result["type"] == "groupby":
        
        top_row = result["data"].iloc[0]

        return (
            f"{top_row[result['category']]} has the highest "
            f"{result['metric']} value of "
            f"{round(top_row[result['metric']], 2)}."
        )
    
    elif result["type"] == "trend":
    
        max_row = result["data"].iloc[
            result["data"][
                result["metric"]
            ].idxmax()
        ]

        return (
            f"Peak {result['metric']} occurred "
            f"in {max_row['Month']}."
        )
    
    elif result["type"] == "anomaly":
        
        return (
            f"{len(result['data'])} anomalies detected."
        )
    
    elif result["type"] == "drivers":
    
        top_driver = result["data"].iloc[0]

        return (
            f"{top_driver['Feature']} is the strongest driver."
        )
    
    elif result["type"] == "rootcause":
        
        top_driver = result["data"].iloc[0]

        return (
            f"The strongest driver is "
            f"{top_driver['Feature']} "
            f"(correlation = {top_driver['Correlation']})."
        )
        
    elif result["type"] == "forecast":
    
        return (
            f"Predicted next value for "
            f"{result['metric']} is "
            f"{result['forecast']}."
        )
        
    return "No insight available."