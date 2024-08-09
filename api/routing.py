from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/ride_requests/', consumers.RideRequestConsumer.as_asgi()),
]
