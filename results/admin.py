from django.contrib import admin

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "subject",
        "exam_type",
        "exam_date",
        "total_marks",
        "obtained_marks",
        "percentage_display",
        "grade_display",
    )

    list_filter = (
        "exam_type",
        "exam_date",
        "session",
        "classroom",
        "section",
        "subject",
    )

    search_fields = (
        "student__admission_no",
        "student__first_name",
        "student__last_name",
        "subject__name",
    )

    ordering = (
        "-exam_date",
        "student__first_name",
    )

    readonly_fields = (
        "created_at",
        "percentage_display",
        "grade_display",
    )

    @admin.display(
        description="Percentage"
    )
    def percentage_display(self, obj):

        return f"{obj.percentage}%"

    @admin.display(
        description="Grade"
    )
    def grade_display(self, obj):

        return obj.grade