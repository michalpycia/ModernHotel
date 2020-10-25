import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Reservation, Room


# Create your tests here.
class TestLandingPage(TestCase):
    """
    Landing page loading test
    """

    def test_ok(self):
        response = self.client.get('/')
        assert response.status_code == 200


class TestNewReservationsView(TestCase):
    """
    New reservation view loading test
    """

    def test_ok(self):
        response = self.client.get('/new_reservation')
        assert response.status_code == 200


class TestNewestReservationsView(TestCase):
    """
    Newest reservations view loading test
    """

    def test_ok(self):
        response = self.client.get('/reservations/newest')
        assert response.status_code == 200



class TestCurrentReservationsView(TestCase):
    """
    Current reservations view loading test
    """

    def test_ok(self):
        response = self.client.get('/reservations/stay')
        assert response.status_code == 200



class TestArrivalsReservationsView(TestCase):
    """
    Arrivals reservation view loading test
    """

    def test_ok(self):
        response = self.client.get('/reservations/arrivals')
        assert response.status_code == 200




class TestPastReservationsView(TestCase):
    """
    Past reservations view loading test
    """

    def test_ok(self):
        response = self.client.get('/reservations/past')
        assert response.status_code == 200




class TestCancelledReservationsView(TestCase):
    """
    Cancelled reservations view loading test
    """

    def test_ok(self):
        response = self.client.get('/reservations/cancelled')
        assert response.status_code == 200




class TestRoomsView(TestCase):
    """
    test if rooms view is loading
    """

    def test_ok(self):
        response = self.client.get('/rooms/')
        assert response.status_code == 200




@pytest.mark.django_db
def test_login_user(client):
    """
    Login view test, created user should be able to login
    """
    user = User.objects.create_user(username='michal', password='Zaq12wsxcde')
    user.save()
    url = "/login/"
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, {'username': 'michal', 'password': 'Zaq12wsxcde'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_failed_login_user(client):
    """
    Test for login view. Incorrect data provided
    """
    user = User.objects.create_user(username='michal', password='Zaq12wsxcde')
    user.save()
    url = "/login/"
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, {'username': 'michal', 'password': 'Zaq12wsxcde1'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_reservation(client, rooms):
    """
    Test to create an Reservation object in DB
    """
    url = '/new_reservation'
    response = client.post(url, {'room_id': 1, 'date_range_0': '2020-11-06', 'date_range_1': '2020-11-08',
                                 'client_surname': 'Boom', 'client_name': 'Josh', 'contact_number': '1232123',
                                 'email': 'a@a.com', 'arrival': '00:00', 'check_in': False, 'check_out': False,
                                 'cancelled': False, 'price_for_day': 150})
    assert response.status_code == 200
    assert Reservation.objects.count() == 1


@pytest.mark.django_db
def test_create_reservation_failed(client):
    """
    Test to create reservation for already booked time.
    """
    room = Room.objects.create(number=1, room_type='Single', bed_type='Single', air_conditioner=True, price=150)
    room.save()
    res = Reservation.objects.create(room=Room.objects.get(pk=1), date_range='[2020-11-05,2020-11-07)',
                                     client_name='Jack',
                                     client_surname='Jack', contact_number=123123321, email='a@a.com', cancelled=False,
                                     arrival='00:00', check_in=False, check_out=False, price_for_day=150)
    res.save()
    url = '/new_reservation'
    response = client.post(url, {'room_id': ['1'], 'date_range_0': '2020-11-06', 'date_range_1': '2020-11-08',
                                 'client_surname': 'Boom', 'client_name': 'Josh', 'contact_number': '1232123',
                                 'email': 'a@a.com', 'arrival': '00:00', 'check_in': False, 'check_out': False,
                                 'cancelled': False, 'price_for_day': 150})
    assert response.status_code == 200
    assert Reservation.objects.count() == 1


@pytest.mark.django_db
def edit_room(client):
    """
    Test edit room view with correct data
    """
    room = Room.objects.create(number=1, room_type='Single', bed_type='Single', air_conditioner=True, price=150)
    room.save()
    url = f'/room/{room.id}/edit'
    response = client.post(url, {'room_type': 'Single', 'bed_type': 'Twin', 'air_conditioner': True,
                                 'price': 200})
    assert response.status_code == 302
    room.refresh_from_db()
    assert room.bed_type == 'Twin'


@pytest.mark.django_db
def edit_room_failed(client):
    """
    Test edit room view with incorrect data
    """
    room = Room.objects.create(number=1, room_type='Single', bed_type='Single', air_conditioner=True, price=150)
    room.save()
    url = f'/room/{room.id}/edit'
    response = client.post(url, {'room_type': 'King', 'bed_type': 'Twin', 'air_conditioner': 'Yes',
                                 'price': 200})
    assert Reservation.objects.count() == 1
    assert room.room_type == 'Single'
    assert response.status_code == 200
