from django.contrib import admin
from .models import Fee, FeeStructure


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):

    list_display = (
        "classroom",
        "monthly_fee",
        "admission_fee",
        "exam_fee",
    )

    search_fields = (
        "classroom__name",
    )


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "month",
        "year",
        "amount",
        "paid",
        "payment_date",
    )

    list_filter = (
        "paid",
        "month",
        "year",
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
        "student__admission_no",
    )