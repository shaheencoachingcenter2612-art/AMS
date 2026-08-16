from django import forms

from .models import Attendance
from students.models import Student
from academics.models import Session, ClassRoom, Section


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance

        fields = [
            "student",
            "session",
            "classroom",
            "section",
            "date",
            "status",
            "remarks",
        ]

        widgets = {

            "student": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "session": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

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

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "remarks": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional remarks",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        student = cleaned_data.get("student")
        session = cleaned_data.get("session")
        date = cleaned_data.get("date")

        if student and session and date:

            existing = Attendance.objects.filter(
                student=student,
                session=session,
                date=date,
            )

            if self.instance.pk:
                existing = existing.exclude(
                    pk=self.instance.pk
                )

            if existing.exists():
                raise forms.ValidationError(
                    "Attendance for this student on this date already exists."
                )

        return cleaned_data


class BulkAttendanceFilterForm(forms.Form):

    session = forms.ModelChoiceField(
        queryset=Session.objects.all(),
        empty_label="Select Session",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    classroom = forms.ModelChoiceField(
        queryset=ClassRoom.objects.all(),
        empty_label="Select Class",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        empty_label="Select Section",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        )
    )