from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.text import slugify
from django.db.models import Q
from django.views.generic import ListView
from .models import Job


class JobListView(ListView):
    model = Job
    template_name = "job/browse_jobs.html"
    context_object_name = "jobs"
    paginate_by = 5

    def get_queryset(self):
        queryset = Job.all_jobs()

        # Basic search filters
        title_query = self.request.GET.get("title", "")
        location_query = self.request.GET.get("location", "")

        if title_query:
            queryset = queryset.filter(job_title__icontains=title_query)
            exact_matches = queryset.filter(job_title__iexact=title_query)
            partial_matches = queryset.exclude(
                job_id__in=exact_matches.values("job_id")
            )
            queryset = exact_matches | partial_matches

        if location_query:
            queryset = queryset.filter(location__icontains=location_query)

        # Checkbox filters (Multiple values)
        employment_types = self.request.GET.getlist("employment-type")
        if employment_types:
            queryset = queryset.filter(employment_type__in=employment_types)

        job_categories = self.request.GET.getlist("job-category")
        if job_categories:
            queryset = queryset.filter(category__in=job_categories)

        job_levels = self.request.GET.getlist("job-level")
        if job_levels:
            queryset = queryset.filter(job_level__in=job_levels)

        salary_ranges = self.request.GET.getlist("salary-range")
        if salary_ranges:
            salary_q = Q()
            for salary_range in salary_ranges:
                if salary_range == "120000-plus":
                    salary_q |= Q(salary__gte=120000)
                else:
                    try:
                        min_salary, max_salary = map(int, salary_range.split("-"))
                        salary_q |= Q(salary__gte=min_salary, salary__lte=max_salary)
                    except ValueError:
                        continue  # Skip invalid formats
            queryset = queryset.filter(salary_q)

        return queryset


def get_job_detail(request, job_id, job_title):
    job = get_object_or_404(Job, job_id=job_id)
    expected_slug = slugify(job.job_title)
    if job_title != expected_slug:
        correct_url = reverse(
            "job_detail", kwargs={"job_id": job.job_id, "job_title": expected_slug}
        )
        return HttpResponsePermanentRedirect(correct_url)

    context = {"job": job, "page_name": "jobs"}
    return render(request, "job/job_detail.html", context)
