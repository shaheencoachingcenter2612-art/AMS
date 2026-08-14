from django import forms

from .models import TimetableEntry


class TimetableEntryForm(forms.ModelForm):

    class Meta:
        model = TimetableEntry

        fields = [
            "session",
            "classroom",
            "section",
            "subject",
            "teacher",
            "day",
            "start_time",
            "end_time",
            "room",
            "remarks",
        ]

        widgets = {

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

            "teacher": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "day": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "start_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "end_time": forms.TimeInput(
                attrs={
                    "type": "time",
                    "class": "form-control"
                }
            ),

            "room": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Room / Hall"
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

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and end_time <= start_time:

            self.add_error(
                "end_time",
                "End time must be later than start time."
            )

        return cleaned_data