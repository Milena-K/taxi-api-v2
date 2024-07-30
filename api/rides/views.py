from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated

from .models import RideRequest
from .serializers import RideRequestSerializer
from ..users.serializers import UserSerializer

User = get_user_model()


# requesting a ride
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def request_ride(request: Request):
    """
    API endpoint for clients to create a request for a ride from the drivers.
    """
    data = JSONParser().parse(request) # request.data?
    passenger_serializer = UserSerializer(request.user) # TODO: change to passenger serializer
    username = passenger_serializer.data.pop("username")
    passenger = User.objects.get(username=username)
    data["passenger"] = passenger.pk
    ride_serializer = RideRequestSerializer(data=data)
    if ride_serializer.is_valid():
        ride_serializer.save()
        return Response(data=ride_serializer.data, status=status.HTTP_201_CREATED)
    return Response(ride_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return Response(data=data, status=status.HTTP_201_CREATED)


# listing available drivers rides
@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def list_rides(request: Request):
    """
    API endpoint for listing every ride made
    """
    rides = RideRequest.objects.all()
    serializer = RideRequestSerializer(data=rides, many=True)
    serializer.is_valid()
    return Response(data=serializer.data, status=status.HTTP_200_OK)

# TODO: get an active ride of the current user

# TODO: canceling a ride
