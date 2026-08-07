from django.urls import path
from . import views


urlpatterns = [
    path(
        "add/",
        views.add_student,
        name="add_student",
    ),

    path(
        "list/",
        views.student_list,
        name="student_list",
    ),

    path(
        "<int:pk>/",
        views.student_detail,
        name="student_detail",
    ),

    path(
        "<int:pk>/edit/",
        views.edit_student,
        name="edit_student",
    ),
]