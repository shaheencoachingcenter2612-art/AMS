from django.urls import path

from . import views


app_name = "fee_management"


urlpatterns = [

    # =====================================================
    # FEE DASHBOARD
    # =====================================================

    path(
        "",
        views.fee_dashboard,
        name="fee_dashboard",
    ),

    path(
        "dashboard/",
        views.fee_dashboard,
        name="fee_dashboard_page",
    ),


    # =====================================================
    # FEE REPORT
    # =====================================================

    path(
        "report/",
        views.fee_report,
        name="fee_report",
    ),

    path(
        "report/print/",
        views.print_fee_report,
        name="print_fee_report",
    ),


    # =====================================================
    # ADD FEE
    # =====================================================

    path(
        "add/",
        views.add_fee,
        name="add_fee",
    ),


    # =====================================================
    # FEE LIST
    # =====================================================

    path(
        "list/",
        views.fee_list,
        name="fee_list",
    ),


    # =====================================================
    # FEE STRUCTURE
    # =====================================================

    path(
        "structure/",
        views.fee_structure_list,
        name="fee_structure_list",
    ),

    path(
        "structure/add/",
        views.add_fee_structure,
        name="add_fee_structure",
    ),

    path(
        "structure/<int:pk>/edit/",
        views.edit_fee_structure,
        name="edit_fee_structure",
    ),

    path(
        "structure/<int:pk>/delete/",
        views.delete_fee_structure,
        name="delete_fee_structure",
    ),


    # =====================================================
    # PRINT / DOWNLOAD FEE RECEIPT
    # =====================================================

    path(
        "<int:pk>/print/",
        views.print_fee_receipt,
        name="print_fee_receipt",
    ),


    # =====================================================
    # FEE DETAIL
    # =====================================================

    path(
        "<int:pk>/",
        views.fee_detail,
        name="fee_detail",
    ),


    # =====================================================
    # EDIT FEE
    # =====================================================

    path(
        "<int:pk>/edit/",
        views.edit_fee,
        name="edit_fee",
    ),


    # =====================================================
    # DELETE FEE
    # =====================================================

    path(
        "<int:pk>/delete/",
        views.delete_fee,
        name="delete_fee",
    ),
]