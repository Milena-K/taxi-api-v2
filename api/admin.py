from django.contrib import admin

from .rides.models import Rating, Ride
from .users.models import Driver, Passenger


@admin.register(Passenger)
class PassengerModelAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "rides_taken",
    )


@admin.register(Driver)
class DriverModelAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "car_type",
        "rides_offered",
    )


@admin.register(Ride)
class RideModelAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "status",
        "passenger",
        "driver",
        "ride_uuid",
        "starting_location",
        "destination",
        "start_time",
        "end_time",
        "ride_duration",
        "dropoff_time",
        "price",
    )


@admin.register(Rating)
class RatingModelAdmin(admin.ModelAdmin):
    list_display = (
        "ride",
        "rating",
        "comment",
    )
