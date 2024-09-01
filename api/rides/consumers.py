from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync

import json

class RideRequestsConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.groups.append("requests_group") # important otherwise some cleanup does not happened on disconnect.
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
            "passenger": event["passenger"],
            "starting_location": event["starting_location"],
            "destination": event["destination"],
            "dropoff_time": event["dropoff_time"],
            "ride_duration": event["ride_duration"],
            "ride_uuid": event["ride_uuid"]
        }, cls=DjangoJSONEncoder))


    def cancel_ride(self, event):
        self.send(text_data=json.dumps({
            "passenger": event["passenger"],
            "ride_uuid": event["ride_uuid"]
        }, cls=DjangoJSONEncoder))


# class ActiveRidesConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_uuid = self.scope['url_route']['kwargs']['room_uuid']
#         self.accept()
#         self.group_name = f"active_ride_{self.room_uuid}"
#         self.groups.append(self.group_name) # important otherwise some cleanup does not happened on disconnect.
#         async_to_sync(self.channel_layer.group_add)(
#             self.group_name,
#             self.channel_name
#         )

#     def disconnect(self, close_code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.group_name,
#             self.channel_name
#         )

#     def start_ride(self, event):
#         self.send(text_data=json.dumps({
#             "message": "The ride is starting!",
#             "ride_uuid": event["ride_uuid"],
#             "passenger": event["passenger"],
#             "price": event["price"],
#             "room_uuid": event["room_uuid"],
#         }, cls=DjangoJSONEncoder))

#     # the driver should send constant location messages to user in send_location() method
#     def send_location_data(self, event):
#         self.send(text_data=json.dumps({
#             "current_location": event["current_location"],
#             "driver": event["driver"]
#         }, cls=DjangoJSONEncoder))


class DriversLocationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.group_name = "drivers_location"
        self.groups.append(self.group_name) # important otherwise some cleanup does not happened on disconnect.
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def send_car_location(self, event):
        self.send(text_data=json.dumps({
            "driver": event["driver"],
            "location": event["location"], # (long, lat)
        }, cls=DjangoJSONEncoder))
