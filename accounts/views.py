from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import UserCreateForm
from .models import UserProfile
from .utils import role_required


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            auth_login(
                request,
                user,
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(
        request,
        "accounts/login.html",
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    return redirect(
        "accounts:login"
    )


# =========================================================
# USER LIST
# SUPER ADMIN ONLY
# =========================================================

@login_required
@role_required("Super Admin")
def user_list(request):

    users = User.objects.select_related(
        "profile",
        "teacher_profile",
    ).all().order_by(
        "username"
    )

    return render(
        request,
        "accounts/user_list.html",
        {
            "users": users,
        },
    )


# =========================================================
# CREATE USER
# SUPER ADMIN ONLY
# =========================================================

@login_required
@role_required("Super Admin")
def create_user(request):

    if request.method == "POST":

        form = UserCreateForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            messages.success(
                request,
                f"User '{user.username}' created successfully.",
            )

            return redirect(
                "accounts:user_list"
            )

    else:

        form = UserCreateForm()

    return render(
        request,
        "accounts/create_user.html",
        {
            "form": form,
        },
    )


# =========================================================
# USER DETAIL
# SUPER ADMIN ONLY
# =========================================================

@login_required
@role_required("Super Admin")
def user_detail(request, user_id):

    try:

        user = User.objects.select_related(
            "profile",
            "teacher_profile",
        ).get(
            id=user_id
        )

    except User.DoesNotExist:

        messages.error(
            request,
            "User not found.",
        )

        return redirect(
            "accounts:user_list"
        )

    return render(
        request,
        "accounts/user_detail.html",
        {
            "user_obj": user,
        },
    )


# =========================================================
# TEACHER PROFILE
# =========================================================

@login_required
def my_teacher_profile(request):

    if not hasattr(
        request.user,
        "teacher_profile",
    ):

        messages.error(
            request,
            "No teacher profile is linked with your account.",
        )

        return redirect(
            "dashboard"
        )

    teacher = request.user.teacher_profile

    return render(
        request,
        "accounts/my_teacher_profile.html",
        {
            "teacher": teacher,
        },
    )