from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync

import json

class RideRequestsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "requests_group",
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            "requests_group",
            self.channel_name
        )

    def new_passenger_request(self, event):
        self.send(text_data=json.dumps({
            "passenger": event['passenger'],
            "starting_location": event['starting_location'],
            "destination": event['destination'],
            "ride_uuid": event["ride_uuid"]
        }, cls=DjangoJSONEncoder))


class RideOffersConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None

    def connect(self):
        self.ride_uuid = self.scope['url_route']['kwargs']['ride_uuid']
        self.group_name = f"offers_group_{self.ride_uuid}"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def new_driver_offer(self, event):
        self.send(text_data=json.dumps({
            "driver": event["driver"],
            "vehicle": event["vehicle"],
            "price": event["price"],
            "ride_uuid": event["ride_uuid"]
        }, cls=DjangoJSONEncoder))


class ActiveRidesConsumer(WebsocketConsumer):
    def connect(self):
        self.room_uuid = self.scope['url_route']['kwargs']['room_uuid']
        self.group_name = f"active_ride_{self.room_uuid}"
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def recieve(self, event):
        # TODO: the driver should send constant location messages to user in send_location() method
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))

    def create_private_room(self, event):
        self.send(text_data=json.dumps({
            "ride_uuid": event["ride_uuid"],
            "passenger": event["passenger"],
            "vehicle": event["vehicle"],
            "price": event["price"],
            "room_uuid": event["room_uuid"],
        }, cls=DjangoJSONEncoder))

    # TODO: the driver should send constant location messages to user in send_location() method
    def send_location_data(self, event):
        pass

# {"passenger": 1, "starting_location": "skopje", "destination": "berlin", "ride_id": 2}
# import json
# from channels.auth import login
# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer


# class RideRequestConsumer(AsyncWebsocketConsumer):
#     """
#     Connects every user to the drivers group channel
#     """

#     # TODO: write a middleware that authenticates users using sesame
#     async def connect(self):
#         # print(self.scope["user"])
#         user = self.scope["user"]
#         print(user)
#         await login(self.scope, user, backend='django.contrib.auth.backends.ModelBackend') # TODO: change the backend to sesame
#         await self.channel_layer.group_add("drivers", self.channel_name)
#         await self.accept()
