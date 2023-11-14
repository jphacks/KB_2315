from uuid import UUID

from fastapi import APIRouter

from kb_2315 import notify
from kb_2315.backend.crud import crud_sensor, crud_session, crud_shoe
from kb_2315.backend.schemas import schema_sensor


router = APIRouter()


@router.post("/")
def search_shoe(item: schema_sensor.sensor) -> None:
    try:
        uuid = UUID(item.session_id)

        crud_sensor.add_sensor(
            device_id=item.device_id,
            external_temperature=item.external_temperature,
            external_humidity=item.external_humidity,
            internal_temperature=item.internal_temperature,
            internal_humidity=item.internal_humidity,
            sesison_id=uuid,
            drying=item.drying,
        )

        if not item.drying:
            shoe_name: str = "靴"

            shoe_id: int | None = crud_session.search_session_by(session_id=uuid)[0].shoe_id

            try:
                shoe_name = crud_shoe.search_shoe_by(shoe_id=shoe_id)[0].name
            except IndexError:
                pass

            notify.line.send_message(
                message=f"{shoe_name} の乾燥が完了しました\nシューズキーパーを入れてください",
            )

        return None
    except ValueError:
        pass
