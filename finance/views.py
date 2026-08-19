from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import (
    login_required
)

from django.contrib import messages

from django.db.models import Sum

from django.utils import timezone

from .models import Expense

from .forms import ExpenseForm

from accounts.utils import role_required


@login_required
@role_required(
    "Super Admin",
    "Accountant",
    "Vice Principal"
)
def expense_list(request):

    today = timezone.localdate()

    expenses = Expense.objects.all()

    month = request.GET.get(
        "month",
        ""
    )

    year = request.GET.get(
        "year",
        ""
    )

    if month:

        expenses = expenses.filter(
            expense_date__month=month
        )

    if year:

        expenses = expenses.filter(
            expense_date__year=year
        )

    total_expenses = (
        expenses.aggregate(
            total=Sum("amount")
        )["total"] or 0
    )

    return render(
        request,
        "finance/expense_list.html",
        {
            "expenses": expenses,

            "total_expenses":
                total_expenses,

            "month": month,

            "year": year,

            "today": today,
        }
    )


@login_required
@role_required(
    "Super Admin",
    "Accountant"
)
def add_expense(request):

    if request.method == "POST":

        form = ExpenseForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Expense added successfully."
            )

            return redirect(
                "finance:expense_list"
            )

    else:

        form = ExpenseForm(
            initial={
                "expense_date":
                    timezone.localdate()
            }
        )

    return render(
        request,
        "finance/add_expense.html",
        {
            "form": form
        }
    )


@login_required
@role_required(
    "Super Admin",
    "Accountant"
)
def edit_expense(request, pk):

    expense = get_object_or_404(
        Expense,
        pk=pk
    )

    if request.method == "POST":

        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Expense updated successfully."
            )

            return redirect(
                "finance:expense_list"
            )

    else:

        form = ExpenseForm(
            instance=expense
        )

    return render(
        request,
        "finance/add_expense.html",
        {
            "form": form,
            "expense": expense,
            "edit_mode": True,
        }
    )


@login_required
@role_required("Super Admin")
def delete_expense(request, pk):

    expense = get_object_or_404(
        Expense,
        pk=pk
    )

    if request.method == "POST":

        expense.delete()

        messages.success(
            request,
            "Expense deleted successfully."
        )

        return redirect(
            "finance:expense_list"
        )

    return render(
        request,
        "finance/delete_expense.html",
        {
            "expense": expense
        }
    )