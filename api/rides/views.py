from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated

from .models import RideRequest, RideOffer, RideAccepted
from .permissions import PassengerAccessPermission, DriverAccessPermission
from .serializers import RideRequestSerializer, RideOfferSerializer, RideAcceptedSerializer
from ..users.serializers import UserSerializer
from ..users.models import Passenger

User = get_user_model()


class RideRequestViewSet(ModelViewSet):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'delete']:
            permission_classes = [permissions.IsAuthenticated, PassengerAccessPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def create(self, request, args, kwargs):
        super().create(request, args, kwargs)




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
