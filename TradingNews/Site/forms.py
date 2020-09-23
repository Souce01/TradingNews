from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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
