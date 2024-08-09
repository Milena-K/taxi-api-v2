from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = ["email", "password"]
    USERNAME_FIELD = "username"
    objects = UserManager()

    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    profile_picture = models.CharField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # TODO: change later to False, and only True if user confirms email

    def __str__(self):
        return self.username


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True)
    car_type = models.CharField(blank=False)
    rating = models.FloatField(blank=False)


class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, unique=True)
    credit_card = models.CharField(blank=True)
