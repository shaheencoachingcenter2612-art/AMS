from django import forms

from .models import Teacher
from salary.models import Salary


# =========================================================
# TEACHER FORM
# =========================================================

class TeacherForm(forms.ModelForm):

    class Meta:

        model = Teacher

        fields = [
            "employee_id",
            "first_name",
            "last_name",
            "father_name",
            "photo",
            "gender",
            "date_of_birth",
            "phone",
            "email",
            "cnic",
            "qualification",
            "subject",
            "salary",
            "joining_date",
            "address",
            "status",
        ]

        widgets = {

            "employee_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Employee ID",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First Name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name",
                }
            ),

            "father_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Father Name",
                }
            ),

            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "joining_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone Number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),

            "cnic": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "CNIC",
                }
            ),

            "qualification": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Qualification",
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Subject",
                }
            ),

            "salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Monthly Salary",
                    "step": "0.01",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Complete Address",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


# =========================================================
# SALARY FORM
# =========================================================

class SalaryForm(forms.ModelForm):

    class Meta:

        model = Salary

        fields = [
            "teacher",
            "month",
            "year",
            "basic_salary",
            "allowance",
            "advance",
            "deduction",
            "paid",
            "payment_method",
            "payment_date",
            "remarks",
        ]

        widgets = {

            "teacher": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "month": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "2026",
                    "min": "2020",
                    "max": "2100",
                }
            ),

            "basic_salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Basic Salary",
                }
            ),

            "allowance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Allowance",
                }
            ),

            "advance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Advance",
                }
            ),

            "deduction": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Deduction",
                }
            ),

            "paid": forms.Select(
                choices=[
                    (False, "Pending"),
                    (True, "Paid"),
                ],
                attrs={
                    "class": "form-select",
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "payment_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional remarks",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["teacher"].queryset = (
            Teacher.objects
            .filter(status="Active")
            .order_by(
                "first_name",
                "last_name"
            )
        )

        self.fields["year"].initial = 2026