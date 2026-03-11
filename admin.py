from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from .models import Job,Application

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ("Role Information", {
            "fields": ("contact_number", "is_candidate", "is_interviewer"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Role Information", {
            "fields": ("contact_number", "is_candidate", "is_interviewer"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Job)
admin.site.register(Application)