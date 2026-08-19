from django.urls import path

from . import views


app_name = "accounts"


urlpatterns = [

    # =====================================================
    # LOGIN
    # =====================================================

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    # =====================================================
    # LOGOUT
    # =====================================================

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    # =====================================================
    # USER MANAGEMENT
    # SUPER ADMIN ONLY
    # =====================================================

    path(
        "users/",
        views.user_list,
        name="user_list",
    ),

    path(
        "users/create/",
        views.create_user,
        name="create_user",
    ),

    path(
        "users/<int:user_id>/",
        views.user_detail,
        name="user_detail",
    ),

    path(
        "users/<int:user_id>/edit/",
        views.edit_user,
        name="edit_user",
    ),

    path(
        "users/<int:user_id>/reset-password/",
        views.reset_user_password,
        name="reset_user_password",
    ),

    path(
        "users/<int:user_id>/toggle-status/",
        views.toggle_user_status,
        name="toggle_user_status",
    ),

    path(
        "users/<int:user_id>/delete/",
        views.delete_user,
        name="delete_user",
    ),

    # =====================================================
    # MY TEACHER PROFILE
    # =====================================================

    path(
        "my-teacher-profile/",
        views.my_teacher_profile,
        name="my_teacher_profile",
    ),

]