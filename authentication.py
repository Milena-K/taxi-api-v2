import asyncio
import json

import aioredis
import django
import websockets
from django.contrib.contenttypes.models import ContentType
from sesame.utils import get_user
from websockets import WebSocketServer
from websockets.frames import CloseCode

django.setup()

CONNECTIONS = {}


def get_content_types(user):
    """Return the set of IDs of content types visible to the user."""
    return {
        ct.id
        for ct in ContentType.objects.all()
        if user.has_perm(f"{ct.app_label}.view_{ct.model}")
        or user.has_perm(f"{ct.app_label}.change_{ct.model}")
    }


async def handler(
    websocket: WebSocketServer,
):
    sesame = await websocket.recv()
    user = await asyncio.to_thread(get_user, sesame)
    if user is None:
        await websocket.close(
            CloseCode.INTERNAL_ERROR,
            "authentication failed",
        )
        return

    ct_ids = await asyncio.to_thread(
        get_content_types,
        user,
    )
    CONNECTIONS[websocket] = {"content_type_ids": ct_ids}
    try:
        await websocket.wait_closed()
    finally:
        del CONNECTIONS[websocket]


async def process_events():
    """Listen to events in Redis and process them."""
    redis = aioredis.from_url("redis://127.0.0.1:6379/1")
    pubsub = redis.pubsub()
    await pubsub.subscribe("events")
    async for message in pubsub.listen():
        if message["type"] != "message":
            continue
        payload = message["data"].decode()
        # broadcast event
        event = json.loads(payload)
        recipients = (
            websocket
            for websocket, connection in CONNECTIONS.items()
            if event["content_type_id"] in connection["content_type_ids"]
        )
        websockets.broadcast(
            recipients,
            payload,
        )


async def main():
    async with websockets.serve(
        handler,
        "localhost",
        8888,
    ):
        await process_events()


if __name__ == "__main__":
    asyncio.run(main())
