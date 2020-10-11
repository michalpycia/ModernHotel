from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import FormView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse

from .forms import LoginUserForm, NewReservationForm
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
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            response = HttpResponse('Zalogowano')
            response.set_cookie('logged_in', value='', max_age=600)
        else:
            return HttpResponse("Wrong name or password")
        return super(LoginUserView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('landing-page'))


class RoomsView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, 'rooms.html', {'rooms': rooms})


class NewReservationView(CreateView):
    form_class = NewReservationForm
    template_name = 'modernhotel/reservation_form.html'
    success_url = 'reservations'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            return render(request, template_name=self.template_name,
                          context={'message': 'Room already booked for this time, chose another room or date',
                                   'form': self.get_form()})


class ReservationsView(View):
    def get(self, request):
        stay_active = Reservation.objects.filter(check_in=True, check_out=False, cancelled=False).order_by(
            '-date_range')[:5]
        check_in_expected = Reservation.objects.filter(check_in=False, check_out=False, cancelled=False).order_by(
            'date_range')[:5]
        past = Reservation.objects.filter(check_in=True, check_out=True, cancelled=False).order_by(
            '-date_range')[:5]
        cancelled = Reservation.objects.filter(cancelled=True).order_by(
            '-date_range')[:5]
        newest = Reservation.objects.filter(check_in=False, check_out=False, cancelled=False).order_by('-id')[:5]
        return render(request, 'reservations.html', {"stay_active": stay_active, "check_in_expected": check_in_expected,
                                                     "past": past, "cancelled": cancelled, "newest": newest})


class RoomDetailsView(View):
    def get(self, request, room_number):
        room = Room.objects.get(number=room_number)
        reservations = Reservation.objects.filter(room=room, check_in=False, check_out=False).order_by('date_range')
        reservations_past = Reservation.objects.filter(room=room, check_in=True, check_out=True).order_by('date_range')
        return render(request, 'room_detail.html',
                      {'room': room, 'reservations': reservations, 'reservations_past': reservations_past})


class RoomPriceView(View):
    def get(self, request, room_number):
        room = Room.objects.get(number=room_number)
        return render(request, 'room_price.html', {'room': room})


class ReservationsViewOrder(View):

    def get(self, request):
        all = Reservation.objects.all().order_by('-date_range')
        stay_active_query = Reservation.objects.filter(check_in=True, check_out=False, cancelled=False).order_by(
            '-date_range')
        stay_active = self.paginator(request, stay_active_query)
        check_in_expected_query = Reservation.objects.filter(check_in=False, check_out=False, cancelled=False).order_by(
            'date_range')
        check_in_expected = self.paginator(request, check_in_expected_query)
        past_query = Reservation.objects.filter(check_in=True, check_out=True, cancelled=False).order_by(
            '-date_range')
        past = self.paginator(request, past_query)
        cancelled_query = Reservation.objects.filter(cancelled=True).order_by(
            '-date_range')
        cancelled = self.paginator(request, cancelled_query)
        newest_query = Reservation.objects.filter(check_in=False, check_out=False, cancelled=False).order_by('-id')
        newest = self.paginator(request, newest_query)
        return render(request, 'reservations.html',
                      {"all": all, "stay_active": stay_active, "check_in_expected": check_in_expected,
                       "past": past, "cancelled": cancelled, "newest": newest})

    def paginator(self, request, reservations):
        paginator = Paginator(reservations, 50)
        page = request.GET.get('page')
        reservations = paginator.get_page(page)
        return reservations

    def post(self, request):
        reservation_search = request.POST.get('reservation_search')
        search = Reservation.objects.filter(client_name__iexact=reservation_search).order_by('-date_range')
        return render(request, 'reservations.html', {"search": search})
