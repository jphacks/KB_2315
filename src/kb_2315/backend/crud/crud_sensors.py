from uuid import UUID

from sqlalchemy.orm import Query

from kb_2315.backend.models import Sensors

from .base_crud import base_CRUD


class CRUD_Sensors(base_CRUD):
    def add_sensor(
        self,
        device_id: str,
        external_temperature: float,
        external_humidity: float,
        internal_temperature: float,
        internal_humidity: float,
        sesison_id: UUID,
    ) -> None:
        with self._Session() as session:
            new_sensor = Sensors()
            new_sensor.device_id = device_id
            new_sensor.external_temperature = external_temperature
            new_sensor.external_humidity = external_humidity
            new_sensor.internal_temperature = internal_temperature
            new_sensor.internal_humidity = internal_humidity
            new_sensor.session_id = sesison_id

            session.add(new_sensor)
            session.commit()

    def search_sensor_by(
        self,
        id: int | None = None,
        device_id: str | None = None,
        session_id: UUID | None = None,
    ) -> list[Sensors]:
        with self._Session() as session:
            query: Query[Sensors] = session.query(Sensors)

            if id is not None:
                query = query.filter(Sensors.id == id)
            if device_id is not None:
                query = query.filter(Sensors.device_id == id)

            if session_id is not None:
                query = query.filter(Sensors.session_id == session_id)

            return query.all()
