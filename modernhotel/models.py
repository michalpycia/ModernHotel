from django.contrib.postgres.constraints import ExclusionConstraint
from django.db import models
from django.contrib.postgres.fields import DateRangeField, RangeOperators
from datetime import datetime
# Create your models here.
from django.db.models import UniqueConstraint, Q
from django.core.validators import MinValueValidator


class Room(models.Model):
    ROOM_TYPE = (
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Triple', 'Triple'),
    )
    BED_TYPE = (
        ('Single', 'Single'),
        ('Twin', 'Twin'),
        ('Double', 'Double'),
        ('King', 'King'),
    )

    number = models.IntegerField(unique=True)
    room_type = models.CharField(choices=ROOM_TYPE, default='Single', max_length=20)
    bed_type = models.CharField(choices=BED_TYPE, default='Single', max_length=20)
    air_conditioner = models.BooleanField(default=True)
    price = models.FloatField()

    def __str__(self):
        return f'{self.number}'


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_range = DateRangeField()
    client_name = models.CharField(max_length=256)
    client_surname = models.CharField(max_length=256)
    contact_number = models.CharField(max_length=16)
    email = models.EmailField()
    comment = models.TextField(null=True)
    cancelled = models.BooleanField(default=False)
    arrival = models.TimeField(default='00:00')
    check_in = models.BooleanField(default=False)
    check_out = models.BooleanField(default=False)
    price_for_day = models.IntegerField(
        validators=[MinValueValidator(49)],
        default=49)

    def __str__(self):
        return f'{self.room}, {self.client_name} {self.client_surname}, {self.date_range}'

    @property
    def duration(self):
        date_format = "%Y-%m-%d"
        date_range = str(self.date_range)
        date_start = datetime.strptime(date_range[1:11], date_format)
        date_stop = datetime.strptime(date_range[13:23], date_format)
        delta = date_stop - date_start
        return delta.days

    @property
    def charge(self):
        return self.duration * self.price_for_day

    class Meta:
        constraints = [
            ExclusionConstraint(
                name='exclude_overlapping_reservations',
                expressions=[
                    ('date_range', RangeOperators.OVERLAPS),
                    ('room', RangeOperators.EQUAL),
                ],
                condition=Q(cancelled=False),
            )
        ]


class Client(models.Model):
    client_name = models.CharField(max_length=256)
    client_surname = models.CharField(max_length=256)
    contact_number = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return f'{self.client_name} {self.client_surname} - Contact number: {self.contact_number}'
