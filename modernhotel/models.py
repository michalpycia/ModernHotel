from django.db import models
from django.contrib.postgres.fields import DateRangeField


# Create your models here.
from django.db.models import UniqueConstraint, Q


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
        return f'Room {self.number}'


class Reservation(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_range = DateRangeField()
    client_name = models.CharField(max_length=256)
    client_surname = models.CharField(max_length=256)
    contact_number = models.CharField(max_length=16)
    email = models.EmailField()
    comment = models.TextField(null=True)

    def __str__(self):
        return f'{self.room_id}, {self.client_name} {self.client_surname}, {self.date_range}'


    class Meta:
        constraints = [UniqueConstraint(fields=['room_id'], condition=Q(), name='unique_draft_user')]


