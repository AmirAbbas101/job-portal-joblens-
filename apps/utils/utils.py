from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import FileResponse
import nltk
from nltk.corpus import stopwords


def generate_pdf_report(results):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Resume Analysis Report")

    y = 770
    for line in results:
        p.drawString(80, y, f"- {line}")
        y -= 20

    p.save()
    buffer.seek(0)
    return buffer


nltk.download("stopwords")


def analyze_keywords(text):
    keywords = [
        "Python",
        "Django",
        "Tailwind",
        "REST",
        "SQL",
        "HTML",
        "JavaScript",
        "Linux",
        "Git",
    ]
    words = text.lower().split()
    words = [w for w in words if w not in stopwords.words("english")]

    results = []
    for kw in keywords:
        score = words.count(kw.lower())
        if score:
            results.append(f"{kw}: Found {score} time(s)")
        else:
            results.append(f"{kw}: Not found")
    return results
