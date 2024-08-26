from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import RideRequest, RideOffer, RideAccepted
from .permissions import PassengerAccessPermission, DriverAccessPermission
from .serializers import RideRequestSerializer, RideOfferSerializer, RideAcceptedSerializer
from ..users.serializers import UserSerializer
from ..users.models import Passenger
from .tasks import find_driver_for_ride

User = get_user_model()
channel_layer = get_channel_layer()

class RideRequestViewSet(ModelViewSet):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            permission_classes = [permissions.IsAuthenticated, PassengerAccessPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request):
        # i won't be saving 
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        headers = self.get_success_headers(serializer.data)
        passenger = request.data.get("passenger")
        starting_location = request.data.get("starting_location")
        destination = request.data.get("destination")
        print(ride.id)
        find_driver_for_ride.delay(passenger, starting_location, destination, ride.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RideOfferViewSet(ModelViewSet):
    queryset = RideOffer.objects.all()
    serializer_class = RideOfferSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            permission_classes = [permissions.IsAuthenticated, DriverAccessPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class RideAcceptedViewSet(ModelViewSet):
    queryset = RideAccepted.objects.all()
    serializer_class = RideAcceptedSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            permission_classes = [permissions.IsAuthenticated, PassengerAccessPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]