from django import forms

from .models import DiaryEntry


class DiaryEntryForm(forms.ModelForm):

    class Meta:

        model = DiaryEntry

        fields = [
            "teacher",
            "date",
            "classroom",
            "section",
            "subject",
            "topic",
            "description",
            "homework",
            "remarks",
        ]

        widgets = {

            "teacher": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
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

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Subject"
                }
            ),

            "topic": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Lesson / Topic taught"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe what was taught..."
                }
            ),

            "homework": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Homework assigned..."
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Additional remarks..."
                }
            ),
        }