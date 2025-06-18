from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from apps.job.models import Job
from apps.utils.decorators import recruiter

from .forms import CompanyForm
from .models import Company


@login_required
def edit_company_profile(request):
    """
    Handles both creating a new company profile and editing an existing one.
    """
    try:
        company = request.user.company
        is_new = False
    except ObjectDoesNotExist:
        company = None
        is_new = True

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            print(f"This is testing message {company.company_name}")
            return redirect(
                "company_profile", company.company_name
            )  # Redirect to the company profile view
    else:
        form = CompanyForm(instance=company)

    return render(
        request,
        "company/edit_company_profile.html",
        {"form": form, "is_new": is_new},
    )


def company_profile(request, id, company_name):
    """
    Displays the company profile along with jobs posted by the specific company.
    """
    company = get_object_or_404(Company, id=id)
    jobs = Job.objects.filter(company=company)  # Only this company's jobs

    return render(
        request, "company/company_profile.html", {"company": company, "jobs": jobs}
    )


# @recruiter
@login_required
def post_job(request, user_id):
    if request.method == "POST":
        job_title = request.POST.get("job-title")
        job_description = request.POST.get("job-description")
        job_type = request.POST.get("job-type")
        location = request.POST.get("location")
        salary_range = request.POST.get("salary-range")
        experience_level = request.POST.get("experience-level")
        skills_required = request.POST.get("skills-required")
        application_deadline = request.POST.get("application-deadline")
        job_category = request.POST.get("job-category")
        responsibilities = request.POST.get("responsibilities")
        positions = request.POST.get("positions")
        requirements = request.POST.get("requirements")
        is_featured = request.POST.get("is-featured")
        employer = request.user
        company = get_object_or_404(Company, user=employer)
        Job.objects.create(
            employer=employer,
            company=company,
            job_title=job_title,
            job_description=job_description,
            job_type=job_type,
            location=location,
            salary_range=salary_range,
            experience_level=experience_level,
            skills_required=skills_required,
            application_deadline=application_deadline,
            job_category=job_category,
            responsibilities=responsibilities,
            positions=positions,
            requirements=requirements,
            is_featured=is_featured,
        )
        return redirect(reverse_lazy("home"))
    return render(request, "company/post_new_job.html")


@login_required
def company_dashboard(request):
    page_name = "Dashboard"
    return render(request, "company/company_dashboard.html", {"page_name": page_name})
