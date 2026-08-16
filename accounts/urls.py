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
    # SUPER ADMIN
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

    # =====================================================
    # MY TEACHER PROFILE
    # =====================================================

    path(
        "my-teacher-profile/",
        views.my_teacher_profile,
        name="my_teacher_profile",
    ),
]