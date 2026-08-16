from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .models import DiaryEntry
from .forms import DiaryEntryForm

from teachers.models import Teacher


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

    query = request.GET.get(
        "q",
        ""
    ).strip()

    teacher_id = request.GET.get(
        "teacher",
        ""
    ).strip()

    date = request.GET.get(
        "date",
        ""
    ).strip()

    diaries = DiaryEntry.objects.select_related(
        "teacher",
        "classroom",
        "section",
    )


    # =====================================================
    # SEARCH
    # =====================================================

    if query:

        diaries = diaries.filter(
            Q(teacher__first_name__icontains=query)
            |
            Q(teacher__last_name__icontains=query)
            |
            Q(teacher__employee_id__icontains=query)
            |
            Q(classroom__name__icontains=query)
            |
            Q(section__name__icontains=query)
            |
            Q(subject__icontains=query)
            |
            Q(topic__icontains=query)
            |
            Q(description__icontains=query)
        )


    # =====================================================
    # TEACHER FILTER
    # =====================================================

    if teacher_id:

        diaries = diaries.filter(
            teacher_id=teacher_id
        )


    # =====================================================
    # DATE FILTER
    # =====================================================

    if date:

        diaries = diaries.filter(
            date=date
        )


    # =====================================================
    # ORDERING
    # =====================================================

    diaries = diaries.order_by(
        "-date",
        "-id",
    )


    # =====================================================
    # ACTIVE TEACHERS
    # =====================================================

    teachers_list = Teacher.objects.filter(
        status="Active"
    ).order_by(
        "first_name",
        "last_name",
    )


    return render(
        request,
        "teacher_diary/diary_list.html",
        {
            "diaries": diaries,
            "query": query,
            "teacher_id": teacher_id,
            "date": date,
            "teachers_list": teachers_list,
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
            "diary": diary,
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
            "diary": diary,
        }
    )


# =========================================================
# PRINT DIARY
# =========================================================

def print_diary(request):

    query = request.GET.get(
        "q",
        ""
    ).strip()

    teacher_id = request.GET.get(
        "teacher",
        ""
    ).strip()

    date = request.GET.get(
        "date",
        ""
    ).strip()


    diaries = DiaryEntry.objects.select_related(
        "teacher",
        "classroom",
        "section",
    )


    # =====================================================
    # SEARCH
    # =====================================================

    if query:

        diaries = diaries.filter(
            Q(teacher__first_name__icontains=query)
            |
            Q(teacher__last_name__icontains=query)
            |
            Q(teacher__employee_id__icontains=query)
            |
            Q(classroom__name__icontains=query)
            |
            Q(section__name__icontains=query)
            |
            Q(subject__icontains=query)
            |
            Q(topic__icontains=query)
            |
            Q(description__icontains=query)
        )


    # =====================================================
    # TEACHER FILTER
    # =====================================================

    if teacher_id:

        diaries = diaries.filter(
            teacher_id=teacher_id
        )


    # =====================================================
    # DATE FILTER
    # =====================================================

    if date:

        diaries = diaries.filter(
            date=date
        )


    # =====================================================
    # ORDERING
    # =====================================================

    diaries = diaries.order_by(
        "-date",
        "-id",
    )


    return render(
        request,
        "teacher_diary/print_diary.html",
        {
            "diaries": diaries,
            "query": query,
            "teacher_id": teacher_id,
            "date": date,
        }
    )