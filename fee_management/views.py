from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.db.models import (
    Q,
    Sum,
    Count
)

from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from decimal import Decimal

from .models import Fee, FeeStructure
from .forms import (
    FeeForm,
    FeeStructureForm
)

from accounts.utils import role_required


# =========================================================
# FEE DASHBOARD
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant",
    "Vice Principal"
)
def fee_dashboard(request):

    today = timezone.localdate()

    current_month = today.strftime("%B")
    current_year = today.year

    fees = Fee.objects.all()

    total_fees = fees.count()

    total_amount = (
        fees.aggregate(
            total=Sum("total_amount")
        )["total"] or Decimal("0.00")
    )

    total_paid = (
        fees.aggregate(
            total=Sum("amount_paid")
        )["total"] or Decimal("0.00")
    )

    total_remaining = (
        fees.aggregate(
            total=Sum("remaining_amount")
        )["total"] or Decimal("0.00")
    )

    paid_fees = fees.filter(
        paid=True
    ).count()

    unpaid_fees = fees.filter(
        paid=False
    ).count()

    today_collected = (
        fees.filter(
            payment_date=today
        ).aggregate(
            total=Sum("amount_paid")
        )["total"] or Decimal("0.00")
    )

    # =====================================================
    # CURRENT MONTH
    # =====================================================

    current_fees = fees.filter(
        month=current_month,
        year=current_year
    )

    current_collected = (
        current_fees.aggregate(
            total=Sum("amount_paid")
        )["total"] or Decimal("0.00")
    )

    current_pending = (
        current_fees.aggregate(
            total=Sum("remaining_amount")
        )["total"] or Decimal("0.00")
    )

    # =====================================================
    # EXPECTED MONTHLY REVENUE
    # =====================================================

    from students.models import Student

    active_students = (
        Student.objects
        .filter(is_active=True)
    )

    expected_monthly_revenue = (
        active_students.aggregate(
            total=Sum("monthly_fee")
        )["total"] or Decimal("0.00")
    )

    # =====================================================
    # EXPENSES
    # =====================================================

    try:

        from finance.models import Expense

        current_expenses = Expense.objects.filter(
            expense_date__year=current_year,
            expense_date__month=today.month
        )

        monthly_expenses = (
            current_expenses.aggregate(
                total=Sum("amount")
            )["total"] or Decimal("0.00")
        )

    except Exception:

        monthly_expenses = Decimal("0.00")

    # =====================================================
    # NET REVENUE
    # =====================================================

    net_revenue = (
        current_collected - monthly_expenses
    )

    # =====================================================
    # CLASS-WISE REVENUE
    # =====================================================

    class_revenue = []

    classrooms = (
        active_students
        .values(
            "classroom__id",
            "classroom__name"
        )
        .annotate(
            student_count=Count("id")
        )
        .order_by(
            "classroom__name"
        )
    )

    for classroom in classrooms:

        classroom_id = classroom[
            "classroom__id"
        ]

        classroom_name = classroom[
            "classroom__name"
        ]

        students_count = classroom[
            "student_count"
        ]

        expected = (
            active_students
            .filter(
                classroom_id=classroom_id
            )
            .aggregate(
                total=Sum("monthly_fee")
            )["total"] or Decimal("0.00")
        )

        collected = (
            current_fees
            .filter(
                student__classroom_id=classroom_id
            )
            .aggregate(
                total=Sum("amount_paid")
            )["total"] or Decimal("0.00")
        )

        pending = (
            expected - collected
        )

        if pending < 0:
            pending = Decimal("0.00")

        class_revenue.append({
            "classroom": classroom_name,
            "students": students_count,
            "monthly_fee": expected,
            "expected": expected,
            "collected": collected,
            "pending": pending,
        })

    # =====================================================
    # MONTHLY SUMMARY
    # =====================================================

    month_summary = (
        fees.values(
            "year",
            "month"
        )
        .annotate(
            total=Count("id"),
            collected=Sum("amount_paid"),
            remaining=Sum("remaining_amount")
        )
        .order_by(
            "-year",
            "month"
        )
    )

    # =====================================================
    # RECENT PAYMENTS
    # =====================================================

    recent_fees = (
        Fee.objects
        .select_related("student")
        .order_by("-id")[:10]
    )

    context = {

        "total_fees":
            total_fees,

        "total_amount":
            total_amount,

        "total_paid":
            total_paid,

        "total_remaining":
            total_remaining,

        "paid_fees":
            paid_fees,

        "unpaid_fees":
            unpaid_fees,

        "today_collected":
            today_collected,

        "current_month":
            current_month,

        "current_year":
            current_year,

        "expected_monthly_revenue":
            expected_monthly_revenue,

        "current_collected":
            current_collected,

        "current_pending":
            current_pending,

        "monthly_expenses":
            monthly_expenses,

        "net_revenue":
            net_revenue,

        "class_revenue":
            class_revenue,

        "month_summary":
            month_summary,

        "recent_fees":
            recent_fees,
    }

    return render(
        request,
        "fee_management/fee_dashboard.html",
        context
    )


# =========================================================
# ADD FEE
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant"
)
def add_fee(request):

    if request.method == "POST":

        form = FeeForm(request.POST)

        if form.is_valid():

            student = form.cleaned_data["student"]
            month = form.cleaned_data["month"]
            year = form.cleaned_data["year"]

            amount_paid = (
                form.cleaned_data["amount_paid"]
                or Decimal("0.00")
            )

            discount = (
                form.cleaned_data["discount"]
                or Decimal("0.00")
            )

            fine = (
                form.cleaned_data["fine"]
                or Decimal("0.00")
            )

            # =================================================
            # DUPLICATE MONTH CHECK
            # =================================================

            if Fee.objects.filter(
                student=student,
                month=month,
                year=year
            ).exists():

                messages.error(
                    request,
                    (
                        f"Fee for {student.first_name} "
                        f"for {month} {year} has already "
                        "been entered."
                    )
                )

                return render(
                    request,
                    "fee_management/add_fee.html",
                    {
                        "form": form,
                        "edit_mode": False,
                    }
                )

            # =================================================
            # STUDENT MONTHLY FEE
            # =================================================

            monthly_fee = (
                student.monthly_fee
                or Decimal("0.00")
            )

            if monthly_fee <= 0:

                messages.error(
                    request,
                    (
                        f"Monthly fee has not been set "
                        f"for {student.first_name}."
                    )
                )

                return render(
                    request,
                    "fee_management/add_fee.html",
                    {
                        "form": form,
                        "edit_mode": False,
                    }
                )

            # =================================================
            # PREVIOUS BALANCE
            # =================================================

            previous_balance = (
                Fee.objects
                .filter(
                    student=student,
                    remaining_amount__gt=0
                )
                .aggregate(
                    total=Sum(
                        "remaining_amount"
                    )
                )["total"]
                or Decimal("0.00")
            )

            # =================================================
            # ADMISSION FEE
            # =================================================

            admission_fee = Decimal("0.00")

            if not Fee.objects.filter(
                student=student
            ).exists():

                admission_fee = (
                    FeeStructure.objects
                    .filter(
                        classroom=student.classroom
                    )
                    .values_list(
                        "admission_fee",
                        flat=True
                    )
                    .first()
                    or Decimal("0.00")
                )

            # =================================================
            # EXAM FEE
            # =================================================

            exam_fee = Decimal("0.00")

            # =================================================
            # TOTAL AMOUNT
            # =================================================

            total_amount = (
                monthly_fee
                + previous_balance
                + admission_fee
                + exam_fee
                + fine
                - discount
            )

            if total_amount < 0:

                total_amount = Decimal("0.00")

            # =================================================
            # PAYMENT VALIDATION
            # =================================================

            if amount_paid > total_amount:

                messages.error(
                    request,
                    (
                        "Amount paid cannot be greater "
                        "than total amount due."
                    )
                )

                return render(
                    request,
                    "fee_management/add_fee.html",
                    {
                        "form": form,
                        "edit_mode": False,
                    }
                )

            # =================================================
            # SAVE
            # =================================================

            fee = form.save(
                commit=False
            )

            fee.monthly_fee = monthly_fee

            fee.previous_balance = (
                previous_balance
            )

            fee.admission_fee = (
                admission_fee
            )

            fee.exam_fee = (
                exam_fee
            )

            fee.discount = (
                discount
            )

            fee.fine = (
                fine
            )

            fee.total_amount = (
                total_amount
            )

            fee.amount_paid = (
                amount_paid
            )

            fee.save()

            messages.success(
                request,
                (
                    "Fee collected successfully. "
                    f"Receipt: {fee.receipt_no}"
                )
            )

            return redirect(
                "fee_management:fee_detail",
                pk=fee.pk
            )

    else:

        form = FeeForm(
            initial={
                "year":
                    timezone.localdate().year,

                "month":
                    timezone.localdate().strftime(
                        "%B"
                    ),

                "payment_date":
                    timezone.localdate(),
            }
        )

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
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant",
    "Vice Principal"
)
def fee_list(request):

    query = request.GET.get(
        "q",
        ""
    )

    month = request.GET.get(
        "month",
        ""
    )

    year = request.GET.get(
        "year",
        ""
    )

    payment_method = request.GET.get(
        "payment_method",
        ""
    )

    paid = request.GET.get(
        "paid",
        ""
    )

    fees = Fee.objects.select_related(
        "student"
    )

    if query:

        fees = fees.filter(
            Q(
                receipt_no__icontains=query
            )
            |
            Q(
                student__admission_no__icontains=query
            )
            |
            Q(
                student__first_name__icontains=query
            )
            |
            Q(
                student__last_name__icontains=query
            )
        )

    if month:

        fees = fees.filter(
            month=month
        )

    if year:

        fees = fees.filter(
            year=year
        )

    if payment_method:

        fees = fees.filter(
            payment_method=payment_method
        )

    if paid == "paid":

        fees = fees.filter(
            paid=True
        )

    elif paid == "unpaid":

        fees = fees.filter(
            paid=False
        )

    fees = fees.order_by("-id")

    return render(
        request,
        "fee_management/fee_list.html",
        {
            "fees": fees,
            "query": query,
            "month": month,
            "year": year,
            "payment_method":
                payment_method,
            "paid": paid,
            "month_choices":
                Fee.MONTH_CHOICES,
            "payment_methods":
                Fee.PAYMENT_METHODS,
        }
    )


# =========================================================
# FEE DETAIL
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant",
    "Vice Principal"
)
def fee_detail(request, pk):

    fee = get_object_or_404(
        Fee.objects.select_related(
            "student"
        ),
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
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant"
)
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

            fee_obj = form.save(
                commit=False
            )

            monthly_fee = (
                fee_obj.student.monthly_fee
                or Decimal("0.00")
            )

            fee_obj.monthly_fee = (
                monthly_fee
            )

            fee_obj.total_amount = (
                fee_obj.monthly_fee
                + fee_obj.previous_balance
                + fee_obj.admission_fee
                + fee_obj.exam_fee
                + fee_obj.fine
                - fee_obj.discount
            )

            if fee_obj.total_amount < 0:

                fee_obj.total_amount = (
                    Decimal("0.00")
                )

            fee_obj.save()

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
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant",
    "Vice Principal"
)
def fee_structure_list(request):

    structures = (
        FeeStructure.objects
        .select_related("classroom")
        .order_by("classroom__name")
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
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant"
)
def add_fee_structure(request):

    if request.method == "POST":

        form = FeeStructureForm(
            request.POST
        )

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
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant"
)
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
# PRINT RECEIPT
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant",
    "Vice Principal"
)
def print_fee_receipt(request, pk):

    fee = get_object_or_404(
        Fee.objects.select_related(
            "student"
        ),
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
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant",
    "Vice Principal"
)
def fee_report(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    month = request.GET.get(
        "month",
        ""
    ).strip()

    year = request.GET.get(
        "year",
        ""
    ).strip()

    payment_method = request.GET.get(
        "payment_method",
        ""
    ).strip()

    paid = request.GET.get(
        "paid",
        ""
    ).strip()

    fees = (
        Fee.objects
        .select_related("student")
        .all()
    )

    if query:

        fees = fees.filter(
            Q(
                receipt_no__icontains=query
            )
            |
            Q(
                student__admission_no__icontains=query
            )
            |
            Q(
                student__first_name__icontains=query
            )
            |
            Q(
                student__last_name__icontains=query
            )
        )

    if month:

        fees = fees.filter(
            month=month
        )

    if year:

        fees = fees.filter(
            year=year
        )

    if payment_method:

        fees = fees.filter(
            payment_method=payment_method
        )

    if paid == "paid":

        fees = fees.filter(
            paid=True
        )

    elif paid == "unpaid":

        fees = fees.filter(
            paid=False
        )

    summary = fees.aggregate(
        total_amount=Sum(
            "total_amount"
        ),

        total_paid=Sum(
            "amount_paid"
        ),

        total_remaining=Sum(
            "remaining_amount"
        ),
    )

    return render(
        request,
        "fee_management/fee_report.html",
        {
            "fees":
                fees.order_by("-id"),

            "query":
                query,

            "month":
                month,

            "year":
                year,

            "payment_method":
                payment_method,

            "paid":
                paid,

            "total_amount":
                summary["total_amount"]
                or Decimal("0.00"),

            "total_paid":
                summary["total_paid"]
                or Decimal("0.00"),

            "total_remaining":
                summary["total_remaining"]
                or Decimal("0.00"),

            "month_choices":
                Fee.MONTH_CHOICES,

            "payment_methods":
                Fee.PAYMENT_METHODS,
        }
    )


# =========================================================
# PRINT REPORT
# =========================================================

@login_required
@role_required(
    "Super Admin",
    "Accountant",
    "Vice Principal"
)
def print_fee_report(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    month = request.GET.get(
        "month",
        ""
    ).strip()

    year = request.GET.get(
        "year",
        ""
    ).strip()

    payment_method = request.GET.get(
        "payment_method",
        ""
    ).strip()

    paid = request.GET.get(
        "paid",
        ""
    ).strip()

    fees = (
        Fee.objects
        .select_related("student")
        .all()
    )

    if query:

        fees = fees.filter(
            Q(
                receipt_no__icontains=query
            )
            |
            Q(
                student__admission_no__icontains=query
            )
            |
            Q(
                student__first_name__icontains=query
            )
            |
            Q(
                student__last_name__icontains=query
            )
        )

    if month:

        fees = fees.filter(
            month=month
        )

    if year:

        fees = fees.filter(
            year=year
        )

    if payment_method:

        fees = fees.filter(
            payment_method=payment_method
        )

    if paid == "paid":

        fees = fees.filter(
            paid=True
        )

    elif paid == "unpaid":

        fees = fees.filter(
            paid=False
        )

    summary = fees.aggregate(
        total_amount=Sum(
            "total_amount"
        ),

        total_paid=Sum(
            "amount_paid"
        ),

        total_remaining=Sum(
            "remaining_amount"
        ),
    )

    return render(
        request,
        "fee_management/print_fee_report.html",
        {
            "fees":
                fees.order_by("-id"),

            "total_amount":
                summary["total_amount"]
                or Decimal("0.00"),

            "total_paid":
                summary["total_paid"]
                or Decimal("0.00"),

            "total_remaining":
                summary["total_remaining"]
                or Decimal("0.00"),
        }
    )