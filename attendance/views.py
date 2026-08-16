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
from academics.models import ClassRoom, Section


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
# BULK DAILY ATTENDANCE
# =========================================================

def mark_attendance(request):

    filter_form = BulkAttendanceFilterForm(
        request.GET or None
    )

    students = Student.objects.none()

    selected_session = None
    selected_classroom = None
    selected_section = None
    selected_date = timezone.localdate()

    if filter_form.is_valid():

        selected_session = filter_form.cleaned_data["session"]
        selected_classroom = filter_form.cleaned_data["classroom"]
        selected_section = filter_form.cleaned_data["section"]
        selected_date = filter_form.cleaned_data["date"]

        students = Student.objects.filter(
            session=selected_session,
            classroom=selected_classroom,
            section=selected_section,
        ).order_by(
            "first_name",
            "last_name",
        )

    if request.method == "POST":

        session_id = request.POST.get("session")
        classroom_id = request.POST.get("classroom")
        section_id = request.POST.get("section")
        date = request.POST.get("date")

        if not all([
            session_id,
            classroom_id,
            section_id,
            date,
        ]):
            messages.error(
                request,
                "Please select session, class, section and date.",
            )

            return redirect(
                "attendance:mark_attendance"
            )

        students = Student.objects.filter(
            session_id=session_id,
            classroom_id=classroom_id,
            section_id=section_id,
        ).order_by(
            "first_name",
            "last_name",
        )

        saved_count = 0

        for student in students:

            status = request.POST.get(
                f"status_{student.id}",
                "Present",
            )

            remarks = request.POST.get(
                f"remarks_{student.id}",
                "",
            )

            Attendance.objects.update_or_create(
                student=student,
                session_id=session_id,
                date=date,
                defaults={
                    "classroom_id": classroom_id,
                    "section_id": section_id,
                    "status": status,
                    "remarks": remarks,
                },
            )

            saved_count += 1

        messages.success(
            request,
            f"Attendance saved successfully for {saved_count} students.",
        )

        return redirect(
            f"/attendance/mark/?session={session_id}"
            f"&classroom={classroom_id}"
            f"&section={section_id}"
            f"&date={date}"
        )

    existing_attendance = {}

    if (
        selected_session
        and selected_classroom
        and selected_section
        and selected_date
    ):

        records = Attendance.objects.filter(
            session=selected_session,
            classroom=selected_classroom,
            section=selected_section,
            date=selected_date,
        )

        existing_attendance = {
            record.student_id: record
            for record in records
        }

    return render(
        request,
        "attendance/mark_attendance.html",
        {
            "filter_form": filter_form,
            "students": students,
            "existing_attendance": existing_attendance,
            "selected_session": selected_session,
            "selected_classroom": selected_classroom,
            "selected_section": selected_section,
            "selected_date": selected_date,
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