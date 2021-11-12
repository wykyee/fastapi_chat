import asyncio
from dataclasses import dataclass

import httpx
from fastapi import WebSocket
from fastapi.exceptions import WebSocketRequestValidationError

from settings import DjangoServerSettings


@dataclass
class UserWebsocket:
    user_id: int
    websocket: WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[UserWebsocket] = []

    async def connect(self, websocket: WebSocket, token: str, django_settings: DjangoServerSettings):
        user = await self.__check_auth(token, django_settings)
        await websocket.accept()
        self.active_connections.append(UserWebsocket(user["id"], websocket))

    async def disconnect(self, websocket: WebSocket):
        for i, connection in enumerate(self.active_connections):
            if connection.websocket == websocket:
                self.active_connections.pop(i)
                break

    async def broadcast(self, message: str, user_ids: list[int]):
        for connection in self.active_connections:
            if connection.user_id in user_ids:
                await connection.websocket.send_text(message)

    @staticmethod
    async def __check_auth(token: str, django_settings: DjangoServerSettings) -> dict:
        async with httpx.AsyncClient() as client:
            token = f"{django_settings.token_type} {token}"
            task = await asyncio.gather(
                client.get(django_settings.get_user_url, headers={"Authorization": token})
            )
        response = task[0]
        if response.status_code != 200:
            raise WebSocketRequestValidationError(errors=["token must be provided"])
        return response.json()


connection_manager = ConnectionManager()
