from utils import db
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def gen_prescription(created_prescription):
    patient_id = created_prescription["patient_id"]
    patient_obj = db.get_patient_by_id(patient_id)
    doctor_id = created_prescription["doctor_id"]
    doctor_obj = db.get_doctor_by_id(doctor_id)

    date = datetime.now().strftime("%d-%m-%Y")
    pdf_path = f"/tmp/prescription_{patient_id}_{date}.pdf"
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica", 14)

    c.drawString(50, 750, f"Prescription ID: {created_prescription['_id']}")
    c.drawString(50, 730, f"Patient ID: {patient_id}")
    c.drawString(50, 710, f"Patient Name: {patient_obj['name']}")
    c.drawString(50, 690, f"Doctor ID: {doctor_id}")
    c.drawString(50, 670, f"Doctor Name: {doctor_obj['name']}")
    c.drawString(50, 650, "Medications:")

    y_offset = 620
    for index, medication in enumerate(created_prescription['medication'], start=1):
        c.drawString(70, y_offset, f"{index}. Medication Name: {medication['name']}")
        c.drawString(70, y_offset - 20, f"   Dosage: {medication['dosage']}")
        c.drawString(70, y_offset - 40, f"   Instructions: {medication['instructions']}")
        y_offset -= 60

    c.drawString(50, y_offset, f"Diagnosis: {created_prescription['diagnosis']}")
    c.drawString(50, y_offset - 20, f"Date Prescribed: {created_prescription['created_at']}")

    c.save()
    return pdf_path
