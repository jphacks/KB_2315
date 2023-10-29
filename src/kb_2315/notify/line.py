from linebot import LineBotApi
from linebot.models import TextSendMessage

import kb_2315.config as config


conf: config.env = config.read_config(dir=config.root_dir)


def send_message(
    message: str,
    channel_access_token: str = conf.line_channel_access_token,
    send_to_id: str = conf.line_group_id,
) -> None:
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(send_to_id, TextSendMessage(text=message))
