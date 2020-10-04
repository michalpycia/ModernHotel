from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from django.contrib.postgres.forms import RangeWidget

from modernhotel.models import Reservation


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class NewReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = '__all__'


class NewResForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"
        widgets = {
            'date_range': RangeWidget(AdminDateWidget())
        }
