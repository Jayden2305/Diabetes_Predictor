from fpdf import FPDF
import datetime
from io import BytesIO

def export_prediction_to_pdf(role, inputs, risk, prob):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Diabetes Risk Prediction Report", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"User Role: {role}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Input Data:", ln=True)
    pdf.set_font("Arial", size=12)

    feature_names = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                     "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]

    for name, value in zip(feature_names, inputs):
        pdf.cell(0, 10, f"{name}: {value}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Prediction Result:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(220, 50, 50) if risk == "High Risk" else pdf.set_text_color(50, 150, 50)
    pdf.cell(0, 10, f"{risk} (Confidence: {prob*100:.2f}%)", ln=True)

    # Output as bytes
    pdf_buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_output)
    pdf_buffer.seek(0)
    return pdf_buffer
