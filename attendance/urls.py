from django.urls import path

from . import views


app_name = "attendance"


urlpatterns = [

    # =====================================================
    # ATTENDANCE HOME
    # =====================================================

    # /attendance/
    # Opens the class list
    path(
        "",
        views.mark_attendance,
        name="attendance_home",
    ),

    # Old attendance dashboard
    # /attendance/dashboard/
    path(
        "dashboard/",
        views.attendance_dashboard,
        name="attendance_dashboard",
    ),


    # =====================================================
    # CLASS-BASED DAILY ATTENDANCE
    # =====================================================

    # Shows all classes
    # /attendance/mark/
    path(
        "mark/",
        views.mark_attendance,
        name="mark_attendance",
    ),

    # Opens selected class
    # /attendance/class/4/
    path(
        "class/<int:classroom_id>/",
        views.class_attendance,
        name="class_attendance",
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
    # SINGLE ATTENDANCE
    # =====================================================

    path(
        "add/",
        views.add_attendance,
        name="add_attendance",
    ),

    path(
        "<int:pk>/",
        views.attendance_detail,
        name="attendance_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.edit_attendance,
        name="edit_attendance",
    ),

    path(
        "<int:pk>/delete/",
        views.delete_attendance,
        name="delete_attendance",
    ),


    # =====================================================
    # REPORTS
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
]