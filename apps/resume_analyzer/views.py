# resume/views.py
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
from .models import Resume
from apps.utils.utils import analyze_keywords, generate_pdf_report

from django.http import FileResponse


def resume_upload(request):
    results = None

    if "download" in request.POST:
        pdf_buffer = generate_pdf_report(results)
        return FileResponse(
            pdf_buffer, as_attachment=True, filename="resume_report.pdf"
        )

    if request.method == "POST" and request.FILES["resume"]:
        uploaded_file = request.FILES["resume"]
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Save resume to DB
        resume = Resume.objects.create(file=uploaded_file)

        # Extract text
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        # Analyze
        results = analyze_keywords(text)
        resume.analysis_results = results
        resume.save()

        return render(
            request, "resume_analyzer/resume_upload.html", {"results": results}
        )

    return render(request, "resume_analyzer/resume_upload.html")
