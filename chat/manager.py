import json
from typing import Optional

import httpx
from fastapi import WebSocket

from .settings import DjangoServerSettings


class ConnectionManager:
    @staticmethod
    async def connect(websocket: WebSocket):
        await websocket.accept()

    @staticmethod
    async def disconnect(websocket: WebSocket):
        await websocket.close()

    @staticmethod
    async def send_if_needed(user_id: int, msg: bytes, websocket: WebSocket):
        """
        Sends via websocket json, if it directed to current user
        (user's id is sender's id or in receivers' ids)
        """
        msg = json.loads(msg.decode("utf-8"))
        receiver_ids = msg.get("receiver_ids", [])
        sender_id = msg.get("sender_id")
        message_obj = msg.get("message", {})
        if user_id == sender_id or user_id in receiver_ids:
            await websocket.send_json(message_obj)

    @staticmethod
    async def check_auth(token: str, django_settings: DjangoServerSettings) -> Optional[int]:
        """
        Sends request to django server with token to ensure connection and get user's id.
        """
        async with httpx.AsyncClient() as client:
            token = f"{django_settings.token_type} {token}"
            response = await client.get(django_settings.get_user_url, headers={"Authorization": token})
        if response.status_code == 200:
            return response.json().get(django_settings.user_response_id_field)


connection_manager = ConnectionManager()
