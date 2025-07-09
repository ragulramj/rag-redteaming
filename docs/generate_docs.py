"""Generate synthetic medical PDFs for testing."""

from fpdf import FPDF
import os

OUT_DIR = os.path.dirname(__file__)

SAMPLES = [
    {
        "patient": "Jane Doe",
        "prescription": "ExampleDrug 10mg",
        "notes": "Take one pill daily"
    },
    {
        "patient": "John Smith",
        "prescription": "SampleMed 5mg",
        "notes": "With food"
    }
]


def create_pdf(data, fname):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Synthetic patient record", ln=True)
    pdf.cell(0, 10, f"Patient: {data['patient']}", ln=True)
    pdf.cell(0, 10, f"Prescription: {data['prescription']}", ln=True)
    pdf.cell(0, 10, f"Notes: {data['notes']}", ln=True)
    pdf.output(os.path.join(OUT_DIR, fname))


def main():
    for i, info in enumerate(SAMPLES, start=1):
        create_pdf(info, f"patient_{i}.pdf")


if __name__ == '__main__':
    main()
