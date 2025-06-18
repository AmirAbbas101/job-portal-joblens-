from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.job_seeker_dashboard, name="job_seeker_dashboard"),
    path("profile/", views.get_job_seeker_profile, name="job_seeker_profile"),
    path(
        "profile/my-applications",
        views.job_seeker_applications,
        name="job_seeker_applications",
    ),
    path(
        "settings/",
        views.job_seeker_profile_settings,
        name="job_seeker_profile_settings",
    ),
]
