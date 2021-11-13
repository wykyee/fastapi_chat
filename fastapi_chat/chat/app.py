import aioredis
from fastapi import FastAPI, WebSocket, Depends, HTTPException
from starlette.websockets import WebSocketDisconnect

from .manager import connection_manager
from .redis_connector import connect_redis
from .settings import DjangoServerSettings, get_django_settings, BrokerSettings, get_broker_settings


app = FastAPI()
REDIS: aioredis.Redis


@app.on_event("startup")
async def startup_event():
    global REDIS
    REDIS = await connect_redis()


@app.websocket("/chat")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    django_settings: DjangoServerSettings = Depends(get_django_settings),
    broker_settings: BrokerSettings = Depends(get_broker_settings),
):
    user_id = await connection_manager.check_auth(token, django_settings)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    await connection_manager.connect(websocket)

    (channel,) = await REDIS.subscribe(broker_settings.channel_name)
    try:
        while await channel.wait_message():
            msg = await channel.get()
            await connection_manager.send_if_needed(user_id, msg, websocket)
    except WebSocketDisconnect:
        channel.close()
        await connection_manager.disconnect(websocket)
