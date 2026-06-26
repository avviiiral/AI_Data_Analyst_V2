import streamlit as st
import pandas as pd


# ==========================================================
# INITIALIZE SESSION
# ==========================================================

def initialize_session(df):
    """
    Initialize session state.
    """

    if "original_df" not in st.session_state:

        st.session_state.original_df = df.copy()

    if "cleaned_df" not in st.session_state:

        st.session_state.cleaned_df = df.copy()

    if "cleaning_history" not in st.session_state:

        st.session_state.cleaning_history = []


# ==========================================================
# GET DATASET
# ==========================================================

def get_cleaned_df():

    return st.session_state.cleaned_df


def get_original_df():

    return st.session_state.original_df


# ==========================================================
# UPDATE DATASET
# ==========================================================

def update_dataset(df, action):

    st.session_state.cleaned_df = df

    st.session_state.cleaning_history.append(action)


# ==========================================================
# RESET
# ==========================================================

def reset_dataset():

    st.session_state.cleaned_df = (
        st.session_state.original_df.copy()
    )

    st.session_state.cleaning_history = []


# ==========================================================
# HISTORY
# ==========================================================

def get_history():

    return st.session_state.cleaning_history


# ==========================================================
# SUMMARY
# ==========================================================

def session_summary():

    original = st.session_state.original_df

    cleaned = st.session_state.cleaned_df

    summary = {

        "Rows Before": len(original),

        "Rows After": len(cleaned),

        "Rows Removed":
            len(original) - len(cleaned),

        "Columns Before":
            len(original.columns),

        "Columns After":
            len(cleaned.columns),

        "Columns Removed":
            len(original.columns)
            - len(cleaned.columns)

    }

    return summary


# ==========================================================
# HAS SESSION
# ==========================================================

def has_session():

    return (

        "original_df" in st.session_state

        and

        "cleaned_df" in st.session_state

    )