from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Ride
from ..users.models import Passenger, Driver

User = get_user_model()

class RideSerializer(serializers.HyperlinkedModelSerializer):
    passenger = serializers.PrimaryKeyRelatedField(queryset=Passenger.objects.all())
    class Meta:
        model = Ride
        fields = ['starting_location', 'destination', 'passenger', 'pk']
        depth = 1


# class RideOfferSerializer(serializers.HyperlinkedModelSerializer):
#     ride_request = serializers.PrimaryKeyRelatedField(queryset=RideRequest.objects.all())
#     driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())
#     class Meta:
#         model = RideOffer
#         fields = ['pk', 'ride_request', 'driver', 'arrival_time', 'price']


# class RideAcceptedSerializer(serializers.HyperlinkedModelSerializer):
#     offer = serializers.PrimaryKeyRelatedField(queryset=RideOffer.objects.all())
#     passenger = serializers.PrimaryKeyRelatedField(queryset=Passenger.objects.all())
#     class Meta:
#         model = RideAccepted
#         fields = ['accepted_on', 'offer', 'passenger']
