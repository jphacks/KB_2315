import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kb_2315.backend.db.base import Base

from .model_sensor import Sensor


if TYPE_CHECKING:
    from .model_shoe import Shoe  # noqa: F401


class Session(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    device_id: Mapped[int] = mapped_column(Integer, nullable=False)
    shoe_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("shoe.id"), nullable=True)

    weather_code: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    sensors: Mapped[list[Sensor]] = relationship("Sensor", backref="event")
