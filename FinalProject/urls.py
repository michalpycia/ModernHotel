"""FinalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from modernhotel.views import LandingPageView, LoginUserView, LogoutView, RoomsView, NewReservationView, \
    ReservationsView, RoomDetailsView, ReservationsViewOrder, ReservationEditView, RoomEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',  LoginUserView.as_view(), name='login-page'),
    path('logout_user/', LogoutView.as_view(), name="logout-user"),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('rooms/', RoomsView.as_view(), name='rooms'),
    path('room/<int:room_number>', RoomDetailsView.as_view()),
    path('new_reservation', NewReservationView.as_view(), name='new-reservation'),
    path('reservations', ReservationsViewOrder.as_view(), name='reservations'),
    path('reservations/<int:pk>', ReservationEditView.as_view(), name='reservation-edit'),
    path('room/<int:pk>/edit', RoomEditView.as_view(), name='room-edit'),
]
