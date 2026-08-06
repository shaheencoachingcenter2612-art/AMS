from django.contrib import admin
from .models import Session, ClassRoom, Section, Subject


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "start_year",
        "end_year",
        "is_active",
    )


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "classroom",
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )