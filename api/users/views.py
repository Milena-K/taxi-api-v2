import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import permissions, status, generics
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer, MyTokenObtainPairSerializer,  PassengerSerializer, DriverSerializer
from .models import Passenger, Driver

User = get_user_model()
channel_layer = get_channel_layer()

# TODO:
# user login
# signup
# verify
# update profile details
# retrieve

class UserViewSet(ModelViewSet):
    """
    API endpoint for handling user data
    """
    queryset = User.objects.all() # TODO: add order_by()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # TODO: change to IsAdminOnly

#Register User
class RegisterView(generics.CreateAPIView):
    """
    API endpoint for registering users
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def getProfile(request):
    """
    API endpoint for getting user's profile data
    """
    user = request.user
    profile_data = {
        "username": user.username,
        "profile_picture": user.profile_picture
    }
    return Response(data=profile_data, status=status.HTTP_200_OK)


class PassengerViewSet(ViewSet):
    """
    API endpoint for handling passenger data
    """
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def list(self, request: Request):
        """
        Get method for listing every passenger

        url /passengers/
        """
        serializer = PassengerSerializer(self.queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request: Request):
        """
        POST method for creating passengers

        url /passengers/
        """
        print(request.data)
        passenger_serializer = PassengerSerializer(data=request.data)
        if passenger_serializer.is_valid():
            passenger_serializer.save()
            return Response(data=passenger_serializer.data, status=status.HTTP_200_OK)
        return Response(data=passenger_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """
        GET method for getting information
        about a specific passenger.

        url /passengers/1/
        """
        try:
            passenger = Passenger.objects.get(user_id=pk)
            serializer = PassengerSerializer(passenger)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(data={"message": "There is no passenger with this pk"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        """
        PATCH method for partially updating passenger info

        url /passengers/1/
        """
        user = User.objects.get(username=request.user.username)
        if int(user.pk) == int(pk): # TODO: or user.is_superuser
            passenger = Passenger.objects.get(user_id=pk)
            serializer = PassengerSerializer(instance=passenger, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "You don't have the right authorization."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        """
        PUT method for updating full passenger info

        url /passengers/1/
        """
        user = User.objects.get(username=request.user.username)
        if int(user.pk) == int(pk): # TODO: or user.is_superuser
            passenger = Passenger.objects.get(user_id=pk)
            serializer = PassengerSerializer(instance=passenger, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "You don't have the right authorization."}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):
        """
        DELETE method for deleting passenger info

        url /passengers/1/
        """
        passenger = Passenger.objects.get(user_id=pk)
        print(passenger)
        passenger.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all() # TODO: add order_by()
    serializer_class = DriverSerializer
    permission_classes = [permissions.AllowAny] # TODO: change to IsAdminOnly

    def partial_update(self, request, pk=None):
        """
        PATCH method for partially updating passenger info

        url /passengers/1/
        """
        user = User.objects.get(username=request.user.username)
        if int(user.pk) == int(pk): # TODO: or user.is_superuser
            driver = Driver.objects.get(user_id=pk)
            serializer = DriverSerializer(instance=driver, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "You don't have the right authorization."}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        """
        PUT method for updating full passenger info

        url /passengers/1/
        """
        user = User.objects.get(username=request.user.username)
        if int(user.pk) == int(pk): # TODO: or user.is_superuser
            driver = Driver.objects.get(user_id=pk)
            serializer = DriverSerializer(instance=driver, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "You don't have the right authorization."}, status=status.HTTP_401_UNAUTHORIZED)


