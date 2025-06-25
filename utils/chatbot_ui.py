from fpdf import FPDF
from io import BytesIO
import datetime

class PDFWithHeaderFooter(FPDF):
    def header(self):
        self.image("assets/header.png", x=0, y=0, w=210)  # Full A4 width
        self.set_y(30)

    def footer(self):
        self.set_y(-5)
        self.image("assets/footer.png", x=0, y=self.get_y(), w=210)

def export_prediction_to_pdf(role, inputs, risk, prob, patient_name, weight, height):
    pdf = PDFWithHeaderFooter()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=30)

    # pdf.set_font("Arial", 'B', 16)
    # pdf.ln(9)
    # pdf.cell(0, 10, "Diabetes Risk Prediction Report", ln=True, align='C')

    pdf.set_text_color(0, 51, 102)  # Dark blue (RGB)
    pdf.set_font("Arial", 'B', 22)  # Increased from 16 to 18
    pdf.ln(9)
    pdf.cell(0, 10, "Diabetes Risk Prediction Report", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)  # Reset color back to black after title


    # Summary Section
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    summary = f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}    |    User Role: {role}"
    pdf.cell(0, 10, summary, ln=True)

    # Patient Information
    pdf.set_font("Arial", 'B', 14)
    pdf.ln(6)
    pdf.cell(0, 10, "Patient Information:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Name: {patient_name}", ln=True)

    pdf.set_font("Arial", 'B', 14)
    pdf.ln(8)
    pdf.cell(0, 10, "Prediction Result:", ln=True)
    pdf.set_font("Arial", size=12)
    if risk == "High Risk":
        pdf.set_text_color(220, 50, 50)
    else:
        pdf.set_text_color(50, 150, 50)
    pdf.cell(0, 10, f"{risk} (Confidence: {prob*100:.2f}%)", ln=True)
    pdf.set_text_color(0, 0, 0)

    # Input Data in Two Columns
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Data Received:", ln=True)
    pdf.set_font("Arial", size=12)

    feature_names = [
    ("Weight (kg)", weight),
    ("Height (cm)", height),
    ("Pregnancies", inputs[0]),
    ("Glucose", inputs[1]),
    ("BloodPressure", inputs[2]),
    ("SkinThickness", inputs[3]),
    ("Insulin", inputs[4]),
    ("BMI", inputs[5]),
    ("DiabetesPedigreeFunction", inputs[6]),
    ("Age", inputs[7]),
]


    col1_x = 15
    col2_x = 110
    y_start = pdf.get_y()
    row_height = 8

    for i, (name, value) in enumerate(feature_names):

        x = col1_x if i < len(feature_names) / 2 else col2_x
        y = y_start + (i % (len(feature_names) // 2)) * row_height
        pdf.set_xy(x, y)
        pdf.cell(90, row_height, f"{name}: {value}", ln=0)

    pdf.set_y(y + row_height + 5)

    # Optional interpretation text
    if pdf.get_y() > 230:  # adjust threshold as needed
        pdf.add_page()

    pdf.set_font("Arial", 'B', 14)
    pdf.ln(5)
    pdf.cell(0, 10, "Interpretation:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, "This prediction is based on health metrics you entered. Please consult a healthcare professional for a full diagnosis and treatment plan.")

    # Export to PDF
    pdf_output = pdf.output(dest='S').encode('latin1')
    return BytesIO(pdf_output)


