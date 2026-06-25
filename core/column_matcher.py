from difflib import SequenceMatcher

BUSINESS_SYNONYMS = {

    "sales": [
        "sales",
        "revenue",
        "income",
        "turnover"
    ],

    "profit": [
        "profit",
        "margin",
        "earnings"
    ],

    "quantity": [
        "quantity",
        "units",
        "volume"
    ],

    "department": [
        "department",
        "team",
        "group"
    ]
}


def similarity(a, b):
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()


def find_best_columns(df, query):

    query = query.lower()

    matches = []

    for col in df.columns:

        col_lower = (
            col.lower()
            .replace("_", " ")
        )

        score = similarity(
            col_lower,
            query
        )

        for key, values in BUSINESS_SYNONYMS.items():

            if any(
                word in query
                for word in values
            ):

                if key in col_lower:
                    score += 0.5

        matches.append(
            (col, score)
        )

    matches.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return [
        col
        for col, score
        in matches[:3]
    ]