from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kb_2315.backend.db.base import Base

from .model_session_id import Sessions


class Shoe(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="Shoe")

    sessions: Mapped[list[Sessions]] = relationship("Sessions", backref="event")
