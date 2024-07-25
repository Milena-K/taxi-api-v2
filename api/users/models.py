from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


# CreateUser
# UpdateUser
# DisplayUser

class User(AbstractBaseUser):
    REQUIRED_FIELDS = ["email", ]
    USERNAME_FIELD = "username"
    objects = UserManager()

    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    profile_picture = models.CharField(blank=True)
    role = models.CharField(
        max_length=1, choices=[("D", ("Driver")), ("C", ("Customer"))], help_text="Please register as Driver or Customer"
    )
    #auth_token Auto?
    #ride_history should be defined in Ride model
    def __str__(self):
        return "Username: " + self.username + " Role: " + self.role
