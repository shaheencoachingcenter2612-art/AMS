from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum, Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Teacher
from .forms import TeacherForm, SalaryForm

from salary.models import Salary

from accounts.utils import role_required


# =========================================================
# TEACHER DASHBOARD
# SUPER ADMIN + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Vice Principal")
def teacher_dashboard(request):

    total_teachers = Teacher.objects.count()

    active_teachers = Teacher.objects.filter(
        status="Active"
    ).count()

    inactive_teachers = Teacher.objects.filter(
        status="Inactive"
    ).count()

    male_teachers = Teacher.objects.filter(
        gender="Male"
    ).count()

    female_teachers = Teacher.objects.filter(
        gender="Female"
    ).count()

    salary_data = Teacher.objects.aggregate(
        total_salary=Sum("salary")
    )

    total_salary = salary_data["total_salary"] or 0

    subject_summary = Teacher.objects.values(
        "subject"
    ).annotate(
        total=Count("id")
    ).order_by("subject")

    recent_teachers = Teacher.objects.all().order_by(
        "-created_at"
    )[:5]

    return render(
        request,
        "teachers/teacher_dashboard.html",
        {
            "total_teachers": total_teachers,
            "active_teachers": active_teachers,
            "inactive_teachers": inactive_teachers,
            "male_teachers": male_teachers,
            "female_teachers": female_teachers,
            "total_salary": total_salary,
            "subject_summary": subject_summary,
            "recent_teachers": recent_teachers,
        }
    )


# =========================================================
# TEACHER LIST
# SUPER ADMIN + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Vice Principal")
def teacher_list(request):

    query = request.GET.get("q", "").strip()

    teachers = Teacher.objects.all()

    if query:
        teachers = teachers.filter(
            Q(employee_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(subject__icontains=query) |
            Q(phone__icontains=query) |
            Q(cnic__icontains=query)
        )

    teachers = teachers.order_by(
        "first_name",
        "last_name"
    )

    return render(
        request,
        "teachers/teacher_list.html",
        {
            "teachers": teachers,
            "query": query,
        }
    )


# =========================================================
# ADD TEACHER
# SUPER ADMIN + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Vice Principal")
def add_teacher(request):

    if request.method == "POST":

        form = TeacherForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            teacher = form.save()

            messages.success(
                request,
                "Teacher added successfully."
            )

            return redirect(
                "teachers:teacher_detail",
                pk=teacher.pk
            )

    else:
        form = TeacherForm()

    return render(
        request,
        "teachers/add_teacher.html",
        {
            "form": form
        }
    )


# =========================================================
# TEACHER DETAIL
# SUPER ADMIN + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Vice Principal")
def teacher_detail(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    return render(
        request,
        "teachers/teacher_detail.html",
        {
            "teacher": teacher
        }
    )


# =========================================================
# EDIT TEACHER
# SUPER ADMIN + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Vice Principal")
def edit_teacher(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    if request.method == "POST":

        form = TeacherForm(
            request.POST,
            request.FILES,
            instance=teacher
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Teacher updated successfully."
            )

            return redirect(
                "teachers:teacher_detail",
                pk=teacher.pk
            )

    else:

        form = TeacherForm(
            instance=teacher
        )

    return render(
        request,
        "teachers/add_teacher.html",
        {
            "form": form,
            "teacher": teacher,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE TEACHER
# SUPER ADMIN + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Vice Principal")
def delete_teacher(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    if request.method == "POST":

        teacher.delete()

        messages.success(
            request,
            "Teacher deleted successfully."
        )

        return redirect(
            "teachers:teacher_list"
        )

    return render(
        request,
        "teachers/delete_teacher.html",
        {
            "teacher": teacher
        }
    )


# =========================================================
# TEACHER REPORT
# SUPER ADMIN + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Vice Principal")
def teacher_report(request):

    query = request.GET.get("q", "").strip()
    gender = request.GET.get("gender", "").strip()
    status = request.GET.get("status", "").strip()
    subject = request.GET.get("subject", "").strip()

    teachers = Teacher.objects.all()

    # SEARCH
    if query:
        teachers = teachers.filter(
            Q(employee_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(subject__icontains=query) |
            Q(phone__icontains=query) |
            Q(cnic__icontains=query)
        )

    # GENDER
    if gender:
        teachers = teachers.filter(
            gender=gender
        )

    # STATUS
    if status:
        teachers = teachers.filter(
            status=status
        )

    # SUBJECT
    if subject:
        teachers = teachers.filter(
            subject__icontains=subject
        )

    teachers = teachers.order_by(
        "first_name",
        "last_name"
    )

    return render(
        request,
        "teachers/teacher_report.html",
        {
            "teachers": teachers,
            "query": query,
            "gender": gender,
            "status": status,
            "subject": subject,
            "gender_choices": Teacher._meta.get_field("gender").choices,
            "status_choices": Teacher._meta.get_field("status").choices,
        }
    )


# =========================================================
# PRINT TEACHER REPORT
# SUPER ADMIN + VICE PRINCIPAL
# =========================================================

@login_required
@role_required("Super Admin", "Vice Principal")
def print_teacher_report(request):

    query = request.GET.get("q", "").strip()
    gender = request.GET.get("gender", "").strip()
    status = request.GET.get("status", "").strip()
    subject = request.GET.get("subject", "").strip()

    teachers = Teacher.objects.all()

    if query:
        teachers = teachers.filter(
            Q(employee_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(subject__icontains=query) |
            Q(phone__icontains=query) |
            Q(cnic__icontains=query)
        )

    if gender:
        teachers = teachers.filter(
            gender=gender
        )

    if status:
        teachers = teachers.filter(
            status=status
        )

    if subject:
        teachers = teachers.filter(
            subject__icontains=subject
        )

    teachers = teachers.order_by(
        "first_name",
        "last_name"
    )

    return render(
        request,
        "teachers/print_teacher_report.html",
        {
            "teachers": teachers,
            "query": query,
            "gender": gender,
            "status": status,
            "subject": subject,
        }
    )


# =========================================================
# SALARY LIST
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def salary_list(request):

    query = request.GET.get("q", "").strip()
    month = request.GET.get("month", "").strip()
    year = request.GET.get("year", "").strip()
    paid = request.GET.get("paid", "").strip()

    salaries = Salary.objects.select_related(
        "teacher"
    ).all()

    if query:
        salaries = salaries.filter(
            Q(teacher__employee_id__icontains=query) |
            Q(teacher__first_name__icontains=query) |
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

    if paid == "true":
        salaries = salaries.filter(
            paid=True
        )

    elif paid == "false":
        salaries = salaries.filter(
            paid=False
        )

    salaries = salaries.order_by(
        "-year",
        "-id"
    )

    return render(
        request,
        "teachers/salary_list.html",
        {
            "salaries": salaries,
            "query": query,
            "month": month,
            "year": year,
            "paid": paid,
        }
    )


# =========================================================
# ADD SALARY
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def add_salary(request):

    if request.method == "POST":

        form = SalaryForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Salary added successfully."
            )

            return redirect(
                "teachers:salary_list"
            )

        messages.error(
            request,
            "Salary was not saved. Please check the form errors."
        )

    else:

        form = SalaryForm()

    return render(
        request,
        "teachers/add_salary.html",
        {
            "form": form
        }
    )


# =========================================================
# SALARY DETAIL
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def salary_detail(request, pk):

    salary = get_object_or_404(
        Salary.objects.select_related(
            "teacher"
        ),
        pk=pk
    )

    return render(
        request,
        "teachers/salary_detail.html",
        {
            "salary": salary
        }
    )


# =========================================================
# EDIT SALARY
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
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

            messages.success(
                request,
                "Salary updated successfully."
            )

            return redirect(
                "teachers:salary_list"
            )

    else:

        form = SalaryForm(
            instance=salary
        )

    return render(
        request,
        "teachers/add_salary.html",
        {
            "form": form,
            "salary": salary,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE SALARY
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def delete_salary(request, pk):

    salary = get_object_or_404(
        Salary,
        pk=pk
    )

    if request.method == "POST":

        salary.delete()

        messages.success(
            request,
            "Salary deleted successfully."
        )

        return redirect(
            "teachers:salary_list"
        )

    return render(
        request,
        "teachers/delete_salary.html",
        {
            "salary": salary
        }
    )


# =========================================================
# SALARY REPORT
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def salary_report(request):

    month = request.GET.get("month", "").strip()
    year = request.GET.get("year", "").strip()
    paid = request.GET.get("paid", "").strip()

    salaries = Salary.objects.select_related(
        "teacher"
    ).all()

    if month:
        salaries = salaries.filter(
            month=month
        )

    if year:
        salaries = salaries.filter(
            year=year
        )

    if paid == "true":
        salaries = salaries.filter(
            paid=True
        )

    elif paid == "false":
        salaries = salaries.filter(
            paid=False
        )

    summary = salaries.aggregate(
        total_salary=Sum("net_salary"),
        total_basic=Sum("basic_salary"),
        total_allowance=Sum("allowance"),
        total_advance=Sum("advance"),
        total_deduction=Sum("deduction"),
    )

    paid_amount = salaries.filter(
        paid=True
    ).aggregate(
        total=Sum("net_salary")
    )["total"] or 0

    pending_amount = salaries.filter(
        paid=False
    ).aggregate(
        total=Sum("net_salary")
    )["total"] or 0

    return render(
        request,
        "teachers/salary_report.html",
        {
            "salaries": salaries.order_by(
                "-year",
                "-id"
            ),

            "month": month,
            "year": year,
            "paid": paid,

            "total_salary": summary["total_salary"] or 0,
            "total_basic": summary["total_basic"] or 0,
            "total_allowance": summary["total_allowance"] or 0,
            "total_advance": summary["total_advance"] or 0,
            "total_deduction": summary["total_deduction"] or 0,

            "paid_amount": paid_amount,
            "pending_amount": pending_amount,
        }
    )


# =========================================================
# PRINT SALARY REPORT
# SUPER ADMIN + ACCOUNTANT
# =========================================================

@login_required
@role_required("Super Admin", "Accountant")
def print_salary_report(request):

    month = request.GET.get("month", "").strip()
    year = request.GET.get("year", "").strip()
    paid = request.GET.get("paid", "").strip()

    salaries = Salary.objects.select_related(
        "teacher"
    ).all()

    if month:
        salaries = salaries.filter(
            month=month
        )

    if year:
        salaries = salaries.filter(
            year=year
        )

    if paid == "true":
        salaries = salaries.filter(
            paid=True
        )

    elif paid == "false":
        salaries = salaries.filter(
            paid=False
        )

    summary = salaries.aggregate(
        total_salary=Sum("net_salary"),
        total_basic=Sum("basic_salary"),
        total_allowance=Sum("allowance"),
        total_advance=Sum("advance"),
        total_deduction=Sum("deduction"),
    )

    return render(
        request,
        "teachers/print_salary_report.html",
        {
            "salaries": salaries.order_by(
                "-year",
                "-id"
            ),

            "total_salary": summary["total_salary"] or 0,
            "total_basic": summary["total_basic"] or 0,
            "total_allowance": summary["total_allowance"] or 0,
            "total_advance": summary["total_advance"] or 0,
            "total_deduction": summary["total_deduction"] or 0,

            "month": month,
            "year": year,
            "paid": paid,
        }
    )