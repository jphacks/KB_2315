import uuid
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kb_2315.backend.db.base import Base

from .model_sensors import Sensors


if TYPE_CHECKING:
    from .model_shoe import Shoe  # noqa: F401


class Sessions(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), default=uuid.uuid4(), unique=True, nullable=False)

    shoe_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("shoe.id"), nullable=True)

    sensors: Mapped[list[Sensors]] = relationship("Sensors", backref="event")
