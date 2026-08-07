from django.db import models
from students.models import Student
from academics.models import ClassRoom


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

    exam_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.classroom} - Rs. {self.monthly_fee}"


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

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    month = models.CharField(
        max_length=20,
        choices=MONTH_CHOICES
    )

    year = models.PositiveIntegerField()

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
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

    def __str__(self):
        return f"{self.student} - {self.month} {self.year}"