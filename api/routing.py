from django.urls import (
    path,
    re_path,
)
from .rides import (
    consumers as rides_consumers,
)
from .users import (
    consumers as users_consumers,
)

websocket_urlpatterns = [
    re_path(
        r"ws/driver/(?P<driver_id>\w+)/$",
        users_consumers.DriverConsumer.as_asgi(),
    ),
    path(
        "ws/ride-requests/",
        rides_consumers.RideRequestsConsumer.as_asgi(),
    ),
    re_path(
        r"ws/ride-offer/(?P<passenger_id>\w+)/$",
        users_consumers.PassengerConsumer.as_asgi(),
    ),
    re_path(
        r"ws/accept-ride/(?P<driver_id>\w+)/$",
        users_consumers.DriverConsumer.as_asgi(),
    ),
]
