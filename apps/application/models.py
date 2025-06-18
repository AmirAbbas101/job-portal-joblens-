# your_app_name/models.py
from django.conf import settings
from django.db import models
from apps.job.models import Job


class Application(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("reviewing", "Under Review"),
        ("interview", "Interview Scheduled"),
        ("rejected", "Rejected"),
        ("accepted", "Accepted"),
    ]

    INTERVIEW_TYPE_CHOICES = [
        ("phone", "Phone Interview"),
        ("video", "Video Interview"),
        ("onsite", "On-site Interview"),
        ("technical", "Technical Interview"),
        ("final", "Final Round Interview"),
        ("screening", "Screening Interview"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # New fields for interview details
    interview_date = models.DateField(null=True, blank=True)
    interview_time = models.TimeField(null=True, blank=True)
    interview_type = models.CharField(
        max_length=20, choices=INTERVIEW_TYPE_CHOICES, null=True, blank=True
    )
    interview_meeting_link = models.URLField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ("user", "job")
        ordering = ["-applied_at"]

    def __str__(self):
        return f"{self.user} → {self.job.job_title} ({self.status})"
