from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone

from students.models import Student
from academics.models import Session, ClassRoom, Section
from fee_management.models import Fee
from teachers.models import Teacher
from salary.models import Salary
from attendance.models import Attendance
from teacher_diary.models import DiaryEntry
from results.models import Result


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(
        request,
        "home.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login(request):

    if request.user.is_authenticated:
        return redirect("website:dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(
                request,
                user
            )

            return redirect("website:dashboard")

    return render(
        request,
        "login.html"
    )


# =========================================================
# MAIN ERP DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    today = timezone.localdate()

    # =====================================================
    # STUDENTS
    # =====================================================

    total_students = Student.objects.count()

    recent_students = Student.objects.order_by(
        "-id"
    )[:5]


    # =====================================================
    # TEACHERS
    # =====================================================

    total_teachers = Teacher.objects.count()

    active_teachers = Teacher.objects.filter(
        status="Active"
    ).count()

    inactive_teachers = Teacher.objects.filter(
        status="Inactive"
    ).count()


    # =====================================================
    # ACADEMICS
    # =====================================================

    total_sessions = Session.objects.count()

    total_classes = ClassRoom.objects.count()

    total_sections = Section.objects.count()


    # =====================================================
    # FEES
    # =====================================================

    total_fees = Fee.objects.count()

    total_fee_amount = Fee.objects.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    total_fee_paid = Fee.objects.aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    total_fee_remaining = Fee.objects.aggregate(
        total=Sum("remaining_amount")
    )["total"] or 0

    today_fees = Fee.objects.filter(
        payment_date=today
    )

    today_fee_collection = today_fees.aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    today_fee_receipts = today_fees.count()


    # =====================================================
    # SALARY
    # =====================================================

    total_salary_records = Salary.objects.count()

    total_salary = Salary.objects.aggregate(
        total=Sum("net_salary")
    )["total"] or 0

    paid_salary = Salary.objects.filter(
        paid=True
    ).aggregate(
        total=Sum("net_salary")
    )["total"] or 0

    pending_salary = Salary.objects.filter(
        paid=False
    ).aggregate(
        total=Sum("net_salary")
    )["total"] or 0


    # =====================================================
    # TODAY'S ATTENDANCE
    # =====================================================

    today_attendance = Attendance.objects.filter(
        date=today
    )

    today_present = today_attendance.filter(
        status="Present"
    ).count()

    today_absent = today_attendance.filter(
        status="Absent"
    ).count()

    today_leave = today_attendance.filter(
        status="Leave"
    ).count()

    today_attendance_total = today_attendance.count()


    # =====================================================
    # TODAY'S DIARY
    # =====================================================

    today_diary = DiaryEntry.objects.filter(
        date=today
    ).select_related(
        "teacher",
        "classroom",
        "section"
    )

    today_diary_count = today_diary.count()

    recent_diary = today_diary.order_by(
        "-id"
    )[:5]


    # =====================================================
    # RECENT RESULTS
    # =====================================================

    recent_results = Result.objects.select_related(
        "student",
        "subject"
    ).order_by(
        "-exam_date",
        "-id"
    )[:5]


    # =====================================================
    # DASHBOARD CONTEXT
    # =====================================================

    context = {

        # -------------------------------------------------
        # Students
        # -------------------------------------------------

        "total_students": total_students,
        "recent_students": recent_students,


        # -------------------------------------------------
        # Teachers
        # -------------------------------------------------

        "total_teachers": total_teachers,
        "active_teachers": active_teachers,
        "inactive_teachers": inactive_teachers,


        # -------------------------------------------------
        # Academics
        # -------------------------------------------------

        "total_sessions": total_sessions,
        "total_classes": total_classes,
        "total_sections": total_sections,


        # -------------------------------------------------
        # Fees
        # -------------------------------------------------

        "total_fees": total_fees,
        "total_fee_amount": total_fee_amount,
        "total_fee_paid": total_fee_paid,
        "total_fee_remaining": total_fee_remaining,

        "today_fee_collection": today_fee_collection,
        "today_fee_receipts": today_fee_receipts,


        # -------------------------------------------------
        # Salary
        # -------------------------------------------------

        "total_salary_records": total_salary_records,
        "total_salary": total_salary,
        "paid_salary": paid_salary,
        "pending_salary": pending_salary,


        # -------------------------------------------------
        # Attendance
        # -------------------------------------------------

        "today": today,

        "today_attendance_total": today_attendance_total,
        "today_present": today_present,
        "today_absent": today_absent,
        "today_leave": today_leave,


        # -------------------------------------------------
        # Diary
        # -------------------------------------------------

        "today_diary_count": today_diary_count,
        "recent_diary": recent_diary,


        # -------------------------------------------------
        # Results
        # -------------------------------------------------

        "recent_results": recent_results,
    }


    return render(
        request,
        "dashboard.html",
        context
    )