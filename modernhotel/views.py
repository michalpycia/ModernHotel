from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, ListView
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse_lazy, reverse

from .forms import LoginUserForm, NewReservationForm, NewResForm
from .models import *
from django.contrib.auth import authenticate, login, logout


# Create your views here.
class LandingPageView(View):
    # Landing page class view.
    def get(self, request):
        return render(request, 'base.html')


class LoginUserView(FormView):
    template_name = 'index.html'
    form_class = LoginUserForm
    success_url = 'dashboard/'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
        else:
            return HttpResponse("Wrong name or password")
        return super(LoginUserView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('logout-user'))


class RoomsView(View):
    def get(self, request):
        rooms = Room.objects.all()

        return render(request, 'rooms.html', {'rooms': rooms})


class NewReservationView(FormView):
    form_class = NewResForm
    template_name = 'modernhotel/reservation_form.html'
    success_url = '/reservations'

#class NewReservation(View):
