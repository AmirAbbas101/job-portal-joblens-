from django.urls import path
from . import views

urlpatterns = [
    path("", views.JobListView.as_view(), name="job_list"),
    path(
        "<int:job_id>/<slug:job_title>/",
        views.get_job_detail,
        name="job_detail",
    ),
]
