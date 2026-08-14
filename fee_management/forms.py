from django import forms
from .models import Fee, FeeStructure


class FeeStructureForm(forms.ModelForm):

    class Meta:
        model = FeeStructure

        fields = [
            "classroom",
            "monthly_fee",
            "admission_fee",
            "registration_fee",
            "exam_fee",
        ]

        widgets = {
            "classroom": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "monthly_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Monthly Fee"
                }
            ),

            "admission_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Admission Fee"
                }
            ),

            "registration_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Registration Fee"
                }
            ),

            "exam_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Exam Fee"
                }
            ),
        }


class FeeForm(forms.ModelForm):

    payment_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
            }
        ),
        required=False,
    )

    class Meta:
        model = Fee

        fields = [
            "student",
            "month",
            "year",
            "monthly_fee",
            "admission_fee",
            "exam_fee",
            "discount",
            "fine",
            "total_amount",
            "amount_paid",
            "payment_method",
            "payment_date",
            "remarks",
        ]

        widgets = {

            "student": forms.Select(
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
                    "placeholder": "Year"
                }
            ),

            "monthly_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Monthly Fee"
                }
            ),

            "admission_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Admission Fee"
                }
            ),

            "exam_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Exam Fee"
                }
            ),

            "discount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Discount"
                }
            ),

            "fine": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Fine"
                }
            ),

            "total_amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Total Amount"
                }
            ),

            "amount_paid": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Amount Paid"
                }
            ),

            "payment_method": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Remarks"
                }
            ),
        }