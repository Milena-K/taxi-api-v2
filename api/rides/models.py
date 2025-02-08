from django.contrib.auth import get_user_model
from django.db import models

from ..users.models import Driver, Passenger

User = get_user_model()


class Ride(models.Model):
    class Status(models.IntegerChoices):
        CREATED = 0
        ACTIVE = 1
        COMPLETED = 2
        CANCELED = 3

    status = models.IntegerField(
        choices=Status,
        default=Status.CREATED,
    )
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        blank=False,
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        blank=False,
    )
    ride_uuid = models.UUIDField(
        unique=True,
        blank=False,
    )
    starting_location = models.CharField(blank=False)
    destination = models.CharField(blank=False)
    start_time = models.DateTimeField(
        blank=True,
        null=True,
    )
    end_time = models.DateTimeField(
        blank=True,
        null=True,
    )
    price = models.FloatField(blank=False, default=0)
    dropoff_time = models.DateTimeField(blank=False)
    ride_duration = models.IntegerField(blank=False)

    def __str__(self):
        return (
            "Ride(passenger={},"
            " driver={},"
            " ride_uuid={}),"
            " starting_location={},"
            " destination={},"
            " start_time={},"
            " end_time={},"
            " price={},"
            " ride_duration={},"
            " dropoff_time={})"
        ).format(
            self.passenger,
            self.driver,
            self.ride_uuid,
            self.starting_location,
            self.destination,
            self.start_time,
            self.end_time,
            self.price,
            self.ride_duration,
            self.dropoff_time,
        )


class Rating(models.Model):
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
    )
    rating = models.FloatField(
        default=5.0,
        blank=False,
    )
    comment = models.CharField(blank=False)

    def __str__(self):
        return ("Rating(ride={})," " rating={}," " comment={})").format(
            self.ride,
            self.rating,
            self.comment,
        )
