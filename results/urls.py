from django.urls import path
from . import views


app_name = "results"


urlpatterns = [

    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "",
        views.result_dashboard,
        name="result_dashboard",
    ),


    # =====================================================
    # RESULT LIST
    # =====================================================

    path(
        "list/",
        views.result_list,
        name="result_list",
    ),


    # =====================================================
    # ADD RESULT
    # =====================================================

    path(
        "add/",
        views.add_result,
        name="add_result",
    ),


    # =====================================================
    # RESULT CARD
    # =====================================================

    path(
        "card/<int:student_id>/",
        views.result_card,
        name="result_card",
    ),


    # =====================================================
    # PRINT RESULT CARD
    # =====================================================

    path(
        "card/<int:student_id>/print/",
        views.print_result_card,
        name="print_result_card",
    ),


    # =====================================================
    # RESULT DETAIL
    # =====================================================

    path(
        "<int:pk>/",
        views.result_detail,
        name="result_detail",
    ),


    # =====================================================
    # EDIT RESULT
    # =====================================================

    path(
        "<int:pk>/edit/",
        views.edit_result,
        name="edit_result",
    ),


    # =====================================================
    # DELETE RESULT
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_result,
        name="delete_result",
    ),

]