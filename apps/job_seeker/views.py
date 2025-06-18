from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from apps.application.models import Application

User = get_user_model()


@login_required
def job_seeker_dashboard(request):
    user = request.user

    # Calculate date range for dashboard stats (last 7 days)
    current_date = timezone.localdate()
    one_week_ago = current_date - timedelta(days=7)
    one_week_later = current_date + timedelta(days=7)

    # --- Stats Calculation ---
    total_applications = Application.objects.filter(user=user).count()

    # Applications in the last week
    applications_last_week = Application.objects.filter(
        user=user, applied_at__gte=one_week_ago, applied_at__lte=current_date
    ).count()

    # Applications before last week to calculate percentage change
    applications_before_last_week = Application.objects.filter(
        user=user,
        applied_at__lt=one_week_ago - timedelta(days=7),  # Compare with the week before
        applied_at__gte=one_week_ago - timedelta(days=14),
    ).count()

    percentage_change_applications = 0
    if applications_before_last_week > 0:
        percentage_change_applications = (
            (applications_last_week - applications_before_last_week)
            / applications_before_last_week
        ) * 100
    elif applications_last_week > 0:
        percentage_change_applications = (
            100  # If no applications before, but some now, it's a 100% increase
        )

    # Interviews
    interviews_scheduled = Application.objects.filter(
        user=user,
        status="interview",
        interview_date__gte=timezone.localdate(),  # Only upcoming interviews
    ).count()

    # Offers (assuming 'accepted' status for offers)
    offers_received = Application.objects.filter(user=user, status="accepted").count()
    new_offers_this_week = Application.objects.filter(
        user=user,
        status="accepted",
        updated_at__gte=one_week_ago,  # Assuming updated_at changes when status is updated to accepted
        updated_at__lte=current_date,
    ).count()

    # Rejections
    rejections = Application.objects.filter(user=user, status="rejected").count()

    rejection_percentage = 0
    if total_applications > 0:
        rejection_percentage = (rejections / total_applications) * 100

    # --- Application Status Chart Data (Dummy/Placeholder) ---
    # For a real chart, you'd fetch data grouped by status and perhaps time.
    # This is a placeholder, you'd integrate with a JS charting library on the frontend.
    application_status_data = (
        Application.objects.filter(user=user)
        .values("status")
        .annotate(count=Count("status"))
    )
    # Example output: [{'status': 'applied', 'count': 10}, {'status': 'interview', 'count': 3}]

    # --- Upcoming Interviews ---
    upcoming_interviews = Application.objects.filter(
        user=user,
        status="interview",
        interview_date__gte=timezone.localdate(),  # Filter for today or future dates
    ).order_by("interview_date", "interview_time")[
        :3
    ]  # Get up to 3 upcoming interviews

    # --- Recent Applications ---
    recent_applications = Application.objects.filter(user=user).order_by("-applied_at")[
        :5
    ]  # Get up to 5 recent applications

    context = {
        "current_date": current_date,
        "one_week_later": one_week_later,
        "total_applications": total_applications,
        "percentage_change_applications": round(percentage_change_applications)
        if applications_before_last_week > 0
        else 0,  # Round for display
        "interviews_scheduled": interviews_scheduled,
        "offers_received": offers_received,
        "new_offers_this_week": new_offers_this_week,
        "rejections": rejections,
        "rejection_percentage": round(rejection_percentage, 2),
        "application_status_data": application_status_data,  # Pass for potential chart use
        "upcoming_interviews": upcoming_interviews,
        "recent_applications": recent_applications,
        "page_name": "Dashboard",
    }
    return render(request, "job_seeker/dashboard.html", context)


@login_required
def get_job_seeker_profile(request):
    user_id = request.user.id
    user = get_object_or_404(User, pk=user_id)
    # data = Candidate.objects.get(id=user_id)

    page_name = "My Profile"
    return render(
        request,
        "job_seeker/profile.html",
        {"page_name": page_name, "user": user},
    )


@login_required
def job_seeker_profile_settings(request):
    return render(
        request,
        "job_seeker/settings.html",
        {"page_name": "Settings", "active_section": "my_profile"},
    )


# def job_seeker_applications(request):
#     return render(
#         request, "job_seeker/my_applications.html", {"page_name": "My Applications"}
#     )


@login_required
def job_seeker_applications(request):
    user = request.user

    # Calculate date range for display (optional, can be adjusted)
    current_date = timezone.localdate()
    # Using specific dates as in your frontend example, adjust as needed
    start_date = timezone.datetime(2023, 7, 19).date()
    end_date = timezone.datetime(2023, 7, 25).date()

    # Get all applications for the current user
    applications = (
        Application.objects.filter(user=user)
        .select_related("job__company")
        .order_by("-applied_at")
    )

    # Get counts for each status for the navigation buttons
    status_counts = applications.values("status").annotate(count=Count("status"))
    status_count_dict = {item["status"]: item["count"] for item in status_counts}

    # Prepare counts for frontend display
    total_applications_count = applications.count()
    in_review_count = status_count_dict.get(
        "reviewing", 0
    )  # 'reviewing' from your STATUS_CHOICES
    interview_count = status_count_dict.get(
        "interview", 0
    )  # 'interview' from your STATUS_CHOICES
    offered_count = status_count_dict.get(
        "accepted", 0
    )  # 'accepted' from your STATUS_CHOICES
    hired_count = status_count_dict.get(
        "accepted", 0
    )  # Assuming 'accepted' means hired, adjust if you have a separate 'hired' status

    # Determine active filter (e.g., from a query parameter)
    # This allows you to filter applications displayed on the page
    filter_status = request.GET.get("status")
    if filter_status and filter_status != "all":
        if (
            filter_status == "assessment"
        ):  # Map 'assessment' from frontend to 'interview' in backend
            applications = applications.filter(status="interview")
        elif (
            filter_status == "offered"
        ):  # Map 'offered' from frontend to 'accepted' in backend
            applications = applications.filter(status="accepted")
        elif (
            filter_status == "hired"
        ):  # Map 'hired' from frontend to 'accepted' in backend
            applications = applications.filter(status="accepted")
        else:
            applications = applications.filter(status=filter_status)

    context = {
        "user": user,
        "page_name": "My Applications",
        "start_date": start_date,
        "end_date": end_date,
        "applications": applications,
        "total_applications_count": total_applications_count,
        "in_review_count": in_review_count,
        "assessment_count": interview_count,  # Using interview_count for assessment
        "offered_count": offered_count,
        "hired_count": hired_count,
        "active_filter": filter_status
        if filter_status
        else "all",  # Pass the active filter to highlight buttons
    }
    return render(request, "job_seeker/my_applications.html", context)
