from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, Float, ForeignKey, Integer, Uuid, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from kb_2315.backend.db.base import Base


if TYPE_CHECKING:
    from .model_session import Session  # noqa: F401


class Sensor(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    external_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    external_humidity: Mapped[float] = mapped_column(Float, nullable=False)
    internal_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    internal_humidity: Mapped[float] = mapped_column(Float, nullable=False)
    drying: Mapped[bool] = mapped_column(Boolean, nullable=False)

    session_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("session.session_id"), nullable=False)
