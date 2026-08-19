from django.urls import path

from . import views


app_name = "finance"


urlpatterns = [

    path(
        "expenses/",
        views.expense_list,
        name="expense_list"
    ),

    path(
        "expenses/add/",
        views.add_expense,
        name="add_expense"
    ),

    path(
        "expenses/<int:pk>/edit/",
        views.edit_expense,
        name="edit_expense"
    ),

    path(
        "expenses/<int:pk>/delete/",
        views.delete_expense,
        name="delete_expense"
    ),
]