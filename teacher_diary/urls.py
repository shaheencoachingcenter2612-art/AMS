from django.urls import path
from . import views


app_name = "teacher_diary"


urlpatterns = [

    # =====================================================
    # TEACHER DIARY HOME
    # =====================================================

    path(
        "",
        views.diary_list,
        name="diary_home",
    ),

    # =====================================================
    # ADD DIARY
    # =====================================================

    path(
        "add/",
        views.add_diary,
        name="add_diary",
    ),

    # =====================================================
    # DIARY LIST
    # =====================================================

    path(
        "list/",
        views.diary_list,
        name="diary_list",
    ),

    # =====================================================
    # PRINT DIARY
    # =====================================================

    path(
        "print/",
        views.print_diary,
        name="print_diary",
    ),

    # =====================================================
    # DIARY DETAIL
    # =====================================================

    path(
        "<int:pk>/",
        views.diary_detail,
        name="diary_detail",
    ),

    # =====================================================
    # EDIT DIARY
    # =====================================================

    path(
        "<int:pk>/edit/",
        views.edit_diary,
        name="edit_diary",
    ),

    # =====================================================
    # DELETE DIARY
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_diary,
        name="delete_diary",
    ),
]