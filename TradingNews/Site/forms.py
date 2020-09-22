from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


"""
SignUpForm and SignUpModelForm might be useless but keeping them in case

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


class SignUpModelForm(forms.ModelForm):
    password1 = forms.CharField(
        strip=False,
        label='',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-input',
                'placeholder': 'password'
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-input',
                'placeholder': 'Comfirm Password'
                }
            ),
        strip=False,
    )
    class Meta:
        model = User
        fields = [
            'username'
        ]
        labels = {
            'username': ''
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                'placeholder': 'Username',
                'class': 'form-input'
            })
        }

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
"""

class SignUpModelForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'password'

        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs['placeholder'] = 'Comfirm Password'

        self.fields['username'].label = ''
        self.fields['username'].help_text = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

class LoginModelForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].label = ''
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

        self.fields['username'].label = ''
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
