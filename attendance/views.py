from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.db.models import Q, Count
from django.utils import timezone
from django.contrib import messages

from .models import Attendance
from .forms import (
    AttendanceForm,
    BulkAttendanceFilterForm,
)

from students.models import Student
from academics.models import (
    Session,
    ClassRoom,
    Section,
)


# =========================================================
# ATTENDANCE DASHBOARD
# =========================================================

def attendance_dashboard(request):

    today = timezone.localdate()

    total = Attendance.objects.count()

    present = Attendance.objects.filter(
        status="Present"
    ).count()

    absent = Attendance.objects.filter(
        status="Absent"
    ).count()

    leave = Attendance.objects.filter(
        status="Leave"
    ).count()

    percentage = (
        round((present / total) * 100, 2)
        if total
        else 0
    )

    today_records = Attendance.objects.filter(
        date=today
    )

    today_total = today_records.count()

    today_present = today_records.filter(
        status="Present"
    ).count()

    today_absent = today_records.filter(
        status="Absent"
    ).count()

    today_leave = today_records.filter(
        status="Leave"
    ).count()

    today_percentage = (
        round(
            (today_present / today_total) * 100,
            2,
        )
        if today_total
        else 0
    )

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

    class_summary = []

    for classroom in classrooms:

        records = Attendance.objects.filter(
            classroom=classroom
        )

        class_total = records.count()

        class_present = records.filter(
            status="Present"
        ).count()

        class_absent = records.filter(
            status="Absent"
        ).count()

        class_leave = records.filter(
            status="Leave"
        ).count()

        class_percentage = (
            round(
                (class_present / class_total) * 100,
                2,
            )
            if class_total
            else 0
        )

        class_summary.append({
            "classroom": classroom,
            "total": class_total,
            "present": class_present,
            "absent": class_absent,
            "leave": class_leave,
            "percentage": class_percentage,
        })

    return render(
        request,
        "attendance/attendance_dashboard.html",
        {
            "today": today,
            "total": total,
            "present": present,
            "absent": absent,
            "leave": leave,
            "percentage": percentage,
            "today_total": today_total,
            "today_present": today_present,
            "today_absent": today_absent,
            "today_leave": today_leave,
            "today_percentage": today_percentage,
            "class_summary": class_summary,
        },
    )


# =========================================================
# CLASS-BASED ATTENDANCE
# =========================================================
#
# STEP 1:
# Show all classes.
#
# STEP 2:
# User opens a class.
#
# STEP 3:
# All students belonging to that class are displayed.
#
# STEP 4:
# Mark Present / Absent / Leave.
#
# STEP 5:
# If Leave is selected, remarks/reason can be entered.
# =========================================================


def mark_attendance(request):

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

    today = timezone.localdate()

    class_data = []

    for classroom in classrooms:

        students_count = Student.objects.filter(
            classroom=classroom
        ).count()

        today_records = Attendance.objects.filter(
            classroom=classroom,
            date=today,
        )

        present_count = today_records.filter(
            status="Present"
        ).count()

        absent_count = today_records.filter(
            status="Absent"
        ).count()

        leave_count = today_records.filter(
            status="Leave"
        ).count()

        class_data.append({
            "classroom": classroom,
            "students_count": students_count,
            "present": present_count,
            "absent": absent_count,
            "leave": leave_count,
        })

    return render(
        request,
        "attendance/class_list.html",
        {
            "class_data": class_data,
            "today": today,
        },
    )


# =========================================================
# CLASS ATTENDANCE
# =========================================================

def class_attendance(request, classroom_id):

    classroom = get_object_or_404(
        ClassRoom,
        pk=classroom_id,
    )

    today = timezone.localdate()

    # -----------------------------------------------------
    # SESSION
    # -----------------------------------------------------

    session_id = request.GET.get(
        "session",
        ""
    )

    if not session_id:
        session_id = request.POST.get(
            "session",
            ""
        )

    selected_session = None

    if session_id:
        selected_session = get_object_or_404(
            Session,
            pk=session_id,
        )

    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    date = request.GET.get(
        "date",
        ""
    )

    if not date:
        date = request.POST.get(
            "date",
            ""
        )

    if date:
        try:
            selected_date = timezone.datetime.strptime(
                date,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    # -----------------------------------------------------
    # STUDENTS
    # -----------------------------------------------------

    students_query = Student.objects.filter(
        classroom=classroom
    )

    if selected_session:
        students_query = students_query.filter(
            session=selected_session
        )

    students = students_query.select_related(
        "section",
        "session",
    ).order_by(
        "first_name",
        "last_name",
    )

    # -----------------------------------------------------
    # SAVE ATTENDANCE
    # -----------------------------------------------------

    if request.method == "POST":

        saved_count = 0

        for student in students:

            status = request.POST.get(
                f"status_{student.id}",
                "Present",
            )

            remarks = request.POST.get(
                f"remarks_{student.id}",
                "",
            ).strip()

            # -------------------------------------------------
            # IMPORTANT:
            # If Leave is selected, remarks can contain reason.
            # -------------------------------------------------

            if status == "Leave" and not remarks:

                remarks = "Leave"

            # -------------------------------------------------
            # Student's own session
            # -------------------------------------------------

            student_session = student.session

            if not student_session:
                continue

            # -------------------------------------------------
            # Student's own section
            # -------------------------------------------------

            student_section = student.section

            if not student_section:
                continue

            # -------------------------------------------------
            # Create / Update attendance
            # -------------------------------------------------

            Attendance.objects.update_or_create(
                student=student,
                session=student_session,
                date=selected_date,
                defaults={
                    "classroom": classroom,
                    "section": student_section,
                    "status": status,
                    "remarks": remarks,
                },
            )

            saved_count += 1

        messages.success(
            request,
            f"Attendance saved successfully for "
            f"{saved_count} students.",
        )

        return redirect(
            f"/attendance/class/{classroom.id}/"
            f"?date={selected_date.strftime('%Y-%m-%d')}"
            f"&session={session_id}"
        )

    # -----------------------------------------------------
    # EXISTING ATTENDANCE
    # -----------------------------------------------------

    existing_attendance = {}

    records = Attendance.objects.filter(
        classroom=classroom,
        date=selected_date,
    )

    if selected_session:
        records = records.filter(
            session=selected_session
        )

    existing_attendance = {
        record.student_id: record
        for record in records
    }

    # -----------------------------------------------------
    # AVAILABLE SESSIONS
    # -----------------------------------------------------

    sessions = Session.objects.all().order_by(
        "-id"
    )

    return render(
        request,
        "attendance/class_attendance.html",
        {
            "classroom": classroom,
            "students": students,
            "existing_attendance": existing_attendance,
            "selected_date": selected_date,
            "selected_session": selected_session,
            "sessions": sessions,
            "today": today,
        },
    )


# =========================================================
# ADD SINGLE ATTENDANCE
# =========================================================

def add_attendance(request):

    if request.method == "POST":

        form = AttendanceForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Attendance saved successfully.",
            )

            return redirect(
                "attendance:attendance_list"
            )

    else:

        form = AttendanceForm(
            initial={
                "date": timezone.localdate(),
            }
        )

    return render(
        request,
        "attendance/add_attendance.html",
        {
            "form": form,
            "edit_mode": False,
        },
    )


# =========================================================
# ATTENDANCE LIST
# =========================================================

def attendance_list(request):

    query = request.GET.get(
        "q",
        "",
    ).strip()

    date = request.GET.get(
        "date",
        "",
    ).strip()

    classroom_id = request.GET.get(
        "classroom",
        "",
    ).strip()

    section_id = request.GET.get(
        "section",
        "",
    ).strip()

    status = request.GET.get(
        "status",
        "",
    ).strip()

    attendances = Attendance.objects.select_related(
        "student",
        "session",
        "classroom",
        "section",
    )

    if query:

        attendances = attendances.filter(
            Q(
                student__first_name__icontains=query
            )
            |
            Q(
                student__last_name__icontains=query
            )
            |
            Q(
                student__admission_no__icontains=query
            )
        )

    if date:
        attendances = attendances.filter(
            date=date
        )

    if classroom_id:
        attendances = attendances.filter(
            classroom_id=classroom_id
        )

    if section_id:
        attendances = attendances.filter(
            section_id=section_id
        )

    if status:
        attendances = attendances.filter(
            status=status
        )

    attendances = attendances.order_by(
        "-date",
        "student__first_name",
    )

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

    sections = Section.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "attendance/attendance_list.html",
        {
            "attendances": attendances,
            "query": query,
            "date": date,
            "classroom_id": classroom_id,
            "section_id": section_id,
            "status": status,
            "classrooms": classrooms,
            "sections": sections,
        },
    )


# =========================================================
# DETAIL
# =========================================================

def attendance_detail(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk,
    )

    return render(
        request,
        "attendance/attendance_detail.html",
        {
            "attendance": attendance,
        },
    )


# =========================================================
# EDIT
# =========================================================

def edit_attendance(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk,
    )

    if request.method == "POST":

        form = AttendanceForm(
            request.POST,
            instance=attendance,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Attendance updated successfully.",
            )

            return redirect(
                "attendance:attendance_detail",
                pk=attendance.pk,
            )

    else:

        form = AttendanceForm(
            instance=attendance,
        )

    return render(
        request,
        "attendance/add_attendance.html",
        {
            "form": form,
            "edit_mode": True,
            "attendance": attendance,
        },
    )


# =========================================================
# DELETE
# =========================================================

def delete_attendance(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk,
    )

    if request.method == "POST":

        attendance.delete()

        messages.success(
            request,
            "Attendance deleted successfully.",
        )

        return redirect(
            "attendance:attendance_list"
        )

    return render(
        request,
        "attendance/delete_attendance.html",
        {
            "attendance": attendance,
        },
    )


# =========================================================
# DAILY REPORT
# =========================================================

def attendance_report(request):

    date = request.GET.get(
        "date",
        "",
    )

    classroom_id = request.GET.get(
        "classroom",
        "",
    )

    section_id = request.GET.get(
        "section",
        "",
    )

    attendances = Attendance.objects.select_related(
        "student",
        "classroom",
        "section",
    )

    if date:
        attendances = attendances.filter(
            date=date
        )

    if classroom_id:
        attendances = attendances.filter(
            classroom_id=classroom_id
        )

    if section_id:
        attendances = attendances.filter(
            section_id=section_id
        )

    summary = attendances.aggregate(
        total=Count("id"),
        present=Count(
            "id",
            filter=Q(status="Present"),
        ),
        absent=Count(
            "id",
            filter=Q(status="Absent"),
        ),
        leave=Count(
            "id",
            filter=Q(status="Leave"),
        ),
    )

    total = summary["total"] or 0
    present = summary["present"] or 0
    absent = summary["absent"] or 0
    leave = summary["leave"] or 0

    percentage = (
        round(
            (present / total) * 100,
            2,
        )
        if total
        else 0
    )

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

    sections = Section.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "attendance/attendance_report.html",
        {
            "attendances": attendances.order_by(
                "-date",
                "student__first_name",
            ),
            "classrooms": classrooms,
            "sections": sections,
            "date": date,
            "classroom_id": classroom_id,
            "section_id": section_id,
            "total": total,
            "present": present,
            "absent": absent,
            "leave": leave,
            "percentage": percentage,
        },
    )


# =========================================================
# STUDENT-WISE REPORT
# =========================================================

def student_attendance_report(request):

    classroom_id = request.GET.get(
        "classroom",
        "",
    )

    section_id = request.GET.get(
        "section",
        "",
    )

    attendances = Attendance.objects.select_related(
        "student",
        "classroom",
        "section",
    )

    if classroom_id:

        attendances = attendances.filter(
            classroom_id=classroom_id
        )

    if section_id:

        attendances = attendances.filter(
            section_id=section_id
        )

    student_summary = attendances.values(
        "student",
        "student__admission_no",
        "student__first_name",
        "student__last_name",
        "classroom",
        "section",
    ).annotate(
        total=Count("id"),
        present=Count(
            "id",
            filter=Q(status="Present"),
        ),
        absent=Count(
            "id",
            filter=Q(status="Absent"),
        ),
        leave=Count(
            "id",
            filter=Q(status="Leave"),
        ),
    ).order_by(
        "student__first_name"
    )

    report_data = []

    for student in student_summary:

        total = student["total"]
        present = student["present"]

        percentage = (
            round(
                (present / total) * 100,
                2,
            )
            if total
            else 0
        )

        report_data.append({
            "admission_no":
                student["student__admission_no"],

            "name":
                f'{student["student__first_name"]} '
                f'{student["student__last_name"]}'.strip(),

            "classroom":
                student["classroom"],

            "section":
                student["section"],

            "total":
                total,

            "present":
                present,

            "absent":
                student["absent"],

            "leave":
                student["leave"],

            "percentage":
                percentage,
        })

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

    sections = Section.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "attendance/student_attendance_report.html",
        {
            "report_data": report_data,
            "classrooms": classrooms,
            "sections": sections,
            "classroom_id": classroom_id,
            "section_id": section_id,
        },
    )


# =========================================================
# MONTHLY REPORT
# =========================================================

def monthly_attendance_report(request):

    month = request.GET.get(
        "month",
        "",
    )

    classroom_id = request.GET.get(
        "classroom",
        "",
    )

    section_id = request.GET.get(
        "section",
        "",
    )

    attendances = Attendance.objects.select_related(
        "student",
        "classroom",
        "section",
    )

    if month:

        attendances = attendances.filter(
            date__month=month
        )

    if classroom_id:

        attendances = attendances.filter(
            classroom_id=classroom_id
        )

    if section_id:

        attendances = attendances.filter(
            section_id=section_id
        )

    student_summary = attendances.values(
        "student",
        "student__admission_no",
        "student__first_name",
        "student__last_name",
        "classroom",
        "section",
    ).annotate(
        total=Count("id"),
        present=Count(
            "id",
            filter=Q(status="Present"),
        ),
        absent=Count(
            "id",
            filter=Q(status="Absent"),
        ),
        leave=Count(
            "id",
            filter=Q(status="Leave"),
        ),
    ).order_by(
        "student__first_name"
    )

    report_data = []

    for student in student_summary:

        total = student["total"]
        present = student["present"]

        percentage = (
            round(
                (present / total) * 100,
                2,
            )
            if total
            else 0
        )

        report_data.append({
            "admission_no":
                student["student__admission_no"],

            "name":
                f'{student["student__first_name"]} '
                f'{student["student__last_name"]}'.strip(),

            "classroom":
                student["classroom"],

            "section":
                student["section"],

            "total":
                total,

            "present":
                present,

            "absent":
                student["absent"],

            "leave":
                student["leave"],

            "percentage":
                percentage,
        })

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

    sections = Section.objects.all().order_by(
        "name"
    )

    return render(
        request,
        "attendance/monthly_attendance_report.html",
        {
            "report_data": report_data,
            "classrooms": classrooms,
            "sections": sections,
            "month": month,
            "classroom_id": classroom_id,
            "section_id": section_id,
        },
    )