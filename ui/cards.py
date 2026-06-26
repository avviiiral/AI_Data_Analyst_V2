import streamlit as st


def kpi_card(title, value, icon):

    st.markdown(
        f"""
        <div class="kpi-card">

        <div class="icon">{icon}</div>

        <div class="value">{value}</div>

        <div class="title">{title}</div>

        </div>
        """,
        unsafe_allow_html=True
    )