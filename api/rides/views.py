import uuid
from datetime import datetime

from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db.models import ObjectDoesNotExist
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..rides.models import Rating, Ride
from ..rides.permissions import IsDriver, IsPassenger
from ..rides.serializers import RatingSerializer, RideSerializer
from .tasks import (
    accept_ride_offer,
    cancel_active_ride_task,
    cancel_ride_task,
    find_driver_for_ride,
    send_ride_offer,
    start_ride_task,
)

User = get_user_model()
channel_layer = get_channel_layer()


class RidesViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for modifying or listing Rides.
    """

    serializer_class = RideSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """
        Optionally filters rides by querystring parameter ride_uuid.
        """
        queryset = Ride.objects.all()
        ride_uuid = self.request.query_params.get("ride_uuid")
        if ride_uuid is not None:
            queryset = Ride.objects.filter(ride_uuid=ride_uuid)
        return queryset


class RideRatingsViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for modifying or listing RideRatings.
    """

    serializer_class = RatingSerializer
    queryset = Rating.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in [
            "update",
            "partial_update",
            "destroy",
        ]:
            permission_classes = [permissions.IsAdminUser]
        else:  # list, create
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
        IsPassenger,
    ]
)
def request_ride(request):
    """
    Endpoint for a user to request a ride with a starting location and a destination
    """
    passenger_id = request.user.pk
    starting_location = request.data.get("starting_location")  # expects (long, lat)
    destination = request.data.get("destination")  # expects (long, lat)
    ride_uuid = uuid.uuid4()
    print(request.session)
    print(request.session.keys())
    if not (starting_location and destination):
        return Response(
            {"message": "starting_location and destination are required."},
            status.HTTP_400_BAD_REQUEST,
        )
    find_driver_for_ride.delay(
        passenger_id,
        starting_location,
        destination,
        ride_uuid,
    )
    response_data = {**request.data, "ride_uuid": ride_uuid.hex}
    return Response(
        response_data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
        IsDriver,
    ]
)
def offer_ride(request):
    """
    Endpoint for drivers to accept the request and give an offer for a ride
    """
    driver = request.user.pk
    passenger_id = request.data.get("passenger_id")
    # TODO the price should be calculated on the server
    price = 10
    ride_uuid = request.data.get("ride_uuid")
    try:
        ride = Ride.objects.get(ride_uuid=ride_uuid)
        if ride:
            return Response(
                {"message": "This ride already exists, try another ride_uuid."},
                status.HTTP_400_BAD_REQUEST,
            )
    except ObjectDoesNotExist:
        ride_duration = 0  # TODO calculate
        dropoff_time = 0  # time.now() + ride_duration
        if not (price and ride_uuid and passenger_id):
            return Response(
                {"message": "ride_uuid and passenger_id are required."},
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
    [
        IsAuthenticated,
        IsPassenger,
    ]
)
def accept_ride(request):
    """
    Endpoint for users to accept the ride offer from a driver
    """
    passenger_id = request.user.pk
    driver_id = request.data.get("driver_id")
    starting_location = request.data.get("starting_location")  # expects (long, lat)
    destination = request.data.get("destination")  # expects (long, lat)
    price = request.data.get("price")
    ride_uuid = request.data.get("ride_uuid")
    dropoff_time = request.data.get("dropoff_time")
    start_time = request.data.get("start_time")
    ride_duration = request.data.get("ride_duration")
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
                "message": "driver_id, starting_location,\
                destination, dropoff_time, ride_duration,\
                price and ride_uuid are required."
            },
            status.HTTP_400_BAD_REQUEST,
        )

    try:
        Ride.objects.get(ride_uuid=ride_uuid)
        return Response(
            {"message": "This ride already exists."},
            status.HTTP_400_BAD_REQUEST,
        )
    except ObjectDoesNotExist:
        # create a ride
        serializer = RideSerializer(
            data={
                "status": Ride.Status.CREATED,
                "passenger": passenger_id,
                "driver": driver_id,
                "ride_uuid": ride_uuid,
                "starting_location": starting_location,
                "destination": destination,
                "ride_duration": ride_duration,
                "dropoff_time": dropoff_time,
                "start_time": start_time,
                "price": price,
            }
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
            serializer.errors,
            status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
        IsDriver,
    ]
)
def start_ride(request):
    """
    Endpoint for starting the ride
    """
    driver = request.user.pk
    passenger = request.data.get("passenger")
    ride_uuid = request.data.get("ride_uuid")
    if not (ride_uuid and passenger):
        return Response(
            {"message": "ride_uuid and passenger are required."},
            status.HTTP_400_BAD_REQUEST,
        )
    try:
        ride = Ride.objects.get(ride_uuid=ride_uuid)
        if ride.status == Ride.Status.COMPLETED:
            return Response(
                {"message": "This ride is completed."},
                status.HTTP_400_BAD_REQUEST,
            )
        elif ride.status == Ride.Status.CREATED:
            ride.start_time = datetime.now()
            ride.status = Ride.Status.ACTIVE
            ride.save()
            # the driver should periodically send location data to passenger ws

            start_ride_task.delay(
                passenger,
                driver,
                ride_uuid,
            )
        return Response(
            {"message": "This ride is started."},
            status.HTTP_200_OK,
        )
    except ObjectDoesNotExist:
        return Response(
            {"message": "No ride with this ride_uuid was found."},
            status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
        IsDriver,
    ]
)
def finish_ride(
    request,
):
    """
    Endpoint for a successfull ending of a ride from the driver
    """
    passenger = request.data.get("passenger")
    driver = request.user.pk
    ride_uuid = request.data.get("ride_uuid")
    if not (ride_uuid and passenger):
        return Response(
            {"message": "ride_uuid and passenger are required."},
            status.HTTP_400_BAD_REQUEST,
        )
    try:
        ride = Ride.objects.get(ride_uuid=ride_uuid)
        if ride.status == Ride.Status.ACTIVE:
            ride.end_time = datetime.now()
            ride.status = Ride.Status.COMPLETED
            # calculate price: curernt_time - start_time * 7 (per minute)
            time_now = datetime.now().astimezone()
            price = ((time_now - ride.start_time).seconds / 60) * 7
            ride.price = price
            ride.save()
            # send message to passenger the ammount owned
            cancel_active_ride_task.delay(
                passenger,
                driver,
                price,
                ride_uuid,
            )
            return Response(
                {"message": "This ride has completed."},
                status.HTTP_200_OK,
            )
        return Response(
            {"message": "This ride is not active."},
            status.HTTP_400_BAD_REQUEST,
        )
    except ObjectDoesNotExist:
        return Response(
            {"message": "Can't find the ride you are looking for"},
            status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
        IsPassenger,
    ]
)
def cancel_ride(request):
    """
    Endpoint for canceling a ride when a user changes their mind
    """
    # TODO: there should be punishment for changing mind often (spamming)
    passenger_id = request.user.pk
    driver_id = request.data.get("driver_id")
    ride_uuid = request.data.get("ride_uuid")
    if not (ride_uuid and driver_id):
        return Response(
            {"message": "ride_uuid and driver_id are required."},
            status.HTTP_400_BAD_REQUEST,
        )
    try:
        ride = Ride.objects.get(ride_uuid=ride_uuid)
        if ride.status == Ride.Status.CREATED:  # if ride hasn't started yet
            # send direct message to driver that the ride is canceled
            ride.status = Ride.Status.CANCELED
            ride.save()
            cancel_ride_task(
                passenger_id,
                driver_id,
                ride_uuid,
            )
            return Response(
                {
                    "message": "requested ride is canceled.",
                },
                status.HTTP_200_OK,
            )
        elif ride.status == Ride.Status.ACTIVE:
            # TODO:
            # calculate price: curernt_time - start_time * 7 (per minute)
            # send message to passenger the ammount owned
            time_now = datetime.now().astimezone()
            ride.status = Ride.Status.CANCELED
            price = ((time_now - ride.start_time).seconds / 60) * 7
            ride.price = price
            ride.save()
            cancel_active_ride_task.delay(
                passenger_id,
                driver_id,
                price,
                ride_uuid,
            )
            return Response(
                {
                    "message": "active ride is canceled.",
                    "price": price,
                },
                status.HTTP_200_OK,
            )
        return Response(
            {
                "message": "this ride is already canceled.",
            },
            status.HTTP_200_OK,
        )

    except ObjectDoesNotExist:
        return Response(
            {"message": "Can't find the ride you are looking for"},
            status.HTTP_404_NOT_FOUND,
        )


@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
        IsPassenger,
    ]
)
def rate_ride(request):
    """
    Endpoint for giving rating from a user that has finished a ride
    """
    # TODO: user can rate only the ride they've ridden
    ride_uuid = request.data.get("ride_uuid")
    if not (ride_uuid):
        return Response(
            {"message": "ride_uuid is required."},
            status.HTTP_400_BAD_REQUEST,
        )
    try:
        ride = Ride.objects.get(ride_uuid=ride_uuid)
        serializer = RatingSerializer(
            data={
                "ride": ride.pk,
                "rating": 2.0,
                "comment": "It aint.",
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "data is valid"},
                status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST,
        )

    except ObjectDoesNotExist:
        return Response(
            {"message": "Can't find the ride you are looking for"},
            status.HTTP_404_NOT_FOUND,
        )
