import uvicorn

from chat.settings import UvicornSettings


def main():
    uvicorn.run(**UvicornSettings().dict())


if __name__ == "__main__":
    main()
