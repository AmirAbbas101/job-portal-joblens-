from django.urls import path
from . import views

urlpatterns = [
    path(
        "edit-company-porfile/", views.edit_company_profile, name="edit_company_profile"
    ),
    path("dashboard/", views.company_dashboard, name="company_dashboard"),
    path(
        "profile/<int:id>/<str:company_name>/",
        views.company_profile,
        name="company_profile",
    ),
    path("post-job/<int:user_id>", views.post_job, name="post_job"),
]
