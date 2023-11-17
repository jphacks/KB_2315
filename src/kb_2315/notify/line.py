from uuid import UUID

from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    PostbackAction,
    TemplateSendMessage,
    TextSendMessage,
)

from kb_2315.backend.crud import crud_shoe
from kb_2315.backend.models import Shoe
from kb_2315.config import conf


def send_message(
    message: str,
    send_to_id: str = conf.line_group_id,
) -> None:
    line_bot_api = LineBotApi(conf.line_channel_access_token)

    try:
        line_bot_api.push_message(
            to=send_to_id,
            messages=TextSendMessage(text=message),
        )
    except LineBotApiError as e:
        print(f"Send Message Error:\n{e}")


def shoe_list_carousel(send_to_id: str = conf.line_group_id) -> None:
    columns_list: list[CarouselColumn] = []
    shoes: list[Shoe] = crud_shoe.search_shoe_by()

    for shoe in shoes:
        columns_list.append(
            CarouselColumn(
                text=f"靴 {shoe.name}",
                thumbnail_image_url=shoe.image_url,
                actions=[
                    PostbackAction(label=f"{shoe.name} を選ぶ", data=" :"),
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
        print(f"LineBotApiError: {e}")


def shoe_select_carousel(send_to_id: str = conf.line_group_id, session_id: UUID | None = None) -> None:
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
