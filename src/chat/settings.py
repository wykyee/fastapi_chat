from functools import lru_cache
from os import getenv
from pydantic import BaseSettings


class UvicornSettings(BaseSettings):
    app: str = "chat.app:app"
    host: str = getenv("CHAT_HOST", "0.0.0.0")
    port: int = getenv("CHAT_PORT", 8088)
    workers: int = getenv("CHAT_WORKERS", 1)
    reload: bool = True


class BrokerSettings(BaseSettings):
    host: str = getenv("CHAT_BROKER_HOST", "0.0.0.0")
    port: int = getenv("CHAT_BROKER_PORT", 6300)
    db: int = getenv("CHAT_BROKER_DB", 2)
    channel_name: str = getenv("CHAT_CHANNEL_NAME", "chat_channel")


class DjangoServerSettings(BaseSettings):
    base_url: str = getenv("CHAT_DJANGO_BASE_URL", "http://localhost:4114/")
    get_user_url: str = getenv("CHAT_DJANGO_GET_USER_URL", base_url + "api/v1/me/")
    token_type: str = getenv("CHAT_DJANGO_TOKEN_TYPE", "Bearer")
    user_response_id_field: str = getenv("CHAT_DJANGO_USER_RESPONSE_ID_FIELD", "id")


@lru_cache
def get_django_settings():
    return DjangoServerSettings()


@lru_cache
def get_broker_settings():
    return BrokerSettings()
