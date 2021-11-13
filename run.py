import uvicorn

from chat.settings import UvicornSettings


if __name__ == "__main__":
    uvicorn.run(**UvicornSettings().dict())
