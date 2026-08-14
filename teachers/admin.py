from django.contrib import admin

from .models import Teacher


# =========================================================
# TEACHER ADMIN
# =========================================================

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "first_name",
        "last_name",
        "subject",
        "qualification",
        "phone",
        "salary",
        "status",
    )

    list_filter = (
        "subject",
        "status",
        "gender",
    )

    search_fields = (
        "employee_id",
        "first_name",
        "last_name",
        "phone",
        "cnic",
        "subject",
    )

    ordering = (
        "first_name",
    )