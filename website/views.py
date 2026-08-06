from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "home.html")


def login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")

    return render(request, "login.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html")