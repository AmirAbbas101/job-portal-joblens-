from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.text import slugify

from .models import Application
from .forms import ApplicationForm
from apps.job.models import Job


class ApplyJobView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "application/apply.html"

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(Job, pk=self.kwargs["job_id"])

        # Prevent duplicate application
        if Application.objects.filter(user=self.request.user, job=self.job).exists():
            messages.warning(request, "You’ve already applied for this job.")
            return redirect(
                "job_detail",
                job_id=self.job.job_id,
                job_title=slugify(self.job.job_title),
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.job = self.job
        messages.success(self.request, "Application submitted successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "job_detail",
            kwargs={
                "job_id": self.job.job_id,
                "job_title": slugify(self.job.job_title),
            },
        )
