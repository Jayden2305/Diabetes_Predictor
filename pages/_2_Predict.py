import streamlit as st
import numpy as np
import joblib
import json
from utils.pdf_export import export_prediction_to_pdf
from utils.style import set_bg_from_local

# Set background
set_bg_from_local("assets/predict_bg.png")



# --- Load model and median values ---
model = joblib.load("model/model.pkl")
with open("model/median_values.json", "r") as f:
    median_values = json.load(f)

# --- Title and description ---
st.markdown("<h2 style='font-size: 48px;'>🧪 Diabetes Risk Assessment</h2>", unsafe_allow_html=True)
st.markdown("#### Fill in the correct values to enable accurate predictions.")



# --- Get role from session state ---
role = st.session_state.get("user_role", "Normal User")
is_provider = role == "Healthcare Provider"

st.markdown("<hr>", unsafe_allow_html=True)

# --- Input layout ---
col1, col2 = st.columns(2)

def get_input(label, key, default, is_visible=True, help_text=""):
    if is_visible:
        with col1 if key in ["Pregnancies", "BloodPressure", "SkinThickness", "BMI"] else col2:
            return st.number_input(
                f"{label}", min_value=0.0, value=float(default), step=1.0,
                key=f"input_{key}", help=help_text
            )
    else:
        return float(median_values[key])

# --- Input fields ---
pregnancies = get_input("Pregnancies", "Pregnancies", 1,
                        help_text="Number of times you have been pregnant")

glucose = get_input("Glucose Level", "Glucose", 120,
                    help_text="Plasma glucose level in mg/dL (Normal < 140)")

blood_pressure = get_input("Blood Pressure", "BloodPressure", 70,
                           help_text="Diastolic blood pressure in mm Hg (Normal ~80)")

skin_thickness = get_input("Skin Thickness", "SkinThickness", 20, is_provider,
                           help_text="Triceps skin fold thickness in mm")

insulin = get_input("Insulin Level", "Insulin", 80, is_provider,
                    help_text="2-Hour serum insulin in mu U/mL")

bmi = get_input("BMI", "BMI", 25.0,
                help_text="Body Mass Index (kg/m²). Normal: 18.5–24.9")

dpf = get_input("Diabetes Pedigree Function", "DiabetesPedigreeFunction", 0.5, is_provider,
                help_text="Genetic likelihood of diabetes (0 to 2)")

age = get_input("Age", "Age", 30,
                help_text="Age in years")

st.markdown("<hr>", unsafe_allow_html=True)

# --- Prediction ---
if st.button("🔍 Predict", key="predict_btn"):
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                            insulin, bmi, dpf, age]])

    prediction = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][prediction]

    if prediction == 1:
        st.error(f"⚠️ High Risk of Diabetes\nConfidence: {prob*100:.2f}%")
        risk = "High Risk"
    else:
        st.success(f"✅ Low Risk of Diabetes\nConfidence: {prob*100:.2f}%")
        risk = "Low Risk"

    # Export to PDF
    pdf_data = export_prediction_to_pdf(role, input_data.flatten(), risk, prob)
    st.download_button(
        label="📄 Download Prediction Report",
        data=pdf_data,
        file_name="diabetes_prediction_result.pdf",
        mime="application/pdf",
        key="download_pdf"
    )
