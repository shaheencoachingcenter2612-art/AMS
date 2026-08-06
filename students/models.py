from django.db import models
from academics.models import Session, ClassRoom, Section


class Student(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    admission_no = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)

    father_name = models.CharField(max_length=150)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    phone = models.CharField(max_length=20)

    address = models.TextField()

    session = models.ForeignKey(
        Session,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    section = models.ForeignKey(
        Section,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    admission_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"