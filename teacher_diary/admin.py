from django.contrib import admin

from .models import DiaryEntry


@admin.register(DiaryEntry)
class DiaryEntryAdmin(admin.ModelAdmin):

    list_display = (
        "teacher",
        "date",
        "classroom",
        "section",
        "subject",
        "topic",
    )

    list_filter = (
        "date",
        "teacher",
        "subject",
        "classroom",
        "section",
    )

    search_fields = (
        "teacher__first_name",
        "teacher__last_name",
        "teacher__employee_id",
        "subject",
        "topic",
        "description",
    )

    ordering = (
        "-date",
        "-id",
    )