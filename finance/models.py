from django.db import models


class Expense(models.Model):

    CATEGORY_CHOICES = [

        ("Salary", "Salary"),

        ("Rent", "Rent"),

        ("Electricity", "Electricity"),

        ("Internet", "Internet"),

        ("Stationery", "Stationery"),

        ("Maintenance", "Maintenance"),

        ("Marketing", "Marketing"),

        ("Other", "Other"),
    ]

    title = models.CharField(
        max_length=200
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    expense_date = models.DateField()

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-expense_date", "-id"]

    def __str__(self):

        return (
            f"{self.title} - "
            f"Rs. {self.amount}"
        )