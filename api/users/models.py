from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class User(AbstractBaseUser):
    REQUIRED_FIELDS = ["email", "password"]
    USERNAME_FIELD = "username"
    objects = UserManager()

    username = models.CharField(max_length=50, blank=False, unique=True)
    email = models.EmailField(blank=False, unique=True)
    profile_picture = models.CharField(blank=True)
    role = models.CharField(
        max_length=1, choices=[("D", ("Driver")), ("C", ("Customer"))], help_text="Please register as Driver or Customer"
    )
    #ride_history should be defined in Ride model

    def __str__(self):
        return "Username: " + self.username + " Role: " + self.role


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


