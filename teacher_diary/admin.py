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
        "classroom",
        "subject",
    )


    search_fields = (
        "teacher__first_name",
        "teacher__last_name",
        "subject",
        "topic",
    )


    ordering = (
        "-date",
    )