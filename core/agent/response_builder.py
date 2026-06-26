"""
AI Data Analyst Agent

Response Builder

Combines outputs from multiple tools into one
business-friendly response.
"""

import pandas as pd


class ResponseBuilder:

    def __init__(self):
        pass

    # ==========================================================
    # BUILD RESPONSE
    # ==========================================================

    def build(self, query, results):

        response = {

            "query": query,

            "summary": [],

            "details": {},

            "recommendations": [],

            "status": "success"

        }

        # ======================================================
        # LOOP THROUGH TOOL RESULTS
        # ======================================================

        for tool, output in results.items():

            if output["status"] != "success":

                response["summary"].append(

                    f"❌ {tool} failed."

                )

                continue

            data = output["data"]

            response["details"][tool] = data

            # --------------------------------------------------

            if tool == "statistics":

                response["summary"].append(

                    "Dataset statistics generated successfully."

                )

            elif tool == "trend":

                response["summary"].append(

                    "Trend analysis completed."

                )

            elif tool == "forecast":

                response["summary"].append(

                    "Forecast generated."

                )

            elif tool == "dashboard":

                response["summary"].append(

                    "Dashboard metrics prepared."

                )

            elif tool == "cleaning":

                response["summary"].append(

                    "Dataset quality assessed."

                )

            elif tool == "driver_analysis":

                response["summary"].append(

                    "Key drivers identified."

                )

            elif tool == "root_cause":

                response["summary"].append(

                    "Root cause analysis completed."

                )

            elif tool == "anomaly":

                response["summary"].append(

                    "Anomaly detection completed."

                )

            elif tool == "insight":

                response["summary"].append(

                    "Business insight generated."

                )

        # ======================================================
        # RECOMMENDATIONS
        # ======================================================

        if "cleaning" in response["details"]:

            response["recommendations"].append(

                "Review dataset quality before modeling."

            )

        if "forecast" in response["details"]:

            response["recommendations"].append(

                "Compare forecast with historical trends."

            )

        if "driver_analysis" in response["details"]:

            response["recommendations"].append(

                "Focus on the strongest business drivers."

            )

        if "root_cause" in response["details"]:

            response["recommendations"].append(

                "Investigate identified root causes."

            )

        if "anomaly" in response["details"]:

            response["recommendations"].append(

                "Review detected anomalies."

            )

        return response

    # ==========================================================
    # FORMAT RESPONSE
    # ==========================================================

    def format_markdown(self, response):

        text = "# AI Analysis Report\n\n"

        text += "## Summary\n\n"

        for item in response["summary"]:

            text += f"- {item}\n"

        text += "\n"

        if response["recommendations"]:

            text += "## Recommendations\n\n"

            for item in response["recommendations"]:

                text += f"- {item}\n"

        return text