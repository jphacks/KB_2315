import sys
from typing import Literal, cast
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
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


machines:dict[int, dict[str, bool]] = {}

@app.post("/sensor")
def get_sensor(machine: schemas.machine) -> None:
    if machine.id in machines.keys():
        for sensor_id, sensor_status in machine.status.items():
            match (machines[machine.id][sensor_id], sensor_status):
                case (False, True):
                    notify.line.send_message(message=f"靴 {sensor_id} がセットされました")
                case (True, False):
                    notify.line.send_message(message=f"靴 {sensor_id} の乾燥が完了しました\nシューキーパーを入れてください")
            machines[machine.id][sensor_id] = sensor_status
        machines[machine.id] = machine.status.copy()


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
