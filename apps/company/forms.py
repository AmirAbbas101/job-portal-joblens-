from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            "company_name",
            "company_website",
            "company_address",
            "company_logo",
            "company_description",
            "company_email",
            "company_phone",
            "contact_person",
            "industry",
            "company_size",
            "established_year",
        )
