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

    teacher = getattr(
        request.user,
        "teacher_profile",
        None
    )

    if teacher is None:

        return render(
            request,
            "teacher_diary/add_diary.html",
            {
                "error":
                    "Your teacher profile is not linked "
                    "with your user account."
            }
        )

    if request.method == "POST":

        form = DiaryEntryForm(
            request.POST
        )

        if form.is_valid():

            diary = form.save(
                commit=False
            )

            diary.teacher = teacher

            diary.save()

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

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if query:

        diaries = diaries.filter(

            Q(
                teacher__first_name__icontains=query
            )
            |
            Q(
                teacher__last_name__icontains=query
            )
            |
            Q(
                teacher__employee_id__icontains=query
            )
            |
            Q(
                classroom__name__icontains=query
            )
            |
            Q(
                section__name__icontains=query
            )
            |
            Q(
                subject__icontains=query
            )
            |
            Q(
                topic__icontains=query
            )
            |
            Q(
                description__icontains=query
            )
        )

    # -----------------------------------------------------
    # TEACHER FILTER
    # -----------------------------------------------------

    if teacher_id:

        diaries = diaries.filter(
            teacher_id=teacher_id
        )

    # -----------------------------------------------------
    # DATE FILTER
    # -----------------------------------------------------

    if date:

        diaries = diaries.filter(
            date=date
        )

    diaries = diaries.order_by(
        "-date",
        "-id",
    )

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

            updated_diary = form.save(
                commit=False
            )

            updated_diary.teacher = diary.teacher

            updated_diary.save()

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
# PRINT / JPG DIARY
# =========================================================

def print_diary(request):

    # -----------------------------------------------------
    # FILTER VALUES
    # -----------------------------------------------------

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

    classroom_id = request.GET.get(
        "classroom",
        ""
    ).strip()

    section_id = request.GET.get(
        "section",
        ""
    ).strip()

    # -----------------------------------------------------
    # BASE QUERYSET
    # -----------------------------------------------------

    diaries = DiaryEntry.objects.select_related(
        "teacher",
        "classroom",
        "section",
    )

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if query:

        diaries = diaries.filter(

            Q(
                teacher__first_name__icontains=query
            )
            |
            Q(
                teacher__last_name__icontains=query
            )
            |
            Q(
                teacher__employee_id__icontains=query
            )
            |
            Q(
                classroom__name__icontains=query
            )
            |
            Q(
                section__name__icontains=query
            )
            |
            Q(
                subject__icontains=query
            )
            |
            Q(
                topic__icontains=query
            )
            |
            Q(
                description__icontains=query
            )
            |
            Q(
                homework__icontains=query
            )
            |
            Q(
                remarks__icontains=query
            )
        )

    # -----------------------------------------------------
    # TEACHER FILTER
    # -----------------------------------------------------

    if teacher_id:

        diaries = diaries.filter(
            teacher_id=teacher_id
        )

    # -----------------------------------------------------
    # DATE FILTER
    # -----------------------------------------------------

    if date:

        diaries = diaries.filter(
            date=date
        )

    # -----------------------------------------------------
    # CLASS FILTER
    # -----------------------------------------------------

    if classroom_id:

        diaries = diaries.filter(
            classroom_id=classroom_id
        )

    # -----------------------------------------------------
    # SECTION FILTER
    # -----------------------------------------------------

    if section_id:

        diaries = diaries.filter(
            section_id=section_id
        )

    # -----------------------------------------------------
    # ORDERING
    # -----------------------------------------------------

    diaries = diaries.order_by(
        "date",
        "subject",
        "id",
    )

    # -----------------------------------------------------
    # AVAILABLE CLASSES
    # -----------------------------------------------------

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

    # -----------------------------------------------------
    # AVAILABLE SECTIONS
    # -----------------------------------------------------

    sections = Section.objects.select_related(
        "classroom"
    ).all().order_by(
        "classroom__name",
        "name",
    )

    # -----------------------------------------------------
    # ACTIVE TEACHERS
    # -----------------------------------------------------

    teachers_list = Teacher.objects.filter(
        status="Active"
    ).order_by(
        "first_name",
        "last_name",
    )

    # -----------------------------------------------------
    # SELECTED INFORMATION
    # -----------------------------------------------------

    first_diary = diaries.first()

    combined_date = None
    combined_classroom = None
    combined_section = None

    if first_diary:

        combined_date = first_diary.date
        combined_classroom = first_diary.classroom
        combined_section = first_diary.section

    # -----------------------------------------------------
    # IF USER SELECTED CLASS
    # -----------------------------------------------------

    if classroom_id:

        try:
            combined_classroom = ClassRoom.objects.get(
                pk=classroom_id
            )
        except ClassRoom.DoesNotExist:
            combined_classroom = None

    # -----------------------------------------------------
    # IF USER SELECTED SECTION
    # -----------------------------------------------------

    if section_id:

        try:
            combined_section = Section.objects.get(
                pk=section_id
            )
        except Section.DoesNotExist:
            combined_section = None

    # -----------------------------------------------------
    # DATE / DAY
    # -----------------------------------------------------

    day_name = ""

    if combined_date:

        day_name = combined_date.strftime(
            "%A"
        )

    # -----------------------------------------------------
    # FINAL RENDER
    # -----------------------------------------------------

    return render(
        request,
        "teacher_diary/print_diary.html",
        {
            "diaries": diaries,

            "query":
                query,

            "teacher_id":
                teacher_id,

            "date":
                date,

            "classroom_id":
                classroom_id,

            "section_id":
                section_id,

            "teachers_list":
                teachers_list,

            "classrooms":
                classrooms,

            "sections":
                sections,

            "combined_date":
                combined_date,

            "combined_classroom":
                combined_classroom,

            "combined_section":
                combined_section,

            "day_name":
                day_name,
        }
    )