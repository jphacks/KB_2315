from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from kb_2315.backend.db.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, default="Taro")
    line_channel_id: Mapped[str] = mapped_column(String, nullable=True)

    ido_longitude: Mapped[float] = mapped_column(Float, nullable=False)
    keido_latitude: Mapped[float] = mapped_column(Float, nullable=False)
