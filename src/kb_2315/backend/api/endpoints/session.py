from uuid import UUID

from fastapi import APIRouter

from kb_2315 import notify
from kb_2315.backend.crud import crud_session, crud_user
from kb_2315.backend.models import User
from kb_2315.backend.schemas import schema_session
from kb_2315.config import conf


router = APIRouter()


@router.get("/")
def create_session(device_id: int) -> schema_session.create_session:
    user: User = crud_user.search_user_by()[0]

    session_id: UUID = crud_session.add_session(user=user, device_id=device_id)

    notify.line.send_message(
        message=f"乾燥を開始しました\n{conf.host_url}/analyze/?session_id={session_id}\n\n靴を選んでください",
        send_to_id=user.line_channel_id,
    )
    notify.line.shoe_select_carousel(
        session_id=session_id,
        send_to_id=user.line_channel_id,
    )

    return schema_session.create_session(session_id=session_id)
