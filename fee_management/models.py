from django.db import models
from students.models import Student
from academics.models import ClassRoom
from datetime import datetime


class FeeStructure(models.Model):

    classroom = models.OneToOneField(
        ClassRoom,
        on_delete=models.CASCADE
    )

    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    admission_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    exam_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):

        return (
            f"{self.classroom} - "
            f"Rs. {self.monthly_fee}"
        )


class Fee(models.Model):

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

    receipt_no = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="fees"
    )

    month = models.CharField(
        max_length=20,
        choices=MONTH_CHOICES
    )

    year = models.PositiveIntegerField()

    # Automatically taken from FeeStructure
    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Previous unpaid balance
    previous_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    admission_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    exam_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    fine = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    remaining_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="Cash"
    )

    paid = models.BooleanField(
        default=False
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

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "month",
                    "year"
                ],
                name="unique_student_month_year_fee"
            )
        ]

        ordering = ["-id"]

    def save(self, *args, **kwargs):

        if not self.receipt_no:

            current_year = datetime.now().year

            last_fee = (
                Fee.objects
                .filter(
                    receipt_no__startswith=f"RCP-{current_year}-"
                )
                .order_by("-id")
                .first()
            )

            if last_fee and last_fee.receipt_no:

                try:

                    last_number = int(
                        last_fee.receipt_no.split("-")[-1]
                    )

                except ValueError:

                    last_number = 0

            else:

                last_number = 0

            self.receipt_no = (
                f"RCP-{current_year}-{last_number + 1:05d}"
            )

        self.remaining_amount = (
            self.total_amount - self.amount_paid
        )

        if self.remaining_amount < 0:
            self.remaining_amount = 0

        self.paid = (
            self.remaining_amount <= 0
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.receipt_no} - "
            f"{self.student}"
        )