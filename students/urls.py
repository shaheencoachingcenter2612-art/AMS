from django.urls import path
from . import views

app_name = "students"

urlpatterns = [

    # =====================================================
    # ADD STUDENT
    # =====================================================

    path(
        "add/",
        views.add_student,
        name="add_student",
    ),


    # =====================================================
    # STUDENT LIST
    # =====================================================

    path(
        "list/",
        views.student_list,
        name="student_list",
    ),


    # =====================================================
    # STUDENT DETAIL
    # =====================================================

    path(
        "<int:pk>/",
        views.student_detail,
        name="student_detail",
    ),


    # =====================================================
    # EDIT STUDENT
    # =====================================================

    path(
        "<int:pk>/edit/",
        views.edit_student,
        name="edit_student",
    ),


    # =====================================================
    # DELETE STUDENT
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_student,
        name="delete_student",
    ),


    # =====================================================
    # STUDENT REPORT
    # =====================================================

    path(
        "report/",
        views.student_report,
        name="student_report",
    ),


    # =====================================================
    # PRINT STUDENT REPORT
    # =====================================================

    path(
        "report/print/",
        views.print_student_report,
        name="print_student_report",
    ),

]