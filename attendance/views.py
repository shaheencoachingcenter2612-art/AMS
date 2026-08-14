from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.utils import timezone

from .models import Attendance
from .forms import AttendanceForm

from academics.models import ClassRoom, Section


# =========================================================
# ADD ATTENDANCE
# =========================================================

def add_attendance(request):

    if request.method == "POST":

        form = AttendanceForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                "attendance:attendance_list"
            )

    else:

        form = AttendanceForm()

    return render(
        request,
        "attendance/add_attendance.html",
        {
            "form": form
        }
    )


# =========================================================
# ATTENDANCE LIST
# =========================================================

def attendance_list(request):

    query = request.GET.get("q", "")
    date = request.GET.get("date", "")
    classroom_id = request.GET.get("classroom", "")
    section_id = request.GET.get("section", "")
    status = request.GET.get("status", "")

    attendances = Attendance.objects.select_related(
        "student",
        "session",
        "classroom",
        "section"
    )

    if query:

        attendances = attendances.filter(
            Q(student__first_name__icontains=query) |
            Q(student__last_name__icontains=query) |
            Q(student__admission_no__icontains=query)
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
        "student__first_name"
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
        }
    )


# =========================================================
# ATTENDANCE DETAIL
# =========================================================

def attendance_detail(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk
    )

    return render(
        request,
        "attendance/attendance_detail.html",
        {
            "attendance": attendance
        }
    )


# =========================================================
# EDIT ATTENDANCE
# =========================================================

def edit_attendance(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk
    )

    if request.method == "POST":

        form = AttendanceForm(
            request.POST,
            instance=attendance
        )

        if form.is_valid():

            form.save()

            return redirect(
                "attendance:attendance_detail",
                pk=attendance.pk
            )

    else:

        form = AttendanceForm(
            instance=attendance
        )

    return render(
        request,
        "attendance/add_attendance.html",
        {
            "form": form,
            "edit_mode": True,
            "attendance": attendance,
        }
    )


# =========================================================
# DELETE ATTENDANCE
# =========================================================

def delete_attendance(request, pk):

    attendance = get_object_or_404(
        Attendance,
        pk=pk
    )

    if request.method == "POST":

        attendance.delete()

        return redirect(
            "attendance:attendance_list"
        )

    return render(
        request,
        "attendance/delete_attendance.html",
        {
            "attendance": attendance
        }
    )


# =========================================================
# ATTENDANCE REPORT
# =========================================================

def attendance_report(request):

    date = request.GET.get("date", "")
    classroom_id = request.GET.get("classroom", "")
    section_id = request.GET.get("section", "")

    attendances = Attendance.objects.select_related(
        "student",
        "classroom",
        "section"
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
            filter=Q(status="Present")
        ),

        absent=Count(
            "id",
            filter=Q(status="Absent")
        ),

        leave=Count(
            "id",
            filter=Q(status="Leave")
        ),
    )

    total = summary["total"] or 0
    present = summary["present"] or 0
    absent = summary["absent"] or 0
    leave = summary["leave"] or 0

    if total > 0:

        percentage = round(
            (present / total) * 100,
            2
        )

    else:

        percentage = 0

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
                "student__first_name"
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
        }
    )


# =========================================================
# STUDENT-WISE ATTENDANCE REPORT
# =========================================================

def student_attendance_report(request):

    classroom_id = request.GET.get(
        "classroom",
        ""
    )

    section_id = request.GET.get(
        "section",
        ""
    )

    attendances = Attendance.objects.select_related(
        "student",
        "classroom",
        "section"
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
        "section"

    ).annotate(

        total=Count("id"),

        present=Count(
            "id",
            filter=Q(status="Present")
        ),

        absent=Count(
            "id",
            filter=Q(status="Absent")
        ),

        leave=Count(
            "id",
            filter=Q(status="Leave")
        ),

    ).order_by(
        "student__first_name"
    )

    report_data = []

    for student in student_summary:

        total = student["total"]
        present = student["present"]

        if total > 0:

            percentage = round(
                (present / total) * 100,
                2
            )

        else:

            percentage = 0

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
        }
    )


# =========================================================
# MONTHLY ATTENDANCE REPORT
# =========================================================

def monthly_attendance_report(request):

    month = request.GET.get(
        "month",
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

    attendances = Attendance.objects.select_related(
        "student",
        "classroom",
        "section"
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
        "section"

    ).annotate(

        total=Count("id"),

        present=Count(
            "id",
            filter=Q(status="Present")
        ),

        absent=Count(
            "id",
            filter=Q(status="Absent")
        ),

        leave=Count(
            "id",
            filter=Q(status="Leave")
        ),

    ).order_by(
        "student__first_name"
    )

    report_data = []

    for student in student_summary:

        total = student["total"]
        present = student["present"]

        if total > 0:

            percentage = round(
                (present / total) * 100,
                2
            )

        else:

            percentage = 0

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
        }
    )


# =========================================================
# ATTENDANCE DASHBOARD
# =========================================================

def attendance_dashboard(request):

    today = timezone.localdate()

    # -----------------------------------------------------
    # OVERALL STATISTICS
    # -----------------------------------------------------

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

    if total > 0:

        percentage = round(
            (present / total) * 100,
            2
        )

    else:

        percentage = 0


    # -----------------------------------------------------
    # TODAY'S ATTENDANCE
    # -----------------------------------------------------

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

    if today_total > 0:

        today_percentage = round(
            (today_present / today_total) * 100,
            2
        )

    else:

        today_percentage = 0


    # -----------------------------------------------------
    # CLASS-WISE ATTENDANCE
    # -----------------------------------------------------

    class_summary = []

    classrooms = ClassRoom.objects.all().order_by(
        "name"
    )

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

        if class_total > 0:

            class_percentage = round(
                (class_present / class_total) * 100,
                2
            )

        else:

            class_percentage = 0

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
            "total": total,

            "present": present,

            "absent": absent,

            "leave": leave,

            "percentage": percentage,

            "today": today,

            "today_total": today_total,

            "today_present": today_present,

            "today_absent": today_absent,

            "today_leave": today_leave,

            "today_percentage": today_percentage,

            "class_summary": class_summary,
        }
    )