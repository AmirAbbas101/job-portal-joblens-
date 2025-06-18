from django.shortcuts import render
from apps.job.models import Job


def home(request):
    featured_jobs = Job.featured_jobs()
    jobs = Job.all_jobs()
    companies = ["intel", "intel", "intel", "intel"]
    context = {
        "jobs": jobs,
        "featured_jobs": featured_jobs,
        "companies": companies,
        "page_name": "home",
    }
    return render(request, "home/home.html", context)


def about(request):
    return render(request, "about.html")
