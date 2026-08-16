from django import forms
from django.contrib.auth.models import User

from .models import UserProfile
from teachers.models import Teacher


class UserCreateForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        )
    )

    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.filter(
            status="Active",
            user__isnull=True,
        ).order_by(
            "first_name",
            "last_name",
        ),
        required=False,
        empty_label="Select Teacher",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        )
    )

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

        widgets = {

            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Username",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "First Name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Last Name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email Address",
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        role = cleaned_data.get("role")
        teacher = cleaned_data.get("teacher")

        if role == "Teacher" and not teacher:

            self.add_error(
                "teacher",
                "Please select a teacher for this Teacher account."
            )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password"]
        )

        if commit:

            user.save()

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    "role": self.cleaned_data["role"]
                }
            )

            teacher = self.cleaned_data.get("teacher")

            if (
                self.cleaned_data["role"] == "Teacher"
                and teacher
            ):

                teacher.user = user
                teacher.save(
                    update_fields=["user"]
                )

        return user