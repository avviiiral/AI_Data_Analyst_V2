import streamlit as st


def render_feature_cards():

    st.markdown(
        """
<style>

.features{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:18px;
    margin-top:20px;
    margin-bottom:35px;
}

.feature-card{

    background:#161d2d;

    border:1px solid #273449;

    border-radius:18px;

    padding:22px;

    text-align:center;

    transition:.35s;

    box-shadow:0px 8px 20px rgba(0,0,0,.25);

}

.feature-card:hover{

    transform:translateY(-8px);

    border-color:#3b82f6;

    box-shadow:0px 15px 35px rgba(59,130,246,.35);

}

.feature-icon{

    font-size:42px;

    margin-bottom:10px;

}

.feature-title{

    color:white;

    font-size:22px;

    font-weight:700;

    margin-bottom:10px;

}

.feature-text{

    color:#94a3b8;

    font-size:15px;

}

@media(max-width:1100px){

.features{

grid-template-columns:repeat(2,1fr);

}

}

@media(max-width:700px){

.features{

grid-template-columns:1fr;

}

}

</style>


<div class="features">

<div class="feature-card">

<div class="feature-icon">📊</div>

<div class="feature-title">
Smart Analysis
</div>

<div class="feature-text">
Automatically profile and understand any dataset.
</div>

</div>


<div class="feature-card">

<div class="feature-icon">🧠</div>

<div class="feature-title">
AI Analyst
</div>

<div class="feature-text">
Ask questions in natural language and receive instant insights.
</div>

</div>


<div class="feature-card">

<div class="feature-icon">📈</div>

<div class="feature-title">
Forecasting
</div>

<div class="feature-text">
Predict future trends using built-in machine learning models.
</div>

</div>


<div class="feature-card">

<div class="feature-icon">🚀</div>

<div class="feature-title">
Business Insights
</div>

<div class="feature-text">
Generate executive summaries and discover key business drivers.
</div>

</div>

</div>

""",
        unsafe_allow_html=True
    )