from django.db import models
from django.contrib.auth import get_user_model
from ..users.models import Driver, Passenger


User = get_user_model()

class RideRequest(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    starting_location = models.CharField(blank=False)
    destination = models.CharField(blank=False)

    def __str__(self):
        return f"Passenger {self.passenger} is traveling from {self.starting_location}, to {self.destination}"


class RideOffer(models.Model):
    ride_request = models.ForeignKey(RideRequest, on_delete=models.CASCADE, blank=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=False)
    arrival_time = models.IntegerField(blank=False) # arriving on the starting location
    price = models.FloatField(blank=False)

class RideAccepted(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, blank=False)
    offer = models.ForeignKey(RideOffer, on_delete=models.CASCADE, blank=False)
    accepted_on = models.DateTimeField(auto_now_add=True)
