import sys
from typing import Literal

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    AsyncApiClient,
    AsyncMessagingApi,
    Configuration,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import MessageEvent, TextMessageContent

import kb_2315.config as config

conf: config.env = config.read_config(dir=config.root_dir)

app = FastAPI()
channel_access_token: str = conf.line_channel_access_token
channel_secret: str = conf.line_channel_secret


if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

configuration = Configuration(access_token=channel_access_token)

app = FastAPI()
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)


@app.post("/callback")
async def handle_callback(request: Request) -> Literal["OK"]:
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    byte_body: bytes = await request.body()
    body: str = byte_body.decode()

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessageContent):
            continue

        await line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)],
            )
        )

    return "OK"


if __name__ == "__main__":
    server = uvicorn.Server(
        config=uvicorn.Config(
            app=app,
            port=8888,
            host="0.0.0.0",
        )
    )
    server.run()
