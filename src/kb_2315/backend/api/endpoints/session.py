from uuid import UUID

from fastapi import APIRouter

from kb_2315 import notify
from kb_2315.backend.crud import crud_session, crud_shoe
from kb_2315.backend.schemas import schema_session


router = APIRouter()


@router.get("/")
def create_session(shoe_id: int) -> schema_session.create_session:
    shoe_name: str | None = "靴"

    session_id: UUID = crud_session.add_session(shoe_id=shoe_id)

    try:
        shoe_name = crud_shoe.search_shoe_by(id=shoe_id)[0].name
    except IndexError:
        pass

    notify.line.send_message(
        message=f"{shoe_name} の乾燥を開始します",
    )

    return schema_session.create_session(session_id=session_id)
