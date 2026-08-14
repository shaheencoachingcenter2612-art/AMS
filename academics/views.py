from django.shortcuts import render, redirect, get_object_or_404

from .models import Session, ClassRoom, Section, Subject
from .forms import (
    SessionForm,
    ClassRoomForm,
    SectionForm,
    SubjectForm,
)


# =========================================================
# ACADEMICS DASHBOARD
# =========================================================

def academics_dashboard(request):

    context = {
        "total_sessions": Session.objects.count(),
        "active_sessions": Session.objects.filter(
            is_active=True
        ).count(),

        "total_classes": ClassRoom.objects.count(),
        "total_sections": Section.objects.count(),
        "total_subjects": Subject.objects.count(),

        "active_session": Session.objects.filter(
            is_active=True
        ).first(),
    }

    return render(
        request,
        "academics/dashboard.html",
        context
    )


# =========================================================
# SESSION LIST
# =========================================================

def session_list(request):

    sessions = Session.objects.all().order_by(
        "-start_year"
    )

    return render(
        request,
        "academics/session_list.html",
        {
            "sessions": sessions
        }
    )


# =========================================================
# ADD SESSION
# =========================================================

def add_session(request):

    if request.method == "POST":

        form = SessionForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "academics:session_list"
            )

    else:

        form = SessionForm()

    return render(
        request,
        "academics/session_form.html",
        {
            "form": form,
            "page_title": "Add Session",
        }
    )


# =========================================================
# EDIT SESSION
# =========================================================

def edit_session(request, pk):

    session = get_object_or_404(
        Session,
        pk=pk
    )

    if request.method == "POST":

        form = SessionForm(
            request.POST,
            instance=session
        )

        if form.is_valid():

            form.save()

            return redirect(
                "academics:session_list"
            )

    else:

        form = SessionForm(
            instance=session
        )

    return render(
        request,
        "academics/session_form.html",
        {
            "form": form,
            "page_title": "Edit Session",
            "session": session,
        }
    )


# =========================================================
# DELETE SESSION
# =========================================================

def delete_session(request, pk):

    session = get_object_or_404(
        Session,
        pk=pk
    )

    if request.method == "POST":

        session.delete()

        return redirect(
            "academics:session_list"
        )

    return render(
        request,
        "academics/session_list.html",
        {
            "sessions": Session.objects.all(),
            "delete_confirm": session,
        }
    )


# =========================================================
# CLASSROOM LIST
# =========================================================

def classroom_list(request):

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "academics/classroom_list.html",
        {
            "classrooms": classrooms
        }
    )


# =========================================================
# ADD CLASSROOM
# =========================================================

def add_classroom(request):

    if request.method == "POST":

        form = ClassRoomForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "academics:classroom_list"
            )

    else:

        form = ClassRoomForm()

    return render(
        request,
        "academics/classroom_form.html",
        {
            "form": form,
            "page_title": "Add Class",
        }
    )


# =========================================================
# EDIT CLASSROOM
# =========================================================

def edit_classroom(request, pk):

    classroom = get_object_or_404(
        ClassRoom,
        pk=pk
    )

    if request.method == "POST":

        form = ClassRoomForm(
            request.POST,
            instance=classroom
        )

        if form.is_valid():

            form.save()

            return redirect(
                "academics:classroom_list"
            )

    else:

        form = ClassRoomForm(
            instance=classroom
        )

    return render(
        request,
        "academics/classroom_form.html",
        {
            "form": form,
            "page_title": "Edit Class",
            "classroom": classroom,
        }
    )


# =========================================================
# DELETE CLASSROOM
# =========================================================

def delete_classroom(request, pk):

    classroom = get_object_or_404(
        ClassRoom,
        pk=pk
    )

    if request.method == "POST":

        classroom.delete()

        return redirect(
            "academics:classroom_list"
        )

    return render(
        request,
        "academics/classroom_list.html",
        {
            "classrooms": ClassRoom.objects.all(),
            "delete_confirm": classroom,
        }
    )


# =========================================================
# SECTION LIST
# =========================================================

def section_list(request):

    sections = Section.objects.select_related(
        "classroom"
    ).order_by(
        "classroom__name",
        "name"
    )

    return render(
        request,
        "academics/section_list.html",
        {
            "sections": sections
        }
    )


# =========================================================
# ADD SECTION
# =========================================================

def add_section(request):

    if request.method == "POST":

        form = SectionForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "academics:section_list"
            )

    else:

        form = SectionForm()

    return render(
        request,
        "academics/section_form.html",
        {
            "form": form,
            "page_title": "Add Section",
        }
    )


# =========================================================
# EDIT SECTION
# =========================================================

def edit_section(request, pk):

    section = get_object_or_404(
        Section,
        pk=pk
    )

    if request.method == "POST":

        form = SectionForm(
            request.POST,
            instance=section
        )

        if form.is_valid():

            form.save()

            return redirect(
                "academics:section_list"
            )

    else:

        form = SectionForm(
            instance=section
        )

    return render(
        request,
        "academics/section_form.html",
        {
            "form": form,
            "page_title": "Edit Section",
            "section": section,
        }
    )


# =========================================================
# DELETE SECTION
# =========================================================

def delete_section(request, pk):

    section = get_object_or_404(
        Section,
        pk=pk
    )

    if request.method == "POST":

        section.delete()

        return redirect(
            "academics:section_list"
        )

    return render(
        request,
        "academics/section_list.html",
        {
            "sections": Section.objects.all(),
            "delete_confirm": section,
        }
    )


# =========================================================
# SUBJECT LIST
# =========================================================

def subject_list(request):

    subjects = Subject.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "academics/subject_list.html",
        {
            "subjects": subjects
        }
    )


# =========================================================
# ADD SUBJECT
# =========================================================

def add_subject(request):

    if request.method == "POST":

        form = SubjectForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "academics:subject_list"
            )

    else:

        form = SubjectForm()

    return render(
        request,
        "academics/subject_form.html",
        {
            "form": form,
            "page_title": "Add Subject",
        }
    )


# =========================================================
# EDIT SUBJECT
# =========================================================

def edit_subject(request, pk):

    subject = get_object_or_404(
        Subject,
        pk=pk
    )

    if request.method == "POST":

        form = SubjectForm(
            request.POST,
            instance=subject
        )

        if form.is_valid():

            form.save()

            return redirect(
                "academics:subject_list"
            )

    else:

        form = SubjectForm(
            instance=subject
        )

    return render(
        request,
        "academics/subject_form.html",
        {
            "form": form,
            "page_title": "Edit Subject",
            "subject": subject,
        }
    )


# =========================================================
# DELETE SUBJECT
# =========================================================

def delete_subject(request, pk):

    subject = get_object_or_404(
        Subject,
        pk=pk
    )

    if request.method == "POST":

        subject.delete()

        return redirect(
            "academics:subject_list"
        )

    return render(
        request,
        "academics/subject_list.html",
        {
            "subjects": Subject.objects.all(),
            "delete_confirm": subject,
        }
    )