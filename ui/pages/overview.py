import streamlit as st

from core.profiler import profile_dataset
from core.schema_detector import detect_schema
from core.question_generator import generate_questions


def render_overview(df):
    """
    Overview Page
    """

    st.header("🏠 Dataset Overview")

    profile = profile_dataset(df)

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Rows", profile["Rows"])
    c2.metric("Columns", profile["Columns"])
    c3.metric("Missing", profile["Missing Values"])
    c4.metric("Duplicates", profile["Duplicate Rows"])
    c5.metric("Memory (MB)", profile["Memory Usage MB"])

    st.divider()

    # ======================================
    # DATA PREVIEW
    # ======================================

    st.subheader("Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True,
        height=350
    )

    st.divider()

    # ======================================
    # DATA TYPES
    # ======================================

    st.subheader("Column Information")

    info = []

    for col in df.columns:

        info.append(
            {
                "Column": col,
                "Type": str(df[col].dtype),
                "Unique": df[col].nunique(),
                "Missing": int(df[col].isna().sum())
            }
        )

    st.dataframe(
        info,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # SCHEMA
    # ======================================

    st.subheader("Detected Schema")

    schema = detect_schema(df)

    st.dataframe(
        schema,
        use_container_width=True
    )

    st.divider()

    # ======================================
    # QUESTIONS
    # ======================================

    st.subheader("Suggested Questions")

    questions = generate_questions(df)

    for q in questions:

        st.info(q)

    st.divider()

    # ======================================
    # DATA TYPES SUMMARY
    # ======================================

    st.subheader("Dataset Composition")

    numeric = len(
        df.select_dtypes(include="number").columns
    )

    categorical = len(
        df.select_dtypes(
            exclude="number"
        ).columns
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Numeric Columns",
        numeric
    )

    c2.metric(
        "Categorical Columns",
        categorical
    )

    st.success("Dataset loaded successfully and ready for analysis.")