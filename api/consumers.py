import json
from channels.auth import login
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class RideRequestConsumer(AsyncWebsocketConsumer):

    # TODO: write a middleware that authenticates users using sesame
    async def connect(self):
        user = self.scope["user"]
        print(user)
        await login(self.scope, user, backend='django.contrib.auth.backends.ModelBackend') # TODO: change the backend to sesame
        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        # print(data["room"])

        # broadcast the received message to all clients
        await self.channel_layer.group_send("chat", {
            "type": "chat_message",
            "message": message
        })

        # TODO: periodically use get_user(scope) to be sure that the user is still logged in.

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({
            "message": message
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)
