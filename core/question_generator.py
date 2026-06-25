from core.schema_detector import detect_schema


def generate_questions(df):

    schema = detect_schema(df)

    metrics = schema[
        schema["Detected Type"] == "Metric"
    ]["Column"].tolist()

    categories = schema[
        schema["Detected Type"] == "Category"
    ]["Column"].tolist()

    questions = []

    if metrics:
        questions.append(
            f"What factors influence {metrics[0]}?"
        )

    if len(metrics) > 1:
        questions.append(
            f"How does {metrics[0]} relate to {metrics[1]}?"
        )

    if categories and metrics:
        questions.append(
            f"Which {categories[0]} has the highest {metrics[0]}?"
        )

    if categories and metrics:
        questions.append(
            f"Compare {metrics[0]} across {categories[0]}"
        )

    questions.append(
        "What are the key trends and anomalies?"
    )

    return questions