from django.urls import path, re_path
from .rides import consumers as rides_consumers
from .users import consumers as users_consumers

websocket_urlpatterns = [
    re_path(r'ws/drivers/(?P<driver_id>\w+)/$', users_consumers.DriverConsumer.as_asgi()),
    path('ws/ride-requests/', rides_consumers.RideRequestsConsumer.as_asgi()),
    re_path(r'ws/ride-offers/(?P<ride_uuid>[0-9a-fA-F\-]{36})/$', rides_consumers.RideOffersConsumer.as_asgi()),
    re_path(r'ws/start-ride/(?P<room_uuid>[0-9a-fA-F\-]{36})/$', rides_consumers.ActiveRidesConsumer.as_asgi()),
]
