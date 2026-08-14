from django.urls import path

from . import views


app_name = "salary"


urlpatterns = [

    # Dashboard

    path(
        "",
        views.salary_dashboard,
        name="salary_dashboard",
    ),

    # List

    path(
        "list/",
        views.salary_list,
        name="salary_list",
    ),

    # Add

    path(
        "add/",
        views.add_salary,
        name="add_salary",
    ),

    # Print Slip

    path(
        "<int:pk>/print/",
        views.print_salary_slip,
        name="print_salary_slip",
    ),

    # Detail

    path(
        "<int:pk>/",
        views.salary_detail,
        name="salary_detail",
    ),

    # Edit

    path(
        "<int:pk>/edit/",
        views.edit_salary,
        name="edit_salary",
    ),

    # Delete

    path(
        "<int:pk>/delete/",
        views.delete_salary,
        name="delete_salary",
    ),
]