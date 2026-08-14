from django.urls import path

from . import views


app_name = "timetable"


urlpatterns = [

    # Dashboard

    path(
        "",
        views.timetable_dashboard,
        name="timetable_dashboard",
    ),

    path(
        "dashboard/",
        views.timetable_dashboard,
        name="timetable_dashboard_page",
    ),

    # List

    path(
        "list/",
        views.timetable_list,
        name="timetable_list",
    ),

    # Add

    path(
        "add/",
        views.add_timetable,
        name="add_timetable",
    ),

    # Detail

    path(
        "<int:pk>/",
        views.timetable_detail,
        name="timetable_detail",
    ),

    # Edit

    path(
        "<int:pk>/edit/",
        views.edit_timetable,
        name="edit_timetable",
    ),

    # Delete

    path(
        "<int:pk>/delete/",
        views.delete_timetable,
        name="delete_timetable",
    ),
]