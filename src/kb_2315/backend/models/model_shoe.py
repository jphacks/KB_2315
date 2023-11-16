from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from kb_2315.backend.db.base import Base

from .model_session import Session


class Shoe(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="Shoe")
    image_url: Mapped[str] = mapped_column(String, )

    sessions: Mapped[list[Session]] = relationship("Session", backref="event")
