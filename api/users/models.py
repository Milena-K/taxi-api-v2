from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from phonenumber_field.modelfields import (
    PhoneNumberField,
)

from .managers import (
    UserManager,
)


class User(
    AbstractBaseUser,
    PermissionsMixin,
):
    REQUIRED_FIELDS = [
        "password",
    ]
    USERNAME_FIELD = (
        "username"
    )
    objects = UserManager()
    email = models.EmailField(
        blank=True
    )
    date_created = (
        models.DateField(
            auto_now=True
        )
    )
    phone_number = (
        PhoneNumberField(
            blank=True
        )
    )
    username = (
        models.CharField(
            max_length=50,
            blank=False,
            unique=True,
        )
    )
    profile_picture = (
        models.CharField(
            blank=True
        )
    )
    birthday = (
        models.DateField(
            blank=True,
            auto_now=True,
        )
    )
    is_staff = (
        models.BooleanField(
            default=False
        )
    )
    is_superuser = (
        models.BooleanField(
            default=False
        )
    )
    is_active = models.BooleanField(
        default=True
    )  # TODO: change later to False, and only True if user is confirmed through sms code

    def __str__(self):
        return self.username


class Driver(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        unique=True,
    )
    car_type = (
        models.CharField(
            blank=False
        )
    )
    rides_offered = (
        models.IntegerField(
            default=0
        )
    )

    def __str__(self):
        return (
            "driver: "
            + str(self.user)
        )


class Passenger(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        unique=True,
    )
    rides_taken = (
        models.IntegerField(
            default=0
        )
    )

    def __str__(self):
        return (
            "passenger: "
            + str(self.user)
        )
