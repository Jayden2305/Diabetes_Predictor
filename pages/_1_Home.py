import streamlit as st
import pandas as pd
from utils.style import set_bg_from_local

set_bg_from_local("assets/home_bg.png")

# --- HEADER ---
st.markdown("""
    <h1 style='text-align: center; font-size: 3em;'>🩺 Welcome to the Diabetes Risk Predictor</h1>
    <h3 style='text-align: center;'>Empowering users with data-driven predictions</h3>
    <hr style='border: 1px solid #ccc;'>
""", unsafe_allow_html=True)

# --- WELCOME CARD ---
st.markdown("""
<div style='display: flex; justify-content: center; margin-top: 2em;'>
    <div style='max-width: 850px; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);'>
        <p style='font-size: 1.3em; text-align: justify;'>
            This app uses a machine learning model trained on a real diabetes dataset to estimate your risk of developing diabetes based on health parameters.
        </p>
        <ul style='font-size: 1.1em; line-height: 1.6;'>
            <li><b>Pregnancies</b>: Number of pregnancies (for female patients).</li>
            <li><b>Glucose</b>: Plasma glucose concentration (mg/dL).</li>
            <li><b>Blood Pressure</b>: Diastolic blood pressure (mmHg).</li>
            <li><b>BMI</b>: Body Mass Index (kg/m²).</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- User Role Selection ---
user_type = st.selectbox("👤 Who are you?", ["Normal User", "Healthcare Provider"])
st.session_state["user_role"] = user_type

if st.button("Proceed to Prediction ➡️"):
    st.switch_page("pages/_2_Predict.py")

