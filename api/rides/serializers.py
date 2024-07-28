from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import RideRequest, OfferRide, AcceptedRide


User = get_user_model()

class RideRequestSerializer(serializers.HyperlinkedModelSerializer):
    passenger = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = RideRequest
        fields = ['starting_location', 'destination', 'passenger']
        depth = 1


class OfferRideSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferRide
        fields = ['driver', 'arrival_time', 'price']


class AcceptedRideSerializer(OfferRideSerializer):
    class Meta:
        model = AcceptedRide
        fields = ['accepted_on']

