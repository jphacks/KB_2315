from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DATETIME, Float, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from kb_2315.backend.db.base import Base


if TYPE_CHECKING:
    from .model_sessions import Sessions  # noqa: F401


class Sensors(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[str] = mapped_column(String)
    time: Mapped[datetime] = mapped_column(DATETIME, default=datetime.utcnow(), nullable=False)
    external_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    external_humidity: Mapped[float] = mapped_column(Float, nullable=False)
    internal_temperature: Mapped[float] = mapped_column(Float, nullable=False)
    internal_humidity: Mapped[float] = mapped_column(Float, nullable=False)

    session_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("sessions.session_id"), nullable=False)
