from django.db import models

from teachers.models import Teacher
from academics.models import ClassRoom, Section


class DiaryEntry(models.Model):

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="diary_entries"
    )

    date = models.DateField()

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name="diary_entries"
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="diary_entries"
    )

    subject = models.CharField(
        max_length=100
    )

    topic = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    homework = models.TextField(
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
            "-date",
            "teacher__first_name",
        ]

    def __str__(self):
        return (
            f"{self.teacher} - "
            f"{self.subject} - "
            f"{self.date}"
        )