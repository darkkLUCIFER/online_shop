from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from apps.accounts.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
        fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", "phone_number", "full_name"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href='../password/'>this form</a>.")

    class Meta:
        model = User
        fields = ["email", "phone_number", "full_name", "password", "last_login"]


class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput, label="Email")
    full_name = forms.CharField(label="Full Name", widget=forms.TextInput)
    phone = forms.CharField(label="Phone Number", widget=forms.TextInput, max_length=11)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")

        return confirm_password

    def clean_email(self):
        email = self.cleaned_data['email']

        email_existence = User.objects.filter(email=email)
        if email_existence.exists():
            raise ValidationError("Email already registered")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']

        phone_existence = User.objects.filter(phone_number=phone)
        if phone_existence.exists():
            raise ValidationError("Phone number already registered")
        return phone


class VerifyOtpCodeForm(forms.Form):
    code = forms.IntegerField()
