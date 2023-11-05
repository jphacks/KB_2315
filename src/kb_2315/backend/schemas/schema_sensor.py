from pydantic import BaseModel


class sensor(BaseModel):
    session_id: str
    device_id: int
    external_temperature: float
    external_humidity: float
    internal_temperature: float
    internal_humidity: float
    drying: bool
