from linebot import LineBotApi
from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    PostbackAction,
    TemplateSendMessage,
    TextSendMessage,
)

from kb_2315.config import conf


def send_message(
    message: str,
    channel_access_token: str = conf.line_channel_access_token,
    send_to_id: str = conf.line_group_id,
) -> None:
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(
        to=send_to_id,
        messages=TextSendMessage(text=message),
    )


def shoe_select_carousel(send_to_id: str = conf.line_group_id, session_id: UUID | None = None) -> None:
    columns_list: list[CarouselColumn] = []
    columns_list.append(
        CarouselColumn(
            title="タイトルだよ",
            text="よろしくね",
            thumbnail_image_url="https://picsum.photos/200/300",
            actions=[
                PostbackAction(label="詳細を表示", data="詳細表示"),
            ],
        )
    )
    columns_list.append(
        CarouselColumn(
            title="タイトルだよ",
            text="よろしくね",
            actions=[
                PostbackAction(label="詳細を表示", data="詳細表示"),
            ],
        )
    )
    carousel_template_message = TemplateSendMessage(
        alt_text="会話ログを表示しています", template=CarouselTemplate(columns=columns_list)
    )
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(
        to=send_to_id,
        messages=carousel_template_message,
    )
