import asyncio

import aioredis.client
from fastapi import FastAPI, WebSocket, Depends
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect

from chat.manager import connection_manager
from chat.redis import connect_redis, subscribe_channel
from settings import DjangoServerSettings, get_django_settings, get_broker_settings, BrokerSettings

app = FastAPI()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/chat?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM2ODAwNjIyLCJqdGkiOiJhOTVlMWRiNjAwMTY0ZDJiOTUzMzEyZDRhNmJkZDQ5NSIsInVzZXJfaWQiOjF9.1o3mXUbWv8RcLh1ltNXXF7bdYjFo4E6S5n4vYNOOmxI");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


CHANNEL: aioredis.client.PubSub = ...


@app.on_event("startup")
async def startup_event():
    broker_settings: BrokerSettings = get_broker_settings()
    global CHANNEL
    redis = await connect_redis(broker_settings.host, broker_settings.port)
    CHANNEL = await subscribe_channel(redis, broker_settings.channel_name)


@app.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket, token: str, django_settings: DjangoServerSettings = Depends(get_django_settings)
):
    await connection_manager.connect(websocket, token, django_settings)
    global CHANNEL
    try:
        while True:
            message = await CHANNEL.get_message(timeout=0.5)
            if message is not None:
                await connection_manager.broadcast(message.decode("utf-8"), [1])

            # await asyncio.sleep(1)
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket)
