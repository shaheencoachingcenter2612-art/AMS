from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Avg

from .models import Result
from .forms import ResultForm
from students.models import Student


# =========================================================
# RESULTS DASHBOARD
# =========================================================

def result_dashboard(request):

    results = Result.objects.select_related(
        "student",
        "session",
        "classroom",
        "section",
        "subject",
    )

    total_results = results.count()

    average_marks = results.aggregate(
        average=Avg("obtained_marks")
    )["average"] or 0

    passed_results = 0
    failed_results = 0

    for result in results:

        if result.total_marks:

            percentage = (
                result.obtained_marks
                / result.total_marks
            ) * 100

            if percentage >= 40:
                passed_results += 1
            else:
                failed_results += 1

    return render(
        request,
        "results/result_dashboard.html",
        {
            "total_results": total_results,
            "average_marks": round(average_marks, 2),
            "passed_results": passed_results,
            "failed_results": failed_results,
        }
    )


# =========================================================
# RESULT LIST
# =========================================================

def result_list(request):

    query = request.GET.get("q", "")
    exam_type = request.GET.get("exam_type", "")

    results = Result.objects.select_related(
        "student",
        "session",
        "classroom",
        "section",
        "subject",
    )

    if query:

        results = results.filter(
            Q(student__first_name__icontains=query)
            | Q(student__last_name__icontains=query)
            | Q(student__admission_no__icontains=query)
            | Q(subject__name__icontains=query)
        )

    if exam_type:

        results = results.filter(
            exam_type=exam_type
        )

    results = results.order_by(
        "-exam_date",
        "student__first_name",
    )

    return render(
        request,
        "results/result_list.html",
        {
            "results": results,
            "query": query,
            "exam_type": exam_type,
        }
    )


# =========================================================
# ADD RESULT
# =========================================================

def add_result(request):

    if request.method == "POST":

        form = ResultForm(request.POST)

        if form.is_valid():

            result = form.save()

            return redirect(
                "results:result_detail",
                pk=result.pk
            )

    else:

        form = ResultForm()

    return render(
        request,
        "results/add_result.html",
        {
            "form": form
        }
    )


# =========================================================
# RESULT DETAIL
# =========================================================

def result_detail(request, pk):

    result = get_object_or_404(
        Result.objects.select_related(
            "student",
            "session",
            "classroom",
            "section",
            "subject",
        ),
        pk=pk
    )

    return render(
        request,
        "results/result_detail.html",
        {
            "result": result
        }
    )


# =========================================================
# EDIT RESULT
# =========================================================

def edit_result(request, pk):

    result = get_object_or_404(
        Result,
        pk=pk
    )

    if request.method == "POST":

        form = ResultForm(
            request.POST,
            instance=result
        )

        if form.is_valid():

            form.save()

            return redirect(
                "results:result_detail",
                pk=result.pk
            )

    else:

        form = ResultForm(
            instance=result
        )

    return render(
        request,
        "results/add_result.html",
        {
            "form": form,
            "result": result,
            "edit_mode": True,
        }
    )


# =========================================================
# DELETE RESULT
# =========================================================

def delete_result(request, pk):

    result = get_object_or_404(
        Result,
        pk=pk
    )

    if request.method == "POST":

        result.delete()

        return redirect(
            "results:result_list"
        )

    return render(
        request,
        "results/delete_result.html",
        {
            "result": result
        }
    )


# =========================================================
# RESULT CARD DATA
# =========================================================

def get_result_card_data(student_id, exam_type="", exam_date=""):

    # -----------------------------------------------------
    # Student
    # -----------------------------------------------------

    student = get_object_or_404(
        Student,
        pk=student_id
    )

    # -----------------------------------------------------
    # Student Results
    # -----------------------------------------------------

    student_results = Result.objects.select_related(
        "student",
        "session",
        "classroom",
        "section",
        "subject",
    ).filter(
        student=student
    )

    # -----------------------------------------------------
    # If no exam filter is supplied,
    # automatically use the latest examination.
    # -----------------------------------------------------

    if not exam_type and not exam_date:

        latest_result = student_results.order_by(
            "-exam_date",
            "-id"
        ).first()

        if latest_result:

            exam_type = latest_result.exam_type
            exam_date = latest_result.exam_date

    # -----------------------------------------------------
    # Apply Exam Type
    # -----------------------------------------------------

    if exam_type:

        student_results = student_results.filter(
            exam_type=exam_type
        )

    # -----------------------------------------------------
    # Apply Exam Date
    # -----------------------------------------------------

    if exam_date:

        student_results = student_results.filter(
            exam_date=exam_date
        )

    # -----------------------------------------------------
    # No Results
    # -----------------------------------------------------

    if not student_results.exists():

        return {
            "student": student,
            "results": [],
            "no_results": True,
        }

    # -----------------------------------------------------
    # First Result
    # -----------------------------------------------------

    first_result = student_results.order_by(
        "subject__name"
    ).first()

    session = first_result.session
    classroom = first_result.classroom
    section = first_result.section

    # -----------------------------------------------------
    # Results ordered by Subject
    # -----------------------------------------------------

    results = student_results.order_by(
        "subject__name"
    )

    # -----------------------------------------------------
    # Grand Total
    # -----------------------------------------------------

    total_marks = sum(
        result.total_marks
        for result in results
    )

    obtained_marks = sum(
        result.obtained_marks
        for result in results
    )

    # -----------------------------------------------------
    # Percentage
    # -----------------------------------------------------

    if total_marks:

        percentage = round(
            (obtained_marks / total_marks) * 100,
            2
        )

    else:

        percentage = 0

    # -----------------------------------------------------
    # Grade
    # -----------------------------------------------------

    if percentage >= 80:
        grade = "A+"

    elif percentage >= 70:
        grade = "A"

    elif percentage >= 60:
        grade = "B"

    elif percentage >= 50:
        grade = "C"

    elif percentage >= 40:
        grade = "D"

    else:
        grade = "F"

    # -----------------------------------------------------
    # Final Result
    # -----------------------------------------------------

    final_result = (
        "Pass"
        if percentage >= 40
        else "Fail"
    )

    # -----------------------------------------------------
    # Position
    # -----------------------------------------------------

    position = "-"

    ranking_results = Result.objects.filter(
        session=session,
        classroom=classroom,
        section=section,
        exam_type=exam_type,
        exam_date=exam_date,
    )

    student_totals = {}

    for item in ranking_results:

        if item.student_id not in student_totals:

            student_totals[item.student_id] = {
                "total": 0,
                "obtained": 0,
            }

        student_totals[item.student_id]["total"] += (
            item.total_marks
        )

        student_totals[item.student_id]["obtained"] += (
            item.obtained_marks
        )

    ranking = []

    for student_pk, values in student_totals.items():

        if values["total"]:

            student_percentage = (
                values["obtained"]
                / values["total"]
            ) * 100

        else:

            student_percentage = 0

        ranking.append(
            (
                student_pk,
                student_percentage
            )
        )

    ranking.sort(
        key=lambda x: x[1],
        reverse=True
    )

    for index, item in enumerate(
        ranking,
        start=1
    ):

        if item[0] == student.id:

            position = index
            break

    # -----------------------------------------------------
    # Return Data
    # -----------------------------------------------------

    return {
        "student": student,
        "results": results,

        "session": session,
        "classroom": classroom,
        "section": section,

        "total_marks": total_marks,
        "obtained_marks": obtained_marks,
        "percentage": percentage,

        "grade": grade,
        "final_result": final_result,
        "position": position,

        "exam_type": exam_type,
        "exam_date": exam_date,

        "no_results": False,
    }


# =========================================================
# PRINT-FRIENDLY RESULT CARD
# =========================================================

def result_card(request, student_id):

    exam_type = request.GET.get(
        "exam_type",
        ""
    )

    exam_date = request.GET.get(
        "exam_date",
        ""
    )

    data = get_result_card_data(
        student_id,
        exam_type,
        exam_date
    )

    return render(
        request,
        "results/result_card.html",
        data
    )


# =========================================================
# PRINT RESULT CARD
# =========================================================

def print_result_card(request, student_id):

    exam_type = request.GET.get(
        "exam_type",
        ""
    )

    exam_date = request.GET.get(
        "exam_date",
        ""
    )

    data = get_result_card_data(
        student_id,
        exam_type,
        exam_date
    )

    data["print_mode"] = True

    return render(
        request,
        "results/result_card.html",
        data
    )