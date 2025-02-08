from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..users.models import Driver, Passenger
from .models import Rating, Ride

User = get_user_model()


class RideSerializer(serializers.ModelSerializer):
    passenger = serializers.PrimaryKeyRelatedField(queryset=Passenger.objects.all())
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())
    start_time = serializers.DateTimeField(
        input_formats=None,
        allow_null=True,
        required=False,
    )
    end_time = serializers.DateTimeField(
        input_formats=None,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Ride
        fields = [
            "pk",
            "status",
            "passenger",
            "driver",
            "ride_uuid",
            "starting_location",
            "destination",
            "start_time",
            "end_time",
            "ride_duration",
            "dropoff_time",
            "price",
        ]


class RatingSerializer(serializers.HyperlinkedModelSerializer):
    ride = serializers.PrimaryKeyRelatedField(queryset=Ride.objects.all())

    class Meta:
        model = Rating
        fields = [
            "ride",
            "rating",
            "comment",
        ]
        depth = 1
