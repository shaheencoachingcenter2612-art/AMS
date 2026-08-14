from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import UserCreateForm
from .models import UserProfile
from .utils import role_required


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(
                request,
                user
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "accounts/login.html"
    )


@login_required
def logout_view(request):

    logout(request)

    return redirect("accounts:login")


@login_required
@role_required("Super Admin")
def user_list(request):

    users = User.objects.all().order_by(
        "username"
    )

    return render(
        request,
        "accounts/user_list.html",
        {
            "users": users
        }
    )


@login_required
@role_required("Super Admin")
def create_user(request):

    if request.method == "POST":

        form = UserCreateForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "User created successfully."
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
            "form": form
        }
    )