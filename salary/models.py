from django.db import models
from teachers.models import Teacher


# =========================================================
# SALARY / PAYROLL
# =========================================================

class Salary(models.Model):

    MONTH_CHOICES = [
        ("January", "January"),
        ("February", "February"),
        ("March", "March"),
        ("April", "April"),
        ("May", "May"),
        ("June", "June"),
        ("July", "July"),
        ("August", "August"),
        ("September", "September"),
        ("October", "October"),
        ("November", "November"),
        ("December", "December"),
    ]

    PAYMENT_METHODS = [
        ("Cash", "Cash"),
        ("Bank", "Bank"),
        ("JazzCash", "JazzCash"),
        ("EasyPaisa", "EasyPaisa"),
    ]

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="salary_entries"
    )

    month = models.CharField(
        max_length=20,
        choices=MONTH_CHOICES
    )

    year = models.PositiveIntegerField()

    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    allowance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    advance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    deduction = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    paid = models.BooleanField(
        default=False
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="Cash"
    )

    payment_date = models.DateField(
        null=True,
        blank=True
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # AUTOMATIC NET SALARY
    # =====================================================

    def save(self, *args, **kwargs):

        self.net_salary = (
            self.basic_salary
            + self.allowance
            - self.advance
            - self.deduction
        )

        if self.net_salary < 0:
            self.net_salary = 0

        super().save(*args, **kwargs)

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return (
            f"{self.teacher} - "
            f"{self.month} {self.year}"
        )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        ordering = [
            "-year",
            "-id",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "teacher",
                    "month",
                    "year",
                ],
                name="unique_salary_teacher_month_year"
            )
        ]