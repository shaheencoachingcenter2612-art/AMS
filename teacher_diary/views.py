from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import DiaryEntry
from .forms import DiaryEntryForm

from teachers.models import Teacher
from academics.models import ClassRoom, Section


# =========================================================
# ADD DIARY
# =========================================================

def add_diary(request):

    if request.method == "POST":

        form = DiaryEntryForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                "teacher_diary:diary_list"
            )

    else:

        form = DiaryEntryForm()

    return render(
        request,
        "teacher_diary/add_diary.html",
        {
            "form": form,
            "edit_mode": False,
        }
    )


# =========================================================
# DIARY LIST
# =========================================================

def diary_list(request):

    query = request.GET.get("q", "")
    teacher_id = request.GET.get("teacher", "")
    date = request.GET.get("date", "")
    classroom_id = request.GET.get("classroom", "")
    section_id = request.GET.get("section", "")

    diaries = DiaryEntry.objects.select_related(
        "teacher",
        "classroom",
        "section",
    )

    if query:

        diaries = diaries.filter(
            Q(teacher__first_name__icontains=query)
            |
            Q(teacher__last_name__icontains=query)
            |
            Q(subject__icontains=query)
            |
            Q(topic__icontains=query)
        )

    if teacher_id:

        diaries = diaries.filter(
            teacher_id=teacher_id
        )

    if date:

        diaries = diaries.filter(
            date=date
        )

    if classroom_id:

        diaries = diaries.filter(
            classroom_id=classroom_id
        )

    if section_id:

        diaries = diaries.filter(
            section_id=section_id
        )

    diaries = diaries.order_by(
        "-date",
        "-id"
    )

    teachers_list = Teacher.objects.all().order_by(
        "first_name"
    )

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

    sections = Section.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "teacher_diary/diary_list.html",
        {
            "diaries": diaries,

            "query": query,

            "teacher_id": teacher_id,

            "date": date,

            "classroom_id": classroom_id,

            "section_id": section_id,

            "teachers_list": teachers_list,

            "classrooms": classrooms,

            "sections": sections,
        }
    )


# =========================================================
# DIARY DETAIL
# =========================================================

def diary_detail(request, pk):

    diary = get_object_or_404(
        DiaryEntry,
        pk=pk
    )

    return render(
        request,
        "teacher_diary/diary_detail.html",
        {
            "diary": diary
        }
    )


# =========================================================
# EDIT DIARY
# =========================================================

def edit_diary(request, pk):

    diary = get_object_or_404(
        DiaryEntry,
        pk=pk
    )

    if request.method == "POST":

        form = DiaryEntryForm(
            request.POST,
            instance=diary
        )

        if form.is_valid():

            form.save()

            return redirect(
                "teacher_diary:diary_detail",
                pk=diary.pk
            )

    else:

        form = DiaryEntryForm(
            instance=diary
        )

    return render(
        request,
        "teacher_diary/add_diary.html",
        {
            "form": form,

            "diary": diary,

            "edit_mode": True,
        }
    )


# =========================================================
# DELETE DIARY
# =========================================================

def delete_diary(request, pk):

    diary = get_object_or_404(
        DiaryEntry,
        pk=pk
    )

    if request.method == "POST":

        diary.delete()

        return redirect(
            "teacher_diary:diary_list"
        )

    return render(
        request,
        "teacher_diary/delete_diary.html",
        {
            "diary": diary
        }
    )


# =========================================================
# PRINT DIARY
# =========================================================

def print_diary(request):

    query = request.GET.get("q", "")

    teacher_id = request.GET.get(
        "teacher",
        ""
    )

    date = request.GET.get(
        "date",
        ""
    )

    classroom_id = request.GET.get(
        "classroom",
        ""
    )

    section_id = request.GET.get(
        "section",
        ""
    )

    diaries = DiaryEntry.objects.select_related(
        "teacher",
        "classroom",
        "section",
    )

    if query:

        diaries = diaries.filter(
            Q(teacher__first_name__icontains=query)
            |
            Q(teacher__last_name__icontains=query)
            |
            Q(subject__icontains=query)
            |
            Q(topic__icontains=query)
        )

    if teacher_id:

        diaries = diaries.filter(
            teacher_id=teacher_id
        )

    if date:

        diaries = diaries.filter(
            date=date
        )

    if classroom_id:

        diaries = diaries.filter(
            classroom_id=classroom_id
        )

    if section_id:

        diaries = diaries.filter(
            section_id=section_id
        )

    diaries = diaries.order_by(
        "-date",
        "-id"
    )

    return render(
        request,
        "teacher_diary/print_diary.html",
        {
            "diaries": diaries,

            "query": query,

            "teacher_id": teacher_id,

            "date": date,

            "classroom_id": classroom_id,

            "section_id": section_id,
        }
    )