from uuid import UUID

from pydantic import BaseModel


class sensor(BaseModel):
    session_id: UUID
    device_id: str
    external_temperature: float
    external_humidity: float
    internal_temperature: float
    internal_humidity: float
    drying: bool
