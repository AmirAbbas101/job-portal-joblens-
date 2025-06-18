from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Candidate


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "profile_img",
        ]


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = "__all__"
