from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from ..users.models import Driver, Passenger

User = get_user_model()


class IsDriver(permissions.BasePermission):
    message = "This action is only allowed for drivers."

    def has_permission(self, request, view):
        try:
            Driver.objects.get(pk=request.user.pk)
            return True
        except ObjectDoesNotExist:
            return False


class IsPassenger(permissions.BasePermission):
    message = "This action is only allowed for passengers."

    def has_permission(self, request, view):
        try:
            Passenger.objects.get(pk=request.user.pk)
            return True
        except ObjectDoesNotExist:
            return False
