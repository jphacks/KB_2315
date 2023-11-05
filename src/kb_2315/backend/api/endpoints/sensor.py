from fastapi import APIRouter

from kb_2315 import notify
from kb_2315.backend.crud import crud_sensor, crud_session, crud_shoe
from kb_2315.backend.schemas import sensor


router = APIRouter()


@router.post("/")
def search_shoe(item: sensor) -> None:
    crud_sensor.add_sensor(
        device_id=item.device_id,
        external_temperature=item.external_temperature,
        external_humidity=item.external_humidity,
        internal_temperature=item.internal_temperature,
        internal_humidity=item.internal_humidity,
        sesison_id=item.session_id,
        drying=item.drying,
    )

    if not item.drying:
        shoe_id: int | None = crud_session.search_session_by(session_id=item.session_id)[0].shoe_id
        shoe_name: str | None = crud_shoe.search_shoe_by(id=shoe_id)[0].name

        if not shoe_name:
            shoe_name = "靴"

        notify.line.send_message(
            message=f"{shoe_name} の乾燥が完了しました\nシューズキーパーを入れてください",
        )

    return None
