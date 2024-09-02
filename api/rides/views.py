import uuid

from channels.layers import (
    get_channel_layer,
)
from django.contrib.auth import (
    get_user_model,
)
from rest_framework import (
    status,
)
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import (
    Response,
)

from ..users.models import (
    Driver,
    Passenger,
)
from ..rides.serializers import (
    RideSerializer,
)
from .tasks import (
    accept_ride_offer,
    find_driver_for_ride,
    send_ride_offer,
    cancel_ride_task,
)

User = get_user_model()
channel_layer = (
    get_channel_layer()
)


@api_view(["POST"])
@permission_classes(
    [IsAuthenticated]
)
def create_ride(request):
    passenger_id = (
        request.user.pk
    )
    is_passenger = (
        Passenger.objects.get(
            pk=passenger_id
        )
    )
    if not is_passenger:
        return Response(
            {
                "message": "You must be a passenger to create a ride."
            },
            status.HTTP_401_UNAUTHORIZED,
        )

    starting_location = request.data.get(
        "starting_location"
    )  # expects (long, lat)
    destination = (
        request.data.get(
            "destination"
        )
    )  # expects (long, lat)
    ride_uuid = uuid.uuid4()
    if not (
        starting_location
        and destination
    ):
        return Response(
            {
                "message": "starting_location and destination are required."
            },
            status.HTTP_400_BAD_REQUEST,
        )
    find_driver_for_ride.delay(
        passenger_id,
        starting_location,
        destination,
        ride_uuid,
    )
    return Response(
        request.data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes(
    [IsAuthenticated]
)
def offer_ride(request):
    driver = request.user.pk
    is_driver = (
        Driver.objects.get(
            pk=driver
        )
    )
    if not is_driver:
        return Response(
            {
                "message": "You must be a driver to offer a ride."
            },
            status.HTTP_401_UNAUTHORIZED,
        )

    passenger_id = (
        request.data.get(
            "passenger_id"
        )
    )
    price = request.data.get(
        "price"
    )
    dropoff_time = (
        request.data.get(
            "dropoff_time"
        )
    )
    ride_duration = (
        request.data.get(
            "ride_duration"
        )
    )
    ride_uuid = (
        request.data.get(
            "ride_uuid"
        )
    )
    if not (
        price
        and ride_uuid
        and ride_uuid
        and passenger_id
    ):
        return Response(
            {
                "message": "price, ride_uuid, ride_duration, dropoff_time and passenger_id are required."
            },
            status.HTTP_400_BAD_REQUEST,
        )
    send_ride_offer.delay(
        driver,
        price,
        ride_duration,
        dropoff_time,
        ride_uuid,
        passenger_id,
    )
    return Response(
        request.data,
        status.HTTP_200_OK,
    )
    # there should be displayed more info about the driver on the frontend


@api_view(["POST"])
@permission_classes(
    [IsAuthenticated]
)
def accept_ride(request):
    passenger_id = (
        request.user.pk
    )
    is_passenger = (
        Passenger.objects.get(
            pk=passenger_id
        )
    )
    if not is_passenger:
        return Response(
            {
                "message": "You must be a passenger to accept a ride."
            },
            status.HTTP_401_UNAUTHORIZED,
        )

    driver_id = (
        request.data.get(
            "driver_id"
        )
    )
    starting_location = request.data.get(
        "starting_location"
    )  # expects (long, lat)
    destination = (
        request.data.get(
            "destination"
        )
    )  # expects (long, lat)
    price = request.data.get(
        "price"
    )
    ride_uuid = (
        request.data.get(
            "ride_uuid"
        )
    )
    dropoff_time = (
        request.data.get(
            "dropoff_time"
        )
    )
    ride_duration = (
        request.data.get(
            "ride_duration"
        )
    )
    if not (
        driver_id
        and starting_location
        and destination
        and price
        and ride_uuid
        and dropoff_time
        and ride_duration
    ):
        return Response(
            {
                "message": "driver_id, vehicle, price and ride_uuid are required."
            },
            status.HTTP_400_BAD_REQUEST,
        )
    # create a ride
    serializer = (
        RideSerializer(
            driver_id,
            passenger_id,
            starting_location,
            destination,
            ride_duration,
            dropoff_time,
            price,
            ride_uuid,
        )
    )
    if serializer.is_valid():
        serializer.save()
        accept_ride_offer.delay(
            driver_id,
            passenger_id,
            starting_location,
            destination,
            ride_duration,
            dropoff_time,
            price,
            ride_uuid,
        )
        return Response(
            request.data,
            status.HTTP_200_OK,
        )
    return Response(
        request.data,
        status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes(
    [IsAuthenticated]
)
def finish_ride(request):
    driver = request.user.pk
    is_driver = (
        Driver.objects.get(
            pk=driver
        )
    )
    if not is_driver:
        return Response(
            {
                "message": "You must be a driver to finish a ride."
            },
            status.HTTP_401_UNAUTHORIZED,
        )

    passenger_id = (
        request.data.get(
            "ride_uuid"
        )
    )
    price = request.data.get(
        "price"
    )


@api_view(["POST"])
@permission_classes(
    [IsAuthenticated]
)
def cancel_ride(request):
    passenger_id = (
        request.user.pk
    )
    is_passenger = (
        Passenger.objects.get(
            pk=passenger_id
        )
    )
    if not is_passenger:
        return Response(
            {
                "message": "You must be a passenger to accept a ride."
            },
            status.HTTP_401_UNAUTHORIZED,
        )

    ride_uuid = (
        request.data.get(
            "ride_uuid"
        )
    )
    cancel_ride_task.delay(
        passenger_id,
        ride_uuid,
    )
    return Response(
        request.data,
        status.HTTP_200_OK,
    )
