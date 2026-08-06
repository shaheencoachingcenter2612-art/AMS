from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        "admission_no",
        "first_name",
        "father_name",
        "classroom",
        "section",
        "phone",
        "admission_date",
    )

    list_filter = (
        "session",
        "classroom",
        "section",
        "gender",
    )

    search_fields = (
        "admission_no",
        "first_name",
        "last_name",
        "father_name",
        "phone",
    )