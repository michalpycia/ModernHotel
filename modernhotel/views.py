from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import FormView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from .forms import LoginUserForm, NewReservationForm, ReservationEditForm, RoomEditForm
from .models import *
from django.contrib.auth import authenticate, login, logout


# Create your views here.
class LandingPageView(View):
    """
    landing page view - main page of the app
    """

    def get(self, request):
        return render(request, 'base.html')


class LoginUserView(FormView):
    '''
    Login user View based on the LoginUserForm.
    When user is authenticated app is redirecting to main page located at '/'
    '''
    template_name = 'index.html'
    form_class = LoginUserForm
    success_url = '/'

    def form_valid(self, form):
        """
        Function to check if username and password exist in database
        If correct - login user
        If incorrect - inform user
        """
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            response = HttpResponse('Logged')
            response.set_cookie('logged_in', value='', max_age=600)
        else:
            return HttpResponse("Wrong name or password")
        return super(LoginUserView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        """
        View to logout user from application
        Return: redirect to landing page
        """
        logout(request)
        return HttpResponseRedirect(reverse('login-page'))


class RoomsView(View):
    """
    Rooms list view,
    return: list of rooms from DB
    """

    def get(self, request):
        rooms_q = Room.objects.all()
        rooms = self.paginator(request, rooms_q)
        return render(request, 'rooms.html', {'rooms': rooms})

    def paginator(self, request, rooms):
        paginator = Paginator(rooms, 25)
        page = request.GET.get('page')
        pagination = paginator.get_page(page)
        return pagination


class NewReservationView(CreateView):
    """
    View for creating new reservation based on the NewReservationForm
    return: Reservation object created in DB
    """
    form_class = NewReservationForm
    template_name = 'modernhotel/reservation_form.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            return render(request, template_name=self.template_name,
                          context={'message': 'Room already booked for this time, chose another room or date',
                                   'form': self.get_form()})


class RoomDetailsView(View):
    def get(self, request, room_number):
        room = Room.objects.get(number=room_number)
        reservations = Reservation.objects.filter(room=room).order_by('date_range')
        reservations_past = Reservation.objects.filter(room=room).order_by('date_range')
        return render(request, 'room_detail.html',
                      {'room': room, 'reservations': reservations, 'reservations_past': reservations_past})


class ReservationsAllView(View):
    """
    All reservations list view
    return: list of all Reservation model instances
    """

    def get(self, request):
        reservations = self.paginator(request, Reservation.objects.all().order_by('-date_range'))
        message = 'All reservations'
        return render(request, 'reservations.html',
                      {"reservations": reservations, "message": message})

    def post(self, request):
        reservation_search = request.POST.get('reservation_search')
        search = Reservation.objects.filter(
            Q(client_name__iexact=reservation_search) | Q(client_surname__iexact=reservation_search))
        return render(request, 'reservations_search.html', {"search": search})

    def paginator(self, request, reservations):
        paginator = Paginator(reservations, 20)
        page = request.GET.get('page')
        pagination = paginator.get_page(page)
        return pagination


class ReservationEditView(UpdateView):
    """
    View for updating Reservation model instance details
    return: Form with object details that can be updated
    """
    form_class = ReservationEditForm
    template_name = 'modernhotel/reservation_update_form.html'
    queryset = Reservation.objects.all()
    success_url = '/reservations'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Reservation, pk=pk)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class RoomEditView(UpdateView):
    """
    View for updating Room model instance details
    return: Form with object details that can be updated
    """
    form_class = RoomEditForm
    template_name = 'edit_room.html'
    queryset = Room.objects.all()
    success_url = '/rooms'

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Room, pk=pk)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class ReservationsStayView(View):
    """
    View for current stay reservations
    return: List of Reservations objects that check_in field is set to True and fields check_out and cancelled are set
    to False
    """

    def get(self, request):
        reservations = self.paginator(request, Reservation.objects.filter(check_in=True, check_out=False,
                                                                          cancelled=False).order_by(
            '-date_range'))
        message = 'Current stay'
        return render(request, 'reservations.html',
                      {"reservations": reservations, "message": message})

    def post(self, request):
        reservation_search = request.POST.get('reservation_search')
        search = Reservation.objects.filter(
            Q(client_name__iexact=reservation_search) | Q(client_surname__iexact=reservation_search))
        return render(request, 'reservations_search.html', {"search": search})

    def paginator(self, request, reservations):
        paginator = Paginator(reservations, 20)
        page = request.GET.get('page')
        pagination = paginator.get_page(page)
        return pagination


class ReservationsArrivalsView(View):
    """
    View for arrivals reservations
    return: List of Reservations objects that check_in, check_out and cancelled fields are set
    to False
    """

    def get(self, request):
        reservations = self.paginator(request, Reservation.objects.filter(check_in=False, check_out=False,
                                                                          cancelled=False).order_by('date_range'))
        message = 'Check in expected'
        return render(request, 'reservations.html',
                      {"reservations": reservations, "message": message})

    def post(self, request):
        reservation_search = request.POST.get('reservation_search')
        search = self.paginator(request, Reservation.objects.filter(
            Q(client_name__iexact=reservation_search) | Q(client_surname__iexact=reservation_search)))
        return render(request, 'reservations_search.html', {"search": search})

    def paginator(self, request, reservations):
        paginator = Paginator(reservations, 20)
        page = request.GET.get('page')
        pagination = paginator.get_page(page)
        return pagination


class ReservationsPastView(View):
    """
    View for past reservations
    return: List of Reservations objects that check_in and check_out fields are set to True and cancelled field
    is set to False
    """

    def get(self, request):
        reservations = self.paginator(request, Reservation.objects.filter(check_in=True, check_out=True,
                                                                          cancelled=False).order_by('-date_range'))
        message = 'Past reservations'
        return render(request, 'reservations.html',
                      {"reservations": reservations, "message": message})

    def post(self, request):
        reservation_search = request.POST.get('reservation_search')
        search = Reservation.objects.filter(
            Q(client_name__iexact=reservation_search) | Q(client_surname__iexact=reservation_search))
        return render(request, 'reservations_search.html', {"search": search})

    def paginator(self, request, reservations):
        paginator = Paginator(reservations, 20)
        page = request.GET.get('page')
        pagination = paginator.get_page(page)
        return pagination


class ReservationsCancelledView(View):
    """
    View for cancelled reservations
    return: List of Reservations objects that cancelled field is set to True
    """

    def get(self, request):
        reservations = self.paginator(request, Reservation.objects.filter(cancelled=True).order_by(
            '-date_range'))
        message = 'Cancelled reservations'
        return render(request, 'reservations.html',
                      {"reservations": reservations, "message": message})

    def post(self, request):
        reservation_search = request.POST.get('reservation_search')
        search = Reservation.objects.filter(
            Q(client_name__iexact=reservation_search) | Q(client_surname__iexact=reservation_search))
        return render(request, 'reservations_search.html', {"search": search})

    def paginator(self, request, reservations):
        paginator = Paginator(reservations, 20)
        page = request.GET.get('page')
        pagination = paginator.get_page(page)
        return pagination


class ReservationsNewestView(View):
    """
    View for newest reservations
    return: List of Reservations objects that check_in, cancelled and check_out fields are set to False
    """

    def get(self, request):
        reservations = self.paginator(request, Reservation.objects.filter(check_in=False, check_out=False,
                                                                          cancelled=False).order_by('-id'))
        message = 'Newest reservations'
        return render(request, 'reservations.html',
                      {"reservations": reservations, "message": message})

    def post(self, request):
        reservation_search = request.POST.get('reservation_search')
        search = Reservation.objects.filter(
            Q(client_name__iexact=reservation_search) | Q(client_surname__iexact=reservation_search))
        return render(request, 'reservations_search.html', {"search": search})

    def paginator(self, request, reservations):
        paginator = Paginator(reservations, 20)
        page = request.GET.get('page')
        pagination = paginator.get_page(page)
        return pagination
