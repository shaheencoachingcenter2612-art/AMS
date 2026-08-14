from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Fee, FeeStructure
from .forms import FeeForm, FeeStructureForm

from accounts.utils import role_required


# =========================================================
# FEE DASHBOARD
# SUPER ADMIN + ACCOUNTANT + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Accountant", "Vice Principal")
def fee_dashboard(request):

    total_fees = Fee.objects.count()

    total_amount = Fee.objects.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    total_paid = Fee.objects.aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    total_remaining = Fee.objects.aggregate(
        total=Sum("remaining_amount")
    )["total"] or 0

    paid_fees = Fee.objects.filter(
        paid=True
    ).count()

    unpaid_fees = Fee.objects.filter(
        paid=False
    ).count()

    today = timezone.localdate()

    today_fees = Fee.objects.filter(
        payment_date=today
    )

    today_collected = today_fees.aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    month_summary = Fee.objects.values(
        "month"
    ).annotate(
        total=Count("id"),
        collected=Sum("amount_paid")
    ).order_by("month")

    recent_fees = Fee.objects.select_related(
        "student"
    ).order_by("-id")[:5]

    return render(
        request,
        "fee_management/fee_dashboard.html",
        {
            "total_fees": total_fees,
            "total_amount": total_amount,
            "total_paid": total_paid,
            "total_remaining": total_remaining,
            "paid_fees": paid_fees,
            "unpaid_fees": unpaid_fees,
            "today_collected": today_collected,
            "month_summary": month_summary,
            "recent_fees": recent_fees,
        }
    )


# =========================================================
# ADD FEE
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def add_fee(request):

    if request.method == "POST":

        form = FeeForm(request.POST)

        if form.is_valid():

            fee = form.save()

            messages.success(
                request,
                "Fee added successfully."
            )

            return redirect(
                "fee_management:fee_detail",
                pk=fee.pk
            )

    else:

        form = FeeForm()

    return render(
        request,
        "fee_management/add_fee.html",
        {
            "form": form,
            "edit_mode": False,
        }
    )


# =========================================================
# FEE LIST
# SUPER ADMIN + ACCOUNTANT + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Accountant", "Vice Principal")
def fee_list(request):

    query = request.GET.get("q", "")
    month = request.GET.get("month", "")
    year = request.GET.get("year", "")
    payment_method = request.GET.get("payment_method", "")
    paid = request.GET.get("paid", "")

    fees = Fee.objects.select_related("student")

    if query:

        fees = fees.filter(
            Q(receipt_no__icontains=query) |
            Q(student__admission_no__icontains=query) |
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query)
        )

    if month:
        fees = fees.filter(month=month)

    if year:
        fees = fees.filter(year=year)

    if payment_method:
        fees = fees.filter(payment_method=payment_method)

    if paid == "paid":

        fees = fees.filter(paid=True)

    elif paid == "unpaid":

        fees = fees.filter(paid=False)

    fees = fees.order_by("-id")

    return render(
        request,
        "fee_management/fee_list.html",
        {
            "fees": fees,
            "query": query,
            "month": month,
            "year": year,
            "payment_method": payment_method,
            "paid": paid,
            "month_choices": Fee.MONTH_CHOICES,
            "payment_methods": Fee.PAYMENT_METHODS,
        }
    )


# =========================================================
# FEE DETAIL
# SUPER ADMIN + ACCOUNTANT + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Accountant", "Vice Principal")
def fee_detail(request, pk):

    fee = get_object_or_404(
        Fee.objects.select_related("student"),
        pk=pk
    )

    return render(
        request,
        "fee_management/fee_detail.html",
        {
            "fee": fee
        }
    )


# =========================================================
# EDIT FEE
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def edit_fee(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk
    )

    if request.method == "POST":

        form = FeeForm(
            request.POST,
            instance=fee
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee updated successfully."
            )

            return redirect(
                "fee_management:fee_detail",
                pk=fee.pk
            )

    else:

        form = FeeForm(
            instance=fee
        )

    return render(
        request,
        "fee_management/add_fee.html",
        {
            "form": form,
            "fee": fee,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE FEE
# SUPER ADMIN ONLY
# =========================================================

@login_required
@role_required("Super Admin")
def delete_fee(request, pk):

    fee = get_object_or_404(
        Fee,
        pk=pk
    )

    if request.method == "POST":

        fee.delete()

        messages.success(
            request,
            "Fee deleted successfully."
        )

        return redirect(
            "fee_management:fee_list"
        )

    return render(
        request,
        "fee_management/delete_fee.html",
        {
            "fee": fee
        }
    )


# =========================================================
# FEE STRUCTURE LIST
# SUPER ADMIN + ACCOUNTANT + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Accountant", "Vice Principal")
def fee_structure_list(request):

    structures = FeeStructure.objects.select_related(
        "classroom"
    ).order_by(
        "classroom__name"
    )

    return render(
        request,
        "fee_management/fee_structure_list.html",
        {
            "structures": structures
        }
    )


# =========================================================
# ADD FEE STRUCTURE
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def add_fee_structure(request):

    if request.method == "POST":

        form = FeeStructureForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee structure added successfully."
            )

            return redirect(
                "fee_management:fee_structure_list"
            )

    else:

        form = FeeStructureForm()

    return render(
        request,
        "fee_management/add_fee_structure.html",
        {
            "form": form
        }
    )


# =========================================================
# EDIT FEE STRUCTURE
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def edit_fee_structure(request, pk):

    structure = get_object_or_404(
        FeeStructure,
        pk=pk
    )

    if request.method == "POST":

        form = FeeStructureForm(
            request.POST,
            instance=structure
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Fee structure updated successfully."
            )

            return redirect(
                "fee_management:fee_structure_list"
            )

    else:

        form = FeeStructureForm(
            instance=structure
        )

    return render(
        request,
        "fee_management/add_fee_structure.html",
        {
            "form": form,
            "structure": structure,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE FEE STRUCTURE
# SUPER ADMIN ONLY
# =========================================================

@login_required
@role_required("Super Admin")
def delete_fee_structure(request, pk):

    structure = get_object_or_404(
        FeeStructure,
        pk=pk
    )

    if request.method == "POST":

        structure.delete()

        messages.success(
            request,
            "Fee structure deleted successfully."
        )

        return redirect(
            "fee_management:fee_structure_list"
        )

    return render(
        request,
        "fee_management/delete_fee_structure.html",
        {
            "structure": structure
        }
    )


# =========================================================
# PRINT FEE RECEIPT
# SUPER ADMIN + ACCOUNTANT + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Accountant", "Vice Principal")
def print_fee_receipt(request, pk):

    fee = get_object_or_404(
        Fee.objects.select_related("student"),
        pk=pk
    )

    return render(
        request,
        "fee_management/print_fee_receipt.html",
        {
            "fee": fee
        }
    )


# =========================================================
# FEE REPORT
# SUPER ADMIN + ACCOUNTANT + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Accountant", "Vice Principal")
def fee_report(request):

    query = request.GET.get("q", "").strip()
    month = request.GET.get("month", "").strip()
    year = request.GET.get("year", "").strip()
    payment_method = request.GET.get(
        "payment_method",
        ""
    ).strip()
    paid = request.GET.get("paid", "").strip()

    fees = Fee.objects.select_related(
        "student"
    ).all()

    # SEARCH
    if query:

        fees = fees.filter(
            Q(receipt_no__icontains=query) |
            Q(student__admission_no__icontains=query) |
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query)
        )

    # MONTH
    if month:
        fees = fees.filter(
            month=month
        )

    # YEAR
    if year:
        fees = fees.filter(
            year=year
        )

    # PAYMENT METHOD
    if payment_method:
        fees = fees.filter(
            payment_method=payment_method
        )

    # PAYMENT STATUS
    if paid == "paid":

        fees = fees.filter(
            paid=True
        )

    elif paid == "unpaid":

        fees = fees.filter(
            paid=False
        )

    # SUMMARY
    summary = fees.aggregate(
        total_amount=Sum("total_amount"),
        total_paid=Sum("amount_paid"),
        total_remaining=Sum("remaining_amount"),
    )

    return render(
        request,
        "fee_management/fee_report.html",
        {
            "fees": fees.order_by("-id"),

            "query": query,
            "month": month,
            "year": year,
            "payment_method": payment_method,
            "paid": paid,

            "total_amount": summary["total_amount"] or 0,
            "total_paid": summary["total_paid"] or 0,
            "total_remaining": summary["total_remaining"] or 0,

            "month_choices": Fee.MONTH_CHOICES,
            "payment_methods": Fee.PAYMENT_METHODS,
        }
    )


# =========================================================
# PRINT FEE REPORT
# SUPER ADMIN + ACCOUNTANT + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Accountant", "Vice Principal")
def print_fee_report(request):

    query = request.GET.get("q", "").strip()
    month = request.GET.get("month", "").strip()
    year = request.GET.get("year", "").strip()
    payment_method = request.GET.get(
        "payment_method",
        ""
    ).strip()
    paid = request.GET.get("paid", "").strip()

    fees = Fee.objects.select_related(
        "student"
    ).all()

    # SEARCH
    if query:

        fees = fees.filter(
            Q(receipt_no__icontains=query) |
            Q(student__admission_no__icontains=query) |
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query)
        )

    # MONTH
    if month:
        fees = fees.filter(
            month=month
        )

    # YEAR
    if year:
        fees = fees.filter(
            year=year
        )

    # PAYMENT METHOD
    if payment_method:
        fees = fees.filter(
            payment_method=payment_method
        )

    # PAYMENT STATUS
    if paid == "paid":

        fees = fees.filter(
            paid=True
        )

    elif paid == "unpaid":

        fees = fees.filter(
            paid=False
        )

    # SUMMARY
    summary = fees.aggregate(
        total_amount=Sum("total_amount"),
        total_paid=Sum("amount_paid"),
        total_remaining=Sum("remaining_amount"),
    )

    return render(
        request,
        "fee_management/print_fee_report.html",
        {
            "fees": fees.order_by("-id"),

            "total_amount": summary["total_amount"] or 0,
            "total_paid": summary["total_paid"] or 0,
            "total_remaining": summary["total_remaining"] or 0,
        }
    )