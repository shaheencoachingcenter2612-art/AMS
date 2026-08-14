from django.db import models

from academics.models import Session, ClassRoom, Section, Subject
from teachers.models import Teacher


class TimetableEntry(models.Model):

    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="timetable_entries"
    )

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name="timetable_entries"
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="timetable_entries"
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="timetable_entries"
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="timetable_entries"
    )

    day = models.CharField(
        max_length=20,
        choices=DAY_CHOICES
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    room = models.CharField(
        max_length=50,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "day",
            "start_time",
        ]

    def __str__(self):
        return (
            f"{self.classroom} - "
            f"{self.subject} - "
            f"{self.teacher} - "
            f"{self.day}"
        )