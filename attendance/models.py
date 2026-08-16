from django.db import models

from students.models import Student
from academics.models import Session, ClassRoom, Section


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Leave", "Leave"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )

    session = models.ForeignKey(
        Session,
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        related_name="attendance_records",
    )

    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Present",
    )

    remarks = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-date",
            "student__first_name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "date",
                    "session",
                ],
                name="unique_student_attendance_per_day",
            )
        ]

    def __str__(self):
        return (
            f"{self.student} - "
            f"{self.date} - "
            f"{self.status}"
        )