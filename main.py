import json
import sys
from pathlib import Path
from typing import Literal, cast

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import AsyncApiClient, AsyncMessagingApi, Configuration
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks.models.message_event import MessageEvent
from linebot.v3.webhooks.models.source import Source

import kb_2315.config as config
from kb_2315 import notify
from kb_2315.api import schemas


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


@app.post("/sensor")
async def get_sensor(item: schemas.machine) -> None:
    print(item)

    jsonfile: Path = Path(__file__).parent / "data" / "tmp.json"

    with open(jsonfile, mode="r") as f:
        j = json.load(f)

        print(j)

        if str(item.id) in j.keys():
            match (j[str(item.id)], item.status):
                case (False, True):
                    notify.line.send_message(
                        message=f"靴 {item.id} がセットされました",
                    )
                case (True, False):
                    notify.line.send_message(
                        message=f"靴 {item.id} の乾燥が完了しました\nシューキーパーを入れてください",
                    )

        j[str(item.id)] = item.status

    with open(jsonfile, mode="w") as f:
        json.dump(j, f)


@app.post("/callback")
async def handle_callback(request: Request) -> Literal["OK"]:
    signature: str = request.headers["X-Line-Signature"]

    byte_body: bytes = await request.body()
    body: str = byte_body.decode()

    try:
        events: list[MessageEvent] = parser.parse(body, signature)  # type: ignore
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        print(type(event))

        print(cast(Source, event.source).type)
        print(event.source)

        notify.line.send_message(message="sample message")

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
