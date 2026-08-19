from django import forms

from .models import DiaryEntry
from academics.models import ClassRoom, Section


class DiaryEntryForm(forms.ModelForm):

    class Meta:

        model = DiaryEntry

        fields = [
            "classroom",
            "section",
            "subject",
            "topic",
            "description",
            "homework",
            "remarks",
            "date",
        ]

        widgets = {

            "classroom": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "section": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Subject",
                }
            ),

            "topic": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Lesson / Topic taught",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe what was taught...",
                }
            ),

            "homework": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Homework assigned...",
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 2,
                    "placeholder": "Additional remarks...",
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }