"""
AI Data Analyst Agent

Executor V3
"""

import traceback

from core.agent.tools import TOOLS


class Executor:

    def __init__(self):
        pass

    # =====================================================
    # BUILD ARGUMENTS
    # =====================================================

    def build_args(
        self,
        inputs,
        df,
        query,
        results
    ):

        args = []

        for item in inputs:

            if item == "df":

                args.append(df)

            elif item == "query":

                args.append(query)

            elif item == "results":

                args.append(results)

            elif item == "last_result":

                if len(results):

                    last = list(results.values())[-1]

                    if isinstance(last, dict):

                        args.append(last.get("data"))

                    else:

                        args.append(last)

                else:

                    args.append(None)

        return args

    # =====================================================
    # EXECUTE PLAN
    # =====================================================

    def execute(
        self,
        df,
        query,
        plan
    ):

        results = {}

        for step in plan:

            task = step["tool"]

            if task not in TOOLS:

                results[task] = {

                    "status": "error",

                    "message": "Unknown tool"

                }

                continue

            tool = TOOLS[task]

            function = tool["function"]

            inputs = tool["inputs"]

            try:

                args = self.build_args(

                    inputs,

                    df,

                    query,

                    results

                )

                output = function(*args)

                results[task] = {

                    "status": "success",

                    "data": output

                }

            except Exception as e:

                results[task] = {

                    "status": "error",

                    "message": str(e),

                    "traceback": traceback.format_exc()

                }

        return results