from uuid import UUID

from fastapi import APIRouter

from kb_2315 import notify
from kb_2315.backend.crud import crud_session, crud_shoe
from kb_2315.backend.schemas import schema_session


router = APIRouter()


@router.get("/")
def create_session(item: schema_session.create_session) -> UUID:
    session_id: UUID = crud_session.add_session(shoe_id=item.shoe_id)

    shoe_name: str | None = crud_shoe.search_shoe_by(id=item.shoe_id)[0].name

    if not shoe_name:
        shoe_name = "靴"

    notify.line.send_message(
        message=f"{shoe_name} の乾燥を開始します",
    )

    return session_id
