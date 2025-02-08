from django.contrib.auth import get_user_model
from django.views.generic import View
from rest_framework import permissions
from rest_framework.views import Request

User = get_user_model()


class IsOwner(permissions.BasePermission):
    message = "This action is only allowed for owners of the data."

    def has_permission(
        self,
        request: Request,
        view: View,
    ):
        user_pk = view.kwargs.get("pk")
        return bool(request.user and (user_pk == request.user.pk))

    # list, create, retrieve, partial update, update, destroy


class IsAdminOrIsOwner(permissions.BasePermission):
    message = "This action is only allowed for owners of the data."

    def has_permission(
        self,
        request: Request,
        view: View,
    ):
        user_pk = view.kwargs.get("pk")
        return bool(
            request.user and (request.user.is_staff or (user_pk == request.user.pk))
        )
