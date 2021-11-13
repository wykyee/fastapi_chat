import uvicorn

from chat import settings


def main():
    uvicorn.run(**settings.UvicornSettings().dict())


if __name__ == "__main__":
    main()
