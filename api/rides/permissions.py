from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from ..users.models import Passenger, Driver


User = get_user_model()



class DriverAccessPermission(permissions.BasePermission):
    message = 'You are trying to change data you don\'t own.'

    def has_permission(self, request, view):
        user_pk = request.user.pk
        get_object_or_404(Driver, user_id=user_pk)
        driver = int(request.data.get("driver", 0))
        if not driver:
            self.message = "Please give value for the driver id."
            return False
        return user_pk == driver
