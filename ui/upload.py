import streamlit as st

def upload_section():

    st.markdown("""
<div class="upload-card">

<h2>📂 Upload Dataset</h2>

<p>
Supports CSV, Excel and JSON files.
</p>

</div>
""", unsafe_allow_html=True)

    return st.file_uploader(
        "",
        type=["csv", "xlsx", "json"]
    )