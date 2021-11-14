FROM python:3.8.2

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apt update
