from rest_framework import (
    permissions,
)
from django.shortcuts import (
    get_object_or_404,
)
from django.contrib.auth import (
    get_user_model,
)

from ..users.models import (
    Passenger,
    Driver,
)
from django.core.exceptions import (
    ObjectDoesNotExist,
)


User = get_user_model()


class IsDriver(
    permissions.BasePermission
):
    message = "This action is only allowed for drivers."

    def has_permission(
        self, request, view
    ):
        try:
            Driver.objects.get(
                pk=request.user.pk
            )
            return True
        except (
            ObjectDoesNotExist
        ):
            return False


class IsPassenger(
    permissions.BasePermission
):
    message = "This action is only allowed for passengers."

    def has_permission(
        self, request, view
    ):
        try:
            Passenger.objects.get(
                pk=request.user.pk
            )
            return True
        except (
            ObjectDoesNotExist
        ):
            return False
