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
                    "placeholder": "Monthly Fee",
                    "min": "0",
                    "step": "0.01"
                }
            ),

            "admission_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Admission Fee",
                    "min": "0",
                    "step": "0.01"
                }
            ),

            "registration_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Registration Fee",
                    "min": "0",
                    "step": "0.01"
                }
            ),

            "exam_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Exam Fee",
                    "min": "0",
                    "step": "0.01"
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
            "amount_paid",
            "payment_method",
            "payment_date",
            "discount",
            "fine",
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

            "amount_paid": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Amount Paid",
                    "min": "0",
                    "step": "0.01"
                }
            ),

            "discount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Discount",
                    "min": "0",
                    "step": "0.01"
                }
            ),

            "fine": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Fine",
                    "min": "0",
                    "step": "0.01"
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

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["student"].queryset = (
            self.fields["student"]
            .queryset
            .select_related(
                "classroom",
                "section"
            )
            .filter(
                is_active=True
            )
            .order_by(
                "first_name"
            )
        )