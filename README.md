## Usage

1. Set env variables for chat service
2. Run `python run.py` on your server. Chat will be available on endpoint ws://`host`:`port`/chat

As soon as you start server there will be connection to redis.
Using chat's endpoint user subscribes to queue, receiving data from it.
Queue's message must be like:
`{"sender_id": 1, "reciever_ids": [2, 3, 4]}, "message": {"id": 111}}`
- `sender_id` - required (all messages have sender)
- `reciever_ids` - non-required, can be empty list or this field can even not exist
- `message` - non-required, object that will be sent to users


## Env variables
*default in ()
- `CHAT_HOST` - host for running uvicorn application (0.0.0.0)
- `CHAT_PORT` - post for running uvicorn application (8088)
- `CHAT_WORKERS` - number of workers for uvicorn application (1)
- `CHAT_BROKER_HOST` - host for redis to subscribe to the queue (0.0.0.0)
- `CHAT_BROKER_PORT` - port for redis to subscribe to the queue (6300)
- `CHAT_BROKER_DB` - db for redis to subscribe to the queue (2)
- `CHAT_CHANNEL_NAME` - queue's name to subscribe to (chat)
- `CHAT_DJANGO_BASE_URL` - base url of django's application (http://localhost:4114/)
- `CHAT_DJANGO_GET_USER_URL` - django's endpoint to get current user's information (api/v1/me)
- `CHAT_DJANGO_TOKEN_TYPE` - jwt token's start (Bearer) 
- `CHAT_DJANGO_USER_RESPONSE_ID_FIELD` - field for getting user's id after request to CHAT_DJANGO_GET_USER_URL

written using python 3.8.2
