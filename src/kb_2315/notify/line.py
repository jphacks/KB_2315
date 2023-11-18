from uuid import UUID

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    PostbackAction,
    TemplateSendMessage,
    TextSendMessage,
    URIAction,
)

from kb_2315.backend.crud import crud_shoe, crud_user
from kb_2315.backend.models import Shoe
from kb_2315.config import conf


def send_message(
    message: str,
    send_to_id: str | None = None,
) -> None:
    if send_to_id is None:
        send_to_id = crud_user.search_user_by()[0].line_channel_id

    line_bot_api = LineBotApi(conf.line_channel_access_token)

    try:
        line_bot_api.push_message(
            to=send_to_id,
            messages=TextSendMessage(text=message),
        )
    except LineBotApiError as e:
        print(f"Send Message Error:\n{e}")


def shoe_list_carousel(send_to_id: str | None = None) -> None:
    if send_to_id is None:
        send_to_id = crud_user.search_user_by()[0].line_channel_id

    columns_list: list[CarouselColumn] = []
    shoes: list[Shoe] = crud_shoe.search_shoe_by()

    for shoe in shoes:
        columns_list.append(
            CarouselColumn(
                text=f"靴 {shoe.name}",
                thumbnail_image_url=shoe.image_url,
                actions=[URIAction(uri=f"{conf.host_url}/analyze/?shoe_id={shoe.id}", label="データの表示")],
            )
        )

    carousel_template_message = TemplateSendMessage(
        alt_text="乾燥している靴を選んでください", template=CarouselTemplate(columns=columns_list)
    )
    line_bot_api = LineBotApi(conf.line_channel_access_token)

    try:
        line_bot_api.push_message(
            to=send_to_id,
            messages=carousel_template_message,
        )
    except LineBotApiError as e:
        print(f"LineBotApiError: {e}")


def shoe_select_carousel(
    send_to_id: str = crud_user.search_user_by()[0].line_channel_id,
    session_id: UUID | None = None,
) -> None:
    columns_list: list[CarouselColumn] = []
    shoes: list[Shoe] = crud_shoe.search_shoe_by()

    for shoe in shoes:
        columns_list.append(
            CarouselColumn(
                text=f"靴 {shoe.name}",
                thumbnail_image_url=shoe.image_url,
                actions=[
                    PostbackAction(label=f"{shoe.name} を選ぶ", data=f"shoes_select:{shoe.id}:{session_id}"),
                ],
            )
        )

    carousel_template_message = TemplateSendMessage(
        alt_text="乾燥している靴を選んでください", template=CarouselTemplate(columns=columns_list)
    )
    line_bot_api = LineBotApi(conf.line_channel_access_token)

    try:
        line_bot_api.push_message(
            to=send_to_id,
            messages=carousel_template_message,
        )
    except LineBotApiError as e:
        print(f"Select Shoe Carousel Error:\n{e}")
