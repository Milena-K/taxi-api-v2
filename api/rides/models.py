from django.db import models
from django.contrib.auth import (
    get_user_model,
)

from ..users.models import (
    Driver,
    Passenger,
)


User = get_user_model()


class Ride(models.Model):
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
    ride_uuid = (
        models.UUIDField(
            unique=True,
            blank=False,
        )
    )
    starting_location = (
        models.CharField(
            blank=False
        )
    )
    destination = (
        models.CharField(
            blank=False
        )
    )
    start_time = (
        models.DateTimeField(
            blank=False
        )
    )
    end_time = (
        models.DateTimeField(
            auto_now_add=True,
            blank=False,
        )
    )
    price = models.FloatField(
        blank=False, default=0
    )

    def __str__(self):
        return f"Ride(passenger={self.passenger}, driver={self.driver}, ride_uuid={self.ride_uuid})"


class Rating(models.Model):
    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.CASCADE,
        blank=False,
    )  # rated by
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        blank=False,
    )
    ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
    )
    rating = (
        models.FloatField(
            default=5.0,
            blank=False,
        )
    )
    comment = (
        models.CharField(
            blank=False
        )
    )

    def __str__(self):
        if self.comment:
            return f"Rating driver {self.driver} with {self.rating} by passenger {self.passenger} for ride {self.ride} with comment: {self.comment}"
        else:
            return f"Rating driver {self.driver} with {self.rating} by passenger {self.passenger} for ride {self.ride} with no comment."
