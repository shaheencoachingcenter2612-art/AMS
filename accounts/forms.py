from django import forms
from django.contrib.auth.models import User

from .models import UserProfile
from teachers.models import Teacher


# =========================================================
# CREATE USER FORM
# =========================================================

class UserCreateForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        )
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
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
                    "autocomplete": "username",
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
                    "autocomplete": "email",
                }
            ),
        }

    def clean_username(self):

        username = self.cleaned_data.get(
            "username"
        )

        if username:

            username = username.strip()

        if User.objects.filter(
            username__iexact=username
        ).exists():

            raise forms.ValidationError(
                "A user with this username already exists."
            )

        return username

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        password2 = cleaned_data.get(
            "password2"
        )

        role = cleaned_data.get(
            "role"
        )

        teacher = cleaned_data.get(
            "teacher"
        )

        if password and password2:

            if password != password2:

                self.add_error(
                    "password2",
                    "Passwords do not match."
                )

        if role == "Teacher" and not teacher:

            self.add_error(
                "teacher",
                "Please select a teacher for this Teacher account."
            )

        if role != "Teacher" and teacher:

            self.add_error(
                "teacher",
                "Teacher profile can only be linked to a Teacher account."
            )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(
            commit=False
        )

        user.set_password(
            self.cleaned_data["password"]
        )

        user.is_active = True

        if commit:

            user.save()

            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    "role": self.cleaned_data["role"]
                }
            )

            teacher = self.cleaned_data.get(
                "teacher"
            )

            if (
                self.cleaned_data["role"] == "Teacher"
                and teacher
            ):

                teacher.user = user

                teacher.save(
                    update_fields=["user"]
                )

        return user


# =========================================================
# USER PASSWORD RESET FORM
# =========================================================

class UserPasswordResetForm(forms.Form):

    password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter new password",
                "autocomplete": "new-password",
            }
        )
    )

    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm new password",
                "autocomplete": "new-password",
            }
        )
    )

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get(
            "password"
        )

        password2 = cleaned_data.get(
            "password2"
        )

        if password and password2:

            if password != password2:

                self.add_error(
                    "password2",
                    "Passwords do not match."
                )

        return cleaned_data