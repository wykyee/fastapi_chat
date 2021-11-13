from setuptools import setup


setup(
    entry_points={
        "console_scripts": ["start-chat=fastapi_chat.run:main"],
    }
)
