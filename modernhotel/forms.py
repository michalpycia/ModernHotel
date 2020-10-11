from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.auth.models import User
from django.contrib.postgres.forms import RangeWidget

from modernhotel.models import Reservation


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class NewReservationForm(forms.ModelForm):
    def clean_date_range(self):
        date_range = str(self.cleaned_data['date_range'])
        date_start = date_range[1:11]
        date_stop = date_range[13:23]
        if date_start == date_stop:
            raise forms.ValidationError("Reservation must include at least 1 night")
        return self.cleaned_data['date_range']

    class Meta:
        model = Reservation
        fields = '__all__'


