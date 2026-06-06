from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(report_text, filename):
    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("Smart Label Quality Report", styles["Title"])
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(report_text.replace("\n", "<br/>"), styles["BodyText"])
    )

    pdf.build(content)

    return filename