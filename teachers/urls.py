from django.urls import path
from . import views

app_name = "teachers"

urlpatterns = [

    # =====================================================
    # TEACHER DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.teacher_dashboard,
        name="teacher_dashboard",
    ),

    # =====================================================
    # TEACHER REPORT
    # =====================================================

    path(
        "report/",
        views.teacher_report,
        name="teacher_report",
    ),

    # =====================================================
    # PRINT TEACHER REPORT
    # =====================================================

    path(
        "report/print/",
        views.print_teacher_report,
        name="print_teacher_report",
    ),

    # =====================================================
    # TEACHER LIST
    # =====================================================

    path(
        "",
        views.teacher_list,
        name="teacher_list",
    ),

    # =====================================================
    # ADD TEACHER
    # =====================================================

    path(
        "add/",
        views.add_teacher,
        name="add_teacher",
    ),

    # =====================================================
    # TEACHER DETAIL
    # =====================================================

    path(
        "<int:pk>/",
        views.teacher_detail,
        name="teacher_detail",
    ),

    # =====================================================
    # EDIT TEACHER
    # =====================================================

    path(
        "<int:pk>/edit/",
        views.edit_teacher,
        name="edit_teacher",
    ),

    # =====================================================
    # DELETE TEACHER
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_teacher,
        name="delete_teacher",
    ),

    # =====================================================
    # SALARY LIST
    # =====================================================

    path(
        "salary/",
        views.salary_list,
        name="salary_list",
    ),

    # =====================================================
    # ADD SALARY
    # =====================================================

    path(
        "salary/add/",
        views.add_salary,
        name="add_salary",
    ),

    # =====================================================
    # SALARY DETAIL
    # =====================================================

    path(
        "salary/<int:pk>/",
        views.salary_detail,
        name="salary_detail",
    ),

    # =====================================================
    # EDIT SALARY
    # =====================================================

    path(
        "salary/<int:pk>/edit/",
        views.edit_salary,
        name="edit_salary",
    ),

    # =====================================================
    # DELETE SALARY
    # =====================================================

    path(
        "salary/<int:pk>/delete/",
        views.delete_salary,
        name="delete_salary",
    ),

    # =====================================================
    # SALARY REPORT
    # =====================================================

    path(
        "salary-report/",
        views.salary_report,
        name="salary_report",
    ),

    # =====================================================
    # PRINT SALARY REPORT
    # =====================================================

    path(
        "salary-report/print/",
        views.print_salary_report,
        name="print_salary_report",
    ),
]