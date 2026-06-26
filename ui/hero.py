import streamlit as st

def render_hero():

    st.markdown("""
<div class="hero">

<h1>🤖 AI Data Analyst Agent V2</h1>

<p>
Transform raw datasets into actionable business insights using AI.
</p>

<div class="hero-badges">

<span>📊 Dashboard</span>

<span>📈 Forecast</span>

<span>🧠 AI Analyst</span>

<span>🚨 Anomaly Detection</span>

</div>

</div>
""", unsafe_allow_html=True)