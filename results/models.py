from django.db import models

from students.models import Student
from academics.models import Session, ClassRoom, Section, Subject


# =========================================================
# RESULT
# =========================================================

class Result(models.Model):

    EXAM_TYPE_CHOICES = [
        ("FAT", "FAT - First Assessment Test"),
        ("SAT", "SAT - Second Assessment Test"),
        ("Test Session", "Test Session"),
        ("Class Test", "Class Test"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="results"
    )

    session = models.ForeignKey(
        Session,
        on_delete=models.PROTECT
    )

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.PROTECT
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT
    )

    exam_type = models.CharField(
        max_length=30,
        choices=EXAM_TYPE_CHOICES
    )

    exam_date = models.DateField()

    total_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    obtained_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    remarks = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def percentage(self):

        if self.total_marks > 0:
            return round(
                (self.obtained_marks / self.total_marks) * 100,
                2
            )

        return 0

    @property
    def grade(self):

        percentage = self.percentage

        if percentage >= 80:
            return "A+"

        elif percentage >= 70:
            return "A"

        elif percentage >= 60:
            return "B"

        elif percentage >= 50:
            return "C"

        elif percentage >= 40:
            return "D"

        else:
            return "F"

    class Meta:

        ordering = [
            "-exam_date",
            "student__first_name",
            "subject__name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "subject",
                    "session",
                    "exam_type",
                    "exam_date",
                ],
                name="unique_student_subject_result",
            )
        ]

    def __str__(self):

        return (
            f"{self.student} - "
            f"{self.subject} - "
            f"{self.exam_type}"
        )