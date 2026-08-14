from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.utils import timezone

from .models import Salary
from .forms import SalaryForm


# =========================================================
# SALARY DASHBOARD
# =========================================================

def salary_dashboard(request):

    salaries = Salary.objects.select_related(
        "teacher"
    )

    total_records = salaries.count()

    total_salary = salaries.aggregate(
        total=Sum("net_salary")
    )["total"] or 0

    total_paid = salaries.filter(
        paid=True
    ).aggregate(
        total=Sum("net_salary")
    )["total"] or 0

    total_unpaid = salaries.filter(
        paid=False
    ).aggregate(
        total=Sum("net_salary")
    )["total"] or 0

    paid_records = salaries.filter(
        paid=True
    ).count()

    unpaid_records = salaries.filter(
        paid=False
    ).count()

    recent_salaries = salaries.order_by(
        "-id"
    )[:5]

    return render(
        request,
        "salary/salary_dashboard.html",
        {
            "total_records": total_records,
            "total_salary": total_salary,
            "total_paid": total_paid,
            "total_unpaid": total_unpaid,
            "paid_records": paid_records,
            "unpaid_records": unpaid_records,
            "recent_salaries": recent_salaries,
        }
    )


# =========================================================
# SALARY LIST
# =========================================================

def salary_list(request):

    query = request.GET.get("q", "")
    month = request.GET.get("month", "")
    year = request.GET.get("year", "")
    paid = request.GET.get("paid", "")

    salaries = Salary.objects.select_related(
        "teacher"
    )

    if query:

        salaries = salaries.filter(
            Q(teacher__first_name__icontains=query)
            |
            Q(teacher__last_name__icontains=query)
        )

    if month:

        salaries = salaries.filter(
            month=month
        )

    if year:

        salaries = salaries.filter(
            year=year
        )

    if paid == "paid":

        salaries = salaries.filter(
            paid=True
        )

    elif paid == "unpaid":

        salaries = salaries.filter(
            paid=False
        )

    salaries = salaries.order_by(
        "-year",
        "-id"
    )

    return render(
        request,
        "salary/salary_list.html",
        {
            "salaries": salaries,
            "query": query,
            "month": month,
            "year": year,
            "paid": paid,
            "month_choices": Salary.MONTH_CHOICES,
        }
    )


# =========================================================
# ADD SALARY
# =========================================================

def add_salary(request):

    if request.method == "POST":

        form = SalaryForm(request.POST)

        if form.is_valid():

            salary = form.save()

            return redirect(
                "salary:salary_detail",
                pk=salary.pk
            )

    else:

        form = SalaryForm()

    return render(
        request,
        "salary/add_salary.html",
        {
            "form": form,
            "edit_mode": False,
        }
    )


# =========================================================
# SALARY DETAIL
# =========================================================

def salary_detail(request, pk):

    salary = get_object_or_404(
        Salary.objects.select_related(
            "teacher"
        ),
        pk=pk
    )

    return render(
        request,
        "salary/salary_detail.html",
        {
            "salary": salary
        }
    )


# =========================================================
# EDIT SALARY
# =========================================================

def edit_salary(request, pk):

    salary = get_object_or_404(
        Salary,
        pk=pk
    )

    if request.method == "POST":

        form = SalaryForm(
            request.POST,
            instance=salary
        )

        if form.is_valid():

            form.save()

            return redirect(
                "salary:salary_detail",
                pk=salary.pk
            )

    else:

        form = SalaryForm(
            instance=salary
        )

    return render(
        request,
        "salary/add_salary.html",
        {
            "form": form,
            "salary": salary,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE SALARY
# =========================================================

def delete_salary(request, pk):

    salary = get_object_or_404(
        Salary,
        pk=pk
    )

    if request.method == "POST":

        salary.delete()

        return redirect(
            "salary:salary_list"
        )

    return render(
        request,
        "salary/delete_salary.html",
        {
            "salary": salary
        }
    )


# =========================================================
# PRINT SALARY SLIP
# =========================================================

def print_salary_slip(request, pk):

    salary = get_object_or_404(
        Salary.objects.select_related(
            "teacher"
        ),
        pk=pk
    )

    return render(
        request,
        "salary/print_salary_slip.html",
        {
            "salary": salary
        }
    )