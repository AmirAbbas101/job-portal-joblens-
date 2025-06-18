from django.db import models


class Resume(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="resumes/")
    analysis_results = models.JSONField(default=list)

    def __str__(self):
        return self.file.name
