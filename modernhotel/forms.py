from django import forms
from django.contrib.auth.models import User


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
