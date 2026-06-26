import streamlit as st

from core.data_loader import load_data

from ui.pages.overview import render_overview
from ui.pages.analytics import render_analytics
from ui.pages.dashboard import render_dashboard
from ui.pages.copilot import render_copilot
from ui.pages.reports import render_reports


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Data Analyst V2",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# HEADER
# =====================================================

st.title("📊 AI Data Analyst V2")
st.caption(
    "Upload any CSV, Excel or JSON dataset and explore it using AI-powered analytics."
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(

    "Select Page",

    [

        "🏠 Overview",

        "📊 Analytics",

        "📈 Dashboard",

        "🤖 AI Copilot",

        "📄 Reports"

    ]

)

st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader(

    "Upload Dataset",

    type=[

        "csv",

        "xlsx",

        "json"

    ]

)

# =====================================================
# LOAD DATA
# =====================================================

if uploaded_file is None:

    st.info("Upload a dataset from the sidebar to begin.")

    st.stop()

try:

    df = load_data(uploaded_file)

except Exception as e:

    st.error(str(e))

    st.stop()

# =====================================================
# PAGE ROUTER
# =====================================================

if page == "🏠 Overview":

    render_overview(df)

elif page == "📊 Analytics":

    render_analytics(df)

elif page == "📈 Dashboard":

    render_dashboard(df)

elif page == "🤖 AI Copilot":

    render_copilot(df)

elif page == "📄 Reports":

    render_reports(df)