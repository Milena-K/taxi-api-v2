import django
import asyncio
from websockets import WebSocketServer
from websockets.frames import CloseCode

django.setup()


async def handler(websocket: WebSocketServer):
    sesame = await websocket.recv()
    user = await asyncio.to_thread(get_user, sesame)
    if user is None:
        await websocket.close(CloseCode.INTERNAL_ERROR, "authentication failed")
        return

    await websocket.send(f"Hello {user}!")

async def main():
    async with websockets.serve(handler, "localhost", 8888):
        await asyncio.Future() # run forever


if __name__ == "__main__":
    asyncio.run(main())
