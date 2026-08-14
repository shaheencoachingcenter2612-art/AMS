from django.db import models
from datetime import datetime


# =========================================================
# TEACHER
# =========================================================

class Teacher(models.Model):

    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
    ]

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
    ]

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    father_name = models.CharField(
        max_length=150
    )

    photo = models.ImageField(
        upload_to="teachers/",
        blank=True,
        null=True,
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
    )

    date_of_birth = models.DateField()

    phone = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True,
        null=True,
    )

    cnic = models.CharField(
        max_length=15,
        unique=True,
    )

    qualification = models.CharField(
        max_length=150
    )

    subject = models.CharField(
        max_length=100
    )

    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    joining_date = models.DateField()

    address = models.TextField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active",
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.employee_id:

            year = datetime.now().year

            last_teacher = Teacher.objects.order_by(
                "-id"
            ).first()

            if last_teacher and last_teacher.employee_id:

                try:

                    last_number = int(
                        last_teacher.employee_id.split("-")[-1]
                    )

                except ValueError:

                    last_number = 0

            else:

                last_number = 0

            self.employee_id = (
                f"EMP-{year}-{last_number + 1:04d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.employee_id} - "
            f"{self.first_name} "
            f"{self.last_name}"
        )