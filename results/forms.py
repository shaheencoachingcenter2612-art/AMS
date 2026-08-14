from django import forms

from .models import Result


class ResultForm(forms.ModelForm):

    class Meta:

        model = Result

        fields = [
            "student",
            "session",
            "classroom",
            "section",
            "subject",
            "exam_type",
            "exam_date",
            "total_marks",
            "obtained_marks",
            "remarks",
        ]

        widgets = {

            "student": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "session": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "classroom": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "section": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "subject": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "exam_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "exam_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "total_marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Total Marks"
                }
            ),

            "obtained_marks": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Obtained Marks"
                }
            ),

            "remarks": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional remarks"
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        total_marks = cleaned_data.get("total_marks")
        obtained_marks = cleaned_data.get("obtained_marks")

        if (
            total_marks is not None
            and obtained_marks is not None
            and obtained_marks > total_marks
        ):
            self.add_error(
                "obtained_marks",
                "Obtained marks cannot be greater than total marks."
            )

        return cleaned_data