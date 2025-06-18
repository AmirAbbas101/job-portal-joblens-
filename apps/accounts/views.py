from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import PasswordResetView, LoginView
from django.contrib import messages
from django.shortcuts import redirect, render, resolve_url
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, CandidateForm
from .models import Candidate
from django.urls import reverse


@method_decorator(csrf_protect, name="dispatch")
class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_job_seeker:
            return resolve_url("edit_profile")
        elif user.is_recruiter:
            return resolve_url(reverse("edit_company_profile"))
        return super().get_success_url()


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = request.POST.get("role")

            if role == "job_seeker":
                user.is_job_seeker = True
            elif role == "recruiter":
                user.is_recruiter = True

            user.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"context": form})


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        if not User.objects.filter(email=email).exists():
            messages.error(
                self.request, "Ye email registered nahi hai. Pehle account banao."
            )
            return redirect("password_reset")
        return super().form_valid(form)


def user_logout(request):
    logout(request)
    return redirect("login")


class CandidateProfileView(CreateView):
    model = Candidate
    form_class = CandidateForm
    template_name = "accounts/candidate.html"
    success_url = reverse_lazy("home")
