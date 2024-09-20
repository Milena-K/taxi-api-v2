from django.contrib.auth import (
    get_user_model,
)
from rest_framework import (
    serializers,
)

from .models import (
    Ride,
    Rating,
)
from ..users.models import (
    Passenger,
    Driver,
)

User = get_user_model()


class RideSerializer(
    serializers.ModelSerializer
):
    passenger = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all()
    )
    driver = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all()
    )
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

    # def create(
    #     self,
    #     instance,
    #     validated_data,
    # ):
    #     instance.passenger = validated_data.passenger
    #     instance.driver = validated_data.driver
    #     instance.ride_uuid = validated_data.ride_uuid
    #     instance.starting_location = validated_data.starting_location
    #     instance.destination = validated_data.destination
    #     instance.start_time = validated_data.start_time
    #     instance.end_time = validated_data.end_time
    #     instance.ride_duration = validated_data.ride_duration
    #     instance.dropoff_time = validated_data.driver
    #     instance.price = validated_data.price


class RatingSerializer(
    serializers.HyperlinkedModelSerializer
):
    passenger = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all()
    )
    driver = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all()
    )
    ride = serializers.PrimaryKeyRelatedField(
        queryset=Ride.objects.all()
    )

    class Meta:
        model = Rating
        fields = [
            "rating",
            "comment",
        ]
        depth = 1
