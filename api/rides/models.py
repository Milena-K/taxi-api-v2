from django.db import models
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..users.models import Driver, Passenger


User = get_user_model()

class RideRequest(models.Model):
    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_location = models.CharField(blank=False)
    destination = models.CharField(blank=False)

    def __str__(self):
        return f"Passenger {self.passenger} is traveling from {self.starting_location}, to {self.destination}"


class OfferRide(RideRequest):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    arrival_time = models.IntegerField() # arriving on the starting location
    price = models.FloatField()


class AcceptedRide(OfferRide):
    accepted_on = models.DateTimeField(auto_now_add=True)
