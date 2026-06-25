import pandas as pd


def detect_schema(df):

    schema = []

    for col in df.columns:

        dtype = str(df[col].dtype).lower()

        col_lower = col.lower()

        # Identifier detection

        if (
            "id" in col_lower
            or col_lower.endswith("_id")
            or col_lower == "id"
        ):
            detected_type = "Identifier"

        # Date detection

        elif (
            "date" in col_lower
            or "created_at" in col_lower
            or "timestamp" in col_lower
        ):
            detected_type = "Datetime"

        # Numeric

        elif (
            "int" in dtype
            or "float" in dtype
        ):
            detected_type = "Metric"

        else:

            unique_ratio = df[col].nunique() / len(df)

            if unique_ratio < 0.2:
                detected_type = "Category"
            else:
                detected_type = "Text"

        schema.append(
            {
                "Column": col,
                "Detected Type": detected_type
            }
        )

    return pd.DataFrame(schema)