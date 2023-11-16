from datetime import timezone
from uuid import UUID

from sqlalchemy.orm import Query

from kb_2315.backend.models import Sensor

from .base_crud import base_CRUD


class CRUD_Sensor(base_CRUD):
    def add_sensor(
        self,
        device_id: int,
        external_temperature: float,
        external_humidity: float,
        internal_temperature: float,
        internal_humidity: float,
        drying: bool,
        session_id: UUID,
    ) -> None:
        with self._Session() as session:
            new_sensor = Sensor()
            new_sensor.device_id = device_id
            new_sensor.external_temperature = external_temperature
            new_sensor.external_humidity = external_humidity
            new_sensor.internal_temperature = internal_temperature
            new_sensor.internal_humidity = internal_humidity
            new_sensor.session_id = session_id
            new_sensor.drying = drying

            session.add(new_sensor)
            session.commit()

    def search_sensor_by(
        self,
        id: int | None = None,
        device_id: str | None = None,
        session_id: UUID | None = None,
    ) -> list[Sensor]:
        with self._Session() as session:
            query: Query[Sensor] = session.query(Sensor)

            if id is not None:
                query = query.filter(Sensor.id == id)
            if device_id is not None:
                query = query.filter(Sensor.device_id == id)

            if session_id is not None:
                query = query.filter(Sensor.session_id == session_id)

            ret: list[Sensor] = query.all()

            for r in ret:
                r.time = r.time.replace(tzinfo=timezone.utc)

            return ret


crud_sensor = CRUD_Sensor()
