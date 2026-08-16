from django.db import models

from teachers.models import Teacher
from academics.models import ClassRoom, Section


# =========================================================
# TEACHER DIARY
# =========================================================

class DiaryEntry(models.Model):

    # =====================================================
    # TEACHER
    # =====================================================

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="diary_entries",
    )

    # =====================================================
    # CLASS INFORMATION
    # =====================================================

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        related_name="diary_entries",
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="diary_entries",
    )

    # =====================================================
    # LECTURE INFORMATION
    # =====================================================

    subject = models.CharField(
        max_length=100,
    )

    topic = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        verbose_name="What was taught",
    )

    homework = models.TextField(
        blank=True,
    )

    remarks = models.TextField(
        blank=True,
    )

    # =====================================================
    # DATE
    # =====================================================

    date = models.DateField()

    # =====================================================
    # TIMESTAMP
    # =====================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        ordering = [
            "-date",
            "-id",
        ]

        verbose_name = "Diary Entry"
        verbose_name_plural = "Diary Entries"

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return (
            f"{self.teacher.first_name} "
            f"{self.teacher.last_name} - "
            f"{self.subject} - "
            f"{self.date}"
        )