
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.conf import settings

def generate_result_summary_pdf(results):
    file_path = os.path.join(settings.MEDIA_ROOT, 'summaries')
    os.makedirs(file_path, exist_ok=True)
    pdf_path = os.path.join(file_path, 'result_summary.pdf')

    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter
    y = height - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, y, "Result Summary")
    y -= 30

    c.setFont("Helvetica", 10)
    for result in results:
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

        line = f"{result.student.matric_number} | {result.course.code} | {result.score} | {result.grade}"
        c.drawString(50, y, line)
        y -= 20

    c.save()
    return pdf_path
