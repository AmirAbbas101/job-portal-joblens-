from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser, Candidate
from apps.company.models import Company


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_job_seeker:
            Candidate.objects.create(user=instance)
        elif instance.is_recruiter:
            Company.objects.create(user=instance)
