from rest_framework.viewsets import ViewSet
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Ride
#from .serializers import RideRequestSerializer, RideOfferSerializer, RideAcceptedSerializer
from ..users.serializers import UserSerializer
from ..users.models import Passenger, Driver
from .tasks import find_driver_for_ride, send_ride_offer, accept_ride_offer, start_ride
import uuid

User = get_user_model()
channel_layer = get_channel_layer()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_ride(request):
    passenger = request.user.pk
    starting_location = request.data.get("starting_location")
    destination = request.data.get("destination")
    ride_uuid = uuid.uuid4()
    if not (starting_location and destination and ride_uuid):
        return Response({"message": "starting_location, destination and ride_uuid are required."}, status.HTTP_400_BAD_REQUEST)
    find_driver_for_ride.delay(passenger, starting_location, destination, ride_uuid)
    return Response(request.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def offer_ride(request):
    driver = request.user.pk
    vehicle = request.data.get("vehicle")
    price = request.data.get("price")
    ride_uuid = request.data.get("ride_uuid")
    if price is None or ride_uuid is None or ride_uuid is None:
        return Response({"message": "price, vehicle and ride_uuid are required."}, status.HTTP_400_BAD_REQUEST)
    send_ride_offer.delay(driver, vehicle, price, ride_uuid)
    return Response(request.data, status.HTTP_200_OK)
    # there should be displayed more info about the driver on the frontend
    # arrival time on the starting location and estimated time to the final destination are calculated automatically.


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_ride(request):
    passenger_id = request.user.pk
    driver_id = request.data.get("driver")
    vehicle = request.data.get("vehicle")
    price = request.data.get("price")
    ride_uuid = request.data.get("ride_uuid")
    room_uuid = uuid.uuid4()
    if not (driver_id and vehicle and price and ride_uuid):
        return Response({"message": "driver_id, vehicle, price and ride_uuid are required."}, status.HTTP_400_BAD_REQUEST)
    accept_ride_offer.delay(driver_id, passenger_id, vehicle, price, ride_uuid, room_uuid)
    return Response(request.data, status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def start_ride_driver(request):
    driver_id = request.user.pk
    passenger_id = request.data.get("passenger")
    vehicle = request.data.get("vehicle")
    price = request.data.get("price")
    ride_uuid = request.data.get("ride_uuid")
    room_uuid = request.data.get("room_uuid")
    if not (passenger_id and vehicle and price and ride_uuid and room_uuid):
        return Response({"message": "passenger, vehicle, price, ride_uuid, room_uuid are required."}, status.HTTP_400_BAD_REQUEST)
    start_ride.delay(driver_id, passenger_id, vehicle, price, ride_uuid, room_uuid)
    return Response(request.data, status.HTTP_200_OK)



# class RideOfferViewSet(ModelViewSet):
#     queryset = RideOffer.objects.all()
#     serializer_class = RideOfferSerializer

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'delete']:
#             permission_classes = [permissions.IsAuthenticated, DriverAccessPermission]
#         else:
#             permission_classes = [permissions.AllowAny]
#         return [permission() for permission in permission_classes]


# class RideAcceptedViewSet(ModelViewSet):
#     queryset = RideAccepted.objects.all()
#     serializer_class = RideAcceptedSerializer

#     def get_permissions(self):
#         if self.action in ['create', 'update', 'partial_update', 'delete']:
#             permission_classes = [permissions.IsAuthenticated, PassengerAccessPermission]
#         else:
#             permission_classes = [permissions.AllowAny]
#         return [permission() for permission in permission_classes]
