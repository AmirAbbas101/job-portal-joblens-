from django.contrib import admin
from .models import CustomUser, Candidate

admin.site.register(CustomUser)
admin.site.register(Candidate)
