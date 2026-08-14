from django.contrib import admin
from .models import Fee, FeeStructure


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):

    list_display = (
        "classroom",
        "monthly_fee",
        "admission_fee",
        "registration_fee",
        "exam_fee",
    )

    search_fields = (
        "classroom__name",
    )


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):

    list_display = (
        "receipt_no",
        "student",
        "month",
        "year",
        "total_amount",
        "amount_paid",
        "remaining_amount",
        "paid",
        "payment_date",
        "payment_method",
    )

    list_filter = (
        "paid",
        "month",
        "year",
        "payment_method",
    )

    search_fields = (
        "receipt_no",
        "student__first_name",
        "student__last_name",
        "student__admission_no",
    )

    ordering = (
        "-id",
    )