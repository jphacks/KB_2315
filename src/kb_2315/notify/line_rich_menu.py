from pathlib import Path

from linebot import LineBotApi
from linebot.models import RichMenu, RichMenuArea, RichMenuBounds, RichMenuSize
from linebot.models.actions import PostbackAction, URIAction

from kb_2315.config import conf


line_bot_api = LineBotApi(conf.line_channel_access_token)


def create_rich_menu() -> None:
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=1200, height=800),
        selected=True,
        name="richmenu",
        chat_bar_text="メニュー",
        areas=[
            # カレンダー
            RichMenuArea(
                bounds=RichMenuBounds(x=0, y=0, width=600, height=800),
                action=URIAction(
                    uri="https://larrybolt.github.io/online-ics-feed-viewer/"
                    + f"#feed={conf.host_url}/api/calendar/"
                    + "%3Fshoe_id%3D1&cors=false&title=My%20Feed&hideinput=false",
                    label="カレンダーの表示",
                ),
            ),
            # データ
            RichMenuArea(
                bounds=RichMenuBounds(x=600, y=0, width=600, height=400),
                action=URIAction(uri=f"{conf.host_url}/analyze/", label="データの表示"),
            ),
            # 靴一覧
            RichMenuArea(
                bounds=RichMenuBounds(x=600, y=400, width=600, height=400),
                action=PostbackAction(data="shoes_list:"),
            ),
        ],
    )

    richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

    with open(Path(__file__).parent / "image/menu.png", "rb") as f:
        line_bot_api.set_rich_menu_image(richMenuId, "image/png", f)

    line_bot_api.set_default_rich_menu(richMenuId)
