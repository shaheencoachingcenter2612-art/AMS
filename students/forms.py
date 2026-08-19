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
            "monthly_fee",
            "photo",
            "is_active",
        ]

        widgets = {

            "admission_no": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Auto generated"
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First name"
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last name"
                }
            ),

            "father_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Father's name"
                }
            ),

            "gender": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone number"
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Complete address"
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

            "monthly_fee": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter final monthly fee",
                    "min": "0",
                    "step": "0.01"
                }
            ),

            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input"
                }
            ),
        }

        labels = {
            "admission_no": "Admission No.",
            "first_name": "First Name",
            "last_name": "Last Name",
            "father_name": "Father's Name",
            "gender": "Gender",
            "date_of_birth": "Date of Birth",
            "phone": "Phone",
            "address": "Address",
            "session": "Session",
            "classroom": "Class",
            "section": "Section",
            "monthly_fee": "Final Monthly Fee",
            "photo": "Student Photo",
            "is_active": "Active Student",
        }

        help_texts = {
            "monthly_fee": (
                "Enter the final monthly fee agreed with the student "
                "after discount or concession."
            ),
            "is_active": (
                "Active students are included in monthly fee calculations."
            ),
        }