from django import forms

from .models import (
    Session,
    ClassRoom,
    Section,
    Subject,
)


# =========================================================
# SESSION FORM
# =========================================================

class SessionForm(forms.ModelForm):

    class Meta:

        model = Session

        fields = [
            "name",
            "start_year",
            "end_year",
            "is_active",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Session 2026-27",
                }
            ),

            "start_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Start Year",
                }
            ),

            "end_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "End Year",
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


# =========================================================
# CLASSROOM FORM
# =========================================================

class ClassRoomForm(forms.ModelForm):

    class Meta:

        model = ClassRoom

        fields = [
            "name",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 9th, 10th, FSC",
                }
            ),
        }


# =========================================================
# SECTION FORM
# =========================================================

class SectionForm(forms.ModelForm):

    class Meta:

        model = Section

        fields = [
            "name",
            "classroom",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. A, B, C",
                }
            ),

            "classroom": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


# =========================================================
# SUBJECT FORM
# =========================================================

class SubjectForm(forms.ModelForm):

    class Meta:

        model = Subject

        fields = [
            "name",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. English, Physics, Mathematics",
                }
            ),
        }