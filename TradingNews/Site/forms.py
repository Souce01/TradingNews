from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class SignUpForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-input"
            }
        )
    )
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-input"
            }
        )
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-input"
            }
    ))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        obj = User.objects.filter(username=username)
        if obj.count():
            raise ValidationError("Username is taken")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password do not match")
        
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data.get("username"),
            password=self.cleaned_data.get("password1")
        )
        return user
