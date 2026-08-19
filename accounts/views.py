from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserCreateForm, UserPasswordResetForm
from .models import UserProfile
from .utils import role_required


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:

        return redirect(
            "website:dashboard"
        )

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            if not user.is_active:

                messages.error(
                    request,
                    "Your account is inactive. Please contact the administrator.",
                )

                return render(
                    request,
                    "accounts/login.html",
                )

            auth_login(
                request,
                user,
            )

            return redirect(
                "website:dashboard"
            )

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

    messages.success(
        request,
        "You have been logged out successfully.",
    )

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

    user = get_object_or_404(
        User.objects.select_related(
            "profile",
            "teacher_profile",
        ),
        id=user_id,
    )

    return render(
        request,
        "accounts/user_detail.html",
        {
            "user_obj": user,
        },
    )


# =========================================================
# EDIT USER
# SUPER ADMIN ONLY
# =========================================================

@login_required
@role_required("Super Admin")
def edit_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id,
    )

    if user.is_superuser:

        messages.error(
            request,
            "The Super Admin account cannot be edited from this page.",
        )

        return redirect(
            "accounts:user_detail",
            user_id=user.id,
        )

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name",
            "",
        ).strip()

        last_name = request.POST.get(
            "last_name",
            "",
        ).strip()

        email = request.POST.get(
            "email",
            "",
        ).strip()

        role = request.POST.get(
            "role",
            "",
        )

        allowed_roles = dict(
            UserProfile.ROLE_CHOICES
        )

        if role not in allowed_roles:

            messages.error(
                request,
                "Invalid user role selected.",
            )

            return redirect(
                "accounts:edit_user",
                user_id=user.id,
            )

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save(
            update_fields=[
                "first_name",
                "last_name",
                "email",
            ]
        )

        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                "role": role,
            },
        )

        messages.success(
            request,
            f"User '{user.username}' has been updated successfully.",
        )

        return redirect(
            "accounts:user_detail",
            user_id=user.id,
        )

    profile = getattr(
        user,
        "profile",
        None,
    )

    current_role = (
        profile.role
        if profile
        else "Teacher"
    )

    return render(
        request,
        "accounts/edit_user.html",
        {
            "user_obj": user,
            "role_choices": UserProfile.ROLE_CHOICES,
            "current_role": current_role,
        },
    )


# =========================================================
# RESET USER PASSWORD
# SUPER ADMIN ONLY
# =========================================================

@login_required
@role_required("Super Admin")
def reset_user_password(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id,
    )

    if user.is_superuser:

        messages.error(
            request,
            "The Super Admin password cannot be reset from this page.",
        )

        return redirect(
            "accounts:user_detail",
            user_id=user.id,
        )

    if request.method == "POST":

        form = UserPasswordResetForm(
            request.POST
        )

        if form.is_valid():

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save(
                update_fields=[
                    "password",
                ]
            )

            messages.success(
                request,
                f"Password for '{user.username}' has been changed successfully.",
            )

            return redirect(
                "accounts:user_detail",
                user_id=user.id,
            )

    else:

        form = UserPasswordResetForm()

    return render(
        request,
        "accounts/reset_user_password.html",
        {
            "user_obj": user,
            "form": form,
        },
    )


# =========================================================
# TOGGLE USER STATUS
# SUPER ADMIN ONLY
# =========================================================

@login_required
@role_required("Super Admin")
def toggle_user_status(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id,
    )

    if user.is_superuser:

        messages.error(
            request,
            "The Super Admin account cannot be deactivated.",
        )

        return redirect(
            "accounts:user_detail",
            user_id=user.id,
        )

    if user == request.user:

        messages.error(
            request,
            "You cannot deactivate your own account.",
        )

        return redirect(
            "accounts:user_detail",
            user_id=user.id,
        )

    user.is_active = not user.is_active

    user.save(
        update_fields=[
            "is_active",
        ]
    )

    if user.is_active:

        messages.success(
            request,
            f"User '{user.username}' has been activated.",
        )

    else:

        messages.warning(
            request,
            f"User '{user.username}' has been deactivated.",
        )

    return redirect(
        "accounts:user_detail",
        user_id=user.id,
    )


# =========================================================
# DELETE USER
# SUPER ADMIN ONLY
# =========================================================

@login_required
@role_required("Super Admin")
def delete_user(request, user_id):

    user = get_object_or_404(
        User,
        id=user_id,
    )

    if user.is_superuser:

        messages.error(
            request,
            "The Super Admin account cannot be deleted.",
        )

        return redirect(
            "accounts:user_detail",
            user_id=user.id,
        )

    if user == request.user:

        messages.error(
            request,
            "You cannot delete your own account.",
        )

        return redirect(
            "accounts:user_detail",
            user_id=user.id,
        )

    if request.method == "POST":

        username = user.username

        user.delete()

        messages.success(
            request,
            f"User '{username}' has been deleted successfully.",
        )

        return redirect(
            "accounts:user_list"
        )

    return render(
        request,
        "accounts/delete_user.html",
        {
            "user_obj": user,
        },
    )


# =========================================================
# MY TEACHER PROFILE
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
            "website:dashboard"
        )

    teacher = request.user.teacher_profile

    return render(
        request,
        "accounts/my_teacher_profile.html",
        {
            "teacher": teacher,
        },
    )