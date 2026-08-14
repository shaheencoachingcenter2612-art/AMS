from django import forms

from .models import Salary


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
                    "class": "form-select"
                }
            ),

            "month": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "2026"
                }
            ),

            "basic_salary": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Basic Salary"
                }
            ),

            "allowance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Allowance"
                }
            ),

            "advance": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Advance"
                }
            ),

            "deduction": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Deduction"
                }
            ),

            "paid": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "payment_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Optional remarks"
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        basic = cleaned_data.get("basic_salary") or 0
        allowance = cleaned_data.get("allowance") or 0
        advance = cleaned_data.get("advance") or 0
        deduction = cleaned_data.get("deduction") or 0

        paid = cleaned_data.get("paid")
        payment_date = cleaned_data.get("payment_date")

        net_salary = (
            basic
            + allowance
            - advance
            - deduction
        )

        if net_salary < 0:

            raise forms.ValidationError(
                "Salary deductions cannot exceed the total salary."
            )

        if paid and not payment_date:

            self.add_error(
                "payment_date",
                "Payment date is required when salary is marked as Paid."
            )

        return cleaned_data