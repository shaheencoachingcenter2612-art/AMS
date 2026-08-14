from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import StudentForm
from .models import Student


# =========================================================
# ADD STUDENT
# =========================================================

def add_student(request):

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                "students:student_list"
            )

    else:

        form = StudentForm()

    return render(
        request,
        "students/add_student.html",
        {
            "form": form
        }
    )


# =========================================================
# STUDENT LIST
# =========================================================

def student_list(request):

    query = request.GET.get(
        "q",
        ""
    )

    students = Student.objects.all()

    if query:

        students = students.filter(

            Q(
                admission_no__icontains=query
            )

            |

            Q(
                first_name__icontains=query
            )

            |

            Q(
                last_name__icontains=query
            )

            |

            Q(
                father_name__icontains=query
            )

            |

            Q(
                phone__icontains=query
            )

        )

    students = students.order_by(
        "first_name"
    )

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "query": query,
        }
    )


# =========================================================
# STUDENT DETAIL
# =========================================================

def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    return render(
        request,
        "students/student_detail.html",
        {
            "student": student
        }
    )


# =========================================================
# EDIT STUDENT
# =========================================================

def edit_student(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        form = StudentForm(
            request.POST,
            request.FILES,
            instance=student
        )

        if form.is_valid():

            form.save()

            return redirect(
                "students:student_detail",
                pk=student.pk
            )

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        "students/add_student.html",
        {
            "form": form,
            "student": student,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE STUDENT
# =========================================================

def delete_student(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == "POST":

        student.delete()

        return redirect(
            "students:student_list"
        )

    return render(
        request,
        "students/delete_student.html",
        {
            "student": student
        }
    )
    # =========================================================
# STUDENT REPORT
# =========================================================

def student_report(request):

    students = Student.objects.select_related(
        "session",
        "classroom",
        "section"
    ).all()

    query = request.GET.get("q", "").strip()
    classroom = request.GET.get("classroom", "").strip()
    section = request.GET.get("section", "").strip()
    gender = request.GET.get("gender", "").strip()

    # SEARCH
    if query:

        students = students.filter(
            Q(admission_no__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(father_name__icontains=query) |
            Q(phone__icontains=query)
        )

    # CLASS FILTER
    if classroom:
        students = students.filter(
            classroom_id=classroom
        )

    # SECTION FILTER
    if section:
        students = students.filter(
            section_id=section
        )

    # GENDER FILTER
    if gender:
        students = students.filter(
            gender=gender
        )

    students = students.order_by(
        "classroom__name",
        "section__name",
        "first_name"
    )

    return render(
        request,
        "students/student_report.html",
        {
            "students": students,
            "query": query,
            "classroom": classroom,
            "section": section,
            "gender": gender,
        }
    )


# =========================================================
# PRINT STUDENT REPORT
# =========================================================

def print_student_report(request):

    students = Student.objects.select_related(
        "session",
        "classroom",
        "section"
    ).all()

    query = request.GET.get("q", "").strip()
    classroom = request.GET.get("classroom", "").strip()
    section = request.GET.get("section", "").strip()
    gender = request.GET.get("gender", "").strip()

    if query:

        students = students.filter(
            Q(admission_no__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(father_name__icontains=query) |
            Q(phone__icontains=query)
        )

    if classroom:
        students = students.filter(
            classroom_id=classroom
        )

    if section:
        students = students.filter(
            section_id=section
        )

    if gender:
        students = students.filter(
            gender=gender
        )

    students = students.order_by(
        "classroom__name",
        "section__name",
        "first_name"
    )

    return render(
        request,
        "students/print_student_report.html",
        {
            "students": students,
        }
    )