import sys
from typing import Literal, cast
from uuid import UUID

from fastapi import APIRouter, HTTPException, Request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import AsyncApiClient, AsyncMessagingApi, Configuration
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks.models.message_event import MessageEvent
from linebot.v3.webhooks.models.source import Source

from kb_2315 import notify
from kb_2315.backend.crud import crud_session, crud_shoe, crud_user
from kb_2315.backend.models.model_shoe import Shoe
from kb_2315.config import conf


channel_access_token: str = conf.line_channel_access_token
channel_secret: str = conf.line_channel_secret


if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

configuration = Configuration(access_token=channel_access_token)


async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)
router = APIRouter()


@router.post("/callback")
async def handle_callback(request: Request) -> Literal["OK"]:
    signature: str = request.headers["X-Line-Signature"]

    byte_body: bytes = await request.body()
    body: str = byte_body.decode()

    try:
        events: list[MessageEvent] = parser.parse(body, signature)  # type: ignore
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        return_id: str | None = None

        match (event_source := cast(Source, event.source)).type:
            case "user":
                return_id = event_source.user_id  # type: ignore
            case "group":
                return_id = event_source.group_id  # type: ignore
            case "room":
                return_id = event_source.room_id  # type: ignore

        if return_id is None:
            continue
        else:
            print(f"Return ID : {return_id}")

        if event.type == "postback":
            pbdata: str = event.postback.data  # type: ignore

            try:
                pbheader: str = pbdata.split(":")[0]
            except Exception:
                pbheader = ""

            if pbheader == "shoes_list":
                notify.line.shoe_list_carousel()

            elif pbheader == "shoes_select":
                _, shoe_id, session_id = pbdata.split(":")

                if crud_session.map_session_to_shoe(UUID(session_id), int(shoe_id)):
                    shoes: list[Shoe] = crud_shoe.search_shoe_by(shoe_id=int(shoe_id))

                    if len(shoes) > 0:
                        notify.line.send_message(
                            message=f"{shoes[0].name} を選択しました",
                            send_to_id=return_id,
                        )

                else:
                    notify.line.send_message(
                        message="選択済みです",
                        send_to_id=return_id,
                    )
            else:
                pass
        else:
            # 普通に話しかけらた
            if em := event.message:
                if em.text == "hack":  # type: ignore
                    crud_user.set_line_channel_id_by_user_id(user_id=1, line_channel_id=return_id)

    return "OK"
