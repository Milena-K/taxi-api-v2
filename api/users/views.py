from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers import MyTokenObtainPairSerializer
from .models import Driver, Passenger
from .permissions import IsOwner
from .serializers import (
    DriverSerializer,
    PassengerSerializer,
    UserProfileSerializer,
    UserSerializer,
)

User = get_user_model()
channel_layer = get_channel_layer()


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(ModelViewSet):
    """
    API endpoint for handling user data
    """

    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == "create":
    #         permission_classes = [permissions.AllowAny]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]


class ProfileViewSet(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwner]


class PassengerViewSet(ModelViewSet):
    """
    API endpoint for handling passenger data
    """

    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [permissions.AllowAny]

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action in [
    #         "update",
    #         "partial_update",
    #         "retrive",
    #         "destroy",
    #     ]:
    #         permission_classes = [IsOwner]
    #     else:  # list, create
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.AllowAny]

    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     if self.action in [
    #         "update",
    #         "partial_update",
    #         "retrive",
    #     ]:
    #         permission_classes = [IsOwner]
    #     else:  # destroy, list, create
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]
