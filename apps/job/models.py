from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.company.models import Company


# Create your models here.
class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ("Full Time", "Full-Time"),
        ("Part Time", "Part-Time"),
        ("Contact", "Contract"),
        ("Internship", "Internship"),
        ("Freelance", "Freelance"),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ("Entry Level", "Entry-Level"),
        ("Mid Level", "Mid-Level"),
        ("Senior Level", "Senior-Level"),
    ]

    STATUS_CHOICES = [
        ("OP", "Open"),
        ("CL", "Closed"),
        ("DR", "Draft"),
    ]

    job_id = models.BigAutoField(primary_key=True)
    employer = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_type = models.CharField(max_length=15, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=50)
    experience_level = models.CharField(max_length=15, choices=EXPERIENCE_LEVEL_CHOICES)
    skills_required = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="OP")
    positions = models.IntegerField()
    degree_required = models.CharField(
        max_length=200,
    )
    job_category = models.CharField(max_length=100)
    responsibilities = models.TextField()
    requirements = models.TextField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_posted"]
        verbose_name = _("Job")
        verbose_name_plural = _("Jobs")
        indexes = [
            models.Index(fields=["job_title", "location"]),
        ]

    def __str__(self):
        return f"{self.job_title} at {self.location}"

    def expired_jobs(self):
        """
        Mark jobs as expired if the application deadline has passed.
        """
        expired_jobs = Job.objects.filter(
            application_deadline__lt=timezone.now(), status="OP"
        )
        expired_jobs.update(status="EX")

    @classmethod
    def all_jobs(cls):
        """
        Return all jobs that are currently open after marking expired jobs.
        """
        cls.expired_jobs(cls)  # Call expired_jobs to update statuses
        return cls.objects.filter(status="OP")

    @classmethod
    def featured_jobs(cls):
        return cls.objects.filter(is_featured=True, status="OP")

