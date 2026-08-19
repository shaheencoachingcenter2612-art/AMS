from django.db import models
from academics.models import Session, ClassRoom, Section
from datetime import datetime


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

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    father_name = models.CharField(
        max_length=150
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField()

    phone = models.CharField(
        max_length=20
    )

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

    photo = models.ImageField(
        upload_to="students/",
        blank=True,
        null=True
    )

    # Final monthly fee decided at admission
    monthly_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Active student means monthly fee is expected
    is_active = models.BooleanField(
        default=True
    )

    admission_date = models.DateField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.admission_no:

            year = datetime.now().year

            last_student = (
                Student.objects
                .filter(
                    admission_no__startswith=f"SCC-{year}-"
                )
                .order_by("-id")
                .first()
            )

            if last_student and last_student.admission_no:

                try:
                    last_number = int(
                        last_student.admission_no.split("-")[-1]
                    )

                except ValueError:
                    last_number = 0

            else:
                last_number = 0

            self.admission_no = (
                f"SCC-{year}-{last_number + 1:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.admission_no} - "
            f"{self.first_name} "
            f"{self.last_name}"
        )