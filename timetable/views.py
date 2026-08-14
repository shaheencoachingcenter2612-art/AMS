from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import TimetableEntry
from .forms import TimetableEntryForm


# =========================================================
# TIMETABLE DASHBOARD
# =========================================================

def timetable_dashboard(request):

    entries = TimetableEntry.objects.select_related(
        "session",
        "classroom",
        "section",
        "subject",
        "teacher",
    )

    total_entries = entries.count()

    total_teachers = entries.values(
        "teacher"
    ).distinct().count()

    total_classes = entries.values(
        "classroom"
    ).distinct().count()

    total_subjects = entries.values(
        "subject"
    ).distinct().count()

    return render(
        request,
        "timetable/timetable_dashboard.html",
        {
            "total_entries": total_entries,
            "total_teachers": total_teachers,
            "total_classes": total_classes,
            "total_subjects": total_subjects,
        }
    )


# =========================================================
# TIMETABLE LIST
# =========================================================

def timetable_list(request):

    query = request.GET.get("q", "").strip()
    day = request.GET.get("day", "").strip()

    entries = TimetableEntry.objects.select_related(
        "session",
        "classroom",
        "section",
        "subject",
        "teacher",
    )

    if query:

        entries = entries.filter(
            Q(classroom__name__icontains=query)
            |
            Q(section__name__icontains=query)
            |
            Q(subject__name__icontains=query)
            |
            Q(teacher__first_name__icontains=query)
            |
            Q(teacher__last_name__icontains=query)
        )

    if day:

        entries = entries.filter(
            day=day
        )

    entries = entries.order_by(
        "day",
        "start_time"
    )

    return render(
        request,
        "timetable/timetable_list.html",
        {
            "entries": entries,
            "query": query,
            "day": day,
            "day_choices": TimetableEntry.DAY_CHOICES,
        }
    )


# =========================================================
# ADD TIMETABLE
# =========================================================

def add_timetable(request):

    if request.method == "POST":

        form = TimetableEntryForm(
            request.POST
        )

        if form.is_valid():

            entry = form.save()

            return redirect(
                "timetable:timetable_detail",
                pk=entry.pk
            )

    else:

        form = TimetableEntryForm()

    return render(
        request,
        "timetable/add_timetable.html",
        {
            "form": form,
            "edit_mode": False,
        }
    )


# =========================================================
# TIMETABLE DETAIL
# =========================================================

def timetable_detail(request, pk):

    entry = get_object_or_404(
        TimetableEntry.objects.select_related(
            "session",
            "classroom",
            "section",
            "subject",
            "teacher",
        ),
        pk=pk
    )

    return render(
        request,
        "timetable/timetable_detail.html",
        {
            "entry": entry
        }
    )


# =========================================================
# EDIT TIMETABLE
# =========================================================

def edit_timetable(request, pk):

    entry = get_object_or_404(
        TimetableEntry,
        pk=pk
    )

    if request.method == "POST":

        form = TimetableEntryForm(
            request.POST,
            instance=entry
        )

        if form.is_valid():

            form.save()

            return redirect(
                "timetable:timetable_detail",
                pk=entry.pk
            )

    else:

        form = TimetableEntryForm(
            instance=entry
        )

    return render(
        request,
        "timetable/add_timetable.html",
        {
            "form": form,
            "entry": entry,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE TIMETABLE
# =========================================================

def delete_timetable(request, pk):

    entry = get_object_or_404(
        TimetableEntry,
        pk=pk
    )

    if request.method == "POST":

        entry.delete()

        return redirect(
            "timetable:timetable_list"
        )

    return render(
        request,
        "timetable/delete_timetable.html",
        {
            "entry": entry
        }
    )