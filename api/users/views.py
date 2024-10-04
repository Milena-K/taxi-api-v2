from django.contrib.auth import (
    get_user_model,
)
from rest_framework import (
    permissions,
)
from rest_framework import (
    mixins,
)
from rest_framework.viewsets import (
    ModelViewSet,
    GenericViewSet,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from channels.layers import (
    get_channel_layer,
)

from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    PassengerSerializer,
    DriverSerializer,
)
from ..serializers import (
    MyTokenObtainPairSerializer,
)
from .permissions import (
    IsOwner,
)
from .models import (
    Passenger,
    Driver,
)

User = get_user_model()
channel_layer = (
    get_channel_layer()
)


class LoginView(
    TokenObtainPairView
):
    serializer_class = MyTokenObtainPairSerializer


class UserViewSet(
    ModelViewSet
):
    """
    API endpoint for handling user data
    """

    queryset = User.objects.all().order_by(
        "username"
    )
    serializer_class = (
        UserSerializer
    )

    def get_permissions(self):
        permission_classes = []
        if (
            self.action
            == "create"
        ):
            permission_classes = [
                permissions.AllowAny
            ]
        else:
            permission_classes = [
                permissions.IsAdminUser
            ]
        return [
            permission()
            for permission in permission_classes
        ]


class ProfileViewSet(
    GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = (
        User.objects.all()
    )
    serializer_class = (
        UserProfileSerializer
    )
    permission_classes = [
        IsOwner
    ]


class PassengerViewSet(
    ModelViewSet
):
    """
    API endpoint for handling passenger data
    """

    queryset = Passenger.objects.all()
    serializer_class = (
        PassengerSerializer
    )

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in [
            "update",
            "partial_update",
            "retrive",
            "destroy",
        ]:
            permission_classes = [
                IsOwner
            ]
        else:  # destroy, list, create
            permission_classes = [
                permissions.IsAdminUser
            ]
        return [
            permission()
            for permission in permission_classes
        ]


class DriverViewSet(
    ModelViewSet
):
    queryset = (
        Driver.objects.all()
    )
    serializer_class = (
        DriverSerializer
    )

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in [
            "update",
            "partial_update",
            "retrive",
        ]:
            permission_classes = [
                IsOwner
            ]
        else:  # destroy, list, create
            permission_classes = [
                permissions.IsAdminUser
            ]
        return [
            permission()
            for permission in permission_classes
        ]
