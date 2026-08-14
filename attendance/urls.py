from django.urls import path
from . import views


app_name = "attendance"


urlpatterns = [

    # =====================================================
    # ATTENDANCE HOME / DASHBOARD
    # =====================================================

    path(
        "",
        views.attendance_dashboard,
        name="attendance_home",
    ),

    # =====================================================
    # ATTENDANCE LIST
    # =====================================================

    path(
        "list/",
        views.attendance_list,
        name="attendance_list",
    ),

    # =====================================================
    # ADD ATTENDANCE
    # =====================================================

    path(
        "add/",
        views.add_attendance,
        name="add_attendance",
    ),

    # =====================================================
    # ATTENDANCE DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.attendance_dashboard,
        name="attendance_dashboard",
    ),

    # =====================================================
    # ATTENDANCE REPORTS
    # =====================================================

    path(
        "report/",
        views.attendance_report,
        name="attendance_report",
    ),

    path(
        "student-report/",
        views.student_attendance_report,
        name="student_attendance_report",
    ),

    path(
        "monthly-report/",
        views.monthly_attendance_report,
        name="monthly_attendance_report",
    ),

    # =====================================================
    # ATTENDANCE DETAIL
    # =====================================================

    path(
        "<int:pk>/",
        views.attendance_detail,
        name="attendance_detail",
    ),

    # =====================================================
    # EDIT ATTENDANCE
    # =====================================================

    path(
        "<int:pk>/edit/",
        views.edit_attendance,
        name="edit_attendance",
    ),

    # =====================================================
    # DELETE ATTENDANCE
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_attendance,
        name="delete_attendance",
    ),
]