from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student

        fields = [
            "admission_no",
            "first_name",
            "last_name",
            "father_name",
            "gender",
            "date_of_birth",
            "phone",
            "address",
            "session",
            "classroom",
            "section",
            "photo",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),
        }