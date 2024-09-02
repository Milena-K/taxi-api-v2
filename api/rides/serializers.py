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
    serializers.HyperlinkedModelSerializer
):
    passenger = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all()
    )
    driver = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all()
    )

    class Meta:
        model = Ride
        fields = [
            "pk",
            "ride_uuid",
            "starting_location",
            "destination",
            "start_time",
            "end_time",
            "price",
        ]
        depth = 1


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
