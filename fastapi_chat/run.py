import uvicorn

try:
    from fastapi_chat.chat import settings
except ModuleNotFoundError:
    from chat import settings


def main():
    print(*settings.UvicornSettings().dict())
    uvicorn.run(**settings.UvicornSettings().dict())


if __name__ == "__main__":
    uvicorn.run(**settings.UvicornDevSettings().dict())
