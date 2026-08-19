from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

from students.models import Student
from academics.models import Session, ClassRoom, Section
from fee_management.models import Fee
from teachers.models import Teacher
from salary.models import Salary
from attendance.models import Attendance
from teacher_diary.models import DiaryEntry
from results.models import Result

from accounts.utils import get_user_role


# =========================================================
# HOME
# =========================================================

def home(request):

    if request.user.is_authenticated:
        return redirect(
            "website:dashboard"
        )

    return render(
        request,
        "home.html"
    )


# =========================================================
# LOGIN
# =========================================================

def login(request):

    if request.user.is_authenticated:

        return redirect(
            "website:dashboard"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            if not user.is_active:

                return render(
                    request,
                    "login.html",
                    {
                        "error":
                            "Your account is inactive. "
                            "Please contact the administrator."
                    }
                )

            auth_login(
                request,
                user
            )

            return redirect(
                "website:dashboard"
            )

        return render(
            request,
            "login.html",
            {
                "error":
                    "Invalid username or password."
            }
        )

    return render(
        request,
        "login.html"
    )


# =========================================================
# MAIN ROLE-BASED DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    role = get_user_role(
        request.user
    )

    # =====================================================
    # NO ROLE
    # =====================================================

    if not role:

        return render(
            request,
            "dashboard/no_role.html"
        )

    # =====================================================
    # SUPER ADMIN DASHBOARD
    # =====================================================

    if role == "Super Admin":

        return super_admin_dashboard(
            request
        )

    # =====================================================
    # VICE PRINCIPAL DASHBOARD
    # =====================================================

    if role == "Vice Principal":

        return vice_principal_dashboard(
            request
        )

    # =====================================================
    # TEACHER DASHBOARD
    # =====================================================

    if role == "Teacher":

        return teacher_dashboard(
            request
        )

    # =====================================================
    # ACCOUNTANT DASHBOARD
    # =====================================================

    if role == "Accountant":

        return accountant_dashboard(
            request
        )

    # =====================================================
    # UNKNOWN ROLE
    # =====================================================

    return render(
        request,
        "dashboard/no_role.html"
    )


# =========================================================
# SUPER ADMIN DASHBOARD
# =========================================================

def super_admin_dashboard(request):

    today = timezone.localdate()

    # -----------------------------------------------------
    # STUDENTS
    # -----------------------------------------------------

    total_students = Student.objects.count()

    recent_students = Student.objects.order_by(
        "-id"
    )[:5]

    # -----------------------------------------------------
    # TEACHERS
    # -----------------------------------------------------

    total_teachers = Teacher.objects.count()

    active_teachers = Teacher.objects.filter(
        status="Active"
    ).count()

    inactive_teachers = Teacher.objects.filter(
        status="Inactive"
    ).count()

    # -----------------------------------------------------
    # ACADEMICS
    # -----------------------------------------------------

    total_sessions = Session.objects.count()

    total_classes = ClassRoom.objects.count()

    total_sections = Section.objects.count()

    # -----------------------------------------------------
    # FEES
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # SALARY
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # ATTENDANCE
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # DIARY
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    recent_results = Result.objects.select_related(
        "student",
        "subject"
    ).order_by(
        "-exam_date",
        "-id"
    )[:5]

    context = {

        "role": "Super Admin",

        "total_students": total_students,
        "recent_students": recent_students,

        "total_teachers": total_teachers,
        "active_teachers": active_teachers,
        "inactive_teachers": inactive_teachers,

        "total_sessions": total_sessions,
        "total_classes": total_classes,
        "total_sections": total_sections,

        "total_fees": total_fees,
        "total_fee_amount": total_fee_amount,
        "total_fee_paid": total_fee_paid,
        "total_fee_remaining": total_fee_remaining,
        "today_fee_collection": today_fee_collection,
        "today_fee_receipts": today_fee_receipts,

        "total_salary_records": total_salary_records,
        "total_salary": total_salary,
        "paid_salary": paid_salary,
        "pending_salary": pending_salary,

        "today": today,
        "today_attendance_total":
            today_attendance_total,
        "today_present":
            today_present,
        "today_absent":
            today_absent,
        "today_leave":
            today_leave,

        "today_diary_count":
            today_diary_count,
        "recent_diary":
            recent_diary,

        "recent_results":
            recent_results,
    }

    return render(
        request,
        "dashboard/super_admin.html",
        context
    )


# =========================================================
# VICE PRINCIPAL DASHBOARD
# =========================================================

def vice_principal_dashboard(request):

    today = timezone.localdate()

    total_students = Student.objects.count()

    total_teachers = Teacher.objects.count()

    active_teachers = Teacher.objects.filter(
        status="Active"
    ).count()

    total_classes = ClassRoom.objects.count()

    total_sections = Section.objects.count()

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

    today_diary_count = DiaryEntry.objects.filter(
        date=today
    ).count()

    recent_diary = DiaryEntry.objects.filter(
        date=today
    ).select_related(
        "teacher",
        "classroom",
        "section"
    ).order_by(
        "-id"
    )[:10]

    recent_results = Result.objects.select_related(
        "student",
        "subject"
    ).order_by(
        "-exam_date",
        "-id"
    )[:10]

    context = {

        "role": "Vice Principal",

        "today": today,

        "total_students":
            total_students,

        "total_teachers":
            total_teachers,

        "active_teachers":
            active_teachers,

        "total_classes":
            total_classes,

        "total_sections":
            total_sections,

        "today_present":
            today_present,

        "today_absent":
            today_absent,

        "today_leave":
            today_leave,

        "today_diary_count":
            today_diary_count,

        "recent_diary":
            recent_diary,

        "recent_results":
            recent_results,
    }

    return render(
        request,
        "dashboard/vice_principal.html",
        context
    )


# =========================================================
# TEACHER DASHBOARD
# =========================================================

def teacher_dashboard(request):

    today = timezone.localdate()

    teacher = getattr(
        request.user,
        "teacher_profile",
        None
    )

    today_diary = DiaryEntry.objects.filter(
        date=today
    )

    if teacher:

        today_diary = today_diary.filter(
            teacher=teacher
        )

    today_diary = today_diary.select_related(
        "classroom",
        "section"
    ).order_by(
        "-id"
    )

    today_attendance = Attendance.objects.filter(
        date=today
    )

    if teacher:

        today_attendance = today_attendance.filter(
            classroom__in=teacher.classrooms.all()
        ) if hasattr(teacher, "classrooms") else today_attendance

    context = {

        "role": "Teacher",

        "today": today,

        "teacher": teacher,

        "today_diary":
            today_diary[:10],

        "today_diary_count":
            today_diary.count(),

        "today_attendance_count":
            today_attendance.count(),
    }

    return render(
        request,
        "dashboard/teacher.html",
        context
    )


# =========================================================
# ACCOUNTANT DASHBOARD
# =========================================================

def accountant_dashboard(request):

    today = timezone.localdate()

    total_students = Student.objects.count()

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

    today_collection = today_fees.aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    today_receipts = today_fees.count()

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

    context = {

        "role": "Accountant",

        "today": today,

        "total_students":
            total_students,

        "total_fees":
            total_fees,

        "total_fee_amount":
            total_fee_amount,

        "total_fee_paid":
            total_fee_paid,

        "total_fee_remaining":
            total_fee_remaining,

        "today_collection":
            today_collection,

        "today_receipts":
            today_receipts,

        "total_salary":
            total_salary,

        "paid_salary":
            paid_salary,

        "pending_salary":
            pending_salary,
    }

    return render(
        request,
        "dashboard/accountant.html",
        context
    )