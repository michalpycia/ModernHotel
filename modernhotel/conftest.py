import pytest
from django.test import Client
from .models import Reservation, Room

@pytest.fixture
def client():
    client = Client()
    return client

@pytest.fixture
def reservation():
    reservation = Reservation.objects.create(room=Room.objects.get(number=15), date_range='[2021-03-14,2021-03-16)', client_name='Bobek', client_surname='Babek', contact_number='321654231', email='a@a.com', comment='Duze lozko', arrival='00:00')
    return reservation

@pytest.fixture
def rooms():
    Room.objects.create(number=1, room_type='Single', bed_type='Single', air_conditioner=True, price=150)
    Room.objects.create(number=2, room_type='Single', bed_type='Single', air_conditioner=True, price=150)
    Room.objects.create(number=3, room_type='Single', bed_type='Single', air_conditioner=True, price=150)
    return Room.objects.all().order_by('number')