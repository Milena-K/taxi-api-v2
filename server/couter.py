import websockets
from websockets import WebSocketServer
import asyncio
import json

USERS = set()

VALUE = 0

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def value_event():
    pass

def counter(websocket: WebSocketServer):
    global USERS, VALUE
    try:
        # Register user
        USERS.add(websocket)
        websockets.broadcast(USERS, users_event())
        websockets.
    except:
        pass


async def main():
    async with websockets.serve(counter, "localhost", 6789):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())
