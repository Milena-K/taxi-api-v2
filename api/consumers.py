import json
from channels.auth import login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class RideRequestConsumer(AsyncWebsocketConsumer):
    """
    Connects every user to the drivers group channel
    """

    # TODO: write a middleware that authenticates users using sesame
    async def connect(self):
        # print(self.scope["user"])
        user = self.scope["user"]
        print(user)
        await login(self.scope, user, backend='django.contrib.auth.backends.ModelBackend') # TODO: change the backend to sesame
        await self.channel_layer.group_add("drivers", self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        await self.channel_layer.group_send("drivers", {
                "type": "drivers.message",
                "passenger": data["passenger"],
                "starting_location": data["starting_location"],
                "destination": data["destination"],
        })
        # TODO: periodically use get_user(scope) to be sure that the user is still logged in.

    async def drivers_message(self, event):
        await self.send(text_data=json.dumps({
                "passenger": event["passenger"],
                "starting_location": event["starting_location"],
                "destination": event["destination"],
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard("drivers", self.channel_name)
