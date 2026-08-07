from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

from students.models import Student
from academics.models import Session, ClassRoom, Section
from fee_management.models import Fee


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

    context = {
        "total_students": Student.objects.count(),
        "total_sessions": Session.objects.count(),
        "total_classes": ClassRoom.objects.count(),
        "total_sections": Section.objects.count(),
        "total_fees": Fee.objects.count(),
    }

    return render(
        request,
        "dashboard.html",
        context
    )