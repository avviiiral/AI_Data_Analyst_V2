import streamlit as st


def render_sidebar():

    with st.sidebar:

        #st.image("assets/logo.png", width=70)

        st.title("AI Data Analyst V2")

        st.markdown("---")

        st.markdown("## 📬 Feedback")

        st.markdown(
            """
📧 **Email**

avialgoyal739@gmail.com

💼 **LinkedIn**

https://linkedin.com/in/avviiiral
"""
        )

        st.markdown("---")

        st.success("⭐ Star this project on GitHub!")