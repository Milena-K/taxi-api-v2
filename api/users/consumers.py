from channels.generic.websocket import WebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import async_to_sync

import json

class DriverConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_name = None

    def connect(self):
        self.driver_id = self.scope['url_route']['kwargs']['driver_id']
        self.group_name = f"driver_{self.driver_id}"
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "ride_accepted",
                "ride_uuid": data["ride_uuid"],
                "passenger": data["passenger"],
                "vehicle": data["vehicle"],
                "price": data["price"],
                "room_uuid": data["room_uuid"]
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def ride_accepted(self, event):
        self.send(text_data=json.dumps({
                "ride_uuid": event["ride_uuid"],
                "passenger": event["passenger"],
                "vehicle": event["vehicle"],
                "price": event["price"],
                "room_uuid": event["room_uuid"]
        }, cls=DjangoJSONEncoder))
