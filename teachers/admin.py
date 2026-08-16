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
        "user",
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
        "father_name",
        "phone",
        "cnic",
        "subject",
        "qualification",
    )

    ordering = (
        "first_name",
        "last_name",
    )

    list_per_page = 25